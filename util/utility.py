import os
from config import config
from os import listdir
from os.path import isfile, join


def list_file(directory=config.upload_folder):
    only_files = [f for f in listdir(directory) if isfile(join(directory, f))]
    print(only_files)
    return only_files


def delete_file(file):
    # If file exists, delete it ##
    if os.path.isfile(file):
        os.remove(file)
    else:  # Show an error ##
        print("Error: %s file not found" % file)


def create_directory():
    UPLOAD_FOLDER = os.path.join(os.getcwd(), config.upload_folder)
    print(f"checking for dir {UPLOAD_FOLDER} if not create new one")
    # Make directory if "uploads" folder not exists
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)


def get_upload_directory_path():
    UPLOAD_FOLDER = os.path.join(os.getcwd(), config.upload_folder)
    return UPLOAD_FOLDER


def get_file_path(file):
    path = os.path.join(config.upload_folder, file)
    return path


def delete_output_file():
    path = os.path.join(os.getcwd(), config.outfile)
    delete_file(path)


def allowed_extension():
    return set(config.allowed_extensions)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension()


def read_file(file):
    f = open(file=file, mode='r')
    contents = f.readlines()
    f.close()
    return contents
