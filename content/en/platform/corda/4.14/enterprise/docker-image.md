---
date: '2023-01-11'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-corda-nodes
tags:
- docker
- image
title: Official Corda Docker image
weight: 120
---

# Official Corda Docker image

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/u/corda). The [latest version](https://hub.docker.com/layers/corda/corda-enterprise/4.12-zulu-openjdk-alpine/images/sha256-cbe9ca47237b53cbc5c74322bb24a59687a0cfacb080fa0aa916be5218654223?context=explore) is `corda/corda-enterprise:4.12-zulu-openjdk-alpine`.

## Prerequisites

* Install and enable `Docker` and `docker-compose`. Docker CE (Community Edition) is sufficient. Docker, Inc. publish installation instructions for all major operating systems:
    * [Docker CE](https://www.docker.com/community-edition)
    * [Docker Compose](https://docs.docker.com/compose/install/).
* Ensure you have a valid [node.conf file]({{< relref "node/operating/node-database-tables.md" >}}) and set of certificates.

## Getting started

Use `docker run` to create a writeable container layer over the Docker image, and then start it. The container process that runs is isolated, it has its own file system, its own networking,
and its own isolated process tree, separate from the host.

* [Docker run](https://docs.docker.com/engine/reference/commandline/run/) is explained in full detail in the documentation published by Docker, Inc.
* For information on using Docker for development purposes, visit the [creating a node]({{< relref "node/deploy/generating-a-node.md" >}}) page.
* If you have already set up your node and want to learn how to use your code using Docker, go to the [running a node locally]({{< relref "node/deploy/running-a-node.md" >}}) page.
* If you want to learn more about Docker deployments and how to deploy to a compatibility zone, go to the [Docker deployments]({{< relref "node-docker-deployments.md" >}}) page.
