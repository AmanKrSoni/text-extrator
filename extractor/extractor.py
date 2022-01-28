# Import libraries
import cv2
import logging
import pytesseract
import traceback
from pdf2image import convert_from_path
from config import config as config
from preprocessor import image_pre_processor as img_proc
from util import utility as util

# global variables
custom_config = config.custom_config
file_limit = 0
outfile = config.outfile
file_name_prefix = "page_"
file_extension = ".jpg"
file_operation = None


def delete_file(file):
    try:
        util.delete_file(file)
    except Exception as e:
        logging.info("error while deleting file : {}", file)
        logging.error(traceback.format_exc())


def set_file_limit(counter):
    return counter - 1


def open_file(output):
    global file_operation
    file_operation = open(output, "a")


def file_write(content):
    global file_operation
    file_operation.write(content)


def file_close():
    global file_operation
    file_operation.close()


'''
Part #1 : Converting PDF to images
'''


def convert_pdf_to_img(file):
    print(f"reading file :  {file}")
    delete_file(config.outfile)
    try:
        pages = convert_from_path(file, 500)
        image_counter = 1
        for page in pages:
            filename = file_name_prefix + str(image_counter) + file_extension
            # Save the image of the page in system
            page.save(filename, 'JPEG')
            # Increment the counter to update filename
            image_counter = image_counter + 1
        global file_limit
        file_limit = image_counter - 1
    except Exception as e:
        logging.error(traceback.format_exc())


def extract_text():
    try:
        # Iterate from 1 to total number of pages
        for x in range(1, file_limit + 1):
            file_name = file_name_prefix + str(x) + file_extension
            # Recognize the text as string in image using pytesserct
            content = str((pytesseract.image_to_string(pre_process_img(file_name), config=custom_config)))
            content = content.replace('-\n', '')
            # Finally, write the processed text to the file.
            file_write(content)
            delete_file(file_name)
    except Exception as e:
        logging.error("error while extracting text for file : {}", file_name)
        logging.error(traceback.format_exc())
    finally:
        file_close()


def pre_process_img(file):
    print(f"pre-processing file : {file}")
    try:
        return img_proc.perform_adaptive_thresholding(file)
        # img = cv2.imread(file)
        # img_gray = img_proc.get_grayscale(img)
        # thresh = img_proc.thresholding(img_gray)
        # return thresh

    except Exception as e:
        logging.error("error while pre-processing file : {}", file)
        logging.error(traceback.format_exc())
