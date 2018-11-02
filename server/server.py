from flask import Flask, request, abort, jsonify, redirect, url_for, flash, send_file
import uuid
import os
import sqlite3
from werkzeug.utils import secure_filename
from constants import (DB_FILE, USERNAME_KEY, PASSWORD_KEY, FILES_PATH,)
from print_settings import PrintSettings
from user import User
from add_doc_request import (AddDocRequest, DOCUMENT_NAME_KEY,)
from document import Document
from typing import List
import user_auth
import json

STATUS_KEY = 'status'
JSON_KEY = 'json'
FILE_KEY = 'file'

PRINTER_QUEUE: List[Document] = []
user_auth.initialize()

app = Flask(__name__)

try:
    os.mkdir(FILES_PATH)
except:
    pass

def create_return_json(status, data=None):
    if not data:
        return {
            STATUS_KEY: status
        }

    return {
        STATUS_KEY: status,
        JSON_KEY: data
    }


@app.route('/add_doc', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(create_return_json(False))

    if 'json' not in request.files:
        return jsonify(create_return_json(False))

    file = request.files[FILE_KEY]
    if file.filename == '':
        return jsonify(create_return_json(False))

    json_req = json.loads(request.files['json'].read())
    json_req[DOCUMENT_NAME_KEY] = file.filename

    doc_request = AddDocRequest.from_dict(json_req)
    if not doc_request:
        return jsonify(create_return_json(False))

    document = Document.from_add_doc_request(doc_request)
    if not document:
        return jsonify(create_return_json(False))

    filepath = os.path.join(FILES_PATH, document.get_saved_name())
    file.save(filepath)

    PRINTER_QUEUE.append(document)

    return jsonify(create_return_json(True, document.to_dict()))

@app.route('/get_doc', methods=['GET'])
def get_doc():
    if len(PRINTER_QUEUE) is 0:
        return jsonify(create_return_json(False))

    document = PRINTER_QUEUE[0]
    filepath = os.path.join(FILES_PATH, document.get_saved_name())
    return send_file(filepath, attachment_filename=document.get_saved_name())

@app.route('/get_doc_settings', methods=['GET'])
def get_settings():
    if len(PRINTER_QUEUE) is 0:
        return jsonify(create_return_json(False))

    settings_dict = PRINTER_QUEUE[0].settings.to_dict()
    return jsonify(create_return_json(True, settings_dict))

@app.route('/pop_doc', methods=['GET'])
def pop_doc():
    global PRINTER_QUEUE
    if len(PRINTER_QUEUE) is 0:
        return jsonify(create_return_json(False))

    filepath = os.path.join(FILES_PATH, PRINTER_QUEUE[0].get_saved_name())
    os.remove(filepath)

    PRINTER_QUEUE = PRINTER_QUEUE[1:]

    return jsonify(create_return_json(True))

@app.route('/get_queue', methods=['GET'])
def read_queue():
    obj_queue = []
    for doc in PRINTER_QUEUE:
        obj_queue.append(doc.to_dict())
    return jsonify(obj_queue)

@app.route('/authenticate', methods=['POST'])
def register():
    if not request.json:
        return jsonify(create_return_json(False))

    if USERNAME_KEY in request.json and PASSWORD_KEY in request.json:
        ret_val = {}

        uname = request.json[USERNAME_KEY]
        pwd = request.json[PASSWORD_KEY]

        user = user_auth.register_user(uname, pwd)

        if user is not None:
            user_dict = user.to_dict()

            return jsonify(create_return_json(True, user_dict))

        return jsonify(create_return_json(False))

    else:
        return jsonify(create_return_json(False))

@app.route('/authenticate', methods=['GET'])
def authenticate():
    if not request.json:
        return jsonify(create_return_json(False))

    if USERNAME_KEY in request.json and PASSWORD_KEY in request.json:
        uname = request.json[USERNAME_KEY]
        pwd = request.json[PASSWORD_KEY]

        user = user_auth.authenticate_user(uname, pwd)

        if user is not None:
            user_dict = user.to_dict()
            return jsonify(create_return_json(True, user_dict))

        return jsonify(create_return_json(False))

    else:
        return jsonify(create_return_json(False))



if __name__ == '__main__':
    app.run(debug=True)
