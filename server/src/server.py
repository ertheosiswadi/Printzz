from .constants import (USERNAME_KEY, PASSWORD_KEY, FILES_PATH, \
                        USER_ID_KEY, STATUS_KEY, INPUT_FILE_KEY, \
                        DATA_KEY, DOC_ID_KEY, PRINTER_STATUS_KEY,
                        PRINTER_ID, PRINTER_ID_KEY, ERROR_KEY,)
from .document import (Document,)
from .print_settings import (PrintSettings,)
from .user import (User,)
from . import (user_auth, printer_queue,)

from flask import (Flask, request, abort, \
                   jsonify, redirect, url_for, \
                   flash, send_file, render_template,)
from flask_cors import (CORS,)
from flask_restplus import inputs
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

def create_return_json(status, data=None, error=None):
    ret_dict = { STATUS_KEY: status }
    if data:
        ret_dict[DATA_KEY] = data

    if error:
        ret_dict[ERROR_KEY] = error

    return ret_dict

@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/html/<page>', methods=['GET'])
def page_selection(page):
    template = ''
    if page == 'p_upload':
        template = 'print_upload.html'
    elif page == 'p_queue':
        template = 'print_queue.html'
    elif page == 'p_signup':
        template = 'sign_up.html'
    elif page == 'p_login':
        template = 'login.html'
    elif page == 'p_settings':
        template = 'print_settings.html'
    elif page == 'p_review':
        template = 'print_review.html'
    elif page == 'p_success':
        template = 'print_success.html'

    return render_template(template)

@app.route('/add_doc_settings', methods=['POST'])
def upload_settings():
    if request.json is None:
        return jsonify(create_return_json(False, error = 'Settings JSON was not given.'))

    user_id = request.args.get(USER_ID_KEY, type = str)
    user = user_auth.get_user(user_id)
    if not user:
        return jsonify(create_return_json(False, error = f'User with user_id: {user_id} does not exist.'))

    settings = PrintSettings.from_dict(request.json)
    if not settings:
        return jsonify(create_return_json(False, error = 'Settings JSON was invalid.'))

    document = printer_queue.unload_doc(user, settings)
    if not document:
        return jsonify(create_return_json(False, error = f'No document previously loaded for user with user_id: {user_id}'))

    printer_queue.add_to_queue(document)

    return jsonify(create_return_json(True, document.to_dict()))

@app.route('/add_doc_file', methods=['POST'])
def upload_file():
    if INPUT_FILE_KEY not in request.files:
        return jsonify(create_return_json(False, error = 'No file provided.'))

    file = request.files[INPUT_FILE_KEY]
    if file.filename == '':
        return jsonify(create_return_json(False, 'Filename cannot be empty.'))

    user_id = request.args.get(USER_ID_KEY, type = str)
    user = user_auth.get_user(user_id)
    if not user:
        return jsonify(create_return_json(False, error = f'User with user_id: {user_id} does not exist.'))

    doc_filename = printer_queue.load_doc(user, file.filename)
    if not doc_filename:
        return jsonify(create_return_json(False, error = f'Failed to load document.'))

    filepath = os.path.join(FILES_PATH, doc_filename)
    file.save(filepath)

    return jsonify(create_return_json(True))

@app.route('/get_doc', methods=['GET'])
def get_doc():
    printer_id = request.args.get(PRINTER_ID_KEY, type = str)
    if not printer_id or printer_id != PRINTER_ID:
        return jsonify(create_return_json(False, error = 'Invalid printer id!'))

    if printer_queue.get_len() is 0:
        return jsonify(create_return_json(False, error = 'Queue is empty.'))

    document = printer_queue.top()
    filepath = os.path.join('../' + FILES_PATH, document.get_saved_name())
    print(filepath)
    return send_file(filepath, attachment_filename=document.get_saved_name())

@app.route('/get_doc_settings', methods=['GET'])
def get_settings():
    printer_id = request.args.get(PRINTER_ID_KEY, type = str)
    if not printer_id or printer_id != PRINTER_ID:
        return jsonify(create_return_json(False, error = 'Invalid printer id!'))

    if printer_queue.get_len() is 0:
        return jsonify(create_return_json(False, error = 'Queue is empty.'))

    document = printer_queue.top()
    return jsonify(create_return_json(True, document.to_dict()))

@app.route('/pop_doc', methods=['GET'])
def pop_doc():
    printer_id = request.args.get(PRINTER_ID_KEY, type = str)
    if not printer_id or printer_id != PRINTER_ID:
        return jsonify(create_return_json(False, error = 'Invalid printer id!'))

    if printer_queue.get_len() is 0:
        return jsonify(create_return_json(False, error = 'Queue is empty.'))

    document = printer_queue.top()
    filepath = os.path.join(FILES_PATH, document.get_saved_name())
    os.remove(filepath)

    printer_queue.pop()

    return jsonify(create_return_json(True))

@app.route('/delete_doc', methods=['GET'])
def delete_doc():
    user_id = request.args.get(USER_ID_KEY, type = str)
    doc_id = request.args.get(DOC_ID_KEY, type = str)

    if user_id is None:
        return jsonify(create_return_json(False, error = 'No user_id provided.'))

    if doc_id is None:
        return jsonify(create_return_json(False, error = 'No doc_id provided'))

    user = user_auth.get_user(user_id)
    if not user:
        return jsonify(create_return_json(False, error = f'User with user_id: {user_id} does not exist.'))

    if not printer_queue.delete_doc(user, doc_id):
        return jsonify(create_return_json(False, error = f'Document with doc_id: {doc_id} does not exist.'))

    return jsonify(create_return_json(True))

@app.route('/get_queue', methods=['GET'])
def get_queue():
    user_id = request.args.get(USER_ID_KEY, type = str)
    if user_id:
        user = user_auth.get_user(user_id)
        if not user:
            return jsonify(create_return_json(False, error = f'User with user_id: {user_id} does not exist.'))

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
        username = request.json[USERNAME_KEY]
        password = request.json[PASSWORD_KEY]

        user = user_auth.register_user(username, password)

        if user is not None:
            user_dict = user.to_dict()

            return jsonify(create_return_json(True, user_dict))

        return jsonify(create_return_json(False, error = f'User with username: {username} already exists'))

    else:
        return jsonify(create_return_json(False, error = 'Username and Password not specified in json object.'))

@app.route('/login', methods=['POST'])
def authenticate():
    if not request.json:
        return jsonify(create_return_json(False, error = 'No JSON data provided.'))

    if USERNAME_KEY in request.json and PASSWORD_KEY in request.json:
        username = request.json[USERNAME_KEY]
        password = request.json[PASSWORD_KEY]

        user = user_auth.authenticate_user(username, password)

        if user is not None:
            user_dict = user.to_dict()
            return jsonify(create_return_json(True, user_dict))

        return jsonify(create_return_json(False, error = f'Invalid password/username.'))

    else:
        return jsonify(create_return_json(False, error = f'Invalid JSON.'))

@app.route('/printer_status', methods=['POST'])
def update_printer_status():
    printer_id = request.args.get(PRINTER_ID_KEY, type = str)
    printer_status = request.args.get(PRINTER_STATUS_KEY, type = inputs.boolean)

    if not printer_id or printer_id != PRINTER_ID:
        return jsonify(create_return_json(False, error = 'Invalid printer id!'))

    if printer_status is None:
        return jsonify(create_return_json(False, error = 'No status provided.'))

    printer_queue.update_status(printer_status)

    return jsonify(create_return_json(True))

@app.route('/printer_status', methods=['GET'])
def get_printer_status():
    return jsonify(create_return_json(printer_queue.get_status()))
