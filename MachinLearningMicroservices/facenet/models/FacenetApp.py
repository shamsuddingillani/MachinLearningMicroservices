from deepface import DeepFace
import cv2
import json
import requests
from PIL import Image
from deepface.commons import functions
from io import StringIO, BytesIO
import numpy as np

class FacenetApp:

    def __init__(self):
        self.model = DeepFace.build_model("Facenet")

    def transformImage(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        arr = np.uint8(img)
        return arr

    def getModel(self):
        return self.model

    def predict(self, image_link):
        try:
            target_img = functions.preprocess_face(self.transformImage(image_link), target_size=(160, 160),
                                                    enforce_detection=True, detector_backend='mtcnn')
            target_embedding = self.model.predict(target_img)[0].tolist()
            return {"data": target_embedding}
        except:
            print("* * * * * \n\n\n image does not include FACE")
            return {"data": []}