from flask import Flask, request, abort, jsonify, redirect, url_for, flash
import uuid
import os
import sqlite3
from werkzeug.utils import secure_filename
from constants import (DB_FILE, USERNAME_KEY, PASSWORD_KEY, FILES_PATH,)
from print_settings import PrintSettings
from user import User
from add_doc_request import (AddDocRequest, DOCUMENT_NAME_KEY,)
from document import Document
import user_auth
import json

STATUS_KEY = 'status'

FILE_KEY = 'file'

app = Flask(__name__)
user_auth.initialize()

try:
    os.mkdir(FILES_PATH)
except:
    pass

printer_queue: list = []

@app.route('/add_doc', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400)

    if 'json' not in request.files:
        abort(400)

    file = request.files[FILE_KEY]
    if file.filename == '':
        abort(400)

    json_req = json.loads(request.files['json'].read())
    json_req[DOCUMENT_NAME_KEY] = file.filename

    doc_request = AddDocRequest.from_dict(json_req)
    if not doc_request:
        abort(400)

    document = Document.from_add_doc_request(doc_request)
    if not document:
        abort(400)

    filepath = os.path.join(FILES_PATH, document.get_saved_name())
    file.save(filepath)

    printer_queue.append(document)

    return jsonify(document.to_dict())

@app.route('/get_queue', methods=['GET'])
def read_queue():
    obj_queue = []
    for doc in printer_queue:
        obj_queue.append(doc.to_dict())
    return jsonify(obj_queue)

@app.route('/authenticate', methods=['POST'])
def register():
    if not request.json:
        abort(400)

    if USERNAME_KEY in request.json and PASSWORD_KEY in request.json:
        ret_val = {}

        uname = request.json[USERNAME_KEY]
        pwd = request.json[PASSWORD_KEY]

        user = user_auth.register_user(uname, pwd)

        if user is not None:
            user_dict = user.to_dict()
            user_dict[STATUS_KEY] = True

            return jsonify(user_dict)

        return jsonify({STATUS_KEY: False})

    else:
        abort(400)

@app.route('/authenticate', methods=['GET'])
def authenticate():
    if not request.json:
        abort(400)

    if USERNAME_KEY in request.json and PASSWORD_KEY in request.json:
        uname = request.json[USERNAME_KEY]
        pwd = request.json[PASSWORD_KEY]

        user = user_auth.authenticate_user(uname, pwd)

        if user is not None:
            user_dict = user.to_dict()
            user_dict[STATUS_KEY] = True

            return jsonify(user_dict)

        return jsonify({STATUS_KEY: False})

    else:
        abort(400)



if __name__ == '__main__':
    app.run(debug=True)
