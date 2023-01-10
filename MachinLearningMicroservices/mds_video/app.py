from flask import Flask
from flask import request
from FtpApp import FtpApp
import os
from VDownloadApp import VDownloadApp
import redis
from datetime import datetime
from rq import Queue, Worker
import logging
from FtpApp import FtpApp
from kafka import KafkaProducer
import json

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename = "app.log", level = logging.DEBUG)




app = Flask('MDS_VIDEO')
r = redis.Redis(port=6000)

ftp = FtpApp()
ftp_cursor = ftp.getFTP()
node_ip=ftp.node_ip_ftp
mds_ip=ftp.node_ip_MDS_Video
mds_port=ftp.node_port_MDS_Video
kafka_broker = ftp.kafka_broker
producer = KafkaProducer(bootstrap_servers=[kafka_broker],
            value_serializer=lambda data: json.dumps(data).encode("utf-8"))

@app.route("/",methods=['POST'])
def MDS_video():

    if request.method == "POST":
        payload = request.get_json(force=True)
        kafka_id = ""
        if 'video_url' not in payload:
            error = "Manadatory `video_url` parameter missing"
            logging.error(error)
            return error
        
        if 'video_name' not in payload:
            video_name = str(datetime.now().timestamp()).replace('.','')
            warning = "Missing `video_name` adding arbitrary name to video `{}.mp4`".format(video_name)
            logging.warn(warning)
        else:
            video_name = request.json['video_name']
        
        video_url = request.json["video_url"]

        if "kafka_id" in payload:
            kafka_id = request.json['kafka_id']
            logging.info("Found Kakfa-id {} with url {}".format(kafka_id,video_url))

        downloader = VDownloadApp(node_ip=node_ip,mds_ip=mds_ip,mds_port=mds_port,kafka_id=kafka_id)
        downloader.set_video_ftp_url(video_name)
        q = Queue(connection=r,default_timeout="24h")
        job = q.enqueue(downloader.videoToFTP,video_url,video_name)
        logging.info("Queue `{}` with task id {} and final filename {}.mp4".format(video_url,job.id,video_name))
        return {"job_id":job.id,'url':downloader.get_video_ftp_url()}
    else:
        return "Error 405: Method Not Allowed"


@app.route('/save',methods=['POST'])
def save():
    if request.method == "POST":
        payload = request.get_json(force=True)
        if 'video_name' not in payload:
            error = "Failed to Download, Manadatory `video_name` parameter missing"
            logging.error(error)
            return error
        if 'video_ftp_url' not in payload:
            error = "Failed to Download, Manadatory `video_ftp_url` parameter missing"
            logging.error(error)
            return error
        video_name = payload['video_name']
        kafka_id = payload['kafka_id']
        video_ftp_url = payload['video_ftp_url']
        q = Queue('high', connection=r,default_timeout="24h")
        job = q.enqueue(save_to_ftp,video_name,kafka_id,video_ftp_url)
        logging.info("Save To FTP task Queued `{}` with task id {} and final filename {}.mp4".format(video_ftp_url,job.id,video_name))
    return 'Success', 200



def save_to_ftp(video_name,kafka_id,video_ftp_url):
    if not ftp.is_connected():
        ftp.retry_ftp_connection()
    try:
        local_downloaded_file = "TempVideoDir/"+video_name+".mp4"
        file = open(local_downloaded_file,'rb')   # "rb" (reading the local file in binary mode)
        logging.info("Saving {} to FTP ".format(local_downloaded_file))
        ftp_cursor.storbinary("STOR " + video_name + ".mp4", file)
        logging.info("Saved Video to FTP, Success ")
        print(kafka_broker)
        logging.info("Sending data to kafka...")
        logging.info("Checking connection status...")
        logging.info("Connection Status: {}".format(producer.bootstrap_connected()))
        value = {"url":video_ftp_url,"kafka-id":kafka_id}
        producer.send("completed_video_download",value=value)
        producer.flush()
        ftp_cursor.quit()
        file.close()            
        os.remove("TempVideoDir/"+video_name+".mp4")
        logging.error("Finished Downloading {}.mp4".format(video_name))
    except Exception as E:
        os.remove("TempVideoDir/"+video_name+".mp4")
        logging.error("something went wrong... Reason: {}".format(E))


if __name__ == "__main__":
    app.run(debug=True)