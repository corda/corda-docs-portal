---
aliases:
- /head/docker-image.html
- /HEAD/docker-image.html
- /docker-image.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-9-docker-image
    parent: corda-community-4-9-operations
    weight: 350
tags:
- docker
- image
title: Official Corda Docker Image
---
# Official Corda Docker image

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/u/corda). The [latest version](https://hub.docker.com/layers/community/corda/community/4.9.1-zulu-openjdk8/images/sha256-b7b536977dd1d13dc042c57299add348543158479063dbc1ad993373ebfa9f7b?context=explore)
is `corda/corda-enterprise:4.9.1-zulu-openjdk8-alpine`.

## Prerequisites

* Install and enable `Docker` and `docker-compose`. Docker CE (Community Edition) is sufficient. Docker, Inc. publish installation instructions for all major operating systems:
  * [Docker CE](https://www.docker.com/community-edition)
  * [Docker Compose](https://docs.docker.com/compose/install/).
* Ensure you have a valid [node.conf file](../../../../../en/platform/corda/4.9/community/node-database-tables.md) and set of certificates.

## Getting started

Use `docker run` to create a writeable container layer over the Docker image, and then start it. The container process that runs is isolated, it has its own file system, its own networking,
and its own isolated process tree, separate from the host.

* [Docker run](https://docs.docker.com/engine/reference/commandline/run/) is explained in full detail in the documentation published by Docker, Inc.
* For information on using docker for development purposes, visit the [creating a node](../../../../../en/platform/corda/4.9/enterprise/operations/deployment/generating-a-node.md) page.
* If you have already set up your node and want to learn how to use your code using Docker, go to the [running a node locally](../../../../../en/platform/corda/4.9/enterprise/operations/deployment/running-a-node.md) page.
* If you want to learn more about Docker deployments and how to deploy to a compatibility zone, go to the [Docker deployments](node-docker-deployments.md) page.

