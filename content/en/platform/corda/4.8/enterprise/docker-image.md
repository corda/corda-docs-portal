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

The official Corda Docker image is found at the [Corda Docker hub](https://hub.docker.com/u/corda). The [latest version](https://hub.docker.com/layers/corda/corda-enterprise/4.9.2-zulu-openjdk8-alpine/images/sha256-c97af2e8f2fdbf87bfea9bab67a10aad9f65d5c232f0d512e55905fac8488a76?context=explore)
is `corda/corda-enterprise:4.9.2-zulu-openjdk8-alpine`.

## Prerequisites

* Install and enable `Docker` and `docker-compose`. Docker CE (Community Edition) is sufficient. Docker, Inc. publish installation instructions for all major operating systems:
  * [Docker CE](https://www.docker.com/community-edition)
  * [Docker Compose](https://docs.docker.com/compose/install/).
* Ensure you have a valid [node.conf file](../../../../../en/platform/corda/4.8/open-source/node-database-tables.md) and set of certificates.

## Getting started

Use `docker run` to create a writeable container layer over the Docker image, and then start it. The container process that runs is isolated, it has its own file system, its own networking,
and its own isolated process tree, separate from the host.

* [Docker run](https://docs.docker.com/engine/reference/commandline/run/) is explained in full detail in the documentation published by Docker, Inc.
* For information on using docker for development purposes, visit the [creating a node](../../../../../en/platform/corda/4.8/enterprise/operations/deployment/generating-a-node.md) page.
* If you have already set up your node and want to learn how to use your code using Docker, go to the [running a node locally](../../../../../en/platform/corda/4.8/enterprise/operations/deployment/running-a-node.md) page.
* If you want to learn more about Docker deployments and how to deploy to a compatibility zone, go to the [Docker deployments](node-docker-deployments.md) page.


