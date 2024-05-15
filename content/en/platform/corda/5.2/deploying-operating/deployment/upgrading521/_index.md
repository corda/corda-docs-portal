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

This section describes how to upgrade a Corda cluster from 5.2 to 5.2.1. It lists the required [prerequisites](#prerequisites) and describes the following steps required to perform an upgrade:

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

### Kafka Access

### REST API Access

### Corda CLI Tool and Corda 5 Plugins

## Back Up the Corda Database

## Test the Migration

## Migrate Data From Kafka Topics to the Cluster Database

## Scale Down the Running Corda Worker Instances

## Migrate the Corda Cluster Database

## **Optional:** Clear Down Key Rotation Stale Data

## Update Kafka Topics

## Launch the Corda 5.2.1 Workers


