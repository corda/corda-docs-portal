---
date: '2023-05-11'
title: "Prerequisites"
menu:
  corda5:
    parent: corda5-cluster-deploy
    identifier: corda5-cluster-prerequisites
    weight: 1000
section_menu: corda5
---

There are three prerequisites to the Corda deployment process:

* Kubernetes for container orchestration
* Kafka for messaging
* PostgreSQL for persistence

See the [Infrastructure Topology]({{< relref "../topology.md" >}}) subsection for example topologies on the Amazon Web Services
and Microsoft Azure cloud platforms, including initial sizing guidance.

## Container Orchestration

Corda uses Kubernetes to manage the scheduling and availability of Corda workers.
Corda is tested on version 1.23 of Kubernetes, running on Amazon Elastic Kubernetes Service (EKS),
Azure Kubernetes Service (AKS), and Red Hat OpenShift Container Platform.

| Software | Version |
| :----------- | :----------- |
| Kubernetes | 1.23 |
| Amazon Elastic Kubernetes Service (EKS). Currently only supported on EC2, not Fargate. | 1.23 |
| Microsoft Azure Kubernetes Service (AKS) | 1.23 |
| Red Hat OpenShift Container Platform | 4.10 |

The Corda deployment process requires a Kubernetes context with credentials that provide access to the namespace
in which Corda is to be installed. It needs permission to create deployments, secrets, and,
if automatic bootstrapping is used, jobs. Corda does not create any persistent volumes and does not install any cluster-scoped resources.

## Messaging

Corda uses Kafka for communication between the Corda workers. Corda is tested with Kafka 3.2.0,
including Amazon Managed Streaming for Apache Kafka (MSK). Corda is also tested with Confluent Cloud.

| Software | Version |
| :----------- | :----------- |
| Kafka | 3.2.0 |
| Amazon Managed Streaming for Apache Kafka (MSK) | 3.2.0 |
| Confluent Cloud |  |

The Corda deployment process requires the Kafka bootstrap server addresses and their ports.
If the Kafka brokers are using TLS and the certificates used will not be trusted by the JVM’s default trust store,
then a trust store containing the root certificate is required. If automatic bootstrapping is used, the user name
and password are required for a user that has permission to create topics with the given topic prefix and
then define ACLs for each topic. It is recommended that a separate user is then used for each of the seven types of
Corda workers although, for development and test, a single user can be used.

## Database

Corda uses PostgreSQL for the persistence of system and application data, including configuration and state information.
Corda is tested with PostgreSQL 14.4 including Amazon RDS for PostgreSQL, Amazon Aurora PostgreSQL, and Microsoft Azure PostgreSQL.

| Software | Version |
| :----------- | :----------- |
| PostgreSQL | 14.4 |
| Amazon RDS for PostgreSQL | 14.4 |
| Amazon Aurora PostgreSQL | 14.4 |
| Microsoft Azure PostgreSQL | 14.4 |

The Corda deployment process requires the PostgreSQL hostname and port. If automatic bootstrapping is used,
a user name and password are required for a user that has the ability to create the schemas for configuration, crypto,
and RBAC, and can create crypto and RBAC users and grant them access to their respective schemas.
If [bootstrapping manually](bootstrapping.md), an additional virtual node user will still need the ability to create schemas dynamically at runtime.
