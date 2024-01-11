---
description: "Review the prerequisites for deploying Corda 5."
date: '2023-05-11'
version: 'Corda 5.2'
title: "Prerequisites"
menu:
  corda52:
    parent: corda52-cluster-deploy
    identifier: corda52-cluster-prerequisites
    weight: 1000
section_menu: corda52
---
# Prerequisites

The Corda deployment process has the following prerequisites:

* {{< tooltip >}}Kubernetes{{< /tooltip >}} for container orchestration
* {{< tooltip >}}Kafka{{< /tooltip >}} for messaging
* PostgreSQL for persistence

See the [Infrastructure Topology]({{< relref "../topology/_index.md" >}}) subsection for example topologies on the Amazon Web Services and Microsoft Azure cloud platforms, including initial sizing guidance.

## Container Orchestration

Corda uses Kubernetes to manage the scheduling and availability of Corda workers.
Corda is tested on the following:

{{< snippet "prereqs-container.md" >}}

The Corda deployment process requires a Kubernetes context with credentials that provide access to the namespace in which Corda is to be installed. It needs permission to create deployments, secrets, and, if automatic bootstrapping is used, jobs. Corda does not create any persistent volumes and does not install any cluster-scoped resources.

## Messaging

Corda uses Kafka for communication between the Corda workers. Corda is tested with the following:

{{< snippet "prereqs-messaging.md" >}}

The Corda deployment process requires the following:

* Kafka bootstrap server addresses and their ports.
* **Automatic bootstrapping**: user name and password for a user that has permission to:
  * create topics with the given topic prefix.
  * define ACLs for each topic.
  
  You should use a separate user for each type of Corda worker although, for development and test, a single user can be used.
* If the Kafka brokers are using {{< tooltip >}}TLS{{< /tooltip >}} and the certificates used are not trusted by the default JVM {{< tooltip >}}trust store{{< /tooltip >}}, a trust store containing the root certificate is required.

## Database

Corda uses PostgreSQL for the persistence of system and application data, including configuration and state information.
Corda is tested with the following:

{{< snippet "prereqs-databases.md" >}}

The Corda deployment process requires the following:

* PostgreSQL hostnames and ports.
* **Automatic bootstrapping**: user name and password for a user in each database that has the ability to:
  * create the configuration, crypto, RBAC, and state manager schemas.
  * create crypto, RBAC, and state manager users.
  * grant the users access to their respective schemas.
* **[Manual bootstrapping]({{< relref "./deploying/manual-bootstrapping.md" >}})**: additional {{< tooltip >}}virtual node{{< /tooltip >}} user with the ability to create schemas dynamically at runtime.

### Security Vault {{< enterprise-icon >}}

Corda Enterprise supports integration with HashiCorp Vault as an external secret management system. This is the recommended deployment configuration. For more information, see [Configuration Secrets]({{< relref "../config/secrets.md" >}}). Corda is tested with the following:

{{< snippet "prereqs-vault.md" >}}
