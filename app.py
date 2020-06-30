from flask import Flask, render_template, request, redirect, url_for, flash
import json
import webbrowser
from werkzeug.utils import secure_filename
import tempfile
import os
import sys
import shutil
import re
import uuid
import glob
import spacy
import pkg_resources
# from data_controller import save boundaries
app = Flask(__name__)
app.secret_key = str(uuid.uuid1())
DATASET_LOADED = False
ACTIVE_LEARNING_MODEL = None
# TODO: add as default config instead and make editable in the frontend
LABELS = ["PERSON", "LOC", "ORG", "GPE", "NORP", "PHONE", "EMAIL"]
DATA_STORE_LOCATION = ""
domain = "http://127.0.0.1"
CERT_LOCATION = "adhoc"
port = 5000
pkgs = pkg_resources.working_set
pkgs_1 = sorted(["%s==%s" % (i.key, i.version) for i in pkgs])
ALL_INSTALLED = re.findall(
    r"([a-z]{2,3}(?:\-\w+){2,5}\-(?:sm|md|lg))", str(pkgs_1))
ACTIVE = []
AWAIT_OVERRIDE = False
# this would be built from spacy' output
DATASET = [{"uuid": 0,
            "sentence": [{"id": 0, "word": "John"}, {"id": 1, "word": "Smith"}, {"id": 2, "word": "is"}, {"id": 3, "word": "the"}, {"id": 4, "word": "user"},
                         {"id": 5, "word": "of"}, {"id": 6, "word": "john@mail.com"}],
            "spans": {"PERSON": ["0:1"], "EMAIL":["6:6"]}},
           {"uuid": 1,
            "sentence": [{"id": 0, "word": "Here"}, {"id": 1, "word": "is"}, {"id": 2, "word": "a"}, {"id": 3, "word": "sentence"}, {"id": 4, "word": "without"},
                         {"id": 5, "word": "any"}, {"id": 6, "word": "tags"}],
            "spans": None}]
ALPHA_DATASET = []
ALLOWED_EXTENSIONS = ['json']


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'GET':
        return "This will eventually allow you to train with a few clicks. Not worried about this yes since we have to test training data first."
        return render_template('train.html')
    if request.method == 'POST':
        print("in progress")


@app.route('/dataset_loader', methods=['GET', 'POST'])
def load_data():

    global ALL_INSTALLED
    models = ALL_INSTALLED
    print(models)
    global DATA_STORE_LOCATION
    if request.method == 'GET':
        if os.path.exists(os.path.join(DATA_STORE_LOCATION, "completed_models")):
            for file in os.listdir(os.path.join(DATA_STORE_LOCATION, "completed_models")):
                models.append(str(file))
        if len(models) == 0:
            models = None
        if os.path.exists(os.path.join(DATA_STORE_LOCATION, "datasets/untrained")):
            datasets = []
            for file in os.listdir(os.path.join(DATA_STORE_LOCATION, "datasets/untrained")):
                if file.endswith(".json"):
                    datasets.append({"label": str(file).rstrip(
                        ".json"), "filename": str(file)})

            if datasets == []:
                datasets = None
            return render_template('load_generate.html', datasets=datasets,
                                   models=models)

        else:
            return render_template('load_generate.html', datasets=None,
                                   models=models)

    if request.method == 'POST':
        req = request.form.to_dict()
        if not os.path.exists(DATA_STORE_LOCATION):
            os.mkdir(DATA_STORE_LOCATION)
        if not os.path.exists(os.path.join(DATA_STORE_LOCATION, "datasets/untrained")):
            os.mkdir(os.path.join(DATA_STORE_LOCATION, "datasets/untrained"))

        file = request.files["file"]
        max = None
        try:
            if req.get("max-sentences", False):
                max = int(req["max-sentences"])
        except:
            pass
        use_dataset = None
        if file:
            if allowed_file(file.filename):
                if req.get("name", False):
                    ext = str(file.filename).split(".")[-1]
                    filename = secure_filename(req["name"] + "." + ext)
                else:
                    filename = secure_filename(file.filename)
                use_dataset = filename
                full_path = os.path.join(os.path.join(DATA_STORE_LOCATION,
                                                      "datasets/untrained"), filename)
                file.save(full_path)

        print("in progress")


@app.route('/', methods=['GET', 'POST'])
def index():

    global LABELS
    global DATASET
    global DATASET_LOADED
    global ACTIVE
    global AWATT_OVERRIDE
    if len(DATASET) > 0:
        DATASET_LOADED = True
    if request.method == 'GET':
        if not DATASET_LOADED:
            flash("No active data to train on. Please load some data first.")
            return redirect(url_for('load_data'))
        if len(DATASET) == 0:
            if len(ACTIVE) == 0:
                flash(
                    "No data left to train on. Either load more or cheer because you're done!")
                return redirect(url_for('load_data'))
        elif len(ACTIVE) > 0:
            if AWAIT_OVERRIDE:
                AWAIT_OVERRIDE = False
                return render_template('index.html', labels=LABELS,
                                       tokens=ACTIVE[0]["sentence"], spans=ACTIVE[0]["spans"],
                                       sentence_id=ACTIVE[0]["uuid"])

            else:
                AWAIT_OVERRIDE = True
                flash("Someone is still training on your current dataset. Highly recommend waiting until they are finished. If you go to the homepage you will forceably take their training task.")
                return redirect(url_for('load_data'))
        else:
            ACTIVE.append(DATASET[0])
            send = DATASET[0]
            DATASET.remove(DATASET[0])
            return render_template('index.html', labels=LABELS,
                                   tokens=send["sentence"], spans=send["spans"], sentence_id=send["uuid"])
    if request.method == 'POST':
        req = request.form.to_dict()
        sentence_id = None
        sentence_tags = {}
        for a in ACTIVE:
            if str(a["uuid"]) == req["sentence_id"]:
                sentence_id = req["sentence_id"]
                ACTIVE.remove(a)
                break
        if sentence_id:
            for tag in req.keys():
                if tag == "sentence_id":
                    continue

                sentence_tags[tag] = req[tag].split(",")

        print(sentence_id, sentence_tags)
        if not DATASET_LOADED:
            flash(
                "No data left to train on. Either load more or cheer because you're done!")
            return redirect(url_for('load_data'))
        available = False
        while not available:
            if len(DATASET) < 1:
                if len(ACTIVE) == 0:
                    DATASET_LOADED = False
                    flash(
                        "No data left to train on. Either load more or cheer because you're done!")
                    return redirect(url_for('load_data'))
                elif len(ACTIVE) > 0:
                    if AWAIT_OVERRIDE:
                        AWAIT_OVERRIDE = False
                        return render_template('index.html', labels=LABELS, tokens=ACTIVE[0]["sentence"], spans=ACTIVE[0]["spans"], sentence_id=ACTIVE[0]["uuid"])

                    else:
                        AWAIT_OVERRIDE = True
                        return "There is no more data to show you but another user is still tagging a sentence. If you reload this page we will forceably give you the sentence."
            else:
                ACTIVE.append(DATASET[0])
                send = DATASET[0]
                DATASET.remove(DATASET[0])
                return render_template('index.html', tokens=send["sentence"], sentence_id=send["uuid"], labels=LABELS,
                                       spans=send["spans"])


if __name__ == '__main__':
    webbrowser.open(domain + ":" + str(port))
    app.run(debug=False, port=port, threaded=True)
