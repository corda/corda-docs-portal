---
date: '2023-08-10'
version: 'Corda 5.1'
title: "Prerequisites"
menu:
  corda51:
    parent: corda51-cluster-deploy
    identifier: corda51-cluster-prerequisites
    weight: 1000
section_menu: corda51
---
# Prerequisites
There are three prerequisites to the Corda deployment process:

* {{< tooltip >}}Kubernetes{{< /tooltip >}} for container orchestration
* {{< tooltip >}}Kafka{{< /tooltip >}} for messaging
* PostgreSQL for persistence

See the [Infrastructure Topology]({{< relref "../topology/_index.md" >}}) subsection for example topologies on the Amazon Web Services
and Microsoft Azure cloud platforms, including initial sizing guidance.

## Container Orchestration

Corda uses Kubernetes to manage the scheduling and availability of Corda workers.
Corda is tested on version 1.23 of Kubernetes, running on Amazon Elastic Kubernetes Service (EKS),
Azure Kubernetes Service (AKS), and Red Hat OpenShift Container Platform.

{{< snippet "prereqs-container.md" >}}

The Corda deployment process requires a Kubernetes context with credentials that provide access to the namespace
in which Corda is to be installed. It needs permission to create deployments, secrets, and,
if automatic bootstrapping is used, jobs. Corda does not create any persistent volumes and does not install any cluster-scoped resources.

## Messaging

Corda uses Kafka for communication between the Corda workers. Corda is tested with Kafka 3.2.0,
including Amazon Managed Streaming for Apache Kafka (MSK). Corda is also tested with Confluent Cloud.

{{< snippet "prereqs-messaging.md" >}}

The Corda deployment process requires the Kafka bootstrap server addresses and their ports.
If the Kafka brokers are using {{< tooltip >}}TLS{{< /tooltip >}} and the certificates used will not be trusted by the JVM’s default {{< tooltip >}}trust store{{< /tooltip >}},
then a trust store containing the root certificate is required. If automatic bootstrapping is used, the user name
and password are required for a user that has permission to create topics with the given topic prefix and
then define ACLs for each topic. It is recommended that a separate user is then used for each of the seven types of
Corda workers although, for development and test, a single user can be used.

## Database

Corda uses PostgreSQL for the persistence of system and application data, including configuration and state information.
Corda is tested with PostgreSQL 14.4 including Amazon RDS for PostgreSQL, Amazon Aurora PostgreSQL, and Microsoft Azure PostgreSQL.

{{< snippet "prereqs-databases.md" >}}

The Corda deployment process requires the PostgreSQL hostname and port. If automatic bootstrapping is used,
a user name and password are required for a user that has the ability to create the schemas for configuration, crypto,
and {{< tooltip >}}RBAC{{< /tooltip >}}, and can create crypto and RBAC users and grant them access to their respective schemas.
If [bootstrapping manually]({{< relref "./deploying/manual-bootstrapping.md" >}}), an additional {{< tooltip >}}virtual node{{< /tooltip >}} user will still need the ability to create schemas dynamically at runtime.

### Security Vault {{< enterprise-icon >}}

Corda Enterprise supports integration with HashiCorp Vault as an external secret management system. This is the recommended deployment configuration. For more information, see [Configuration Secrets]({{< relref "../config/secrets.md" >}}).

{{< snippet "prereqs-vault.md" >}}