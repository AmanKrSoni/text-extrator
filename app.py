from flask import Flask
from config import config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.upload_folder
app.config['MAX_CONTENT_LENGTH'] = config.max_content_length
