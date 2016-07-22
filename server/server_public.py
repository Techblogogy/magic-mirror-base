from flask import Flask, request, send_from_directory, redirect, render_template
from flask_socketio import SocketIO, emit
import os, json

import thread, time

import decor

from routes.setup import setup_blp
from api_cal.setup import setup

from routes.gcal import gcal_api
from api_cal.gcal import gcal
#from dbase.dbase import dbase

from routes.wardrobe import wrd_api

# Initiate database instance
#db = dbase()
#db.setup()

# import api_cal.calendar

t_running = False

# Important Constants
JSON_DENT = 4

t_count = 0

# Important Constants
IO_SPACE = "/io"

# Flask Elements
app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret"
# socketio = SocketIO(app,async_mode='threading')
socketio = SocketIO(app)

# Reigster Blueprints
app.register_blueprint(gcal_api)
app.register_blueprint(setup_blp)
app.register_blueprint(wrd_api)

@app.route('/')
def main():
    return render_template('setupSite.html', auth = gcal.need_auth(), userName = gcal.get_disp_name())

@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('static', filename)

#calendar Settings
@app.route('/setcal', methods=['GET','POST','OPTIONS'])
def setcal():
    resp = 0
    if (request.form.get('action') == "calendar"):
        gcal.add_cals(request.form.getlist('ids[]'))
        resp = 200

    elif(request.form.get('action') == "position"):
        setup.save_pos(request.form.get('u_lng'), request.form.get('u_lat'))
        resp = 201



    return render_template('setcal.html',
        resp_g = resp,
        # resp_p = setup.response()
        auth = gcal.need_auth(),
        userName = gcal.get_disp_name(),
        cals = gcal.get_cals(),
        c_len = len(gcal.get_cals()),
        # pos = setup_get_pos()x
    )

def send_left(t):
    # global t_count
    # t_count += 1
    while True:
        print "test"
        socketio.emit("r_ctr", "right", namespace=IO_SPACE)
        time.sleep(4)


@socketio.on("connect", namespace=IO_SPACE)
def connected():
    print "client %s connected" % (request.sid)


    # emit("myresponse", db.qry("SELECT * FROM test"))
    # socketio.emit("r_ctr", "left")

@socketio.on("myevent", namespace=IO_SPACE)
def myevent():
    print "EHY!"

# Page 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
#
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#
#         # print self.active_count()
#
#     def active_count(self):
#         # super(myThread, self).active_count()
#
#     def run(self):
#         print "running"
#         # print "Starting " + self.name
#         # print_time(self.name, self.counter, 5)
#         # print "Exiting " + self.name

# thread = myThread(1, "Thread-1", 1)

# Run Server Application
if __name__  == '__main__':
    print "two times"

    try:
        # print thread.active_count()
        # thread.start()
        # print thread.active_count()
        # print t_count
        thread.start_new_thread( send_left, (1,) )
    except:
        print "Error: unable to start thread"

    app.run(debug=True, threaded=True)
