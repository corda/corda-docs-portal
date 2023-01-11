---
date: '2023-01-11'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-10-corda-nodes
tags:
- docker
- image
title: Official Corda Docker image
weight: 120
---

# Official Corda Docker image

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/u/corda). The [latest version](https://hub.docker.com/layers/corda/corda-enterprise/4.10-zulu-openjdk8-alpine/images/sha256-c41b5876238c7d7904d2e5f737a9ebdfcd1d65842a8318c83ee35d550235cb2e)
is `corda/corda-enterprise:4.10-zulu-openjdk8-alpine`.

## Prerequisites

* Install and enable `Docker` and `docker-compose`. Docker CE (Community Edition) is sufficient. Docker, Inc. publish installation instructions for all major operating systems:
    * [Docker CE](https://www.docker.com/community-edition)
    * [Docker Compose](https://docs.docker.com/compose/install/).
* Ensure you have a valid [node.conf file](node/operating/node-database-tables.md) and set of certificates.

## Getting started

Use `docker run` to create a writeable container layer over the Docker image, and then start it. The container process that runs is isolated, it has its own file system, its own networking,
and its own isolated process tree, separate from the host.

* [Docker run](https://docs.docker.com/engine/reference/commandline/run/) is explained in full detail in the documentation published by Docker, Inc.
* For information on using Docker for development purposes, visit the [creating a node](operations/deployment/generating-a-node.md) page.
* If you have already set up your node and want to learn how to use your code using Docker, go to the [running a node locally](operations/deployment/running-a-node.md) page.
* If you want to learn more about Docker deployments and how to deploy to a compatibility zone, go to the [Docker deployments](node-docker-deployments.md) page.
