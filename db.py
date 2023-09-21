import sqlite3
import os


class DB():
    def __init__(self):
        if not os.path.isfile('EasyTask.db'):
            self.current_oid = 0
            self.conn = sqlite3.connect("EasyTask.db")
            self.cur = self.conn.cursor()
            self.cur.execute("CREATE TABLE tasks(name TEXT, difficulty INTEGER)")
        else:
            self.conn = sqlite3.connect("EasyTask.db")
            self.cur = self.conn.cursor()
            fhandler1 = open('record.txt', 'r')
            self.current_oid = int(fhandler1.read())

    def insert(self, name, difficulty):
        self.cur.execute("INSERT INTO tasks VALUES (?, ?)",
                         (name, difficulty))
        self.conn.commit()

    def delete_last_entry(self, oid):
        self.cur.execute("DELETE FROM tasks WHERE oid=(SELECT MAX(oid) FROM tasks)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()