# ![Travis](https://img.shields.io/travis/lsst-sqre/sqre-codekit.svg)

# sqre-git-snapshot

LSST DM SQuaRE github snapshot management tools

## Components

### github-snapshot

Makes mirror clones of all public repositories in the specified
organizations.

### snapshot-purger

Removes old snapshots.  Retention criteria are:

1. Everything is retained for a week.
2. Saturday backups are retained for at least a month.
3. First-of-the-month backups are retained for at least 3 months.
4. First-of-the-quarter backups are never automatically deleted.

## Installation

TODO

