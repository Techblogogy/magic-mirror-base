from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit

from dbase.dwn import download
import thread

# from dbase.dbase import db
# import speech.speech

import time

# FLASK SERVER INITIATION FILE
# USED FOR SOCKET EVENTS

# Important Constants
IO_SPACE = "/io"

# Flask Elements
app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret";
# socketio = SocketIO(app,async_mode='threading')

dwn_thread = None;
t_running = False;

@app.route('/')
def index():

    if !t_running:
        t_running = True;
        thread.start_new_thread(download, ("Thread 1",))

    return "Welcome to Magic Mirror Server :)"

# @socketio.on("connect", namespace=IO_SPACE)
# def connected():
#     print "client %s connected" % (request.sid)
#     #emit("myresponse", db.qry("SELECT * FROM test"))

# Run Server Application
if __name__  == '__main__':
    socketio.run(app)
