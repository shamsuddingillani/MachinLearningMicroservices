# Audio Transcription API

Transcription using Pyannote.audio and Deeppavlov

## Virtual Environment Creation 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the virtualenv package:

```bash
pip3 install virtualenv
```
Create the Environment for Deeppavlov:

```bash
virtualenv --python=/usr/bin/python3.6 transcription_env
```
Activate the virtual environment:

```bash
source transcription_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r requirements.txt
```
Download and install models:

```bash
python -m deeppavlov install asr_tts

python -m deeppavlov download asr_tts
```

Install flask:

```bash
pip install flask
```

## Usage

```python
import requests

#send post request on ip and port at the "diarization" route for Speaker Diarization from config
#audio_ftp_path is a single url sent as string
response = requests.post(ip:port+"/diarization", json={"url": audio_ftp_path})
print(response.json()["data"])


#send post request on ip and port at the "transcription" route for Audio Transcription from config
#chunk_ftp_path is a single url sent as string
response = requests.post(ip:port+"/transcription", json={"url": chunk_ftp_path})
print(response.json()["data"])
```

