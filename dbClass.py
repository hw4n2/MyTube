import sqlite3

class UseDb:

    def __init__(self):
        pass

    def insert1Db(self, table, col, val):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO " + table + " (" + col + ") VALUES ('" + val + "');")
        conn.commit()
        conn.close()

    def insert2Db(self, table, col1, col2, val1, val2):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        cur.execute("INSERT INTO " + table + " (" + col1 + ", " + col2 + ") VALUES ('" + val1 + "', '" + val2 + "');")
        conn.commit()
        conn.close()

    def select1Db(self, table, col, colWh, val):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        cur.execute("SELECT " + col + " FROM " + table + " WHERE " + colWh + " = '" + val + "';")
        data = cur.fetchall()
        conn.close()

        return data

    def select2Db(self, table, col1, col2, colWh, val):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        cur.execute("SELECT " + col1 + ", " + col2 + " FROM " + table + " WHERE " + colWh + " = '" + val + "';")
        data = cur.fetchall()
        conn.close()
    
        return data

    def update1Db(self, table, col, colWh, wh, val):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        cur.execute("UPDATE " + table + " SET " + col + " = ? WHERE " + colWh + " = '" + wh + "';", (val,))
        conn.commit()
        conn.close()