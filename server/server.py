from flask import Flask, request, send_from_directory
import os
# from flask_socketio import SocketIO, emit

from dbase.dbase import db
import calendar.calendar

# FLASK SERVER INITIATION FILE
# USED FOR SOCKET EVENTS

# Important Constants
IO_SPACE = "/io"

# Flask Elements
app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret";
# socketio = SocketIO(app,async_mode='threading')

@app.route('/<path:filename>')
def index(filename):
    return send_from_directory(os.path.dirname(os.getcwd()), filename)

@app.route('/cal')
def cal_route():
    return "hey!";

# @socketio.on("connect", namespace=IO_SPACE)
# def connected():
#     print "client %s connected" % (request.sid)
#     #emit("myresponse", db.qry("SELECT * FROM test"))

# Run Server Application
if __name__  == '__main__':
    # Flask.run(app)
    app.run()
