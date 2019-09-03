#!/usr/bin/env bash

db_path=$1

if [ -z "$db_path" ]
then
  echo "empty db path"
  exit 1
else
  echo db path is $db_path
fi

sqlite3 $db_path .schema > schema.sql
sqlite3 $db_path .dump > dump.sql
grep -vx -f schema.sql dump.sql > data.sql
python `dirname $0`/sqlite3-to-mysql.py data.sql > corrected-data.sql
#rm schema.sql dump.sql data.sql
