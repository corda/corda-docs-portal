ARG REGISTRY=library
FROM ${REGISTRY}/ubuntu:latest

RUN apt-get update && \
    apt-get install curl git tar gzip unzip jq -y
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs

ARG MUFFET_VERSION

RUN mkdir -p /tmp/muffet && cd /tmp/muffet \
 && curl -LO "https://github.com/raviqqe/muffet/releases/download/v${MUFFET_VERSION}/muffet_${MUFFET_VERSION}_Linux_x86_64.tar.gz" \
 && tar zxfv "muffet_${MUFFET_VERSION}_Linux_x86_64.tar.gz" \
 && install -o root -g root -m 0755 muffet /usr/local/bin/muffet \
 && rm -rf /tmp/muffet

ARG CADDY_VERSION

RUN mkdir -p /tmp/caddy && cd /tmp/caddy \
 && curl -LO "https://github.com/caddyserver/caddy/releases/download/v${CADDY_VERSION}/caddy_${CADDY_VERSION}_linux_amd64.tar.gz" \
 && tar zxfv "caddy_${CADDY_VERSION}_linux_amd64.tar.gz" \
 && install -o root -g root -m 0755 caddy /usr/local/bin/caddy \
 && rm -rf /tmp/caddy

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
