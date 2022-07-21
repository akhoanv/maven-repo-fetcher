# Maven Repository Fetcher
Quick fetch packages from Maven Central Repository. This is useful for building custom Maven repository

## Features
- Fetching specific package from https://repo1.maven.org/maven2/ automatically given the string format from build.gradle `group.id:artifact-id:version.number`
- Given the right flag, it will also fetch Javadoc, source code, and tests code
- Recursively fetch dependencies down the list until there is no more dependencies to fetch

## Issues
- This script will not be able to resolve dependencies if the version is not defined, or defined as a variable

## Usage

```
usage: mvnrepositoryfetch.py [-h] [--javadoc] [--sources] [--tests] [--recursive] dependencies [dependencies ...]

Fetching packages from Maven central repository

positional arguments:
  dependencies  Dependencies to fetch

optional arguments:
  -h, --help    show this help message and exit
  --javadoc     Fetch Javadoc if available
  --sources     Fetch Source files if available
  --tests       Fetch Tests if available
  --recursive   Recursively fetching dependencies
```
