import sqlite3
import typing as tp
from aiogram import types  # type: ignore
from .helper_classes import LogItem
from datetime import datetime

selects: tp.Dict[str, str] = {
    'create_table': 'CREATE TABLE IF NOT EXISTS logs'
                    '(chat_id INTEGER, name VARCHAR(100), '
                    'search_time TIMESTAMP)',
    'insert_log': 'INSERT INTO logs VALUES (?, ?, ?)',
    'get_logs': 'SELECT chat_id, name, search_time from logs '
                'WHERE chat_id = ?',
    'get_stats': 'SELECT name, COUNT(*) as cnt FROM logs '
                 'WHERE chat_id = ?'
                 'GROUP BY name ORDER BY cnt desc'
}


class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('bot_db.sql')
        self.cur = self.conn.cursor()
        self.cur.execute(selects['create_table'])
        self.conn.commit()

    def insert_log(self, log: LogItem):
        self.cur.execute(
            selects['insert_log'],
            (log.chat_id, log.name, log.search_time)
        )
        self.conn.commit()

    def get_history(self, chat_id: types.base.Integer):
        self.cur.execute(selects['get_logs'], (chat_id,))
        logs = self.cur.fetchall()
        res = []
        for log in logs:
            search_date = datetime.strptime(
                log[2].split('.')[0], "%Y-%m-%d %H:%M:%S"
            )
            res.append(LogItem(log[0], log[1], search_date))
        return reversed(res)

    def get_stats(self, chat_id: types.base.Integer):
        self.cur.execute(selects['get_stats'], (chat_id,))
        return self.cur.fetchall()
