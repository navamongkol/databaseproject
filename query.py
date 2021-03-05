import sqlite3
from flask import Flask, render_template, request
import json
# from common import config
# from cv import backend
LOCAL_DB = 'local.db'
class QueryFunction:
    def __init__(self):
        self.x = True

    def selectMember(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT Name from Members Where id > 6
                ''')
            
            return cur.fetchall()
queryfunc = QueryFunction()
