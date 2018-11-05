from .constants import (USERNAME_KEY, PASSWORD_KEY, FILES_PATH, \
                        USER_ID_KEY, STATUS_KEY, INPUT_FILE_KEY, \
                        DATA_KEY,)
from .document import (Document,)
from .print_settings import (PrintSettings,)
from .user import (User,)
from . import (user_auth, printer_queue,)

from flask import (Flask, request, abort, \
                   jsonify, redirect, url_for, \
                   flash, send_file,)
from flask_cors import (CORS,)
from typing import (List,)
from werkzeug.utils import (secure_filename,)
import json
import os
import sqlite3
import uuid

user_auth.initialize()
printer_queue.initialize()

app = Flask(__name__)
CORS(app)

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
        DATA_KEY: data
    }

@app.route('/add_doc_settings', methods=['POST'])
def upload_settings():
    if request.json is None:
        return jsonify(create_return_json(False))

    user_id = request.args.get(USER_ID_KEY, type = str)
    user = user_auth.get_user(user_id)
    if not user:
        return jsonify(create_return_json(False))

    settings = PrintSettings.from_dict(request.json)
    if not settings:
        return jsonify(create_return_json(False))

    document = printer_queue.unload_doc(user, settings)
    if not document:
        return jsonify(create_return_json(False))

    printer_queue.add_to_queue(document)

    return jsonify(create_return_json(True, document.to_dict()))

@app.route('/add_doc_file', methods=['POST'])
def upload_file():
    if INPUT_FILE_KEY not in request.files:
        return jsonify(create_return_json(False))

    file = request.files[INPUT_FILE_KEY]
    if file.filename == '':
        return jsonify(create_return_json(False))

    user_id = request.args.get(USER_ID_KEY, type = str)
    user = user_auth.get_user(user_id)
    if not user:
        return jsonify(create_return_json(False))

    doc_filename = printer_queue.load_doc(user, file.filename)
    if not doc_filename:
        return jsonify(create_return_json(False))

    filepath = os.path.join(FILES_PATH, doc_filename)
    file.save(filepath)

    return jsonify(create_return_json(True))

@app.route('/get_doc', methods=['GET'])
def get_doc():
    if printer_queue.get_len() is 0:
        return jsonify(create_return_json(False))

    document = printer_queue.top()
    filepath = os.path.join('../' + FILES_PATH, document.get_saved_name())
    print(filepath)
    return send_file(filepath, attachment_filename=document.get_saved_name())

@app.route('/get_doc_settings', methods=['GET'])
def get_settings():
    if printer_queue.get_len() is 0:
        return jsonify(create_return_json(False))

    settings_dict = printer_queue.top().settings.to_dict()
    return jsonify(create_return_json(True, settings_dict))

@app.route('/pop_doc', methods=['GET'])
def pop_doc():
    if printer_queue.get_len() is 0:
        return jsonify(create_return_json(False))

    document = printer_queue.top()
    filepath = os.path.join(FILES_PATH, document.get_saved_name())
    os.remove(filepath)

    printer_queue.pop()

    return jsonify(create_return_json(True))

@app.route('/get_queue', methods=['GET'])
def get_queue():
    user_id = request.args.get(USER_ID_KEY, type = str)
    if user_id:
        user = user_auth.get_user(user_id)
        if not user:
            return jsonify(create_return_json(False))

        doc_list = printer_queue.get_queue(user)
    else:
        doc_list = printer_queue.get_queue()

    obj_queue = []
    for doc in doc_list:
        obj_queue.append(doc.to_dict())

    return jsonify(obj_queue)

@app.route('/register', methods=['POST'])
def register():
    if not request.json:
        return jsonify(create_return_json(False))

    if USERNAME_KEY in request.json and PASSWORD_KEY in request.json:
        uname = request.json[USERNAME_KEY]
        pwd = request.json[PASSWORD_KEY]

        user = user_auth.register_user(uname, pwd)

        if user is not None:
            user_dict = user.to_dict()

            return jsonify(create_return_json(True, user_dict))

        return jsonify(create_return_json(False))

    else:
        return jsonify(create_return_json(False))

@app.route('/login', methods=['POST'])
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
