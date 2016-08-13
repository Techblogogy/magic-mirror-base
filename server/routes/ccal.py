
from flask import Blueprint, redirect
api_cal.calendar import cal

import os, json

ccal_api = Blueprint('ccal_api', __name__, url_prefix="/cal")

# Calendar API Routes

# main route
@ccal_api.route('/')
def cal_route():
    return "";

# events getter
@ccal_api.route('/events/get', methods=['GET'])
def cal_get_event():
    return json.dumps(cal.get_events(), indent=JSON_DENT)

# events getter in range
@ccal_api.route('/events/get/range', methods=['GET'])
def cal_get_rage_event():
    return json.dumps(cal.get_range_events(
        request.args.get('min'),
        request.args.get('max')
    ), indent=JSON_DENT)

# today event getter
@ccal_api.route('/events/get/today', methods=['GET'])
def cal_get_today_event():
    return json.dumps(cal.get_today_events(), indent=JSON_DENT)

# events adder
@ccal_api.route('/events/add', methods=['POST'])
def cal_add_event():
    return cal.add_event(
        request.form.get('task'),
        request.form.get('date'),
        request.form.get('time'))

# events updater
@ccal_api.route('/events/update', methods=['POST'])
def cal_upt_event():
    return cal.upd_event(
        request.form.get('id', type=int),
        request.form.get('task'),
        request.form.get('date'),
        request.form.get('time'))

# events remover
@ccal_api.route('/events/delete', methods=['POST'])
def cal_rmv_event():
    return cal.rmv_event(request.form.get('id', type=int))
