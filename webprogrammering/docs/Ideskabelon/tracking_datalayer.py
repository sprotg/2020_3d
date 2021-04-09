from flask import g
import sqlite3
import datetime

class TrackingVar():
    def __init__(self, name, type, userid):
        self.name = name
        self.type = type
        self.userid = userid

class TrackingData():

    def __init__(self):
        self.DATABASE = 'tracking.db'

        self._create_db_tables()
        c = self._get_db().cursor()

    def _get_db(self):
        db = g.get('_database', None)
        if db is None:
            db = g._databdase = sqlite3.connect(self.DATABASE)
        return db

    def close_connection(self):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def get_var_list(self, userid):
        db = self._get_db()
        c = db.cursor()
        c.execute("SELECT id, name, type, created FROM TrackingVars WHERE userid = ?", [userid])
        var_list = []
        for i in c:
            var_list.append({'id':i[0], 'name':i[1], 'type':i[2], 'created': i[3]})
        return var_list

    def add_new_var(self, userid, name, type):
        db = self._get_db()
        c = db.cursor()
        c.execute("INSERT INTO TrackingVars (name, type, userid) VALUES (?, ?, ?)", [name, type, userid])
        db.commit()
        print("Added new trackingvar for {}: {},{}".format(userid, name, type))

    def get_tracking_data(self, varid):
        db = self._get_db()
        c = db.cursor()
        c.execute("SELECT value, trackingtime FROM TrackingData WHERE varid = ?", userid)
        var_list = []
        for i in c:
            var_list.append({'id':i[0], 'name':i[1], 'type':i[2], 'created': i[3]})
        return var_list

    def register_new_value(self, varid, date, value):
        db = self._get_db()
        c = db.cursor()
        c.execute("""INSERT INTO TrackingData (varid, value, trackingtime) VALUES (?, ?, ?);""",(varid, value, date))
        db.commit()

    def get_trackingvars_list(self, userid):
        db = self._get_db()
        c = db.cursor()
        c.execute('''SELECT name, type FROM TrackingVars WHERE userid = ?''', [userid])
        vars = []
        for v in c:
            t = TrackingVar(v[0], v[1], userid)
            vars.append(t)
        return vars


    def get_user_id(self, s):
        c = self._get_db().cursor()
        c.execute("SELECT id FROM UserProfiles WHERE username = ?", (s,))
        r = c.fetchone()
        #If the user doesn't exist, the result will be None
        if r is not None:
            return r[0]
        else:
            return None

    def register_user(self, user, pw, email):
        db = self._get_db()
        c = db.cursor()
        c.execute("SELECT * from UserProfiles WHERE username = ? OR email = ?", (user,email))
        r = c.fetchone()
        res = False
        if r is not None:
            #The username og email is already in use
            res = False
        else:
            c.execute("INSERT INTO UserProfiles (username, password, email) VALUES (?,?,?)", (user,pw,email))
            db.commit()
            res = True
        return res

    def get_user_list(self):
        l = []
        c = self._get_db().cursor()
        c.execute('SELECT * FROM UserProfiles;')
        for u in c:
            l.append("Navn: {}, email: {}, pw: {}".format(u[1],u[2],u[3]))
        return l

    def login_success(self, user, pw):
        c = self._get_db().cursor()
        c.execute("SELECT password FROM UserProfiles WHERE username = ?", (user,))
        r = c.fetchone()
        if r is not None:
            db_pw = r[0]
        else:
            return False
        return db_pw == pw



    def _create_db_tables(self):
        db = self._get_db()
        #try:
        #    db.execute("DROP TABLE IF EXISTS Ideas;")
        #    db.commit()
        #except:
        #    print('Fejl ved sletning af tabeller.')
        c = db.cursor()
        try:
            c.execute("""CREATE TABLE UserProfiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT,
                password TEXT);""")
        except Exception as e:
            print(e)

        try:
            c.execute("""CREATE TABLE TrackingVars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userid INTEGER,
                name TEXT,
                type INTEGER,
                created DATETIME DEFAULT CURRENT_TIMESTAMP);""")
        except Exception as e:
            print(e)

        try:
            c.execute("""CREATE TABLE TrackingData (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                varid INTEGER,
                value INTEGER,
                trackingtime DATETIME DEFAULT CURRENT_TIMESTAMP);""")
        except Exception as e:
            print(e)

        db.commit()
        return 'Database tables created'
