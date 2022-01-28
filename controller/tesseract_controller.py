import os
import urllib.request
from flask import Flask, request, redirect, jsonify, app
from config import config
from werkzeug.utils import secure_filename
from util import utility as util
from service import tesseract_service as ts
from app import app


# app = Flask(__name__)


@app.route(config.request_prefix + 'health', methods=['GET'])
def health():
    payload = {'data': "service status is up"}
    resp = jsonify(payload)
    resp.status_code = 200
    return resp


@app.route(config.request_prefix + 'multiple-files-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if config.file_upload_key not in request.files:
        resp = jsonify({'message': 'No file part found in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist(config.file_upload_key)
    util.create_directory()

    errors = {}
    success = False

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(config.upload_folder, filename))
            success = True
        else:
            errors[file.filename] = 'File unable to upload'

    if success and errors:
        errors['message'] = 'Files successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        result = ts.extract()
        resp = jsonify({'message': 'Files successfully uploaded'})
        print(result)
        resp.status_code = 201
        return jsonify(result)
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
