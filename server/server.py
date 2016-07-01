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
JSON_DENT = 4

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
@app.route('/cal/events/get', methods=['GET'])
def cal_get_event():
    return json.dumps(calendar.calendar.cal.get_events(), indent=JSON_DENT)

# events getter in range
@app.route('/cal/events/get/range', methods=['GET'])
def cal_get_rage_event():
    return json.dumps(calendar.calendar.cal.get_range_events(
        request.args.get('min'),
        request.args.get('max')
    ), indent=JSON_DENT)

# today event getter
@app.route('/cal/events/get/today', methods=['GET'])
def cal_get_today_event():
    return json.dumps(calendar.calendar.cal.get_today_events(), indent=JSON_DENT)

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
        request.form.get('id', type=int),
        request.form.get('task'),
        request.form.get('date'),
        request.form.get('time'))

# events remover
@app.route('/cal/events/delete', methods=['POST'])
def cal_rmv_event():
    return calendar.calendar.cal.rmv_event(request.form.get('id', type=int))

# Error Handling
@app.errorhandler(400)
def err_400(e):
    return '{"status": 400, "message":"Bad request"}', 400

@app.errorhandler(404)
def err_404(e):
    return '{"status": 404, "message":"Page not found"}', 404

@app.errorhandler(500)
def err_500(e):
    return '{"status": 500, "message":"Internal server error"}', 500

# @socketio.on("connect", namespace=IO_SPACE)
# def connected():
#     print "client %s connected" % (request.sid)
#     #emit("myresponse", db.qry("SELECT * FROM test"))

# Run Server Application
if __name__  == '__main__':
    # Flask.run(app)
    app.run()
