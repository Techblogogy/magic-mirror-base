import sys

from flask import abort, redirect, request
import httplib2

import datetime
from dbase.dbase import dbase as db

import logging
logger = logging.getLogger("TB")

class setup:

    # Creates setup table
    @staticmethod
    def init_setup_tbl():
        db.qry("""
            CREATE TABLE IF NOT EXISTS tbl_setup (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                lng REAL NOT NULL,
                lat REAL NOT NULL
            )
        """)
    @staticmethod
    def if_setup_tbl():
         return db.qry("SELECT name FROM sqlite_master WHERE type='table' AND name='tbl_setup'")

    @staticmethod
    def create_tut():
        # Create Table if not exists
        db.qry("""
            CREATE TABLE IF NOT EXISTS tbl_tutorial (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                tut_comp INTEGER NOT NULL
            )
        """)

    @staticmethod
    def save_tut():
        setup.create_tut()

        # Save table setup state
        db.qry("""
            INSERT INTO tbl_tutorial(tut_comp)
            SELECT 1
            WHERE NOT EXISTS(SELECT id FROM tbl_tutorial WHERE id=1)
        """)

    @staticmethod
    def is_tut():
        setup.create_tut()

        dt = db.qry("SELECT tut_comp FROM tbl_tutorial WHERE id=1")

        if len(dt) == 0:
            return {"bool": False}

        if dt[0]['tut_comp'] == 0:
            return {"bool": False}
        else:
            return {"bool": True}

        return ""


    # Saves position
    @staticmethod
    def save_pos(u_lng, u_lat):
        setup.init_setup_tbl()

        db.qry("DELETE FROM tbl_setup")

        db.qry("""
            INSERT INTO tbl_setup(lng, lat)
            VALUES (?,?)
        """,(u_lng, u_lat))

        print db.qry("SELECT * FROM tbl_setup")

    # Retuns lat and lng coordinates
    @staticmethod
    def get_position():
        return db.qry("SELECT * FROM tbl_setup")[0]

    # NOTE: WTF is this????
    @staticmethod
    def response():
        if request.method == 'POST':
            return True

#------------------------------------WIDGETS MANAGER--------------------------------------------
    @staticmethod
    def init_widgets_table():
        db.qry("""
            CREATE TABLE IF NOT EXISTS widgets_tbl (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                active INT NOT NULL DEFAULT 1
            )
        """)
        db.qry("""
        INSERT OR REPLACE INTO widgets_tbl(id, name, active)
        VALUES ((SELECT id FROM widgets_tbl WHERE name = ?),?,?)
        VALUES ((SELECT id FROM widgets_tbl WHERE name = ?),?,?)
        VALUES ((SELECT id FROM widgets_tbl WHERE name = ?),?,?)
        """,("weather", "weather",1, "clock", "clock",1,"calendar", "calendar",1))
        return 201

    @staticmethod
    def add_widgets(name,if_active):
        db.qry("""
            UPDATE widgets_tbl
            SET active=?
            WHERE name=?
        """, (if_active,name))
        return 200

    @staticmethod
    def get_widgets():
        setup.init_widgets_table()
        widgets = db.qry("""
            SELECT * FROM widgets_tbl
        """)
        logger.debug(widgets)
        return widgets
