import sqlite3
# from common import config
# from cv import backend
LOCAL_DB = 'local.db'
class LocalStorage:
    
    def __init__(self):
        # self.connection = sqlite3.connect(config.LOCAL_DB)
        # self.cursor = self.connection.cursor()
        if not self.checkTableExist():
            self.initializeDatabase()

    
    def create_connection(self):
        return self.connection.cursor()


    def initializeDatabase(self):
        with sqlite3.connect(LOCAL_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                '''
                CREATE TABLE Positions (
                ID int NOT NULL,
                PositionName varchar(100),
                PRIMARY KEY (ID)
                ) 
                ''')

            cur.execute(
                '''
                CREATE TABLE Addresses (
                ID int NOT NULL,
                Province varchar(100),
                District varchar(100),
                PRIMARY KEY (ID)
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE Members (
                ID int NOT NULL,
                Name varchar(200),
                AddressId INT,
                PositionId INT,
                PRIMARY KEY (ID),
                FOREIGN KEY (PositionId) REFERENCES Positions(ID),
                FOREIGN KEY (AddressId) REFERENCES Addresses(ID)
                )
                ''')
            
            cur.execute(
                '''
                CREATE TABLE Users (
                ID int NOT NULL,
                CitizenId varchar(13),
                Name varchar(100),
                BirthDate varchar(10),
                PhoneNumber varchar(10),
                AddressId INT,
                PRIMARY KEY (ID),
                FOREIGN KEY (AddressId) REFERENCES Addresses(ID)
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE Parties (
                ID int NOT NULL,
                MemberId INT,
                PartyName varchar(100),
                FavoriteCount INT,
                UrlPicture varchar(100),
                PRIMARY KEY (ID),
                FOREIGN KEY (MemberId) REFERENCES Members(ID)
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE Logins (
                ID int NOT NULL,
                Role varchar(50),
                UserId INT,
                Password INT,
                PRIMARY KEY (ID),
                FOREIGN KEY (UserId) REFERENCES Users(ID),
                )
                ''')

            cur.execute(
                '''
                CREATE TABLE Favorites (
                ID int NOT NULL,
                UserId INT,
                PartyId INT,
                PRIMARY KEY (ID),
                FOREIGN KEY (UserId) REFERENCES Users(ID),
                FOREIGN KEY (PartyId) REFERENCES Parties(ID)
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
                    name='Images' 
                ''')  
            
            if cur.fetchone()[0] == 1:
                return True
            else:
                return False


    # def get_features(self, top=None):
    #     with sqlite3.connect(LOCAL_DB) as conn:
    #         cur = conn.cursor()

    #         if top is None:
    #             cur.execute(
    #                 '''
    #                 SELECT *
    #                 FROM Images
    #                 ''')
    #         else:
    #             cur.execute(
    #                 '''
    #                 SELECT *
    #                 FROM Images
    #                 LIMIT ?
    #                 ''', [top])

    #         return [(x[0], x[1], backend.pickle_to_feature(x[2])) for x in cur.fetchall()]

    # def get_feature_by_id(self, index):
    #     with sqlite3.connect(LOCAL_DB) as conn:
    #         cur = conn.cursor()
    #         cur.execute(
    #             '''
    #             SELECT *
    #             FROM Images
    #             WHERE id = ?
    #             ''', [index])

    #         data = cur.fetchone()

    #         return (data[0], data[1], backend.pickle_to_feature(data[2]))


    # def get_feature_by_location_id(self, location_id):
    #     with sqlite3.connect(LOCAL_DB) as conn:
    #         cur = conn.cursor()
    #         cur.execute(
    #             '''
    #             SELECT *
    #             FROM Images
    #             WHERE location_id = ?
    #             ''', [location_id])

    #         return [(x[0], x[1], backend.pickle_to_feature(x[2])) for x in cur.fetchall()]


    # def add_feature(self, product_id, location_id, kp, desc):
    #     with sqlite3.connect(LOCAL_DB) as conn:
    #         feature = backend.feature_to_pickle(kp, desc)
    #         cur = conn.cursor()

    #         cur.execute(
    #             '''
    #             INSERT INTO Images
    #             (id, location_id, body)
    #             VALUES
    #             (?, ?, ?)
    #             ''', [product_id, location_id, feature])

    #         conn.commit()


    # def update_feature(self, index, kp, desc):
    #     with sqlite3.connect(LOCAL_DB) as conn:
    #         feature = backend.feature_to_pickle(kp, desc)
    #         cur = conn.cursor()

    #         cur.execute(
    #             '''
    #             UPDATE Images
    #             SET body = ?
    #             WHERE id = ?
    #             ''', [feature, index])

    #         conn.commit()


    # def delete_features(self, ids):
    #     with sqlite3.connect(LOCAL_DB) as conn:
    #         cur = conn.cursor()
    #         idsQuery = tuple(ids)
    #         cur.execute(
    #             '''
    #             DELETE FROM Images
    #             WHERE id in ?
    #             ''', [idsQuery])

    #         conn.commit()


    # def get_undetected_features_by_location_id(self, location_id):
    #     with sqlite3.connect(LOCAL_DB) as conn:
    #         cur = conn.cursor()
    #         cur.execute(
    #             '''
    #             SELECT *
    #             FROM UnknownImages
    #             WHERE location_id = ?
    #             ''', [location_id])

    #         return [(x[0], x[1], backend.pickle_to_feature(x[2])) for x in cur.fetchall()]


storage = LocalStorage()