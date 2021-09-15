---
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-network
tags:
- UAT
title: Setting up a notary in a segregated network
weight: 2000
---

# Setting up a notary in a segregated network

Segregated networks are a smaller network operating within the context of a larger network. A segregated network allows
a measure of independence and control over the network parameters within a larger Corda network.

When operating in a Corda Network segregated network, you must deploy, register, and operate the notary. There are three
notary implementations to choose from:

- A single notary node
- A notary cluster using a single node
- A highly-available (HA) notary cluster requiring multiple nodes

You should take care when deciding on the type of notary to deploy, as single notary nodes cannot be upgraded to HA notaries later.
In production environments we recommend using a notary cluster for additional reliability and scalability.

## Configuring and deploying a notary

Single-node notaries are simple notary implementations and are not recommended for production environments.

A notary cluster is a group of at least one node that act together as one pooled notary service. Notary clusters can improve
notary scalability and reliability because additional nodes can be added to the notary pool as demand increases.

Single-node and multi-node notary clusters are only available in Corda Enterprise. Before deploying a notary cluster,
read the [JPA notary configuration documentation](../notary/installing-jpa.md/). A notary cluster requires a backend database to store notarised
transactions. A notary cluster can be registered, but not run, without a database.

{{< note >}}
Please note that you must register the notary service identity **before** the initial notary worker registration.
{{< /note >}}

1. Register the notary service identity using the [notary registration tool](../notary/ha-notary-service-setup.html#ha-notary-registration-process).

2. Register each worker node in the notary cluster using the Corda Network process.

    Each worker node requires access to the notary service identity key generated in the preceding step. We recommend using
    an HSM to ensure key security.

3. Add the notary service identity to the network parameters by sending the `nodeInfo-xxx` file using the [Corda Network support portal](https://r3-cev.atlassian.net/servicedesk/customer/portal/7) using either a segregated network request form, or by creating a new task.

4. After the network parameters have been updated, [start the notary worker nodes](../operations/deployment/starting-components.md#starting-a-corda-node).
