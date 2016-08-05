from flask import Flask, request, send_from_directory, redirect, render_template
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret"
app.config['UPLOAD_FOLDER'] = "uploads"

@app.route("/", methods=['POST'])
def upload_thumb():
    if 'file' not in request.files:
        print "[ERROR] File not found"
        return '[ERROR]'

    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return '[UPLOADED]'

if __name__ == "__main__":
    app.run(port="8000")
