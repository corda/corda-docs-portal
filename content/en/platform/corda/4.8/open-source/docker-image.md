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

* You need both `Docker` and `docker-compose` installed and enabled to use this method. Docker CE (Community Edition) is sufficient. Please refer to [Docker CE documentation](https://www.docker.com/community-edition)
    and [Docker Compose documentation](https://docs.docker.com/compose/install/) for installation instructions for all
    major operating systems.
* The official Corda docker image can be found at the [Corda Docker hub](https://hub.docker.com/u/corda). The latest version is `corda/corda-zulu-java1.8-4.8.6` and is found [here](https://hub.docker.com/r/corda/corda-zulu-java1.8-4.8.6).
* Run the docker image using the [`docker run` command](https://docs.docker.com/engine/reference/commandline/run/).

{{< note >}}
Before running any Corda Enterprise Docker images, you must accept the license agreement and indicate that you have done this by setting the environment variable `ACCEPT_LICENSE` to `YES` or `Y` on your machine. If you do not do this, none of the Docker containers will start.

As an alternative, you can specify this parameter when running the `docker-compose up` command, for example:
`ACCEPT_LICENSE=Y docker-compose up`
{{< /note >}}
