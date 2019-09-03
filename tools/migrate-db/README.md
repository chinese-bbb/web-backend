# Migrate Sqlite to mysql

> Premise: target db schema has been defined in target rds instance

1. disable public dns to avoid data conflict; make sure sqlite3 and mysql client is installed in target ec2
2. deploy the code target env
3. ssh into target ec2

then
```sh
cd /opt/python/current/app
source /opt/python/run/venv/bin/activate

sudo chmod +x ./tools/migrate-db/migrate-sqlite-to-mysql.sh
sudo chmod +x ./tools/migrate-db/sqlite3-to-mysql.py
sudo chmod +x ./tools/migrate-db/dump-sqlite-db-data.sh

sudo -u wsgi sh ./tools/migrate-db/migrate-sqlite-to-mysql.sh /home/wsgi/app.db
```
