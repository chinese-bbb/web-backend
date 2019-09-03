# Migrate Sqlite to mysql

> Premise: target db schema has been defined in target rds instance

1. disable public dns to avoid data conflict
2. deploy the code target env
3. ssh into target ec2

then
```sh
cd /opt/python/current/app
source /opt/python/run/venv/bin/activate
./tools/migrate-db/migrate-sqlite-to-mysql.sh /home/wsgi/app.db
```
