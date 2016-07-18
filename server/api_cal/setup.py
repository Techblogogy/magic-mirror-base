import sys

from flask import abort, redirect, request
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

    #save position
    @staticmethod
    def save_pos(u_lng, u_lat):
        setup.init_setup_tbl()

        db.qry("DELETE FROM tbl_setup")

        db.qry("""
            INSERT INTO tbl_setup(lng, lat)
            VALUES (?,?)
        """,(u_lng, u_lat))

        print db.qry("SELECT * FROM tbl_setup")
    @staticmethod
    def get_position():
        return db.qry("SELECT * FROM tbl_setup")[0]
    @staticmethod
    def response():
        if request.method == 'POST':
            return True


    # What do I think abut it? Nice start :) Now lets have a look at how you can store data in the tables
    # There's a thing called SQL. What does that mean
