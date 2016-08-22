import sqlite3
import threading, thread, uuid

from minfo import app_dir

from time import sleep

import logging
logger = logging.getLogger("TB")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

in_queue = False

class dbase:
    _dbpath = '/mirror.db'
    _db = None
    _cn = None;

    # Gets sign of values
    @staticmethod
    def _sign(val):
        if val:
            if val > 0: return 1
            else: return -1
        else:
            return val

    # Gets group of temperature
    @staticmethod
    def _temp_group(val):
        return int( ((abs(val/5)*10)+1)*dbase._sign(val) )

    # def __init__(self):
    #     self._dbpath = 'mirror.db' # Database file path
    #     self.setup()

    # Connect to database
    @classmethod
    def connect(self):
        self._cn = sqlite3.connect(app_dir+self._dbpath) # Created Database "connection"

        # Add custom functions
        self._cn.create_function("sign", 1, self._sign)
        self._cn.create_function("temp_group", 1, self._temp_group)

        self._cn.row_factory = dict_factory
        self._db = self._cn.cursor() # Databse Cursor

    # Querry Database
    @classmethod
    def qry(self, qry, params=()):
        global in_queue

        # Wait for another thread
        if in_queue:
            while in_queue:
                sleep(0.01)

        in_queue = True
        self.connect()

        dat = self.exe(qry,params)

        self.close()
        in_queue = False

        return dat

    # Querry Database
    @classmethod
    def qry_many(self, qry, params=[]):
        global in_queue

        # Wait for another thread
        if in_queue:
            while in_queue:
                sleep(0.01)

        in_queue = True
        self.connect()

        dat = self.exe_many(qry,params)

        self.close()
        in_queue = False

        return dat

    # Only execute querry
    @classmethod
    def exe(self, qry, params=()):
        # print "\n <==="
        # print "[DEBUG INFO] Querry: %s; Thread:" % (qry)
        # print threading.current_thread().ident
        # print "\n ===>"

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

    # Last added id
    @classmethod
    def last_id(self):
        # return self.qry("select last_insert_rowid() as lid")[0]['lid'];
        return self._db.lastrowid

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
