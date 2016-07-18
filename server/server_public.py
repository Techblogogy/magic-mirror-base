from flask import Flask, request, send_from_directory, redirect, render_template
import os, json

import decor

from routes.setup import setup_blp
from api_cal.setup import setup

from routes.gcal import gcal_api
from api_cal.gcal import gcal
#from dbase.dbase import dbase

# Initiate database instance
#db = dbase()
#db.setup()

# import api_cal.calendar

# Important Constants
JSON_DENT = 4

# Flask Elements
app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret"

# Reigster Blueprints
app.register_blueprint(gcal_api)
app.register_blueprint(setup_blp)

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


# Page 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Run Server Application
if __name__  == '__main__':
    app.run(debug=True, threaded=True)
