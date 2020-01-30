FROM ubuntu:latest

RUN apt-get update && \
    apt-get install curl git tar gzip -y

ARG HUGO_VERSION

RUN mkdir -p /usr/local/src && \
    cd /usr/local/src && \
    curl -L https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_Linux-64bit.tar.gz | tar -xz && \
    mv hugo /usr/local/bin/hugo && \
    addgroup --system --gid 1000 hugo && \
    adduser --system --ingroup hugo --home /src hugo

# Where our site will be 'loaded' into the image.
WORKDIR /src

# Expose the default hugo webserver port
EXPOSE 1313 
