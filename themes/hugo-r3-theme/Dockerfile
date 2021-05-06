FROM ubuntu:latest

RUN apt-get update  && \
    apt-get install curl git tar gzip gnupg -y
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt install yarn -y
# Where our site will be 'loaded' into the image.
WORKDIR /src
