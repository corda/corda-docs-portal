---
description: "Learn how to upgrade your cluster from Corda 5.2 to Corda 5.2.1."
date: '2024-05-15'
title: "Upgrading from 5.2 to 5.2.1"
menu:
  corda52:
    parent: corda52-cluster-deploy
    identifier: corda52-cluster-upgrade521
    weight: 5000
---
# Upgrading from 5.2 to 5.2.1

This section describes how to upgrade a Corda cluster from 5.2 to 5.2.1. It includes script excerpts which you can use as a basis for performing upgrades. The entire script is included at the end.

The script is based on upgrading a cluster running on Docker Desktop on a local host using the R3-provided Corda Helm chart for installing PostgreSQL and Kafka. However, you must tailor this script for the specific environment being updated.

The examples provided in this section assume that you installed Corda 5.1 in a namespace called `corda`. This is different to other deployments.

To perform an upgrade, you must fulfill the required [prerequisites](#prerequisites) and go through the following steps:

1. [Back Up the Corda Database](#back-up-the-corda-database)
2. [Test the Migration](#test-the-migration)
3. [Migrate Data From Kafka Topics to the Cluster Database](#migrate-data-from-kafka-topics-to-the-cluster-database)
4. [Scale Down the Running Corda Worker Instances](#scale-down-the-running-corda-worker-instances)
5. [Migrate the Corda Cluster Database](#migrate-the-corda-cluster-database)
6. [**Optional:** Clear Down Key Rotation Stale Data](#optional-clear-down-key-rotation-stale-data)
7. [Update Kafka Topics](#update-kafka-topics)
8. [Launch the Corda 5.2.1 Workers](#launch-the-corda-5.2.1-workers)

For information about how to roll back an upgrade, see [Rolling Back]({{< relref "rolling-back521.md" >}}).

Following a platform upgrade, Network Operators should upgrade their networks. For more information, see [Upgrading an Application Network]({{< relref "../../../application-networks/upgrading/_index.md" >}}).

## Prerequisites

Corda 5 relies on certain underlying prerequisites, namely Kafka and PostgreSQL, administered by the Cluster Administrators.

{{< note >}}
This guide assumes that the Cluster Administrator assigned to upgrade Corda has full administrator access to these prerequisites.
{{< /note >}}

Developers, including customer CorDapp developers, or those trialling Corda, can use the R3-provided [Corda Helm chart]({{< relref "../deploying.html#download-the-corda-helm-chart" >}}) which installs these prerequisites. The Corda Helm chart can also configure Corda so it can reach these prerequisites, allowing a quick and convenient installation of Corda 5.

Customers in production are not expected to follow this path, and generally use managed services for these prerequisites. They also impose significant privilege restrictions in terms of who can administer these services.

The guide cannot provide instructions on how to gain administrator access to customer-managed or self-hosted services.

### Kafka Access

Some complications arise when trying to administer Kafka inside a Corda cluster from a host outside the cluster. Kafka connections are not created directly to the Kafka broker in the first instance, but via a bootstrap server which redirects requests to a broker based on its advertised listeners list. Advertised listeners are set up at Kafka deployment time and might not be accessible to the subnet of a host on a different subnet.

A simple port forward to Kafka is not sufficient as this only forwards traffic to the bootstrap server. The redirection from the bootstrap to a Kafka broker fails unless you are on the same subnet as the Kafka broker’s advertised listener name. Additionally, if SSL is enabled for your Kafka deployment, you cannot access it at a different host name from those covered by the certificate.

This guide cannot describe how to create a connection to any arbitrary Kafka deployment. It is up to the upgrader to ensure this is possible from their host. The examples in the guide use local host DNS mapping to connect to a cluster. The host is configured so that a known advertised listener name maps to an IP address by manipulating the local hosts file. However, this might not be appropriate for your deployment. For example, the automated pipelines at R3 use a pod from within the Corda cluster to perform Kafka upgrade steps. Configuring such a pod, if it is required, is the responsibility of the Corda Operator.

You can test Kafka access using off-the-shelf Kafka tools. For example, if you can list Kafka topics using a command similar to this, you have the required access from your host:

```
kafka-topics --bootstrap-server=prereqs-kafka.test-namespace:9092 --list
```

### REST API Access

To get information about TLS certificate aliases, the data migration step requires access to the Corda REST API. This is required at the same stage when data is extracted from Kafka, which means access to Kafka and the Corda REST API must be available in the same environment at the same time. You must pass credentials and locations of both to the Corda CLI plugin when executed.

Also, you must have `GET` access to the `/key` and `/certificate` APIs.

### Corda CLI Tool and Corda 5 Plugins

Some upgrade steps use the Corda CLI tool used also in Corda 5 [manual bootstrapping]({{< relref "../deploying/manual-bootstrapping.md" >}}). Users who entirely bootstrapped Corda 5 using the Corda Helm chart may not be familiar with this tool because the Corda Helm chart executes it for you. For instructions on how to install Corda CLI, go to [Installing the Corda CLI]({{< relref "../../../application-networks/tooling/installing-corda-cli.md" >}}).

The Corda CLI tool and plugins are also published internally as Docker images. The examples in this script use those Docker images so that:
* The Corda CLI tool does not need to be downloaded or installed.
* The latest published tool is always available.
* The correct version is always used.

{{< note >}}
The version of the Corda CLI tool and plugins must match the version of Corda 5 being upgraded to, that is, 5.2.1.
{{< /note >}}

The functionality of the tools, the database schemas and Kafka topics embedded in them pertain to the version of Corda they were built against.

If you are not using Docker images, where you come across an example of the form:
```
docker run <docker options> $CLI_DOCKER_IMAGE <tool options>
```

This can be replaced with:
```
corda-cli.sh <tool options>
```

To use the Docker images, you must set `CLI_DOCKER_IMAGE` to the 5.2.1 image version, for example, `corda-os-docker.software.r3.com/corda-os-plugins:5.2.1.0` or some beta version prior to 5.2.1 release.

## Back Up the Corda Database

## Test the Migration

## Migrate Data From Kafka Topics to the Cluster Database

## Scale Down the Running Corda Worker Instances

## Migrate the Corda Cluster Database

## **Optional:** Clear Down Key Rotation Stale Data

## Update Kafka Topics

## Launch the Corda 5.2.1 Workers


