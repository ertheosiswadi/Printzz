from flask import Flask, request, abort, jsonify, redirect, url_for
import uuid
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
