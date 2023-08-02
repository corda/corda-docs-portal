---
aliases:
- /head/docker-image.html
- /HEAD/docker-image.html
- /docker-image.html
date: '2023-01-10'
menu:
  corda-community-4-11:
    identifier: corda-community-4-11-docker-image
    parent: corda-community-4-11-release-notes
    weight: 445
tags:
- docker
- image
title: Official Corda Docker Image
---
# Official Corda Docker image

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/u/corda). The [latest version](https://hub.docker.com/layers/corda/community/4.11-zulu-openjdk8/images/sha256-3d94ee8ab9e3ca91c40c0543291c4ac66c1787ed5b5b7c90c3ceadd1e4714168)
is `corda/community:4.11-zulu-openjdk8`.

## Prerequisites

* Install and enable Docker CE (Community Edition) and, optionally, Docker Compose. Docker CE is sufficient. Docker, Inc. publish installation instructions for all major operating systems:
  * [Docker CE](https://www.docker.com/community-edition)
  * [Docker Compose](https://docs.docker.com/compose/install/)
* Ensure you have a valid [node.conf file]({{< relref "corda-configuration-file.md" >}}) and set of certificates.

## Getting started

Use `docker run` to create a writable container layer over the Docker image, and then start it. The container process that runs is isolated: it has its own file system, its own networking, and its own isolated process tree, separate from the host.

* `docker run` is explained in full detail [in the documentation published by Docker, Inc.](https://docs.docker.com/engine/reference/commandline/run/)
* For information on using Docker for development purposes, see [Creating nodes locally]({{< relref "generating-a-node.md" >}})
* If you have already set up your node and want to learn how to use your code using Docker, see [Running nodes locally]({{< relref "running-a-node.md" >}}).
* To learn more about Docker deployments and how to deploy to a compatibility zone, see [Docker deployments]({{< relref "node-docker-deployments.md" >}}).

