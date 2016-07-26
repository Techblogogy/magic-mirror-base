from flask import Flask, request, send_from_directory, redirect, render_template
from flask_socketio import SocketIO, emit

from server import PServer
pserve = PServer()

import os, json, thread, time


import speech.speech
from remote_ctr.remote_ctr import m_remote

#from thead import send_left

#from cvison.play import PlayVid

import decor

from routes.setup import setup_blp
from api_cal.setup import setup

from routes.gcal import gcal_api
from api_cal.gcal import gcal

from routes.wardrobe import wrd_api

# Important Constants
JSON_DENT = 4

# Flask Elements
# pserve.app = Flask(__name__)
# pserve.app.config['SECRET_KEY'] = "supersecret"
# socketio = SocketIO(pserve.app,async_mode='threading')
#socketio = SocketIO(pserve.app)

# Reigster Blueprints
pserve.app.register_blueprint(gcal_api)
pserve.app.register_blueprint(setup_blp)
pserve.app.register_blueprint(wrd_api)


@pserve.app.route('/')
def main():
    return render_template('setupSite.html', auth = gcal.need_auth(), userName = gcal.get_disp_name())

@pserve.app.route('/<path:filename>')
def index(filename):
    return send_from_directory('static', filename)

#calendar Settings
@pserve.app.route('/setcal', methods=['GET','POST','OPTIONS'])
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

@pserve.socketio.on("connect", namespace=pserve.IO_SPACE)
def connected():
    print "client %s connected" % (request.sid)

@pserve.socketio.on("myevent", namespace=pserve.IO_SPACE)
def myevent():
    print "EHY!"

# Page 404
@pserve.app.errorhandler(404)
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
#         print threading.activeCount()
#
#     def run(self):
#         while True:
#             print "[THREAD-1] Sending"
#             socketio.emit("r_ctr", "right", namespace=IO_SPACE)
#
#             time.sleep(4)
#         # print "Starting " + self.name
#         # print_time(self.name, self.counter, 5)
#         # print "Exiting " + self.name

# thread = myThread(1, "Thread-1", 1)

# Run Server Application
if __name__  == '__main__':
    # print "two times"

    try:
        thread.start_new_thread( m_remote, (0,) )
    except:
        print "Error: unable to start thread"

    pserve.app.run(debug=True, threaded=True)
    # socketio.run(pserve.app, debug=True)
