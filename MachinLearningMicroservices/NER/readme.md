# NER with Deeppavlov

NER using Deeppavlov Multi BERT

## Virtual Environment Creation 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the virtualenv package:

```bash
pip3 install virtualenv
```
Create the Environment for Deeppavlov:

```bash
virtualenv --python=/usr/bin/python3.6 ner_env
```
Activate the virtual environment:

```bash
source ner_env/bin/activate
```
Install the required packages from requirements.txt:

```bash
pip install -r requirements.txt
```
Install flask:

```bash
pip install flask
```

## Usage

```python
import requests

#send post request on ip and port for NER from config
response = requests.post(ip:port, json={"text": list_of_strings})

print(response.json()["data"])
```

