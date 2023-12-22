---
aliases:
- /head/docker-image.html
- /HEAD/docker-image.html
- /docker-image.html
date: '2023-01-10'
menu:
  corda-community-4-12:
    identifier: corda-community-4-12-docker-image
    parent: corda-community-4-12-operations
    weight: 350
tags:
- docker
- image
title: Official Corda Docker Image
---
# Official Corda Docker image

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/u/corda). The [latest version](https://hub.docker.com/layers/corda/community/4.12-zulu-openjdk8/images/sha256-8f86f460a4f8b77524e0d7c2075636a39642dd4d21f413f370aa2d0cbfafe2f5?context=explore)
is `corda/community:4.12-zulu-openjdk8`.

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

