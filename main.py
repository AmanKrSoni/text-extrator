# This is a sample Python script.
from controller import tesseract_controller as tc
from app import app
from config import config

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(f"starting server on {config.server_port} context path '{config.request_prefix}'")
    print(f"starting server on 5001")
    app.run()
