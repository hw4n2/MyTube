import sqlite3

class UseDb:

    def insert(self, table, columns, values):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        sqlstring = "INSERT INTO " + table + " ("

        for col in columns:
            sqlstring += col + ","
        
        sqlstring = sqlstring[:-1]
        sqlstring += ") VALUES ("

        for val in values:
            sqlstring += "'" + val + "',"

        sqlstring = sqlstring[:-1]
        sqlstring += ");"

        cur.execute(sqlstring)
        conn.commit()
        conn.close()

    def select(self, table, columns, where, value):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        sqlstring = "SELECT "
        
        for col in columns:
            sqlstring += col + ", "
        
        sqlstring = sqlstring[:-2]
        sqlstring += " FROM " + table + " WHERE " + where + " = '" + value + "';"

        cur.execute(sqlstring)
        data = cur.fetchall()
        return data

    def delete(self, table, where, value):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        cur.execute("DELETE FROM " + table + " WHERE " + where + " = '" + value + "';")

        conn.commit()
        conn.close()

    def update(self, table, columns, values, where, value):
        conn = sqlite3.connect("UserDb.db")
        cur = conn.cursor()

        sqlstring = "UPDATE " + table + " SET "
        for i in range(0, len(columns)):
            sqlstring += columns[i] + " = '" + values[i] + "', "
        
        sqlstring = sqlstring[:-2]
        sqlstring += " WHERE " + where + " = '" + value + "';"

        cur.execute(sqlstring)
        conn.commit()
        conn.close()
