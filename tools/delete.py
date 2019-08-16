import sqlite3

# sudo -u wsgi python delete.py

sqlite_file = '/home/wsgi/app.db'    # name of the sqlite database file
table1      = 'user'
field1      = 'username'
data1       = '13750046503'

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# c.execute("SELECT * FROM user WHERE username = '13750046503'")

c.execute("SELECT * FROM {table1} WHERE {field1} = {data1} "\
          .format(table1=table1, field1=field1, data1=data1))

all_rows = c.fetchall()
print('1):', all_rows)

# c.execute("DELETE FROM user WHERE username = '13750046503'")
# c.execute("DELETE FROM {user} WHERE {field1} = {data1}"\
#           .format(table1=table1, field1=field1, data1=data1))
conn.commit()

# c.execute("SELECT * FROM user WHERE username = '13750046503'")
c.execute("SELECT * FROM {user} WHERE {field1} = {data1}"\
          .format(table1=table1, field1=field1, data1=data1))
all_rows = c.fetchall()
print('2):', all_rows)

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
