# LTS Video

## Virtual Environment Creation 

```
Activate the virtual environment:

```bash
source detectron_env/bin/activate
```

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

