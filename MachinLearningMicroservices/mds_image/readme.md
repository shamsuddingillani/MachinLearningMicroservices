# MDS image download

Image downloading using MDS

## Virtual Environment Creation 

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the virtualenv package:

```bash
pip3 install virtualenv
```
Create the Environment for MDS_image:

```bash
virtualenv --python=/usr/bin/python3.6 MDS_image_env
```
Activate the virtual environment:

```bash
source MDS_image_env/bin/activate
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

#send post request on ip and port for MDS_image from config
response = requests.post(ip:port, json={"imageUrl": image_link})

print(response.json()["FTP_link"])
```

