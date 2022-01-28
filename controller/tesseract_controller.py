import logging
import traceback
import os
import urllib.request
from flask import Flask, request, redirect, jsonify, app
from config import config
from werkzeug.utils import secure_filename
from util import utility as util
from service import tesseract_service as ts
from app import app

log = logging.getLogger("tesseract-controller")
logging.basicConfig(level=logging.INFO)
# app = Flask(__name__)


@app.route(config.request_prefix + 'health', methods=['GET'])
def health():
    payload = {'data': "service status is up"}
    resp = jsonify(payload)
    resp.status_code = 200
    return resp


@app.route(config.request_prefix + 'multiple-files-upload', methods=['POST'])
def extract_text():
    # check if the post request has the file part
    log.info("extracting text ...")
    if config.file_upload_key not in request.files:
        resp = jsonify({'message': 'No file part found in the request'})
        resp.status_code = 400
        return resp
    files = request.files.getlist(config.file_upload_key)
    util.create_directory()

    errors = {}
    success = False

    ts.clean_up()

    success = ts.upload_files(files=files, success=success, errors=errors)

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
