import torch
import numpy as np
from pyannote.core import Annotation

import logging
logger = logging.getLogger(__name__)
if (logger.hasHandlers()):
    logger.handlers.clear()
logging.basicConfig(filename = "app.log", level = logging.DEBUG)


class PyannoteAudioApp:

    def __init__(self):
        self.model = torch.hub.load("pyannote/pyannote-audio", "dia")


    def get_model(self):
        return self.model

    def predict(self, path):
        
        try: 
            diarization = self.model({"audio": path})
            d_labels = []
            for speech_turn, track, speaker in diarization.itertracks(yield_label=True):
                start = speech_turn.start
                end = speech_turn.end
                d_labels.append((speaker, start, end))
            return {"data": d_labels}
        except Exception as E:
            logging.error("Error 500: Internal Server Error : %s", str(E))
            return str(E), 500
    