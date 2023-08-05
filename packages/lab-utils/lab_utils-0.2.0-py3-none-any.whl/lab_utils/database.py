""" Basic interface to a `PostgreSQL <https://www.postgresql.org/>`_ database.

The module consists of a main class :class:`Database <Database>` which
implements methods for connection and disconnection, table verification
and data insertion.

The database settings are set with a
:doc:`config file<../examples/conf/conf_database>`
and the standard library :obj:`configparser`.
"""

import configparser
import logging
from pkg_resources import resource_filename
from enum import Enum

import psycopg2
from psycopg2 import sql


class DataType(Enum):
    """ List of accepted data types for new columns.
    The types are hard-coded for safety reasons: SQL
    insertions are potentially dangerous. See
    `here <https://www.postgresqltutorial.com/postgresql-data-types/>`_
    for more information.
    """

    bool = 'BOOLEAN'        #: Boolean
    short = 'SMALLINT'      #: Integer (2 bytes, range is -32,768 to +32,767)
    int = 'INTEGER'         #: Integer (4 bytes, range is -2,147,483,648 to +2,147,483,647)
    long = 'BIGINT'         #: Integer (8 bytes, range is -9,223,372,036,854,775,808 to +9,223,372,036,854,775,807)
    float = 'FLOAT(24)'     #: Floating-point number, 4 bytes
    double = 'FLOAT(53)'    #: Floating-point number, 8 bytes
    string = 'TEXT'         #: String, unlimited length
    time = 'TIMESTAMPTZ'    #: Time stamp, with time zone information

    def __str__(self) -> str:
        """ Parse the data type as an SQL string
        Returns
        -------
        str
            The SQL query
        """
        return str(self.value)


class Constraint(Enum):
    """ List of accepted constraints for new columns.
    The constraints are hard-coded for safety reasons:
    SQL insertions are potentially dangerous.
    """
    positive = ''' CHECK({column_name} >= 0) '''            #: The variable must be greater or equal to 0
    positive_strict = ''' CHECK({column_name} > 0) '''      #: The variable must be strictly positive

    def __str__(self) -> str:
        """ Parse the constraint as an SQL string
        Returns
        -------
        str
            The SQL query
        """
        return str(self.value)


class Database:
    """Manages connections and operations with a PostgreSQL database.
    The class is based on the library :obj:`psycopg2` and
    on this `tutorial
    <https://www.postgresqltutorial.com/postgresql-python/>`_.
    """

    _host: str = 'localhost'        #: The host name where the database is located
    _port: int = 5432               #: Connection port
    _database: str = 'beam'         #: The database name to connect to
    _user: str = 'cw-beam'          #: User name
    _passfile: str = '~/.pgpass'    #: Location of the pgpass file with the credentials

    _connection = None              #: Connection object returned by psycopg2.connect()
    _db_version: str = ''           #: Database version
    _cursor = None                  #: Cursor provided by _connection.cursor() to execute an SQL query

    # List of predefined SQL queries
    _query_createTimeTable = '''
        CREATE TABLE {table_name} (
            time TIMESTAMPTZ NOT NULL {default}
        )
    '''
    _query_makeTimescaleHypertable = '''
    SELECT create_hypertable (
        %(table_name)s,
        %(key)s
    );
    '''
    _query_checkColumn = '''
        SELECT EXISTS
        (SELECT 1
        FROM information_schema.columns
        WHERE
        table_schema = %(table_schema)s
        AND
        table_name = %(table_name)s
        AND
        column_name = %(column_name)s
        );
    '''
    _query_checkTable = '''
        SELECT EXISTS
        (SELECT 1
        FROM information_schema.columns
        WHERE
        table_schema = %(table_schema)s
        AND
        table_name = %(table_name)s)
        ;
    '''
    _query_addColumn = '''
        ALTER TABLE {table_name}
        ADD COLUMN {column_name}
        {data_type}
        {checks}
        ;
    '''
    _query_insertData = '''
        INSERT INTO {table_name} ({columns})
        VALUES ({data})
        ;
    '''

    def __init__(self, config_file: str = None):
        """ Initializes the :class:`Database` object. If a
        :paramref:`configuration file name<Database.__init__.config_file>`
        is given, the constructor calls the method
        :meth:`~.Database.config` and overrides the default attributes

        Parameters
        ----------
            config_file : str, optional
                Configuration file name, default is `None`. See
                :doc:`here<../../../examples/conf/conf_database>`
                for a configuration file example

        Raises
        ------
        :class:`configparser.Error`
            If a configuration file name was given, the method
            :meth:`config` can fail raising this exception.
        """

        # Read config file, if given
        if config_file is not None:
            self.config(config_file)

    def __del__(self):
        """ Closes the connection to the database, if it was ever open.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """
        self.close()

    def config(self, config_file: str = resource_filename(__name__, 'conf/database.ini')):
        """ Loads the configuration.

        The method reads the :paramref:`config_file`
        using the library :obj:`configparser`. The
        structure of the file is shown in the
        :ref:`examples section<configuration-files>`.

        Parameters
        ----------
        config_file : str, optional
            :doc:`Configuration file name<../../../examples/conf/conf_database>`,
            default is 'conf/database.ini'

        Raises
        ------
        :class:`configparser.Error`
            Error while parsing the file, e.g. no file was found,
            a parameter is missing or it has an invalid value.
        """

        # Use a logger named like the module itself
        logger = logging.getLogger(__name__)
        logger.info("Loading configuration file %s", config_file)

        try:
            # Initialize config parser and read file
            config_parser = configparser.ConfigParser()
            config_parser.read(config_file)

            # Assign values to class attributes
            self._host = config_parser.get(section='Overall', option='host', fallback='localhost')
            self._port = config_parser.getint(section='Overall', option='port', fallback=5432)
            self._database = config_parser.get(section='Overall', option='database', fallback='beam')
            self._user = config_parser.get(section='Overall', option='user', fallback='cw-beam')
            self._passfile = config_parser.get(section='Overall', option='passfile', fallback='~/.pgpass')

        except configparser.Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def connect(self, print_version: bool = False):
        """ Connects to the database.

        If the connection was successful and the flag
        :paramref:`~Database.connect.print` was set, it also
        prints the database version as a connection check.

        Parameters
        ----------
        print_version : bool, optional
            Print the database version, default is False.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """
        # Use a logger named like the module itself
        logger = logging.getLogger(__name__)
        logger.info('Connecting to database <%s> on host <%s> over port <%d> as user <%s>',
                    self._database,
                    self._host,
                    self._port,
                    self._user)

        try:
            # Connect to the database
            logger.debug(self._passfile)
            self._connection = psycopg2.connect(
                dbname=self._database,
                user=self._user,
                host=self._host,
                port=self._port,
                passfile=self._passfile)

            # Read database version, serves as connection check
            self._cursor = self._connection.cursor()
            self._cursor.execute('SELECT version()')
            self._db_version = self._cursor.fetchone()

        except psycopg2.Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

        else:
            if print_version:
                logger.info('Connection successful, database version %s', self._db_version)
            else:
                logger.info('Connection successful')

    def close(self):
        """ Closes the connection to the database.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        # Close, if the connection had been opened
        if self._connection is not None:
            logger = logging.getLogger(__name__)
            logger.info('Closing connection to database %s', self._database)
            try:
                self._connection.close()
            except psycopg2.Error as e:
                logger.error("{}: {}".format(type(e).__name__, e))
                raise
            except BaseException as e:
                # Undefined exception, full traceback to be printed
                logger.exception("{}: {}".format(type(e).__name__, e))
                raise
            finally:
                self._connection = None

    def create_timescale_db(self, table_name: str, default_now: bool = True):
        """ Creates a
        `TimescaleDB <https://docs.timescale.com/latest/main>`_ table.

        The table has a single column named 'time'
        with type 'TIMESTAMPTZ'. If the flag
        :paramref:`~Database.create_timescale_db.default_now`
        is set (default is 'True'), the column 'time'
        will default to 'NOW()'

        Parameters
        ----------
        table_name : str
            The name of the table to be checked
        default_now : bool, optional
            Set the 'time' column default to 'NOW()', default is True.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = logging.getLogger(__name__)

        if self._connection is None:
            raise psycopg2.DatabaseError('Trying to access database without initialization')

        try:
            # Prepare query for table creation
            if default_now:
                logger.debug('Creating TimescaleDB table \'%s\' with default \'time\' NOW()', table_name)
                query = sql.SQL(self._query_createTimeTable.format(
                    table_name=table_name,
                    default=sql.SQL('DEFAULT NOW()').as_string(self._connection)
                ))
            else:
                logger.debug('Creating TimescaleDB table \'%s\' without default \'time\'', table_name)
                query = sql.SQL(self._query_createTimeTable.format(
                    table_name=table_name,
                    default=''
                ))

            # Create the table table
            self._cursor.execute(query)

            # Make the table a TimescaleDB Hypertable
            self._cursor.execute(
                self._query_makeTimescaleHypertable,
                {
                    'table_name':   table_name,
                    'key':          'time'
                }
            )
            self._connection.commit()

        except psycopg2.Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def check_table(self, table_name):
        """ Checks if a table exists.

        Parameters
        ----------
        table_name : str
            The name of the table to be checked

        Returns
        -------
        bool
            True if the table exists, False otherwise.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = logging.getLogger(__name__)

        if self._connection is None:
            raise psycopg2.DatabaseError('Trying to access database without initialization')

        try:
            logger.debug('Checking if table %s exists', table_name)
            self._cursor.execute(
                self._query_checkTable,
                {'table_schema':    'public',
                 'table_name':      table_name,
                 }
            )
            reply = self._cursor.fetchone()
            if reply[0]:
                logger.debug('Table %s does exist', table_name)
                return True
            else:
                logger.debug('Table %s does not exist', table_name)
                return False

        except psycopg2.Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def check_column(self, table_name, column_name):
        """ Checks if a column exists in a given table.

        Parameters
        ----------
        table_name : str
            The table where the column has to be checked
        column_name : str
            The column to be checked

        Returns
        -------
        bool
            True if the column exists, False otherwise.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """

        logger = logging.getLogger(__name__)

        if self._connection is None:
            raise psycopg2.DatabaseError('Trying to access a database without initialization')

        try:
            logger.info('Checking if column %s exists in table %s', column_name, table_name)
            self._cursor.execute(
                self._query_checkColumn,
                {'table_schema':    'public',
                 'table_name':      table_name,
                 'column_name':     column_name,
                 }
            )
            reply = self._cursor.fetchone()
            if reply[0]:
                logger.debug('Column %s does exist in table %s', column_name, table_name)
                return True
            else:
                logger.debug('Column %s does not exist in table %s', column_name, table_name)
                return False

        except psycopg2.Error as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def new_column(
            self,
            table_name: str,
            column_name: str,
            data_type: DataType,
            constraints: list = None,
    ):
        """ Creates a new column in a given table.

        If the column already exists, it just returns True.
        If the table does not exist, returns False.

        Parameters
        ----------
        table_name : str
            Name of the table where the column has to be created
        column_name : str
            Name of the column to be created
        data_type : :class:`DataType`
            Data type of the new column
        constraints : list, optional
            List of :class:`Constraints<Constraint>`, default is 'None'

        Raises
        ------
        :class:`TypeError`
            Invalid constraint or data type
        :class:`ValueError`
            Invalid constraint or data type
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """
        logger = logging.getLogger(__name__)

        if self._connection is None:
            raise psycopg2.DatabaseError('Trying to access database without initialization')

        logger.info('Creating column %s in table %s', column_name, table_name)

        # First let's check if the table exists
        if not self.check_table(table_name):
            raise psycopg2.IntegrityError(
                'Trying to create a column in table %s, which does not exist'.format(table_name))

        # Check if the column already exists
        if self.check_column(table_name, column_name):
            logger.info('Column %s already exists in table %s', column_name, table_name)
            return

        # Now let's send the SQL query
        try:
            if constraints is None:
                constraint_list = sql.SQL(' ')
            else:
                constraint_list = sql.SQL(' ').join(
                    sql.SQL(str(k).format(
                        table_name=table_name,
                        column_name=column_name,
                    )) for k in constraints
                )

            query = sql.SQL(self._query_addColumn.format(
                    table_name=table_name,
                    column_name=column_name,
                    data_type=str(data_type),
                    checks=constraint_list.as_string(self._connection),
                )
            )

            self._cursor.execute(query)
            self._connection.commit()

            # Check if the column was created
            if self.check_column(table_name, column_name):
                logger.debug('Column %s successfully created in table %s', column_name, table_name)
            else:
                raise psycopg2.OperationalError(
                    'Column {c} could not be created in table {t}'.format(c=column_name, t=table_name))

        except (psycopg2.Error, TypeError, ValueError, KeyError) as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            # Undefined exception, full traceback to be printed
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

    def new_entry(
            self,
            table_name: str,
            columns: list,
            data: list,
            check_columns: bool = False,
    ):
        """ Inserts data into a given table.

        See :doc:`this example<../../../examples/ex_database>`
        for usage examples

        Parameters
        ----------
        table_name : str
            Name of the table where the data has to be inserted
        columns : list[str]
            List of columns names corresponding to the data
        data : list
            Values of the new data entry
        check_columns : bool, optional
            Check that columns exist before insertion, default is False

        Raises
        ------
        :class:`TypeError`
            Invalid data
        :class:`ValueError`
            Invalid data
        :class:`psycopg2.Error`
            Base exception for all kind of database errors
        """
        logger = logging.getLogger(__name__)

        if self._connection is None:
            raise psycopg2.DatabaseError('Trying to access database without initialization')

        logger.debug('Inserting data into table %s', table_name)

        # Check if the table and the columns exist
        if check_columns:
            if not self.check_table(table_name):
                raise psycopg2.IntegrityError(
                    'Table %s does not exist'.format(table_name))

            for column in columns:
                if not self.check_column(table_name, column):
                    raise psycopg2.IntegrityError(
                        'Column %s does not exist in table %s'.format(column, table_name))

        # Check the list sizes are the same
        if len(data) != len(columns):
            raise psycopg2.DataError('Data and column list have different sizes')

        # Now let's send the SQL query
        try:
            column_list = sql.SQL(', ').join(
                sql.Identifier(n) for n in columns
            )

            values_list = sql.SQL(', ').join(
                sql.Placeholder() for __ in columns
            )

            query = sql.SQL(self._query_insertData.format(
                    table_name=table_name,
                    columns=column_list.as_string(self._connection),
                    data=values_list.as_string(self._connection),
                )
            )

            self._cursor.execute(query, data)
            self._connection.commit()

        except (psycopg2.Error, TypeError, ValueError) as e:
            logger.error("{}: {}".format(type(e).__name__, e))
            raise

        except BaseException as e:
            logger.exception("{}: {}".format(type(e).__name__, e))
            raise

