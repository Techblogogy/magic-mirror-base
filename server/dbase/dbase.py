import sqlite3

class dbase:
    def __init__(self):
        self._dbpath = 'res/db/mirror.db' # Database file path

        self.connect()
        # self._cn = sqlite3.connect(self._dbpath) # Created Database "connection"
        # self._db = self._cn.cursor() # Databse Cursor

    # Connect to database
    def connect(self):
        self._cn = sqlite3.connect(self._dbpath) # Created Database "connection"
        self._db = self._cn.cursor() # Databse Cursor

    # Querry Database
    def qry(self, qry):
        self.connect()
        self._db.execute(qry)
        self.close()

    # Only execute querry
    def exe(self, qry):
        self._db.execute(qry)

    # Commit changes and close
    def close(self):
        self._cn.commit()
        self._cn.close()

db = dbase()
