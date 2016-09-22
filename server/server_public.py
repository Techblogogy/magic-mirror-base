from flask import Flask, request, send_from_directory, redirect, render_template
from flask_socketio import SocketIO, emit

from minfo import app_dir

import platform, logging

# Setup logging
logging.basicConfig(format="[%(name)s %(levelname)s %(module)s]: %(message)s")

logger = logging.getLogger("TB")
logger.setLevel(logging.DEBUG)

from server import PServer
pserve = PServer()

import os, json, thread, time, sys, sched
from traceback import print_tb

from tb_config import conf_file as g_cfg

from dbase.dbase import dbase as db

from speech.speech import Speech
from remote_ctr.remote_ctr import m_remote
from cvison.play import PlayVid

import decor

import subprocess

from api_cal.setup import Setup as ST
from api_cal.gcal import Gcal as GC
from cvison.store import Clothes as CL


SLEEP_TIME = 0

# Important Constants
JSON_DENT = 4

def create_server():
    cfg = g_cfg().get_cfg()

    machine_plt = platform.machine()[:3]
    ml_pt = (machine_plt == "arm")

    import socket as sct
    # socket.gethostbyname(socket.gethostname())
    logger.debug( "%s:%s" % (sct.gethostbyname(sct.gethostname()), 5000) )

    # Create server singleton instance
    from server import PServer
    pserve = PServer()

    # ---> Reigster Blueprints
    from routes.setup import construct_bp as crt_setup
    setup = ST(db, pserve, app_dir, logger)
    pserve.app.register_blueprint(crt_setup(setup))

    from routes.gcal import construct_bp as crt_gcal
    gcal = GC(db, pserve, app_dir, logger)
    pserve.app.register_blueprint(crt_gcal(gcal, 4))

    from routes.wardrobe import construct_bp as crt_wrd
    clothes = CL(db, pserve, app_dir, logger, config=cfg)
    pserve.app.register_blueprint(crt_wrd(clothes, logger))

    from routes.WDmanager import construct_bp as ctr_mng_wrd
    pserve.app.register_blueprint(ctr_mng_wrd(clothes, logger))


    # Start voice recognition
    voice = Speech(pserve, cfg, logger)
    voice.start()

    # Video playing
    pv = PlayVid(clothes, app_dir, logger, cfg)

    # Import and create PY Camera
    mc = None
    try:
        from cvison.cam import My_Cam
        mc = My_Cam(pserve, clothes, pv, app_dir, cfg, logger)
    except ImportError:
        logger.exception("MyCam failed. Are you on Raspberry PI?")
        logger.info("\n")

    # Start Remote Control
    try:
        thread.start_new_thread( m_remote, (cfg,pserve,logger,) )
        pass
    except:
        logger.exception("Error: unable to start remote control thread")


    # Upload snowboy files
    @pserve.app.route("/sbupload", methods=['POST'])
    def upload_snowboy():
        resp = {"status": 200}
        if 'file' not in request.files:
            resp["status"] = 500
            return '[ERROR]'

        print resp

        file = request.files['file']
        filename = "snowboy.umdl"
        filepath = os.path.join(app_dir+'/voice', filename)

        file.save(filepath)

        return json.dumps(resp, indent=4)

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

        elif(request.form.get('action') == "widgets"):
            setup.update_widgets(request.form.getlist('widgets[]'))
            resp = 201

        return render_template('setcal.html',
            resp_g = resp,

            auth = gcal.need_auth(),

            userName = gcal.get_disp_name(),
            cals = gcal.get_cals(),

            widgets = setup.get_widgets(),
        )

    # SocketIO Connection
    @pserve.socketio.on("connect", namespace=pserve.IO_SPACE)
    def connected():
        logger.info("client %s connected", (request.sid))

    # Page 404
    @pserve.app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Play video on wardrobe page
    @pserve.socketio.on("start_video", namespace=pserve.IO_SPACE)
    def play_video(dat):
        logger.info("Playing video %s", (dat))

        try:
            pv.wrd_size()
            thread.start_new_thread( pv.play_auto, (dat,) )
        except:
            logger.exception("Unable to start video thread")

    # Stop video on wardrobe page
    @pserve.socketio.on("closed", namespace=pserve.IO_SPACE)
    def stop_video():
        logger.info("Stoping video")
        pv.stop_auto()

    @pserve.socketio.on("record_start", namespace=pserve.IO_SPACE)
    def start_recording():
        try:
            mc.rec_start()
        except:
            logger.exception("MyCam failed. Are you on Raspberry PI?")

    @pserve.socketio.on("record_stop", namespace=pserve.IO_SPACE)
    def stop_recording():
        try:
            mc.rec_stop()
        except:
            logger.exception("MyCam failed. Are you on Raspberry PI?")

    # Turn on camera
    @pserve.socketio.on("user_on_add", namespace=pserve.IO_SPACE)
    def start_cam():
        try:
            mc.turn_on()
        except:
            logger.exception("MyCam failed. Are you on Raspberry PI?")

    # Turn off camera
    @pserve.socketio.on("user_on_leave", namespace=pserve.IO_SPACE)
    def start_cam():
        try:
            mc.turn_off()
        except:
            logger.exception("MyCam failed. Are you on Raspberry PI?")

    # === Start Electron UI ===
    if ml_pt:
        os.system("electron /home/pi/master_3/magic-mirror-base/ &")
    else:
        subprocess.Popen('electron ../ ', shell=True, stdout=subprocess.PIPE)
        pass

    logger.info("Starting electron")

    # === Sleeping state logic ===
    try:
        # thread.start_new_thread( pserve.sleep_state, (voice,) )
        # pserve.sleep_state(voice)
        pass
    except:
        logger.exception("Unable to sleeping thread")

    return (pserve.app, pserve.socketio)
