ARG REGISTRY=library
FROM ${REGISTRY}/ubuntu:latest

RUN apt-get update && \
    apt-get install curl git tar gzip unzip jq -y
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs

ARG HUGO_VERSION

RUN mkdir -p /tmp/hugo && cd /tmp/hugo && \
    curl -L https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_Linux-64bit.tar.gz | tar -xz && \
    install -o root -g root -m 755 -t /usr/local/bin hugo && \
    rm -rf /tmp/hugo && \
    addgroup --system --gid 1000 hugo && \
    adduser --system --ingroup hugo --home /src hugo

ARG S3DEPLOY_VERSION

RUN mkdir -p /tmp/s3deploy && cd /tmp/s3deploy && \
    curl -L https://github.com/bep/s3deploy/releases/download/v${S3DEPLOY_VERSION}/s3deploy_${S3DEPLOY_VERSION}_Linux-64bit.tar.gz | tar -xz && \
    install -o root -g root -m 755 -t /usr/local/bin s3deploy && \
    rm -rf /tmp/s3deploy

RUN mkdir -p /tmp/awscli && cd /tmp/awscli && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf /tmp/awscli

# Where our site will be 'loaded' into the image.
WORKDIR /src

# Expose the default hugo webserver port
EXPOSE 1313
