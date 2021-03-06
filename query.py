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

    def APIshowpartiesbyid(self,PartyId):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            
            cur.execute(
                '''
                SELECT Parties.id, Parties.UrlPicture , Members.Name, Parties.PartyName, Parties.FavoriteCount
                from Members inner join Parties on Parties.MemberId = Members.id
                where Members.PositionId = 1 and Parties.Id = ?
                ''',[PartyId])

            data = cur.fetchall()
            result = []
            for i in range(len(data)):
                a = {"Url":data[i][0],
                     "LeaderName": data[i][1],
                     "PartyName": data[i][2],
                     "Count": data[i][3]}    
                result.append(a)
            # return jsonify(result)
            return data

    def APIshowpartiesforgovernment(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            
            cur.execute(
                '''
                SELECT Parties.id, Members.Name, Parties.PartyName, Parties.FavoriteCount
                from Members inner join Parties on Parties.MemberId = Members.id
                where Members.PositionId = 1
                ''')

            data = cur.fetchall()
            result = []
            # return jsonify(result)
            return data

    def APIshowpartiesforuser(self,userid):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            address = conn.cursor()
            member = conn.cursor()

            address.execute(
                '''
                select Addresses.Id
                from Addresses
                inner join Users on Users.AddressId = Addresses.Id
                where Addresses.id = ? and Users.AddressId = ?
                ''',[userid, userid])

            useraddressid = address.fetchone()

            cur.execute(
                '''
                SELECT Parties.id, Parties.PartyName, Members.Name
                from Members
                inner join Parties on Parties.id = Members.PartyId
                where AddressId = 1
                ''')
            
            data = cur.fetchall()
            return data

    def APIloginUser(self, CitizenId, BirthDate, Password):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT Users.id, Users.Name, Users.CitizenId, Users.BirthDate, Logins.Password
                from Logins inner join Users on Users.id = Logins.UserId
                WHERE CitizenId = ? AND BirthDate = ? AND Password = ?
                ''', [CitizenId, BirthDate, Password])
            return cur.fetchone()

    def APIloginGovernment(self, Role, Password):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT Role, Password
                from Logins
                where Role = ? and Password = ?
                ''',[Role, Password])

            return cur.fetchone()

    def APIinsertparty(self):
        if request.method == 'POST':
            partyname = request.form['partyname']
            leadername = request.form['leadername']
            province = request.form['province']
            district = request.form['district']
            with sqlite3.connect(LOCAL_DB) as conn:
                cur = conn.cursor()
                address = conn.cursor()
                member = conn.cursor()

                address.execute(
                '''
                select id 
                from Addresses
                where Province = ? and District = ?
                ''', [province, district]
                )

                addressid = address.fetchone()
                
                cur.execute(
                '''
                insert into Members (Name, AddressId, PositionId) 
                values (?, ?, 1)
                ''', [leadername, addressid[0]]
                )

                member.execute(
                '''
                select id 
                FROM Members
                ORDER BY ID DESC LIMIT 1
                '''
                )

                memberid = member.fetchone()

                cur.execute(
                '''
                insert into Parties (MemberId, PartyName, FavoriteCount, UrlPicture) 
                values (?, ?, 0, null)
                ''', [memberid[0], partyname]
                )
                
                data = cur.execute()
                conn.commit()
            # return redirect(url_for('Showdata'))
            return data

    def APIshowtopfavorite(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT Parties.PartyName, Members.Name, Parties.FavoriteCount
                from Parties
                inner join Members on Parties.MemberId = Members.id
                order by Parties.FavoriteCount desc limit 3
                ''')
            return cur.fetchall()

    def APIupdateUser(self, userid, Province, District, Phonenumber):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            address = conn.cursor()
            
            address.execute(
            '''
                select id
                from Addresses
                where Province = ? and District = ?
            ''',[Province, District])

            addressid = address.fetchone()
            print(addressid)
            cur.execute(
                '''
                update Users
                set Phonenumber = ?,
                    AddressId = ?
                where id = ?

                ''', [Phonenumber, addressid[0], userid])
            return cur.fetchone()

    def APIinsertparty(self, partyname, leadername, province, district):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            address = conn.cursor()
            member = conn.cursor()

            address.execute(
            '''
            select id 
            from Addresses
            where Province = ? and District = ?
            ''', [province, district]
            )

            addressid = address.fetchone()
            
            cur.execute(
            '''
            insert into Members (Name, AddressId, PositionId) 
            values (?, ?, 1)
            ''', [leadername, addressid[0]]
            )

            member.execute(
            '''
            select id 
            FROM Members
            ORDER BY ID DESC LIMIT 1
            '''
            )

            memberid = member.fetchone()

            cur.execute(
            '''
            insert into Parties (MemberId, PartyName, FavoriteCount, UrlPicture) 
            values (?, ?, 0, null)
            ''', [memberid[0], partyname]
            )

            return cur.fetchall()

    def APIdeleteparty(self,partyid):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                delete from Favorites
                where PartyId = ?
                ''',[partyid]
                )
            
            cur.execute(
                '''
                delete from Parties
                where id = ?
                ''',[partyid]
                )
            
            cur.execute(
                '''
                delete from Members
                where PartyId = ?
                ''',[partyid])
            
            conn.commit()
            return cur.fetchall()

    def APIaddmember(self,partyid, name, position, province, district):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            address = conn.cursor()
            positioncur = conn.cursor()

            address.execute(
                '''
                select id
                from Addresses
                where Province = ? and District = ?
                ''',[province, district] 
                )
            addressid = address.fetchone()
            
            positioncur.execute(
                '''
                select id
                from Positions
                where PositionName = ?
                ''',[position]
                )
            positionid = positioncur.fetchone()

            cur.execute(
                '''
                insert into Members (Name, AddressId, PositionId, PartyId)
                values (?,?,?,?)
                ''',[name, addressid[0], positionid[0], partyid]
                )
            
            return cur.fetchall()

    def APIdeletemember(self,partyid, name):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                delete
                from Members
                where name = ? and PartyId = ?
                ''',[name, partyid] 
                )
            
            return cur.fetchall()

    def APIaddfavorite(self,partyid, userid):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                insert into Favorites (UserId, PartyId)
                values(?,?)
                ''',[userid, partyid]
                )
            
            cur.execute(
                '''
                update getParties
                set FavoriteCount = FavoriteCount+1
                where id = ?
                ''',[partyid]
                )
            
            return cur.fetchall()
    
    def APIshowfavorite(self, userid):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
            '''
            select Favorites.id, Parties.Name, Members.Name
            from Parties
            inner join Favorites on Favorites.PartyId = Parties.id
            inner join Members on Members.PartyId = PartyId
            where Favorites.Userid = ?
            ''',[userid]
            )
            return cur.fetchall()
            
queryfunc = QueryFunction()
