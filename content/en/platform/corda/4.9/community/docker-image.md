---
aliases:
- /head/docker-image.html
- /HEAD/docker-image.html
- /docker-image.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-9:
    identifier: corda-community-4-9-docker-image
    parent: corda-community-4-9-operations
    weight: 350
tags:
- docker
- image
title: Official Corda Docker Image
---

# Official Corda Docker image

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/repository/docker/corda/community). 

## Prerequisites

* `Docker` and `docker-compose` must be installed and enabled.
  * Docker CE (Community Edition) is sufficient. Installation instructions for all major operating systems are found in both the [Docker CE documentation](https://www.docker.com/community-edition)
    and [Docker Compose documentation](https://docs.docker.com/compose/install/).
* Ensure you have a valid [node.conf file](../../../../../en/platform/corda/4.9/community/node-database-tables.md) and a valid set of certificates.

## Getting started

The `docker run` command runs the Docker image. [Docker run](https://docs.docker.com/engine/reference/commandline/run/) is explained in more detail in the Docker documentation. Once `docker run` is used,
the container process that runs is isolated in that it has its own file system, its own networking, and its own isolated process tree separate from the host.

* For information on using docker for development purposes, visit the [creating a node](generating-a-node.md) page.
* If you've already set up your node and want to learn how to use your code using docker, go to the [running a node locally](running-a-node.md) page.
* If you want to learn more about docker deployments and how to deploy to a compatibility zone, go to the [docker deployments](node-docker-deployments.md) page.
