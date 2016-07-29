from flask import Flask, request
from flask_socketio import SocketIO, emit

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
        self.socketio = SocketIO(self.app, async_mode='threading')

    def send(self, event, data):
        self.socketio.emit(event, data, namespace="/io")

    def start(self):
        print "[STARTING SERVERS]"
