# UTS Video

## Virtual Environment Creation 

```
Activate the virtual environment:

```bash
source detectron_env/bin/activate
```

sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp


pip install pywebhdfs

pip install pandas

pip install flask

pip install gunicorn


```

## Usage

```python
import requests

response = requests.post(ip:port, json={"imageUrl": image_url})

print(response.json()["data"])
```

