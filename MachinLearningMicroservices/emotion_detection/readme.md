# Emotion Detection

Emotion Detection using zero shot detection

## Virtual Environment Creation 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the virtualenv package:

```bash
pip3 install virtualenv

#if doesnot work then use
#sudo apt-get install python-virtualenv
```
Create the Environment for Emotion Detection:

```bash
virtualenv --python=/usr/bin/python3.6 emotion_env
```
Activate the virtual environment:

```bash
source emotion_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r zero_shot_requirements.txt
```

Install flask:

```bash
pip install flask
```

## Usage

```python
import requests

#send post request on ip and port for Emotion Detection from config
response = requests.post("http://127.0.0.1:5000/",json={"text":target_text})

print(response.json()["label"])
print(response.json()["score"])

#labels are ["Joy", "Disgust","Anger","Sad","Fear","Neutral"]
#label = label with top score
#score = score of top label
```

