
class Dataset:
    """ Base class for all required application modules """

    # Database handler, main server instance
    def __init__(db, server, appdir, logger):
        self._db = db
        self._srv = server
        self._appdir = appdir
        self._log = logger

        self.create_tables()


    # Placeholder for initialization of tables
    def create_tables(self):
        pass

    # Placeholder for table initialization
    def init_tables(self):
        pass
