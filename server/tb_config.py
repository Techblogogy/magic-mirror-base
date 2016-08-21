import ConfigParser


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class conf_file():
    __metaclass__ = Singleton

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.cfg')

    def get_cfg(self):
        return self.config
