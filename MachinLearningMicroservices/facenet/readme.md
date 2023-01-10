# Image Embeddings with Facenet

Image Embeddings for Facial Recognition using Facenet

## Virtual Environment Creation 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the virtualenv package:

```bash
pip3 install virtualenv
```
Create the Environment for Facenet:

```bash
virtualenv --python=/usr/bin/python3.6 facenet_env
```
Activate the virtual environment:

```bash
source facenet_env/bin/activate
```

Install CMake:

```bash
pip install cmake==3.18.4.post1
```


Install torch, torchvision and torch audio:

```bash
pip install torch==1.9.1+cpu torchvision==0.10.1+cpu torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
```


Install the required packages from requirements.txt:

```bash
pip install -r facenet_requirements.txt
```
Install opencv:

```bash
pip install "opencv-python-headless<4.3"
```

Install flask:

```bash
pip install flask
```

## Usage

```python
import requests

#send post request on ip and port for FR from config
response = requests.post(ip:port, json={"imageUrl": single_image_url_string})

print(response.json()["data"])
```

