# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Plugin Supporting HPSS
- Plugin Supporting Oracle HSM

## [0.4.1] - 2020-05-08
### Changed
- Pull #111 Packaging Improvements Pip>=20 by [@dmlb2000](https://github.com/dmlb2000)

## [0.4.0] - 2020-02-28
### Changed
- Pull #105 Pacifica Namespace fixes by [@dmlb2000](https://github.com/dmlb2000)
- Fix #102 HPSS Latency is an integer by [@dmlb2000](https://github.com/dmlb2000)
- Pull #106 Add Seek and Byte Range Options by [@dmlb2000](https://github.com/dmlb2000)
- Fix #95 Add id2filename documentation by [@dmlb2000](https://github.com/dmlb2000)

## [0.3.0] - 2019-12-12
### Changed
- Pull #100 Add Python 3.7 and 3.8 testing by [@dmlb2000](https://github.com/dmlb2000)
- Fix #96 add HPSS Latency configuration by [@karcaw](https://github.com/karcaw)
- Pull #98 Use Pylint 2.0+ by [@dmlb2000](https://github.com/dmlb2000)
- Pull #97 Remove Python 2.7 support by [@dmlb2000](https://github.com/dmlb2000)

## [0.2.2] - 2019-05-30
### Changed
- Fix #87 and #88 More post deployment testing features by [@dmlb2000](https://github.com/dmlb2000)
- Fix #83 and #84 Update HPSS extentions for Python 3 by [@karcaw](https://github.com/karcaw)
- Update Pipeline to test post deployment more by [@dmlb2000](https://github.com/dmlb2000)

## [0.2.1] - 2019-05-10
### Added
- POSIX Backend Support
- ReadtheDocs supported Sphinx docs
- Backend Plugin API
- Post Install Testing
- REST API for sending and recieving data.
  - PUT - Send data to a file.
  - GET - Get data from a file.
  - POST - Stage a file from tape.
  - HEAD - Get file status.
  - PATCH - Move a file into place.

### Changed
