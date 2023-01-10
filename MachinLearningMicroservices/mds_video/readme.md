# MDS Video

## Virtual Environment Creation 


please use the environment of detectron2 (Already created for OJBD) as i have tested them with the same environment. These packages don't have any conflicts with other packages.

```
Activate the virtual environment:

```bash
source detectron_env/bin/activate
```


pip install pywebhdfs

pip install vidgear


```

## Usage

```python
import requests

#send post request on ip and port for OBJD from config
response = requests.post(ip:port, json={"imageUrl": image_url})

print(response.json()["data"])
```

