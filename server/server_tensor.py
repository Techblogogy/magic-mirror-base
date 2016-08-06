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

        codes = []
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            # codes.append( {'code': human_string, 'score': format(score, "0.2f")} )
            codes.append( {'code': human_string, 'score': int(score * 100)} )

            # print('%s (score = %.5f)' % (human_string, score))

        return codes


@app.route("/", methods=['POST'])
def upload_thumb():
    resp = {"status": 200}
    if 'file' not in request.files:
        resp["status"] = 500
        print "[ERROR] File not found"
        return '[ERROR]'

    print resp

    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(filepath)

    dcode = get_dresscode(filepath)
    # print json.dumps(dcode, indent=4)
    resp["dress"] = dcode

    os.remove(filepath)

    # print json.dumps(resp, indent=4)
    return json.dumps(resp, indent=4)



if __name__ == "__main__":
    app.run(port="8000")
