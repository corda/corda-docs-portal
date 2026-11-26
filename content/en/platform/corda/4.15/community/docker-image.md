---
aliases:
- /head/docker-image.html
- /HEAD/docker-image.html
- /docker-image.html
date: '2023-01-10'
menu:
  corda-community-4-15:
    identifier: corda-community-4-15-docker-image
    parent: corda-community-4-15-operations
    weight: 350
tags:
- docker
- image
title: Official Corda Docker Image
---
# Official Corda Docker image

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/u/corda). The [latest version](https://hub.docker.com/layers/corda/open-source/4.15-zulu-openjdk/images/sha256-59242b2e090735738cfae076e32f8b96980d142084ad852eb4d89b3003012410)
is `corda/open-source:4.15-zulu-openjdk`.

## Prerequisites

* Install and enable `Docker` and `docker-compose`. Docker CE (Community Edition) is sufficient. Docker, Inc. publish installation instructions for all major operating systems:
  * [Docker CE](https://www.docker.com/community-edition)
  * [Docker Compose](https://docs.docker.com/compose/install/).
* Ensure you have a valid [node.conf file]({{< relref "node-database-tables.md" >}}) and set of certificates.

## Getting started

Use `docker run` to create a writeable container layer over the Docker image, and then start it. The container process that runs is isolated, it has its own file system, its own networking,
and its own isolated process tree, separate from the host.

* [Docker run](https://docs.docker.com/engine/reference/commandline/run/) is explained in full detail in the documentation published by Docker, Inc.
* For information on using docker for development purposes, visit the [creating a node]({{< relref "generating-a-node.md" >}}) page.
* If you have already set up your node and want to learn how to use your code using Docker, go to the [running a node locally]({{< relref "running-a-node.md" >}}) page.
* If you want to learn more about Docker deployments and how to deploy to a compatibility zone, go to the [Docker deployments]({{< relref "node-docker-deployments.md" >}}) page.

## Image security

The Corda Open Source Edition 4.15 Docker images are hardened. Their default behaviour is the same as in earlier releases, so existing deployments and scripts keep working.

### Base images

The base images are pinned by digest and use a JDK that fixes CVE-2026-114938: Azul Zulu 17.0.21.1 in the `zulu-openjdk` image, and Amazon Corretto 17.0.21 in the `amazonlinux2` image. The OS packages are upgraded when the image is built, and the setuid and setgid bits are removed.

### Non-root user

The node runs as the non-root `corda` user, with the fixed UID and GID `1000:1000`. The image declares the user by number, so Kubernetes `runAsNonRoot: true` works without `runAsUser`. The images support `--cap-drop ALL` and `--security-opt no-new-privileges`.

A folder that you mount from the host and that the node writes to, such as `persistence`, `artemis`, `certificates` or `logs`, must be writable by UID `1000`.

### File permissions

* The Corda binaries in `/opt/corda/bin` are owned by `root` and are read-only.
* The `persistence`, `artemis` and `certificates` folders have mode `750`, so only the `corda` user and group can read them.
* Corda is unpacked from `corda.jar` on every start, so changes to the unpacked copy do not survive a restart.

### Volumes

The images declare these folders as volumes:

* `/opt/corda/cordapps`
* `/opt/corda/persistence`
* `/opt/corda/artemis`
* `/opt/corda/certificates`
* `/opt/corda/drivers`
* `/opt/corda/logs`
* `/opt/corda/additional-node-infos`
* `/etc/corda`

The `cordapps`, `drivers` and configuration (`/etc/corda`) folders can be mounted read-only.

### Health check

The images have a Docker health check, which reports the container as healthy once the node listens on its RPC port. The node opens the port only after it has fully started, and the health check allows five minutes for that. The health check opens no connection to the node, so it adds nothing to the node or Artemis logs.

The health check uses port `10201` by default. If `rpcSettings.address` in the node configuration uses a different port, set the `CORDA_HEALTHCHECK_PORT` environment variable to that port. Otherwise the container is reported as unhealthy, which Docker Swarm acts on.

Kubernetes ignores the Docker health check. To use the same check there, call `/opt/corda/bin/healthcheck` from an `exec` probe, or use a `tcpSocket` probe on the RPC port.

### Limitations

A read-only root file system is not supported yet.

