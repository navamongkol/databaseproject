import sqlite3
from flask import Flask, render_template, request
import json
# from common import config
# from cv import backend
LOCAL_DB = 'local.db'
class LocalStorage:
    
    def __init__(self):
        # self.connection = sqlite3.connect(config.LOCAL_DB)
        # self.cursor = self.connection.cursor()
        if not self.checkTableExist():
            print("Helloworld")
            self.initializeDatabase()
            

    def initializeDatabase(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                CREATE TABLE Positions (
                ID INTEGER PRIMARY KEY,
                PositionName TEXT
                ) 
                ''')

            cur.execute(
                '''
                CREATE TABLE Addresses (
                ID INTEGER PRIMARY KEY,
                Province TEXT,
                District TEXT
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE Members (
                ID INTEGER PRIMARY KEY,
                Name TEXT,
                AddressId INTEGER,
                PositionId INTEGER,
                PartyId INTEGER,
                FOREIGN KEY (PositionId) REFERENCES Positions(ID),
                FOREIGN KEY (AddressId) REFERENCES Addresses(ID),
                FOREIGN KEY (PartyId) REFERENCES Parties(ID)
                )
                ''')
            
            cur.execute(
                '''
                CREATE TABLE Users (
                ID INTEGER PRIMARY KEY,
                CitizenId TEXT,
                Name TEXT,
                BirthDate TEXT,
                PhoneNumber TEXT,
                AddressId INTEGER,
                FOREIGN KEY (AddressId) REFERENCES Addresses(ID)
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE Parties (
                ID INTEGER PRIMARY KEY,
                PartyName TEXT,
                FavoriteCount INT,
                UrlPicture TEXT NULL
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE Logins (
                ID INTEGER PRIMARY KEY,
                Role TEXT,
                UserId INTEGER NULL,
                Password INTEGER,
                FOREIGN KEY (UserId) REFERENCES Users(ID)
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE Favorites (
                ID INTEGER PRIMARY KEY,
                UserId INTEGER,
                MemberId INTEGER,
                FOREIGN KEY (UserId) REFERENCES Users(ID),
                FOREIGN KEY (MemberId) REFERENCES Members(ID)
                )
                ''')

            conn.commit()


    def checkTableExist(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                SELECT count(name) 
                FROM sqlite_master 
                WHERE type='table' 
                    AND 
                    name='Positions' 
                ''')  
            
            if cur.fetchone()[0] == 1:
                return True
            else:
                return False

    def get_tablePositions(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT *
                FROM Positions
                ''')
            
            return cur.fetchall()

    def get_tableAddresses(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT *
                FROM Addresses
                ''')
            
            return cur.fetchall()

    def get_tableMembers(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT *
                FROM Members
                ''')
            
            return cur.fetchall()
    
    def get_tableUsers(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT *
                FROM Users
                ''')
            
            return cur.fetchall()
    
    def get_tableLogins(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT *
                FROM Logins
                ''')
            
            return cur.fetchall()
    
    def get_tableParties(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT *
                FROM Parties
                ''')
            
            return cur.fetchall()

    def get_tableFavorites(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                SELECT *
                FROM Favorites
                ''')
            
            return cur.fetchall()

    def insert_positions(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                insert into Positions (PositionName) values ('Leader');
                ''')

            cur.execute(
                '''
                insert into Positions (PositionName) values ('Secretary');
                ''')
            
            cur.execute(
                '''
                insert into Positions (PositionName) values ('Manager');
                ''')

            cur.execute(
                '''
                insert into Positions (PositionName) values ('General');
                ''')

            conn.commit()
    
    def insert_addresses(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                INSERT into Addresses (Province, District) values ('Bangkok', 'Dusit');
                ''')

            cur.execute(
                '''
                INSERT into Addresses (Province, District) values ('Bangkok', 'Jatujuk');
                ''')
            
            cur.execute(
                '''
                INSERT into Addresses (Province, District) values ('Nonthaburi', 'Bangyai');
                ''')

            cur.execute(
                '''
                INSERT into Addresses (Province, District) values ('Nonthaburi', 'Pakkret');
                ''')

            conn.commit()

    def insert_members(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                INSERT into Members (name, AddressId, PositionId, PartyId) values ('ThanathornJuangroongruangkit', 2, 1, 1);
                ''')

            cur.execute(
                '''
                INSERT into Members (name, AddressId, PositionId, PartyId) values ('PiyabutrSangkanokul', 2, 2, 1);

                ''')
            
            cur.execute(
                '''
                INSERT into Members (name, AddressId, PositionId, PartyId) values ('KultidaRungruengkiet', 1, 3, 1);
                ''')

            cur.execute(
                '''
                INSERT into Members (name, AddressId, PositionId, PartyId) values ('ChumnanJunreuang', 3, 4, 1);
                ''')
            
            cur.execute(
                '''
                INSERT into Members (name, AddressId, PositionId, PartyId) values ('PrayuthJanOCha', 4, 1, 2);
                ''')
            
            cur.execute(
                '''
                INSERT into Members (name, AddressId, PositionId, PartyId) values ('PravitWongsuwan', 5, 2, 2);
                ''')
            
            cur.execute(
                '''
                INSERT into Members (name, AddressId, PositionId, PartyId) values ('AnuchaNakasai', 1, 3, 2);
                ''')
            
            cur.execute(
                '''
                INSERT into Members (name, AddressId, PositionId, PartyId) values ('SontirakSonthijitrawong', 1, 4, 2);
                ''')

            conn.commit()
        
    def insert_users(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                INSERT into Users (CitizenId, name, BirthDate, PhoneNumber, AddressId)
                values ('1138492850123', 'KimmyJosh', '25/01/2001', '0942851923', 1);
                ''')

            cur.execute(
                '''
                INSERT into Users (CitizenId, name, BirthDate, PhoneNumber, AddressId)
                values ('3340129550123', 'EmilyKeen', '14/03/1992', '0852849382', 2);
                ''')
            
            cur.execute(
                '''
                INSERT into Users (CitizenId, name, BirthDate, PhoneNumber, AddressId)
                values ('1827593728412', 'KidneyRose', '14/05/1998', '0851925823', 3);
                ''')

            cur.execute(
                '''
                INSERT into Users (CitizenId, name, BirthDate, PhoneNumber, AddressId)
                values ('1182958302323', 'TeylorHowl', '16/12/1999', '0901482932', 4);
                ''')
            
            cur.execute(
                '''
                INSERT into Users (CitizenId, name, BirthDate, PhoneNumber, AddressId)
                values ('1109892729311', 'DannialOwen', '27/09/1988', '0871925832', 5);
                ''')
            
            cur.execute(
                '''
                INSERT into Users (CitizenId, name, BirthDate, PhoneNumber, AddressId)
                values ('3301923124894', 'JoshWilliam', '20/05/2000', '0989182412', 6);
                ''')

            conn.commit()

    def insert_logins(self):

        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                insert into Logins (Role, UserId, Password) values ('Admin', null, 'jIMPlNq');
                ''')

            cur.execute(
                '''
                insert into Logins (Role, UserId, Password) values ('User', 1, 'TCdCUjf1j');
                ''')
            
            cur.execute(
                '''
                insert into Logins (Role, UserId, Password) values ('User', 2, 'U6fmU9n');
                ''')

            cur.execute(
                '''
                insert into Logins (Role, UserId, Password) values ('User', 3, 'faZ9Ll1k4');
                ''')
            
            cur.execute(
                '''
                insert into Logins (Role, UserId, Password) values ('User', 4, '4n8oTbHc1SbZ');
                ''')
            
            cur.execute(
                '''
                insert into Logins (Role, UserId, Password) values ('Admin', null, '0Ip1iPm');
                ''')

            cur.execute(
                '''
                insert into Logins (Role, UserId, Password) values ('User', 5, 's9vQtqlI');
                ''')

            cur.execute(
                '''
                insert into Logins (Role, UserId, Password) values ('User', 6, 'r9DHsNQ3QdN');
                ''')

            conn.commit()
    
    def insert_parties(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                insert into Parties (PartyName, FavoriteCount, UrlPicture) values ('MoveForward', 3000, null);
                ''')

            cur.execute(
                '''
                insert into Parties (PartyName, FavoriteCount, UrlPicture) values ('Pracharat', '3000', null);
                ''')
            
            conn.commit()
    
    def insert_favorites(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()

            cur.execute(
                '''
                insert into Favorites (UserId, MemberId) values (1,1);
                ''')

            cur.execute(
                '''
                insert into Favorites (UserId, MemberId) values (2,2);
                ''')

            cur.execute(
                '''
                insert into Favorites (UserId, MemberId) values (3,5);
                ''')

            cur.execute(
                '''
                insert into Favorites (UserId, MemberId) values (4,6);
                ''')
            
            conn.commit()

storage = LocalStorage()