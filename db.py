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
