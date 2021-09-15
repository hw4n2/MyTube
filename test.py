import sqlite3

conn = sqlite3.connect("UserDb.db")
cur = conn.cursor()

cur.execute("CREATE TABLE test ( CHAR(50));")