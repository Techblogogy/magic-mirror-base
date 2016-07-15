import sys

from flask import abort, redirect
import httplib2

import datetime
from dbase.dbase import dbase as db
class setup:
    @staticmethod
    def init_setup_tbl():
        db.qry("""
            CREATE TABLE IF NOT EXISTS tbl_setup (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                lng REAL NOT NULL,
                lat REAL NOT NULL
            )
        """)


    # What do I think abut it? Nice start :) Now lets have a look at how you can store data in the tables
    # There's a thing called SQL. What does that mean
