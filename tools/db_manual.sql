# We recommend using sqlite-web to run sql statement onto sqlite.
# Installation instructions:
# pip install sqlite_web
# sqlite_web app.db


# Steps to evolve DB from Huxin v1 to v2

# 1: remove all type5 complaints
DELETE FROM complaint WHERE complain_type = 'type5';

# 2: remove all complaints whose files cannot be displayed
DELETE FROM complaint WHERE id <= 17;

# 3. add urole column to user table
ALTER TABLE user ADD urole varchar(140) DEFAULT 'normal';
update user set urole = 'admin' where username = '13333333333';

