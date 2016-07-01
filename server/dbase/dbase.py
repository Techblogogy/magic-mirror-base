import sqlite3

class dbase:
    def __init__(self):
        self._dbpath = 'res/db/mirror.db' # Database file path
        self.setup()

    # Connect to database
    def connect(self):
        self._cn = sqlite3.connect(self._dbpath) # Created Database "connection"
        self._db = self._cn.cursor() # Databse Cursor

    # Querry Database
    def qry(self, qry, params=()):
        self.connect()
        dat = self.exe(qry,params)
        self.close()

        return dat

    # Only execute querry
    def exe(self, qry, params=()):
        self._db.execute(qry,params)
        return self._db.fetchall()

    # Commit changes and close
    def close(self):
        self._cn.commit()
        self._cn.close()

    #TODO: Add Setup method to initate all of the tables
    def setup(self):
        # self.connect()

        # Create a basic weather test table
        self.qry("""
            CREATE TABLE IF NOT EXISTS temp_video (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                v_path TEXT NOT NULL,
                time INTEGER NOT NULL
            )
            """)

        # self.close()

# Initiate database instance
db = dbase()
db.setup()
