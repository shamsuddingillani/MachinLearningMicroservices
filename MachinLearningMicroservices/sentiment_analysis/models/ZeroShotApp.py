#Import Flask
from flask import json

#Import Libraries for your model
from transformers import pipeline

import logging
logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename = "app.log", level = logging.DEBUG)


class ZeroShotApp:

    def __init__(self):
        self.classifier = pipeline("zero-shot-classification",model="joeddav/xlm-roberta-large-xnli")

    def get_model(self):
        return self.classifier

    def predict(self, x,y):
        target_text = x
        candidate_labels = y
        
        try:
            result = self.classifier(target_text, candidate_labels)
            label = result["labels"][0]
            score = result["scores"][0]
            result
            
            data = {'label': label,'score': score}
            return json.dumps(data)
        except Exception as E:
            logging.error("Error 500:Internal Server Error")
            return str(E), 500
        
