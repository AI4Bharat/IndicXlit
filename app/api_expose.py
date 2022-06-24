"""
Expose Transliteration Engine as an HTTP API.

USAGE:
    1. $ sudo env PATH=$PATH GOOGLE_APPLICATION_CREDENTIALS=/path_to_cred/ python3 api_expose.py

    2. Run in browser: production_port - 80
            http://localhost:8000/tl/ta/amma
            http://localhost:8000/languages

FORMAT:
    Based on the Varnam API standard
    https://api.varnamproject.com/tl/hi/bharat

"""

import os
import csv
from uuid import uuid4
from flask import jsonify, request
from datetime import datetime

## ------------------------- Configure ---------------------------------------- ##

CLOUD_STORE = False ##<<< UPDATE_AS_NEEDED
DEBUG = True

## Set in order to host in specific domain
SSL_FILES = None ##<<< UPDATE_AS_NEEDED
# SSL_FILES = ('/etc/letsencrypt/live/xlit-api.ai4bharat.org/fullchain.pem',
#              '/etc/letsencrypt/live/xlit-api.ai4bharat.org/privkey.pem')

## ------------------------- Logging ---------------------------------------- ##

os.makedirs('logs/', exist_ok=True)
USER_CHOICES_LOGS = 'logs/user_choices.tsv'
ANNOTATION_LOGS = 'logs/annotation_data.tsv'

USER_DATA_FIELDS = ['user_ip', 'user_id', 'timestamp', 'input', 'lang', 'output', 'topk_index']
ANNOTATE_DATA_FIELDS = ['user_ip', 'user_id', 'timestamp','lang', 'native', 'ann1', 'ann2', 'ann3']

def create_log_files():
    if not os.path.isfile(USER_CHOICES_LOGS):
        with open(USER_CHOICES_LOGS, 'w', buffering=1) as f:
            writer = csv.DictWriter(f, fieldnames=USER_DATA_FIELDS, delimiter = "\t")
            writer.writeheader()

    if not os.path.isfile(ANNOTATION_LOGS):
        with open(ANNOTATION_LOGS, 'w', buffering=1) as f:
            writer = csv.DictWriter(f, fieldnames=ANNOTATE_DATA_FIELDS, delimiter = "\t")
            writer.writeheader()

create_log_files()

## ----- Google FireStore
"""
Requires gcp credentials
"""
if CLOUD_STORE:
    from google.cloud import firestore
    db = firestore.Client()
    usrch_coll = "path_to_collection" ##<<< UPDATE_AS_NEEDED
    annot_coll = "path_to_collection" ##<<< UPDATE_AS_NEEDED

def add_document(coll, data): # FireStore
    doc_title = str(uuid4().hex)
    ref = db.collection(coll).document(doc_title)
    ref.set(data)

## --------------------

def write_userdata(data):
    with open(USER_CHOICES_LOGS, 'a', buffering=1) as f:
        writer = csv.DictWriter(f, fieldnames=USER_DATA_FIELDS, delimiter = "\t")
        writer.writerow(data)
    if CLOUD_STORE:
        add_document(usrch_coll, data)
    return

def write_annotatedata(data):
    with open(ANNOTATION_LOGS, 'a', buffering=1) as f:
        writer = csv.DictWriter(f, fieldnames=ANNOTATE_DATA_FIELDS, delimiter = "\t")
        writer.writerow(data)
    if CLOUD_STORE:
        add_document(annot_coll, data)
    return

## ----------------------------- Xlit Engine -------------------------------- ##

from ai4bharat.transliteration import xlit_server
app, engine = xlit_server.get_app()

## -------------------------- Custom Endpoints ------------------------------ ##

@app.route('/learn', methods=['POST'])
def learn_from_user():
    data = request.get_json(force=True)
    data['user_ip'] = request.remote_addr
    if 'user_id' not in data:
        data['user_id'] = request.cookies['xlit_user_id'] if 'xlit_user_id' in request.cookies else None
    data['timestamp'] = str(datetime.utcnow()) + ' +0000 UTC'
    write_userdata(data)
    return jsonify({'status': 'Success'})

@app.route('/annotate', methods=['POST'])
def annotate_by_user():
    data = request.get_json(force=True)
    data['user_ip'] = request.remote_addr
    if 'user_id' not in data:
        data['user_id'] = request.cookies['xlit_user_id'] if 'xlit_user_id' in request.cookies else None
    data['timestamp'] = str(datetime.utcnow()) + ' +0000 UTC'
    write_annotatedata(data)
    return jsonify({'status': 'Success'})

## -------------------------- Server Setup ---------------------------------- ##

def host_https():
    https_server = WSGIServer(('0.0.0.0', 443), app,
                                     certfile=SSL_FILES[0], keyfile=SSL_FILES[1])
    print('Starting HTTPS Server...')
    https_server.serve_forever()
    return

if __name__ == '__main__':

    if not DEBUG: # Production Server
        from flask_cors import CORS, cross_origin
        cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        # app.run(host='0.0.0.0', port=443, ssl_context=SSL_FILES)

        from gevent.pywsgi import WSGIServer
        if SSL_FILES:
            from multiprocessing import Process
            Process(target=host_https).start()

        http_server = WSGIServer(('0.0.0.0', 80), app)
        print('Starting HTTP Server...')
        http_server.serve_forever()
    else: # Development Server
        app.run(debug=True, host='0.0.0.0', port=8000)
