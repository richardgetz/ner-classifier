from flask import Flask, render_template, request, redirect, url_for
import json
import webbrowser
from werkzeug.utils import secure_filename
import tempfile
import os
import sys
import shutil
import re
import uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid1())
domain = "http://127.0.0.1"
port = 5000

tokens = [{"id": 0, "word": "This"}, {"id": 1, "word": "is"}, {"id": 2, "word": "an"}, {"id": 3, "word": "example"},
          {"id": 4, "word": "of"}, {"id": 5, "word": "what"},
          {"id": 6, "word": "a"}, {"id": 7, "word": "sentence"},
          {"id": 8, "word": "looks"}, {"id": 9, "word": "like"}, {"id": 10, "word": "."}]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', tokens=tokens)
    if request.method == 'POST':

        return render_template('index.html')


if __name__ == '__main__':
    webbrowser.open(domain + ":" + str(port))
    # change to ssl on prod
    app.run(debug=False, port=port, threaded=True)
