import decor

from flask import Blueprint, redirect, request
from api_cal.gcal import gcal

import os, json

ALLOWED_ORIGIN = "*"
JSON_DENT = 4
gcal_api = Blueprint('gcal_api', __name__, url_prefix="/gcal")

# GOOGLE CALENDAR API Routes

# Authenication routes
@gcal_api.route('/auth2callback')
def gauth_callback():
    return redirect(gcal.auth_callback(request.args.get('code')))
@gcal_api.route('/gauth')
def gauth_call():
    return redirect(gcal.get_auth_uri())
@gcal_api.route('/isauth')
def gauth_isauth():
    return json.dumps({'is_needed': not gcal.need_auth()})
@gcal_api.route('/deauth')
def gauth_deauth():
    return redirect(gcal.deauth_usr())

# Get todays events
@gcal_api.route('/today', methods=['GET','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def gcal_today():
    return json.dumps(gcal.get_today(), indent=JSON_DENT)

# Get calendars
@gcal_api.route('/calendars', methods=['GET','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def gcal_cals():
    return json.dumps(gcal.get_cals(), indent=JSON_DENT)

# Save calendars
@gcal_api.route('/add/calendars', methods=['POST','OPTIONS'])
@decor.crossdomain(origin=ALLOWED_ORIGIN)
def gcal_save_cals():
    gcal.add_cals(json.loads(request.form.get('ids')))
    return ''
    # return json.dumps(gcal.get_ucals(), indent=JSON_DENT)

# Get todays events
@gcal_api.route('/mail', methods=['GET'])
def gcal_mail():
    return json.dumps(gcal.get_mail(), indent=JSON_DENT)

# === JSON Error Handling ===

@gcal_api.errorhandler(400)
def err_400(e):
    return '{"status": 400, "message":"Bad request"}', 400

@gcal_api.errorhandler(404)
def err_404(e):
    return '{"status": 404, "message":"Page not found"}', 404

@gcal_api.errorhandler(500)
def err_500(e):
    return '{"status": 500, "message":"Internal server error"}', 500
