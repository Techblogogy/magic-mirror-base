from flask import Flask, request
from flask_socketio import SocketIO, emit
from tb_config import conf_file as g_cfg
import logging, time
cfg = g_cfg().get_cfg()
SLEEP_TIME = cfg.getint("GLOBALS", "sleep_time")


# Important Constants
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PServer():
    __metaclass__ = Singleton

    def __init__(self):
        # Flask Elements
        self.IO_SPACE = "/io"

        self.test = "[TEST1]"

        self.app = Flask(__name__)
        self.app.config['DEBUG'] = False
        self.app.config['SECRET_KEY'] = "supersecret";
        # self.socketio = SocketIO(self.app)
        self.socketio = SocketIO(self.app, async_mode='threading')

    # LIttle spleeper
    @staticmethod
    def sleep_state(voice):
        global pserve
        time.sleep(SLEEP_TIME)
        pserve.send("sleep","123")
        logger.debug("WORKS")
        voice.stop_all()
        pserve.is_sleeping = True


    def send(self, event, data):
        self.socketio.emit(event, data, namespace="/io")

    def start(self):
        print "[STARTING SERVERS]"

pserve = PServer()
