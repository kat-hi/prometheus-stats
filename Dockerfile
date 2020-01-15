FROM ubuntu:18.04

RUN apt-get update -y

RUN apt install python3.7 -y 

RUN apt install python-pip -y

RUN apt install curl -y

RUN apt install inetutils-ping
 
RUN apt install vim -y

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD flask run 
