from flask import Flask
from flask import request
from models.PyannoteAudioApp import PyannoteAudioApp
from models.BDownloaderApp import TestBDownloader
from deeppavlov import configs, build_model
from pydub import AudioSegment
import os
import json
import time

import logging
logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename = "app.log", level = logging.DEBUG)


app = Flask('DIARIZATION')

downloader = TestBDownloader()
diarization_model = PyannoteAudioApp()

@app.route("/",methods=['POST'])
def diarization():
    if request.method == "POST":

        input_url = request.json["url"] 
        if type(input_url)!= str:
            logging.error("Error 400: Bad Input")
            return "Error 400: Bad Input", 400
        else:
            file_name = str((input_url.split("/")[-1]).split(".")[0]) + ".wav"
            start_time = time.time()
            temp_path = "Temp/"

            downloader.test_bdownloader_downloads(input_url, file_name)
            print("Time taken for downloading: ", time.time()-start_time)
            start_time = time.time()
            path = os.path.join(temp_path, file_name)
            output = diarization_model.predict(path)
            print("Time taken for diarization: ", time.time()-start_time)
            
            os.remove(os.path.join(temp_path, file_name)) 
            return output
    else:
        logging.error("Error 405: Method Not Allowed")
        return "Error 405: Method Not Allowed", 405




if __name__ == "__main__":
    app.run(debug=True)
