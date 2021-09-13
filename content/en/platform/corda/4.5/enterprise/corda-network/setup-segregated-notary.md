---
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-network
title: Setting up a notary in a segregated network
weight: 2000
---

# Setting up a notary in a segregated network

Segregated networks are a smaller network operating within the context of a larger network. A segregated network allows
a measure of independence and control over the network parameters within a larger Corda network.

When operating in a Corda Network segregated network, you must deploy, register, and operate the notary. There are three
notary implementations to choose from:

- A single-node notary.
- A notary cluster using a single node.
- A highly-available (HA) notary cluster requiring multiple nodes.

By adding additional notary worker nodes, a notary cluster can have more reliability and scalabilty than a single-node notary.

## Configuring and deploying a single-node notary

Single-node notaries do not require a separate notary service identity, these notaries use the node identity and do not require additional notary registration. Single-node notaries are not compatible with a highly-available solution and are not recommended for production networks.

1. Follow steps 3-5 from the [Corda Network joining process](https://corda.network/participation/index/).

2. Register the node using the following command:

    `java -jar corda.jar --initiail-registration --network-root-truststore certificates/network-root-truststore.jks --network-root-truststore-password trustpass`

    The registration process will create a `nodeInfo-xxx` file containing the network address, port number, legal identity, certificates, platform version, and serial number of the notary.

3. Update the network parameters by sending the `nodeInfo-xxx` file using the [Corda Network support portal](https://r3-cev.atlassian.net/servicedesk/customer/portal/7/). Send the `nodeInfo-xxx` file using either a segregated network request form, or create a new task.

4. Restart the notary by running the following command:

    `java -jar /path-of-notary/corda.jar`


## Configuring and deploying a notary

A notary cluster is a group of one or more nodes that act together as a collective notary service. Notary clusters can improve
notary scalability and reliability because additional nodes can be added to the notary pool as demand increases.

Single-node and multi-node notary clusters are only available in Corda Enterprise. Before deploying a notary cluster,
read the [JPA notary configuration documentation](../notary/installing-jpa.md/). A notary cluster requires a backend database to store notarised
transactions. A notary cluster can be registered, but not run, without a database.

{{< note >}}
You must register the notary service identity **before** the initial notary worker registration.
{{< /note >}}

1. Register the notary service identity using the [notary registration tool](../notary/ha-notary-service-setup.md#ha-notary-registration-process).

2. Register each worker node in the notary cluster using the Corda Network process.

    Each worker node requires access to the notary service identity key generated in the preceding step. An HSM should be used to ensure key security.

3. Add the notary service identity to the network parameters by sending the `nodeInfo-xxx` file using the [Corda Network support portal](https://r3-cev.atlassian.net/servicedesk/customer/portal/7/). Send the `nodeInfo-xxx` file using either a segregated network request form, or create a new task.

4. After the network parameters have been updated, [start the notary worker nodes](../operations/deployment/starting-components.md#starting-a-corda-node).
