FROM python:3-stretch

RUN apt-get update \
    && apt-get -y install python3-pip

WORKDIR /src
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
