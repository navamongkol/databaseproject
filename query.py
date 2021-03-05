import sqlite3
from flask import Flask, render_template, request, jsonify
import json
# import jsonify
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
                SELECT id, Name from Members Where id > 6
                ''')

            data = cur.fetchall()
            result = []
            for i in range(len(data)):
                a = {"id":data[i][0],
                     "name": data[i][1]}    
                result.append(a)
            return jsonify(result)
         
    def showparties(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT Parties.id , Members.Name, Parties.PartyName, Parties.FavoriteCount
                from Members inner join Parties on Parties.MemberId = Members.id
                
                ''')

            data = cur.fetchall()
            result = []
            for i in range(len(data)):
                a = {"id":data[i][0],
                     "LeaderName": data[i][1],
                     "PartyName": data[i][2],
                     "Count": data[i][3]}    
                result.append(a)
            return jsonify(data)

queryfunc = QueryFunction()
