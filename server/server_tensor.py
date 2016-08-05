from flask import Flask, request, send_from_directory, redirect, render_template
from werkzeug.utils import secure_filename

import os
import json

import tensorflow as tf
import sys

from minfo import app_dir

# change this as you see fit
# image_path = sys.argv[1]

# Read in the image_data
# image_data = tf.gfile.FastGFile(image_path, 'rb').read()

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line
                   in tf.gfile.GFile(app_dir+"/tf_files/retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile(app_dir+"/tf_files/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


app = Flask(__name__)
app.config['SECRET_KEY'] = "supersecret"
app.config['UPLOAD_FOLDER'] = "uploads"

def get_dresscode(image_path):
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))


@app.route("/", methods=['POST'])
def upload_thumb():
    if 'file' not in request.files:
        print "[ERROR] File not found"
        return '[ERROR]'

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)

    dcode = get_dresscode(filepath)

    os.remove(filepath)

    return '[UPLOADED]'


if __name__ == "__main__":
    app.run(port="8000")
