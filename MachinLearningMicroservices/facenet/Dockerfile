# syntax=docker/dockerfile:1

FROM python:3.6-slim-buster

WORKDIR /frs

COPY requirements.txt requirements.txt
RUN apt-get update -y
RUN apt-get install python3-dev -y
RUN apt-get install gcc -y
RUN pip3 install cmake==3.18.4.post1
RUN pip3 install torch==1.9.1+cpu torchvision==0.10.1+cpu torchaudio==0.9.1 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install "opencv-python-headless<4.3"
RUN pip3 install -r requirements.txt

COPY . .


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=7003"]
