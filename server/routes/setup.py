import decor

from flask import Blueprint, redirect, request, url_for
from api_cal.gcal import gcal

from api_cal.setup import setup

import os, json

import logging
logger = logging.getLogger("TB")

# import socket as sct
# import fcntl, struct

ALLOWED_ORIGIN = "*"
JSON_DENT = 4
setup_blp = Blueprint('setup_blp', __name__, url_prefix="/setup")

IF_NAME = "en0"
IF_PORT = "5000"

# Get IP Address
@setup_blp.route('/getip')
def get_ip():
    # soc = sct.socket(sct.AF_INET, sct.SOCK_DGRAM)
    # return sct.inet_ntoa(fcntl.ioctl(
    #     soc.fileno(),
    #     0x8915,
    #     struct.pack("256s", IF_NAME[:15])
    # )[20:24])
    return "192.168.1.103:5000"
    # return "%s:%s" % (sct.gethostbyname(sct.gethostname()), IF_PORT)

@setup_blp.route('/is_tut')
def is_tut():
    return json.dumps( setup.is_tut(), indent=JSON_DENT )

@setup_blp.route('/set_tut')
def set_tut():
    setup.save_tut()
    return ""


# Authenication routes
# Save calendars
@setup_blp.route('/pos/isconf')
def setup_istblex():
    return json.dumps({'is_confirmed': setup.if_setup_tbl()})

@setup_blp.route("/pos", methods=['POST','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def setup_save_u_pos():
    setup.save_pos(request.form.get('u_lng'), request.form.get('u_lat'))

    logger.debug(request.form)

    return '<meta http-equiv="refresh" content ="1000; URL=http://localhost:5000/setcal">'

@setup_blp.route('/pos/get', methods=['GET','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def get_pos():
    return json.dumps(setup.get_position(), indent=JSON_DENT)

@setup_blp.route('/widgets', methods=['GET','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def get_widgets():
    return json.dumps(setup.get_widgets(), indent=JSON_DENT)
