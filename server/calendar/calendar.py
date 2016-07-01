from server import db

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

    # Returns all events
    @staticmethod
    def get_events():
        return db.qry("""
            SELECT * FROM tbl_cal WHERE c_date AND deleted=0
        """)

    # Adds an event
    @staticmethod
    def add_event(task, date, time=None):
        db.qry("""
            INSERT INTO tbl_cal (task, c_date, c_time)
            VALUES (?,?,?)
        """, (task,date,time,))

    # Updates an event
    @staticmethod
    def upd_event(id, task=None, date=None, time=None):
        db.qry("""
            UPDATE tbl_cal
            SET task=?, c_date=?, c_time=?
            WHERE id=?
        """)

    # Removes an event
    @staticmethod
    def rmv_event(id):
        db.qry("""
            UPDATE tbl_cal
            SET deleted=1
            WHERE id=?
        """, (id,))

cal.init_tables()
cal.add_event("lala", "2016-07-01")
cal.rmv_event(2)
print cal.get_events()
