# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.17] - 2023-03-09
### Changes
- add_member function now takes the permissions as argument instead of a profile
- allowing function "safe.list" to get details for backward comp
- adding system_health related functions

### Bugfixes
- Fixed the type of args for safe search function from string to boolean
- Changing filecategory now returns the updated account (instead of None)


## [0.0.16] - 2023-03-09
### Changes
- Added the add / delete functions in users
- Added the ability to recover password versions
- Added the ability to set a password
- Added the ability to set a password from versions
- Improved the FC update functions
- Improved the safe search functions

### Bugfixes
- Raise the ChallengeResponseException properly