import logging
import traceback
import os
from werkzeug.utils import secure_filename
from util import utility as util
from config import config as conf
from extractor import extractor

log = logging.getLogger("tesseract-service")
logging.basicConfig(level=logging.INFO)


def extract():
    files = list_file()
    print("files ...... ")
    print(files)
    result = {}
    try:
        for file in files:
            print(f'processing start for {file}')
            path = util.get_file_path(file)
            print(f"filePath {path}")
            extractor.convert_pdf_to_img(path)
            extractor.open_file(output=conf.outfile)
            extractor.extract_text()
            extractor.file_close()
            content = util.read_file(conf.outfile)
            result = {'fileName': file, 'content': content}
            # result[file] = content
            util.delete_output_file()
    except Exception as e:
        log.error(traceback.format_exc())
    print("successfully extracted text for all files")
    return result


def list_file():
    return util.list_file()


def upload_files(files, success, errors):
    log.info("uploading files ...")
    for file in files:
        try:
            log.info("process for file : " + file.filename)
            if file:
                try:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(conf.upload_folder, filename))
                    success = True
                except Exception as e:
                    print(e.with_traceback())
            else:
                errors[file.filename] = 'File unable to upload'
        except Exception as e:
            print(e)
            traceback.print_exception(e)
            log.error(errors)
            log.error(traceback.format_exc())
    return success


def clean_up():
    files = list_file()
    if files:
        log.info("cleaning up directories ...")
        for file in files:
            path = util.get_file_path(file)
            print("path : " + path)
            util.delete_file(path)
    else:
        log.info("files is empty.")
