import decor

from flask import Blueprint, redirect, request, url_for
from api_cal.gcal import gcal

from api_cal.setup import setup

import os, json

import socket as sct

ALLOWED_ORIGIN = "*"
JSON_DENT = 4
setup_blp = Blueprint('setup_blp', __name__, url_prefix="/setup")

# Get IP Address
@setup_blp.route('/getip')
def get_ip():
    return sct.gethostbyname(sct.gethostname())

# Authenication routes
# Save calendars
@setup_blp.route('/pos/isconf')
def setup_istblex():
    return json.dumps({'is_confirmed': setup.if_setup_tbl()})

@setup_blp.route("/pos", methods=['POST','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def setup_save_u_pos():
    # print request.form.getlist('ids[]')
    setup.save_pos(request.form.get('u_lng'), request.form.get('u_lat'))
    print request.form
    # redirect(url_for('setcal'))
    # return json.dumps(gcal.get_ucals(), indent=JSON_DENT)
    return '<meta http-equiv="refresh" content ="1000; URL=http://localhost:5000/setcal">'

@setup_blp.route('/pos/get', methods=['GET','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def get_pos():
    return json.dumps(setup.get_position(), indent=JSON_DENT)
