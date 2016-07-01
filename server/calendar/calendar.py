from server import db
from flask import abort

class cal:
    # Creates required tables
    @staticmethod
    def init_tables():
        db.qry("""
            CREATE TABLE IF NOT EXISTS tbl_cal (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                c_date TEXT NOT NULL,
                c_time TEXT,
                deleted INTEGER NOT NULL DEFAULT 0
            ) """)

    # Returns all events from today onwards
    @staticmethod
    def get_events():
        return db.qry("""
            SELECT * FROM tbl_cal WHERE c_date >= date('now') AND deleted=0
        """)

    # Returns events in range
    @staticmethod
    def get_range_events(min, max):
        if min == None or max == None:
            abort(400)
            return

        return db.qry("""
            SELECT * FROM tbl_cal WHERE c_date >= ? AND c_dat <= ? AND deleted=0
        """, (min,max,))

    # Returns todays events
    @staticmethod
    def get_today_events():
        return db.qry("""
            SELECT * FROM tbl_cal WHERE c_date=date('now') AND deleted=0
        """)

    # Adds an event
    @staticmethod
    def add_event(task, date, time=None):
        if task == None or date == None:
            abort(400)
            return

        db.qry("""
            INSERT INTO tbl_cal (task, c_date, c_time)
            VALUES (?,?,?)
        """, (task,date,time,))

        return '{"status": 200, "message":"Event Added"}'

    # Updates an event
    @staticmethod
    def upd_event(id, task, date, time=None):
        if id == None or task == None or date == None:
            abort(400)
            return

        db.qry("""
            UPDATE tbl_cal
            SET task=?, c_date=?, c_time=?
            WHERE id=?
        """)

        return '{"status": 200, "message":"Event Updated"}'

    # Removes an event
    @staticmethod
    def rmv_event(id):
        if id == None:
            abort(400)
            return

        db.qry("""
            UPDATE tbl_cal
            SET deleted=1
            WHERE id=?
        """, (id,))

        return '{"status": 200, "message":"Event Removed"}'

cal.init_tables()
# cal.add_event("lala", "2016-07-01")
# cal.rmv_event(2)
print cal.get_events()
