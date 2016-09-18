from dbase.dataset import Dataset

import sys
from flask import abort, redirect, request

import datetime
# from dbase.dbase import dbase as db
#
# import logging
# logger = logging.getLogger("TB")

class Setup(Dataset):

    # Creates setup table
    def create_tables(self):
        self._db.qry("""
            CREATE TABLE IF NOT EXISTS tbl_setup (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                lng REAL NOT NULL,
                lat REAL NOT NULL
            )
        """)

        self._db.qry("""
            CREATE TABLE IF NOT EXISTS tbl_tutorial (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                tut_comp INTEGER NOT NULL
            )
        """)

        self._db.qry("""
            CREATE TABLE IF NOT EXISTS widgets_tbl (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                active INT NOT NULL DEFAULT 1
            )
        """)


    def init_tables(self):

        self._db.qry("""
            INSERT INTO tbl_setup(lng, lat)
            VALUES (0, 0)
        """)

        self._db.qry_many("""
            INSERT INTO widgets_tbl(name)
            SELECT ?
            WHERE NOT EXISTS(SELECT name FROM widgets_tbl WHERE name=?)
        """, [
            ("weather", "weather"),
            ("clock", "clock"),
            ("calendar", "calendar")
        ])


    # Save table setup state
    def save_tut(self):
        self._db.qry("""
            INSERT INTO tbl_tutorial(tut_comp)
            SELECT 1
            WHERE NOT EXISTS(SELECT id FROM tbl_tutorial WHERE id=1)
        """)


    # Check if tutorial is completed
    def is_tut(self):
        dt = self._db.qry("SELECT tut_comp FROM tbl_tutorial WHERE id=1")

        if len(dt) == 0:
            return {"bool": False}

        if dt[0]['tut_comp'] == 0:
            return {"bool": False}
        else:
            return {"bool": True}

        return ""


    # Saves position
    def save_pos(self, u_lng, u_lat):
        # self._db.qry("DELETE FROM tbl_setup")

        self._db.qry("""
            UPDATE tbl_setup(lng, lat)
            SET lng=?, lat=?
            WHERE id=1
        """,(u_lng, u_lat))

        self._log.debug(self._db.qry("SELECT * FROM tbl_setup"))


    # Retuns lat and lng coordinates
    def get_position(self):
        return self._db.qry("SELECT * FROM tbl_setup")[0]


    def update_widgets(self, widgets):
        self._db.qry("UPDATE widgets_tbl SET active=0")
        self._db.qry_many("UPDATE widgets_tbl SET active=1 WHERE id=?", widgets)


    def get_widgets(self):
        widgets = self._db.qry("""
            SELECT * FROM widgets_tbl
        """)

        return widgets
