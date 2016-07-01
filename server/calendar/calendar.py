from dbase.dbase import db

class Cal:
    def __init__(self):
        pass

    # Creates required tables
    def init_tables(self):
        pass

    # Returns all events
    def get_event(self):
        pass

    # Adds an event
    def add_event(self, text, time=0):
        pass

    # Updates an event
    def upd_event(self, id, text=None, time=None):
        pass

    # Removes an event
    def rmv_event(self, id):
        pass
