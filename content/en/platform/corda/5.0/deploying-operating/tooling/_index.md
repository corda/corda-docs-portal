---
date: '2023-05-10'
title: "Cluster Operator Tooling"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-cluster-tooling
    parent: corda5-cluster
    weight: 2000
section_menu: corda5
---
This section outlines the tools needed by a Cluster Operator to deploy and operate Corda.
There are additional tools which may be required depending on the installation approach taken.

## Kubernetes CLI

Corda 5 is deployed to Kubernetes and to interact with the cluster, the Cluster Operator requires the Kubernetes client kubectl.
The [Kubernetes documentation](https://kubernetes.io/docs/tasks/tools/#kubectl) contains details on how to install kubectl. You should use a version of the CLI that is within one minor version
of the Kubernetes cluster that you are using, for example, if your cluster is v1.23, your CLI should be v1.22, v1.23, or v1.24.

## Helm CLI

Corda 5 is deployed as a Helm chart. To perform the installation, the Cluster Operator requires the Helm CLI.
The [Helm documentation](https://helm.sh/docs/intro/install/) contains details on how to install Helm. The Helm version should be v3.9.4 or newer.

## Corda CLI

The Cluster Operator will require the Corda CLI if they intend to [manually bootstrap](../deploying/bootstrapping.md) Kafka and PostgreSQL.
See the documentation on [installing the Corda CLI](installing-corda-cli.md).

## curl

Examples in this documentation for Linux and macOS use the curl CLI to interact with HTTP endpoints.
See the [curl documentation](https://everything.curl.dev/get) for details on how to install curl.
Alternatives may be used if desired. On Windows, PowerShell contains native support for HTTP calls.

## jq
Examples in this documentation for Linux and macOS use the jq CLI to parse content out of JSON responses received from the Corda REST API.
See the [jq documentation](https://stedolan.github.io/jq/download/) for details on how to install jq.
Alternatives may be used if desired. On Windows, PowerShell contains native support for parsing JSON.

## PostgreSQL Client
The Cluster Operator, or their database administrator, will require a PostgreSQL client if they intend to [manually bootstrap](../deploying/bootstrapping.md) PostgreSQL.
Examples in this documentation use the psql CLI. See the [Postgres documentation](https://www.postgresql.org/download/) for details on how to download Postgres.
Alternatives may be used if desired.

## Kafka Client

The Cluster Operator, or their Kafka administrator, may require a Kafka client if they intend to [manually bootstrap](../deploying/bootstrapping.md) Kafka.
Examples in this documentation use the scripts packaged with Kafka.
See the [Kafka documentation](https://kafka.apache.org/downloads) for details on how to download Kafka. Alternatives may be used if desired.
