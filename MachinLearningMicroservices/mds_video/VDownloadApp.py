import os
import logging
import datetime
from threading import local
import pandas as pd
import subprocess
import json
import logging
import requests

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename = "app.log", level = logging.DEBUG)

class VDownloadApp:

    def __init__(self,node_ip,mds_ip,mds_port,kafka_id):
        self.base_url = "http://"+node_ip+"/osint_system/media_files/MDS_Downloads/MDS_Video/"
        self.video_ftp_url = None
        self.mds_ip = mds_ip
        self.mds_port = mds_port
        self.kafka_id = kafka_id


    def set_video_ftp_url(self,video_name):
        """
        @return String  
        """
        self.video_ftp_url = self.base_url + str(video_name)+".mp4"
        return self.video_ftp_url

    def get_video_ftp_url(self):
        """
        @return String 
        """
        return self.video_ftp_url

    def videoToFTP(self, video_url, video_name):
        
        logging.info('Started')
        self.ctime = str(datetime.datetime.now())
        logging.info("Time: "+str(self.ctime))

        # Create Temp Dir
        if os.path.isdir("TempVideoDir") == False:
            os.mkdir("TempVideoDir")
            os.chmod("TempVideoDir",0o777)

        results = []
        errors = None

        # Download video before accessign FTP, to overcome FTP timeout error
        video_check = self.downloadVideo(video_url,video_name)
                
        if video_check == True:
            url = "http://{}:{}/save".format(self.mds_ip,self.mds_port)
            print(url)
            requests.post(url,data=json.dumps({
                "video_name":video_name,
                "video_ftp_url":self.video_ftp_url,
                "kafka_id":self.kafka_id
            }),timeout=5000)
        else:
            # Internet Disconnected
            logging.error("something went wrong")
            logging.error(str(video_url)) # here it will ge getting error 
            logging.error("Video URL: "+str(video_url))
            logging.error('Finished with error(s)')

        # row_data= {'Failed_URL': video_url, 'File_Name': video_name, 'Retried_Times': str(0)}
        # failed_data_df = self.failed_data.copy()
        # failed_data_df_updated = self.retryFailedURL(row_data, failed_data_df)
        # operation = self.downloadSub()
 

    
    def downloadVideo(self, video_url, video_name):
        output_filename = "TempVideoDir/"+video_name+".mp4"
        # output_filename = '\"{}\"'.format(output_filename)
        cmd = ['yt-dlp',video_url,'--external-downloader','aria2c',"-S","res,ext:mp4:m4a","--recode","mp4",'-o',output_filename]
        
        process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        logging.info("Downloading started : {}".format(video_url))
        # process.wait()
        #process = await asyncio.create_subprocess_exec(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        # Status
        logging.info("Started Downloading: {}, pid={}".format(video_url, process.pid))

        # Wait for the subprocess to finish
        stdout, stderr = process.communicate()
        download_state = True
        # Progress
        if process.returncode == 0:
            stdout = stdout.decode('utf-8').strip().replace('\n',' ')
            logging.info(
                "Done: {}, pid={}, output: {}".format(video_url, process.pid, stdout)
            )
            subprocess.Popen(["chmod", "777",output_filename])
            return download_state
        else:
            download_state = False
            stderr = stderr.decode("utf-8").strip().replace('\n','') #converted to string
            if 'Could not send HEAD request ' in stderr:
                logging.error("Wrong Url Error {}, pid={}, output: {}".format(video_url, process.pid, stderr))
            elif 'gaierror' in stderr and 'Could not send HEAD request' not in stderr:
                logging.error("Internet Unavailable {}, pid={}, output: {}".format(video_url, process.pid, stderr))
            elif 'HTTP Error 404: Not Found' in stderr:
                logging.error("URL Unavailable Error {}, pid={}, output: {}".format(video_url, process.pid, stderr))
            else:
                # self.retryFailedURL(video_url, video_name)
                logging.warn(
                    "Retrying URL: An Exception Occured: {}, pid={}, output: {}".format(video_url, process.pid, stderr)
                )
        return download_state        


    

    