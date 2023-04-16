import sqlite3
from time import time

class Log():
    def __init__(self, database: str):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()
        self.init_tables()

    def close(self):
        self.con.close()

    def init_tables(self):
        sql_encoded = """CREATE TABLE IF NOT EXISTS encoded (
            filename TEXT PRIMARY KEY,
            ts INTEGER,
            deleted INTEGER
        )"""
        self.cur.execute(sql_encoded)
        self.con.commit()

    def encoded_insert(self, fn: str):
        sql = "INSERT INTO encoded (filename, ts, deleted) VALUES (?,?,?)"
        param = (fn, int(time()), 0)
        self.cur.execute(sql, param)
        self.con.commit()

    def encoded_select(self, ts_lt: int, deleted: int = 0) -> list:
        sql = "SELECT filename FROM encoded WHERE ts < ? AND deleted = ?"
        param = (ts_lt, deleted)
        return self.cur.execute(sql, param)

    def encoded_deleted(self, fn: str):
        sql = "UPDATE encoded SET deleted = ? WHERE filename = ?"
        param = (1, fn)
        self.cur.execute(sql, param)
        self.con.commit()
