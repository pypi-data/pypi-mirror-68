# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## TODO

- Implement multithreading

## [0.2.0] - 2020-05-08

- Implement CI with [.__gitlab-ci.yml](.gitlab-ci.yml).
- Improve documentation
- Module socket_comm:
 -  Implement [method](https://lab-utils.readthedocs.io/en/v0.2.0/api/socket_comm/ArgumentParser/lab_utils.socket_comm.ArgumentParser.full_help.html)
    to send a complete help message to the client.
 -  Implement signal ahndler to deal with Ctrl+C nicely
 - Expand [examples](examples/socket_comm) 

## [0.1.0] - 2020-05-05

- First release of the **lab-utils** package
- Installation instructions and setup
- Modules available: **database** and **socket_comm**

[0.1.0]: https://gitlab.ethz.ch/exotic-matter/cw-beam/lab-utils/tree/v0.1.0
[0.1.0]: https://gitlab.ethz.ch/exotic-matter/cw-beam/lab-utils/tree/v0.2.0