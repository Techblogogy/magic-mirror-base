
class Dataset:
    """ Base class for all required application modules """

    # Database handler, main server instance
    def __init__(self, db, server, appdir, logger, config=None):
        self._db = db
        self._srv = server
        self._appdir = appdir
        self._log = logger

        self._cfg = config

        self.create_tables()
        self.init_tables()


    # Placeholder for initialization of tables
    def create_tables(self):
        pass

    # Placeholder for table initialization
    def init_tables(self):
        pass
