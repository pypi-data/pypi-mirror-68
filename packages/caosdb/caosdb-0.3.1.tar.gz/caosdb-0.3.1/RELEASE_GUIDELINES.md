# Release Guidelines for the CaosDB Python Client Library

This document specifies release guidelines in addition to the generel release
guidelines of the CaosDB Project
([RELEASE_GUIDELINES.md](https://gitlab.com/caosdb/caosdb/blob/dev/RELEASE_GUIDELINES.md))

## General Prerequisites

* All tests are passing.
* FEATURES.md is up-to-date and a public API is being declared in that document.
* CHANGELOG.md is up-to-date.
* DEPENDENCIES.md is up-to-date.

## Steps

1. Create a release branch from the dev branch. This prevents further changes
   to the code base and a never ending release process. Naming: `release-<VERSION>`

2. Check all general prerequisites.

3. Prepare [setup.py](./setup.py): Update the `MAJOR`, `MINOR`, `MICRO`, `PRE`
   variables and set `ISRELEASED` to `True`. Use the possibility to issue
   pre-release versions for testing.

4. Merge the release branch into the master branch.

5. Tag the latest commit of the master branch with `v<VERSION>`.

6. Delete the release branch.

7. Remove possibly existing `./dist` directory with old release.

8. Publish the release by executing `./release.sh` with uploads the caosdb
   module to the Python Package Index [pypi.org](https://pypi.org).

9. Merge the master branch back into the dev branch.
