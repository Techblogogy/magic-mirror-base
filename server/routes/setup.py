import decor

from flask import Blueprint, redirect, request, url_for
from api_cal.gcal import gcal

from api_cal.setup import setup

import os, json

ALLOWED_ORIGIN = "*"
JSON_DENT = 4
setup = Blueprint('setup', __name__, url_prefix="/setup")

# Authenication routes
# Save calendars
@setup.route("/setup/pos", methods=['POST','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def setup_get_pos():
    # print request.form.getlist('ids[]')
    print hello
    print request.form
    # redirect(url_for('setcal'))
    # return json.dumps(gcal.get_ucals(), indent=JSON_DENT)
    return '<meta http-equiv="refresh" content ="1000; URL=http://localhost:5000/setcal">'
