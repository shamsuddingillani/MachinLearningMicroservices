from flask import Flask
from flask import request
from models.MDSImageApp import MDSImageApp
import requests
import logging

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s :: %(levelname)s :: %(message)s")

app = Flask("MDS")
model = MDSImageApp()

@app.route("/", methods = ["GET"])
def test():
    return "Test"



@app.route("/", methods=['POST'])
def image_to_FTP():
    if request.method == "POST":
        image_link = request.json["imageUrl"]
        #image_link = request.args.get("imageUrl")
        try:
            logging.info(f"Image{image_link} downloading to FTP started")
            response = model.imageToFTP(image_link)
        except Exception as E:
            print(E)
            response = {"url":image_link}
        logging.info(f"Image {image_link} stored to FTP successfully")
        return response
    else:
        logging.error("Error 405: Method not Allowed")
        return "Error 405: Method not Allowed"


if __name__ == "__main__":
    app.run(debug=True) 

  