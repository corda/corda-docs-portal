---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-corda-nodes
tags:
- docker
- image
title: Official Corda Docker image
weight: 120
---


# Official Corda Docker image

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/u/corda). The [latest version](https://hub.docker.com/r/corda/corda-zulu-java1.8-4.8.6) is `corda/corda-zulu-java1.8-4.8.6`.

## Prerequisites

* `Docker` and `docker-compose` must be installed and enabled.
  * Docker CE (Community Edition) is sufficient. Installation instructions for all major operating systems are found in both the [Docker CE documentation](https://www.docker.com/community-edition)
    and [Docker Compose documentation](https://docs.docker.com/compose/install/).
* Ensure you have a valid [node.conf file](../../../../../en/platform/corda/4.8/open-source/node-database-tables.md) and a valid set of certificates.

## Getting started

The `docker run` command runs the Docker image. [Docker run](https://docs.docker.com/engine/reference/commandline/run/) is explained in more detail in the Docker documentation. Once `docker run` is used,
the container process that runs is isolated in that it has its own file system, its own networking, and its own isolated process tree separate from the host.

* For information on using docker for development purposes, visit the [creating a node](../../../../../en/platform/corda/4.8/enterprise/operations/deployment/generating-a-node.md) page.
* If you've already set up your node and want to learn how to use your code using docker, go to the [running a node locally](../../../../../en/platform/corda/4.8/enterprise/operations/deployment/running-a-node.md) page.
* If you want to learn more about docker deployments and how to deploy to a compatibility zone, go to the [docker deployments](node-docker-deployments.md) page.

