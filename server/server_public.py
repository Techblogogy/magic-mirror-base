from flask import Flask, request, send_from_directory, redirect
import os, json

import decor

from routes.gcal import gcal_api
#from dbase.dbase import dbase

# Initiate database instance
#db = dbase()
#db.setup()

# import api_cal.calendar

# Important Constants
JSON_DENT = 4

# Flask Elements
app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret";

# Reigster Blueprints
app.register_blueprint(gcal_api)

@app.route('/<path:filename>')
def index(filename):
    return send_from_directory(os.path.dirname(os.getcwd()), filename)

# Run Server Application
if __name__  == '__main__':
    app.run()
