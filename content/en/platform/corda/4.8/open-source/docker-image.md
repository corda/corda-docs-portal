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

* To install the Corda Docker image, first ensure both `Docker` and `docker-compose` are installed and enabled. Docker CE (Community Edition) is sufficient. Refer to [Docker CE documentation](https://www.docker.com/community-edition)
    and [Docker Compose documentation](https://docs.docker.com/compose/install/) for installation instructions for all major operating systems.
* The official Corda docker image can be found at the [Corda Docker hub](https://hub.docker.com/u/corda). The latest version is `corda/corda-zulu-java1.8-4.8.6` and is found [here](https://hub.docker.com/r/corda/corda-zulu-java1.8-4.8.6).
* Ensure you have a valid [node.conf file](../../../../../en/platform/corda/4.8/open-source/node-database-tables.md) and a valid set of certificates.
* Run the docker image using the [docker run command](https://docs.docker.com/engine/reference/commandline/run/).

