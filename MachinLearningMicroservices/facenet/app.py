from cmath import log
from flask import Flask
from flask import request
from models.FacenetApp import FacenetApp
from models.Milvus import Milvus
import requests, random

import logging

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename = "app.log", level = logging.DEBUG)

app = Flask('IMG_EMBEDDINGS')
model = FacenetApp()
# milvus = Milvus()

@app.route("/",methods=['GET'])
def hello():
    return "FACENET is Up and Running" , 200

@app.route("/",methods=['POST'])
def img_embeddings():

    if request.method == "POST":
        try:
            image_link = request.json["imageUrl"]
        except:
            error = "unable to find imageUrl field"
            logging.error(error)
            return error, 500
        try:
            embeddings = model.predict(image_link)['data']
        except Exception as E:
            error = "An Exception Occured: {}".format(E)
            logging.error(error)
            return error, 500
        if len(embeddings) == 0:
            embeddings = [float(0.0) for i in range(128)]        

        #return {"embeddings":embeddings}
        try:
            idx = milvus.insert(embeddings,image_link)
        except Exception as E:
            idx = {}
            error = "Failed to Insert Data In Milvus {}".format(E)
            logging.error(error)
            return error,500
        return {"embeddings":embeddings}
    else:
        error = "Error 405: Method Not Allowed"
        logging.error(error)
        return error, 500

@app.route("/milvus/search",methods=['POST'])
def milvus_search():
    if request.method == "POST":
        try:
            image_link = request.json["imageUrl"]
        except:
            error = "unable to find imageUrl field"
            logging.error(error)
            return error, 500
        try:
            return {"data":milvus.search(model.predict(image_link)['data'])}, 200
        except Exception as E:
            error = "Failed to search image_link in elasticsearch {}".format(E)
            logging.error(error)
            return error, 500
    else:
        error = "Method Not Allowed"
        logging.error(error)
        return error,405

if __name__ == "__main__":
    app.run(debug=True)
