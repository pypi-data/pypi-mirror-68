#!/usr/bin/env python3
from pathlib import Path
import re
import sys
import textwrap

#
# a basic release automation script
#
# This should only be called from the Makefile
#

VERSION_FILE = Path('src') / 'cutest' / '_version.py'

help_message = '\n'.join(textwrap.wrap(
    "The argument must be formatted as either 'major', 'minor', 'patch'"
    " or 'X.X.X'\nIf one of the first three options is used then that "
    "part of the version will be incremented and all lesser parts of "
    "the version will be reset to 0."
))


def read_version(string=False):
    with open(VERSION_FILE, 'r') as fp:
        match = re.match(r"^version = '(\d+)\.(\d+)\.(\d+)'$", fp.read())
        if match:
            version_tup = match.groups()
            if string:
                return '.'.join(version_tup)
            else:
                return tuple(int(v) for v in version_tup)
        else:
            raise ValueError('Version file is improperly formatted')


def write_version(major, minor, patch):
    with open(VERSION_FILE, 'w') as fp:
        fp.write(f"version = '{major}.{minor}.{patch}'\n")


def main():
    # when called from the makefile we expect only 1 arg
    assert len(sys.argv) == 2

    arg = sys.argv[1]

    major, minor, patch = read_version()
    print(f'Previous version set to {major}.{minor}.{patch}')

    if arg == 'help':
        print(help_message, file=sys.stderr)
        exit(0)
    elif arg == 'major':
        major += 1
        minor = 0
        patch = 0
    elif arg == 'minor':
        minor += 1
        patch = 0
    elif arg == 'patch':
        patch += 1
    # of form X.X.X
    elif re.match(r'^\d*\.\d*\.\d*$', arg):
        major, minor, patch = tuple(arg.split('.'))
    else:
        print(help_message, file=sys.stderr)
        exit(1)

    write_version(major, minor, patch)
    print('\n'.join(textwrap.wrap(
        f'New version successfully set to {major}.{minor}.{patch}. To '
        'finish release, commit changes. Then create a release on '
        'github with this version number. Travis will automatically '
        'upload to PyPI'
    )))


if __name__ == '__main__':
    main()
