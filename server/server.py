from flask import Flask, request, abort, jsonify, redirect, url_for, flash
import uuid
import os
import sqlite3
from werkzeug.utils import secure_filename

DB_FILE = 'test.db'

USERNAME_KEY = 'usr'
PASSWORD_KEY = 'password'


USER_INSERT_TEMP = "INSERT INTO users (uname, pwd, auth_key) VALUES (?, ?, ?)"
USER_AUTH_TEMP = "SELECT pwd, auth_key FROM users WHERE uname=?"

KEY_INSERT_TEMP = "INSERT INTO keys (auth_key, uname) VALUES (?, ?)"


app = Flask(__name__)
db_con = sqlite3.connect('test.db')

valid_extensions = ['.doc', '.docx', '.txt', '.pdf']

printer_queue = []

def allowed_file(filename):
    _, extension = os.path.splitext(filename)
    return '.' in filename and \
           extension in valid_extensions

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('./', filename)
            file.save(filepath)
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/upload', methods=['POST'])
def add_to_queue():
    if not request.json:
        abort(400)
    filename, extension = os.path.splitext(request.json['file'])
    if not extension in valid_extensions:
        abort(422)
    doc = {
        'id': uuid.uuid4(),
        'pos': len(printer_queue),
        'file': request.json['file'],
        'type': extension[1:]
    }
    printer_queue.append(doc)
    return jsonify(doc)

@app.route('/upload', methods=['GET'])
def read_queue():
    return jsonify(printer_queue)

@app.route('/authenticate', methods=['POST'])
def register():
    if not request.json:
        abort(400)

    if USERNAME_KEY in request.json and PASSWORD_KEY in request.json:
        ret_val = {}

        db_con = sqlite3.connect(DB_FILE)
        c = db_con.cursor()

        uname = request.json[USERNAME_KEY]
        pwd = request.json[PASSWORD_KEY]
        auth_key = str(uuid.uuid4())

        try:
            c.execute(USER_INSERT_TEMP, (uname, pwd, auth_key))
            c.execute(KEY_INSERT_TEMP, (auth_key, pwd))

            db_con.commit()
            db_con.close()

            ret_val['status'] = True
            ret_val['auth_key'] = auth_key
            ret_val['uname'] = uname

            return jsonify(ret_val)
        except:
            ret_val['status'] = False

        return jsonify(ret_val)
    else:
        abort(400)

@app.route('/authenticate', methods=['GET'])
def authenticate():
    if not request.json:
        abort(400)

    if USERNAME_KEY in request.json and PASSWORD_KEY in request.json:
        ret_val = { 'status': True }

        db_con = sqlite3.connect(DB_FILE)
        c = db_con.cursor()

        uname = request.json[USERNAME_KEY]
        given_pwd = request.json[PASSWORD_KEY]

        if uname == '' or given_pwd == '':
            abort(400)

        pwd = ''
        auth_key = ''

        try:
            c.execute(USER_AUTH_TEMP, (uname,))
            response = c.fetchall()[0]
            pwd = response[0]
            auth_key = response[1]

        except:
            ret_val['status'] = False

        if pwd == given_pwd:
            ret_val['auth_key'] = auth_key
            ret_val['usr'] = uname

        else:
            ret_val['status'] = False

        return jsonify(ret_val)
    else:
        abort(400)



if __name__ == '__main__':
    db_con = sqlite3.connect(DB_FILE)

    auth_keys_table='''CREATE TABLE keys (
        auth_key text PRIMARY KEY,
        uname text NOT NULL)'''

    users_table = '''CREATE TABLE users (
        uname text PRIMARY KEY,
        pwd text NOT NULL,
        auth_key text NOT NULL)'''

    c = db_con.cursor()
    try:
        c.execute(auth_keys_table)
    except:
        pass

    try:
        c.execute(users_table)
    except:
        pass

    db_con.commit()
    db_con.close()

    app.run(debug=True)
