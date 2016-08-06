from flask import Flask, request, send_from_directory, redirect, render_template
from flask_socketio import SocketIO, emit

from minfo import app_dir

import ntext.dresscode
ntext.dresscode.get_dresscode()

# import eventlet
# eventlet.monkey_patch()

from blogger import Blogger as bl

from server import PServer
pserve = PServer()

import os, json, thread, time, sys
from traceback import print_tb

mc = None
try:
    from cvison.cam import My_Cam
    mc = My_Cam()
except ImportError:
    bl.log_tb("MyCam failed. Are you on Raspberry PI?")

from speech.speech import Speech
from remote_ctr.remote_ctr import m_remote
from cvison.play import PlayVid

import decor

from api_cal.setup import setup
from api_cal.gcal import gcal


# Important Constants
# JSON_DENT = 4

def create_server():
    # Create server singleton instance
    from server import PServer
    pserve = PServer()

    # Reigster Blueprints
    from routes.setup import setup_blp
    pserve.app.register_blueprint(setup_blp)

    from routes.gcal import gcal_api
    pserve.app.register_blueprint(gcal_api)

    from routes.wardrobe import wrd_api
    pserve.app.register_blueprint(wrd_api)

    from routes.WDmanager import wd_manager_api
    pserve.app.register_blueprint(wd_manager_api)

    # Start voice recognition
    voice = Speech()
    voice.start()

    # Video playing
    pv = PlayVid()

    # Start Remote Control
    # try:
    #     thread.start_new_thread( m_remote, (0,) )
    # except:
    #     print "Error: unable to start thread"

    # Define application routes
    @pserve.app.route('/')
    def main():
        return render_template('setupSite.html', auth = gcal.need_auth(), userName = gcal.get_disp_name())

    # Static directory route
    @pserve.app.route('/<path:filename>')
    def index(filename):
        return send_from_directory('static', filename)


    # Clothes thumbnails static route
    @pserve.app.route('/clothes/<path:filename>')
    def clothes_imgs(filename):
        return send_from_directory(app_dir+"/cls", filename)
        pass

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



    # SocketIO Connection
    @pserve.socketio.on("connect", namespace=pserve.IO_SPACE)
    def connected():
        print "client %s connected" % (request.sid)

    # Page 404
    @pserve.app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Play video
    @pserve.socketio.on("start_video", namespace=pserve.IO_SPACE)
    def play_video(dat):
        print "[TB DUBUG] Playing video %s" % (dat)
        # pv.play_auto(dat)
        try:
            pv.x = 92
            pv.y = 80
            pv.w = 843
            pv.h = 1350
            thread.start_new_thread( pv.play_auto, (dat,) )
        except:
            print "Error: unable to start video thread"

    @pserve.socketio.on("closed", namespace=pserve.IO_SPACE)
    def stop_video():
        print "[TB DUBUG] Stoping video"
        pv.stop_auto()

    @pserve.socketio.on("user_on_add", namespace=pserve.IO_SPACE)
    def start_cam():
        try:
            mc.turn_on()
        except:
            bl.log_tb("MyCam failed. Are you on Raspberry PI?")

    @pserve.socketio.on("user_on_leave", namespace=pserve.IO_SPACE)
    def start_cam():
        # try:
        mc.turn_off()
        # except:
            # bl.log_tb("MyCam failed. Are you on Raspberry PI?")


    return (pserve.app, pserve.socketio)
