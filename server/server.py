from flask import Flask, request, send_from_directory
import os, json
# from flask_socketio import SocketIO, emit

from dbase.dbase import dbase

# Initiate database instance
db = dbase()
db.setup()

import calendar.calendar

# Important Constants
IO_SPACE = "/io"

# Flask Elements
app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret";
# socketio = SocketIO(app,async_mode='threading')

@app.route('/<path:filename>')
def index(filename):
    return send_from_directory(os.path.dirname(os.getcwd()), filename)

# Calendar API Routes
# main route
@app.route('/cal')
def cal_route():
    return "";

# events getter
@app.route('/cal/events/get')
def cal_get_event():
    return json.dumps(calendar.calendar.cal.get_events())

# events adder
@app.route('/cal/events/add', methods=['POST'])
def cal_add_event():
    return calendar.calendar.cal.add_event(
        request.form.get('task'),
        request.form.get('date'),
        request.form.get('time'))

# events updater
@app.route('/cal/events/update', methods=['POST'])
def cal_upt_event():
    return calendar.calendar.cal.upd_event(
        request.form.get('id'),
        request.form.get('task'),
        request.form.get('date'),
        request.form.get('time'))

# events remover
@app.route('/cal/events/delete', methods=['POST'])
def cal_rmv_event():
    return calendar.calendar.cal.rmv_event(request.form.get('id'))


# @socketio.on("connect", namespace=IO_SPACE)
# def connected():
#     print "client %s connected" % (request.sid)
#     #emit("myresponse", db.qry("SELECT * FROM test"))

# Run Server Application
if __name__  == '__main__':
    # Flask.run(app)
    app.run()
