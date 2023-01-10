# Multilingual Embeddings for NLP

A multilingual embedding model is a powerful tool that encodes text from different languages into a shared embedding space, enabling it to be applied to a range of downstream tasks, like text classification, clustering, and others, while also leveraging semantic information for language understanding. 

## Update Distribution
```bash
apt-get update -y
apt-get install python3-dev -y
apt-get install gcc -y
```


## Virtual Environment Creation 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the virtualenv package:

```bash
pip3 install virtualenv
```
Create the Environment for Facenet:

```bash
virtualenv --python=/usr/bin/python3.6 labse_env
```
Activate the virtual environment:

```bash
source labse_env/bin/activate
```

Install CMake:

```bash
pip install cmake==3.18.4.post1
```


Install **Sentence Transformer** packages:

```bash
pip install sentence_transformers
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

#send post request on ip and port for Labse from config
response = requests.post(ip:port, json={"text": list_of_strings})
print(response.json()["data"])
```

