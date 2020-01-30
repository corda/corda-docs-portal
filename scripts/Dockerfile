# Oh no, another docker file.
FROM python:3-buster

RUN apt-get update \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && pip install wheel

ENV PATH="/opt/:${PATH}"
WORKDIR /opt/

#  Run dockerfile from outside this folder
COPY scripts/requirements.txt requirements.txt
RUN pip install -r requirements.txt
