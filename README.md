# maven-repo-fetcher
Quick fetch packages from Maven Central Repository

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
