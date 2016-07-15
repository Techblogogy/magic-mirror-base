from flask import Flask, request, send_from_directory, redirect, render_template
import os, json

import decor

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

@app.route('/')
def main():
    return render_template('setupSite.html', auth = gcal.need_auth(), userName = gcal.get_disp_name())

@app.route('/<path:filename>')
def index(filename):
    return send_from_directory('static', filename)

#calendar Settings
@app.route('/setcal')
def setcal():
    return render_template('setcal.html',
        auth = gcal.need_auth(),
        userName = gcal.get_disp_name(),
        cals = gcal.get_cals(),
        c_len = len(gcal.get_cals())
    )


# Page 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Run Server Application
if __name__  == '__main__':
    app.run(debug=True, threaded=True)
