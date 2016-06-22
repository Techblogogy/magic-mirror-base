from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret!";
socketio = SocketIO(app)

@app.route('/')
def index():
    return "Hello World"

@socketio.on('myevent')
def test_message():
    print("Trigged")
    emit('myresponse', {'data': 'got it!'})

if __name__  == '__main__':
    socketio.run(app)
