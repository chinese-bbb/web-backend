#! /usr/bin/env python
import fileinput
import re
import tempfile
from optparse import OptionParser


IGNOREDPREFIXES = [
    'PRAGMA',
    'DELETE FROM sqlite_sequence;',
    'INSERT INTO "sqlite_sequence"',
]


def _replace(line):
    if any(line.startswith(prefix) for prefix in IGNOREDPREFIXES):
        return
    #    line = line.replace("INTEGER PRIMARY KEY", "INTEGER PRIMARY KEY")
    line = line.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
    line = line.replace('BEGIN TRANSACTION', 'BEGIN')
    line = line.replace("DEFAULT 't'", 'DEFAULT 1')
    line = line.replace("DEFAULT 'f'", 'DEFAULT 0')
    line = line.replace(",'t'", ',1')
    line = line.replace(",'f'", ',0')
    line = line.replace('COLLATE NOCASE_UTF8', '')
    line = line.replace('DEFERRABLE INITIALLY DEFERRED', '')
    line = line.replace('integer DEFAULT 0 NOT NULL', 'integer NOT NULL DEFAULT 0')
    line = line.replace('integer DEFAULT 1 NOT NULL', 'integer NOT NULL DEFAULT 1')
    line = line.replace('varchar ', 'varchar(255) ')
    line = line.replace('varchar,', 'varchar(255),')
    line = line.replace('varchar)', 'varchar(255))')
    line = line.replace(' BLOB ', ' LONGBLOB ')
    line = re.sub(r'\s+CHECK \(.+\),?', '', line)
    line = re.sub('CREATE INDEX.*?;', '', line)
    line = re.sub('CREATE UNIQUE INDEX.*?;', '', line)
    line = re.sub('.*alembic_version.*', '', line)

    return line


def _backticks(line, in_string):
    """
    Replace double quotes by backticks outside (multiline) strings.

    >>> _backticks('''INSERT INTO "table" VALUES ('"string"');''', False)
    ('INSERT INTO `table` VALUES (\\'"string"\\');', False)

    >>> _backticks('''INSERT INTO "table" VALUES ('"Heading''', False)
    ('INSERT INTO `table` VALUES (\\'"Heading', True)

    >>> _backticks('''* "text":http://link.com''', True)
    ('* "text":http://link.com', True)

    >>> _backticks(" ');", True)
    (" ');", False)
    """
    new = ''
    for c in line:
        if not in_string:
            if c == "'":
                in_string = True
            elif c == '"':
                new = new + '`'
                continue
        elif c == "'":
            in_string = False
        new = new + c
    return new, in_string


def _process(opts, lines):
    if opts.database:
        yield '''\
drop database {d};
create database {d} character set utf8;
grant all on {d}.* to {u}@'%' identified by '{p}';
use {d};\n'''.format(
            d=opts.database, u=opts.username, p=opts.password
        )
    yield "SET sql_mode='NO_BACKSLASH_ESCAPES';\n"

    in_string = False
    for line in lines:
        if not in_string:
            line = _replace(line.decode())
            if line is None:
                continue
        line, in_string = _backticks(line, in_string)
        yield line


def _removeNewline(line, in_string):
    new = ''
    for c in line:
        if not in_string:
            if c == "'":
                in_string = True
        elif c == "'":
            in_string = False
        elif in_string:
            if c == '\n':
                new = new + 'Newline333'
                continue
            if c == '\r':
                new = new + 'carriagereturn333'
                continue
        new = new + c
    return new, in_string


def _replaceNewline(lines):
    for line in lines:
        line = line.replace('Newline333', '\n')
        line = line.replace('carriagereturn333', '\r')
        yield line


def _Newline(lines):
    in_string = False
    for line in lines:
        if line is None:
            continue
        line, in_string = _removeNewline(line, in_string)
        yield line


def main():
    op = OptionParser()
    op.add_option('-d', '--database')
    op.add_option('-u', '--username')
    op.add_option('-p', '--password')
    opts, args = op.parse_args()
    lines = (l for l in fileinput.input(args, openhook=fileinput.hook_encoded('utf-8')))
    lines = (l for l in _Newline(lines))
    f = tempfile.TemporaryFile()
    for line in lines:
        f.write(str.encode(line))
    f.seek(0)
    lines = (l for l in f.readlines())
    f.close()
    lines = (l for l in _process(opts, lines))
    for line in _replaceNewline(lines):
        print(line)


if __name__ == '__main__':
    main()
