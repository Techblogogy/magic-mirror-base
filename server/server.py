from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread

from dbase.dbase import db
import voice.voice

import time

IO_SPACE = "/io"

# Flask Elements
app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret";
socketio = SocketIO(app,async_mode='threading')

# Some junk
# client_id = ""
thread = None

# Message ticking thread
def tick_message():
    while True:
        time.sleep(10)
        socketio.emit('myresponse', "GHost", namespace=IO_SPACE)

@app.route('/')
def index():
    return "Welcome to Magic Mirror Server :)"

@socketio.on("connect", namespace='/io')
def connected():
    global thread,db

    print "client %s connected" % (request.sid)
    emit("myresponse", db.qry("SELECT * FROM test"))

    # if thread is None:
    #     thread = Thread(target=tick_message)
    #     thread.deamon = True
    #     thread.start()

if __name__  == '__main__':
    socketio.run(app, debug=True)
