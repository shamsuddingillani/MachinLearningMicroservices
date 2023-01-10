import numpy as np
from ftplib import FTP, error_perm
import requests
import io
from PIL import Image
import requests
import datetime
import configparser
from pywebhdfs.webhdfs import PyWebHdfsClient

import logging

logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename="mds_image_app.log", level=logging.DEBUG, format="%(asctime)s :: %(levelname)s :: %(message)s")


class MDSImageApp:
    
    def __init__(self):

        self.parse_config = configparser.ConfigParser()
        self.parse_config.read("./config.ini")
        self.host_server = str(self.parse_config.get('HDFS', 'ip')).strip()
        self.port_server = int(self.parse_config.get('HDFS', 'port'))

        self.hdfs = PyWebHdfsClient(host=self.host_server,port=self.port_server, user_name='hdfs')
        self.conf_file = 'user/config/config.ini'
        
        self.node_ip_ftp = None
        self.node_port_ftp = None
        self.auth_user_ftp  = None
        self.auth_pass_ftp  = None
        

        # Reading in Bytes, decode to String
        self.conf_read = self.hdfs.read_file(self.conf_file).decode("utf-8") 
        self.buf = io.StringIO(self.conf_read)
        self.parse_config.readfp(self.buf)
        
        self.node_ip_ftp = str(self.parse_config.get('FTP', 'host')).strip()
        self.node_port_ftp = int(self.parse_config.get('FTP', 'port'))
        self.auth_user_ftp = str(self.parse_config.get('FTP', 'username')).strip()
        self.auth_pass_ftp = str(self.parse_config.get('FTP', 'password')).strip()
        
        self.ftp = FTP(host=self.node_ip_ftp,user=self.auth_user_ftp,passwd=self.auth_pass_ftp)
        self.change_to_video_download_dir()

    def change_to_video_download_dir(self):
        video_download_path = '/MDS_Downloads/MDS_Image'
        try:
            if self.ftp.pwd() != video_download_path:
                self.ftp.cwd(video_download_path)
        except Exception as E:
            try:
                self.ftp.cwd('/')
                for folder in video_download_path.split('/')[1:]:
                    self.chdir(folder)
            except Exception as E:
                raise Exception(E)            

    def getFTP(self):
        return self.ftp
    
    def connect(self):
        try:
            logging.info("Connecting FTP")
            self.ftp.connect(self.node_ip_ftp, self.node_port_ftp)
            logging.info("FTP Connection successful")
            return True
        except Exception as e:
            logging.error("FTP connection failed",str(e))
            print(e)
            return False
    
    def retry_connect(self):
        for i in range(5):
            if self.ftp.connect(self.node_ip_ftp, self.node_port_ftp):
                break   
        return True


    def login(self):
        try:
            logging.info("Logging In FTP")
            self.ftp.login(user=self.auth_user_ftp, passwd=self.auth_pass_ftp)
            logging.info("FTP Login Successful")
            return True
        except Exception as e:
            logging.error("FTP login failed",str(e))
            print(e)
            return False
        
    def directory_exists(self,dir):
        filelist = []
        self.ftp.retrlines('LIST', filelist.append)
        #print(filelist)
        for f in filelist:
            if f.split()[-1] == dir and f.upper().startswith('D'):
                return True
        return False

    def chdir(self,dir):        
        if self.directory_exists(dir) is False:
            logging.info("Creating directory on FTP")
            self.ftp.mkd(dir)
            logging.info("Directory created")
        logging.info("Changing current directory")
        self.ftp.cwd(dir)
        logging.info("Current directory changed")

    def transformImage(self, url):
        try:
            response = requests.get(url)
            img = Image.open(io.BytesIO(response.content))
            arr = np.uint8(img)
            logging.info("Transforming image")
            return arr
        except Exception as e:
            logging.error("Error! 404 Url doesnot exist",str(e))
            print("Error! 404")
            print(url, "Url does not exist")
            return False

    def imageToFTP(self, image_link):
        
        connect_ftp = self.connect()
        if connect_ftp == False:
            self.retry_connect()
        print("Attempting Login...")
        self.login()
        self.change_to_video_download_dir()
        print(self.ftp.pwd())
        image = self.transformImage(image_link)
        if image is not False:
            PIL_image = Image.fromarray(np.uint8(image)).convert('RGB')
            temp = io.BytesIO() # This is a file objec
            PIL_image.save(temp, format="jpeg") # Save the content to temp
            temp1 = temp.getvalue() # To print bytes string
            temp.seek(0) # Return the BytesIO's file pointer to the beginning of the file
            print("Creating Link of Image")
            time = datetime.datetime.now().today()
            date_time = time.strftime("%d%m%Y-%H%M%S")
            img_name = "Img"+date_time +".jpeg"

            # Store image to FTP Server
            print("SAVING TO FTP")
            logging.info("Saving Image to FTP")
            self.ftp.storbinary("STOR " + img_name, temp)

            FTP_URL = f"http://{self.node_ip_ftp}/osint_system/media_files/MDS_Downloads/MDS_Image/"
            FTP_Img =  FTP_URL + img_name
            print("File saved to FTP SUCCESSFULLY",FTP_Img)
            logging.info(f"Image saved to FTP successfully ==> {FTP_Img}")
            return {"url" :FTP_Img}

        else:
            logging.error(f"Error! 404 Url doesnot Exist{image_link}")
            message = "Error! 404 Url doesnot Exist"
            print(message)
            return {"url": image_link}
        
      
       
  


   