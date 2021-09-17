import sqlite3

class DbInit:
 
    def __init__(self):
        self.conn = sqlite3.connect("UserDb.db")
        self.cur = self.conn.cursor()

    def initTable(self):
        self.cur.execute("CREATE TABLE user (id VARCHAR(20), pwd VARCHAR(12) , nickname VARCHAR(11), phone CHAR(11));")
        
        
        # self.cur.execute("DROP TABLE aaaa")
        # self.cur.execute("DROP TABLE user")



if __name__ == "__main__":
    db = DbInit()
    db.initTable()