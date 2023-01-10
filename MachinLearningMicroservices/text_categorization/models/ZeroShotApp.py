#Import Flask
from flask import json

#Import Libraries for your model
from transformers import pipeline
import string

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

    def predict(self, x):
        target_text = str(x)
        predictions = []
        confidence = []
        res = sum([i.strip(string.punctuation).isalpha() for i in target_text.split()])
        
        try:
            if res > 8:
        
                ######### SaudiArabia #############
            
                candidate_labels = ["Against SaudiArabia","Supports SaudiArabia","Against Mohammed bin Salman","Supports Mohammed bin Salman"]
                result = self.classifier(target_text, candidate_labels)
                label = result["labels"][0]
                score = result["scores"][0]
                
                if score > 0.5:
                    
                    if label == "Against Mohammed bin Salman":
                        label = "Against SaudiArabia"
                    elif label == "Supports Mohammed bin Salman":
                        label = "Supports SaudiArabia"

                    if label == "Against SaudiArabia":
                        label = "Anti-State"
                    elif label == "Supports SaudiArabia":
                        label = "Pro-State"
                    
                    predictions.append(label)
                    confidence.append(score)
                else:
                    pass
                
                ######### Sexual-Abusive #############
                
                candidate_labels = ["Sexual-Abusive","Non Abusive"]
                result = self.classifier(target_text, candidate_labels)
                label = result["labels"][0]
                score = result["scores"][0]
                if score > 0.7:
                    predictions.append(label)
                    confidence.append(score)
                else:
                    pass
                
                ######### Offence #############
                
                candidate_labels = ["Offence","Peaceful"]
                result = self.classifier(target_text, candidate_labels)
                label = result["labels"][0]
                score = result["scores"][0]
                if score > 0.7:
                    predictions.append(label)
                    confidence.append(score)
                else:
                    pass
                
                ######### Judiciary #############
                
                candidate_labels = ["Against Judiciary","Supports Judiciary"]
                result = self.classifier(target_text, candidate_labels)
                label = result["labels"][0]
                score = result["scores"][0]
                if score > 0.7:
                    
                    predictions.append(label)
                    confidence.append(score)
                else:
                    pass


                ######### Islam #############
                
                candidate_labels = ["Against Islam","Supports Islam"]
                result = self.classifier(target_text, candidate_labels)
                label = result["labels"][0]
                score = result["scores"][0]
                if score > 0.7:
                    
                    predictions.append(label)
                    confidence.append(score)
                else:
                    pass

                if not predictions:
                    predictions.append("Other")
                    confidence.append("0.0")
                else:
                    pass
                
            else:
                predictions.append("Not enough Data")
                confidence.append("0.0")

               
            data = {"confidence": confidence, "predictions": predictions}
            return json.dumps(data)    
        except Exception as E:
            logging.error("Error 500:Internal Server Error")
            return str(E), 500
        
