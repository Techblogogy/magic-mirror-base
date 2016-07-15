import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class dbase:
    _dbpath = 'mirror.db'
    _db = None
    _cn = None;

    # def __init__(self):
    #     self._dbpath = 'mirror.db' # Database file path
    #     self.setup()

    # Connect to database
    @classmethod
    def connect(self):
        self._cn = sqlite3.connect(self._dbpath) # Created Database "connection"
        self._cn.row_factory = dict_factory
        self._db = self._cn.cursor() # Databse Cursor

    # Querry Database
    @classmethod
    def qry(self, qry, params=()):
        self.connect()
        dat = self.exe(qry,params)
        self.close()

        return dat

    # Querry Database
    @classmethod
    def qry_many(self, qry, params=[]):
        self.connect()
        dat = self.exe_many(qry,params)
        self.close()

        return dat

    # Only execute querry
    @classmethod
    def exe(self, qry, params=()):
        self._db.execute(qry,params)
        return self._db.fetchall()


    # Only execute many querry
    @classmethod
    def exe_many(self, qry, params=[]):
        self._db.executemany(qry,params)
        return self._db.fetchall()

    # Commit changes and close
    @classmethod
    def close(self):
        self._cn.commit()
        self._cn.close()

    #TODO: Add Setup method to initate all of the tables
    def setup(self):
        self.connect()

        # Create a basic weather test table
        self.exe("""
            CREATE TABLE IF NOT EXISTS temp_video (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                v_path TEXT NOT NULL,
                time INTEGER NOT NULL
            )
            """)

        self.close()
