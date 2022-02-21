---
aliases:
- /head/docker-image.html
- /HEAD/docker-image.html
- /docker-image.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-docker-image
    parent: corda-os-4-8-operations
    weight: 350
tags:
- docker
- image
title: Official Corda Docker Image
---


# Official Corda Docker Image

The official Corda Docker image can be found at the [Corda Docker hub](https://hub.docker.com/u/corda). The latest version is `corda/corda-zulu-java1.8-4.8.6` and is found [here](https://hub.docker.com/r/corda/corda-zulu-java1.8-4.8.6).

## Prerequisites

* Both `Docker` and `docker-compose` must be installed and enabled. Docker CE (Community Edition) is sufficient. Refer to [Docker CE documentation](https://www.docker.com/community-edition)
    and [Docker Compose documentation](https://docs.docker.com/compose/install/) for installation instructions for all major operating systems.
* Ensure you have a valid [node.conf file](../../../../../en/platform/corda/4.8/open-source/node-database-tables.md) and a valid set of certificates.
* Use the `docker run` command to run the Docker Image. [Docker run](https://docs.docker.com/engine/reference/commandline/run/) is explained in more detail in the Docker documentation.

## Getting started

* For information on using docker for development purposes, visit the [creating a node](generating-a-node.md) page.
* If you've already set up your node and want to learn how to use your code using docker, go to the [running a node locally](running-a-node.md) page.
* If you want to learn more about docker deployments and how to deploy to a compatibility zone, go to the [docker deployments](node-docker-deployments.md) page.
