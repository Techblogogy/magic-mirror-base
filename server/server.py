from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from threading import Thread

import time
import speech_recognition as sr

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!";
socketio = SocketIO(app,async_mode='threading')

client_id = ""
thread = None

def tick_message():
    while True:
        time.sleep(10)
        socketio.emit('myresponse', {'data': 'test'}, namespace='/io')

@app.route('/')
def index():
    return "Hello World"

@socketio.on("connect", namespace='/io')
def connected():
    global thread

    print "client connected"
    client_id = request.sid
    print(client_id)

    if thread is None:
        thread = Thread(target=tick_message)
        thread.deamon = True
        thread.start()


# @socketio.on('myevent')
# def test_message(message):
    # print(message)

# r = sr.Recognizer()
# m = sr.Microphone()
#
# def callback(recon, audio):
#     try:
#         text = recon.recognize_google(audio);
#         print("Google Speech: "+text)
#         socketio.emit("myresponse", 'swing', namespace='/', room=client_id)
#     except sr.UnknownValueError:
#         print("Google Speech unrecognizable")
#     except sr.RequestError as e:
#         print("Service unavalible")

if __name__  == '__main__':
    # with m as source:
    #     r.adjust_for_ambient_noise(source)
    # stop_listening = r.listen_in_background(m,callback)

    socketio.run(app, debug=True)
