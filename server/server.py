from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread

from dbase.dbase import db

import time
import speech_recognition as sr

IO_SPACE = "/io"

# Flask Elements
app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret";
socketio = SocketIO(app,async_mode='threading')

# Some junk
# client_id = ""
thread = None

# Voice Recognizer Elements

# r = sr.Recognizer()
# m = sr.Microphone()

# Message ticking thread
def tick_message():
    while True:
        time.sleep(10)
        socketio.emit('myresponse', "GHost", namespace=IO_SPACE)

# Voice recognition callback
def callback(recon, audio):
    try:
        text = recon.recognize_google(audio);
        print("Google Speech: "+text)

        socketio.emit("myresponse", text, namespace=IO_SPACE)
    except sr.UnknownValueError:
        print("Google Speech unrecognizable")
    except sr.RequestError as e:
        print("Service unavalible")


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

    # with m as source:
    #     r.adjust_for_ambient_noise(source)
    # stop_listening = r.listen_in_background(m,callback)

if __name__  == '__main__':
    socketio.run(app, debug=True)
