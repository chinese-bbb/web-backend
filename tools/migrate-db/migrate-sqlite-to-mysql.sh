#!/usr/bin/env bash

if [ -z "$1" ]
then
  echo "empty db path"
  exit 1
fi

sqlite3 $1 < `dirname $0`/clean-invalid-data.sql

`dirname $0`/dump-sqlite-db-data.sh $1

# only valid on eb env
source /opt/python/current/env

mysql -h $AWS_RDS_MYSQL_HOST -u admin -p huxindb < corrected-data.sql
