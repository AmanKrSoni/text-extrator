import logging
import traceback
from util import utility as util
from config import config as conf
from extractor import extractor


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
            result[file] = content
            util.delete_output_file()
    except Exception as e:
        logging.error(traceback.format_exc())
    print("successfully extracted text for all files")
    return result


def list_file():
    return util.list_file()
