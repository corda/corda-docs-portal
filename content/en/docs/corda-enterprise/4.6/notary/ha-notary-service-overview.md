---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-corda-nodes-notaries
    name: "Notary options in Corda Enterprise"
    parent: corda-enterprise-4-6-notaries
tags:
- ha
- notary
- service
- overview
title: Notary service overview
weight: 10
---


# Notary service overview

Corda Enterprise comes with two notary types:

* **Single-node**: a simple notary service that persists notarisation requests in the node’s database. It is easy to configure
and can be used for testing, or networks that do not have strict availability requirements.
* **Highly available**: a clustered notary service operated by a single party, able to tolerate crash faults.

Corda Enterprise provides two notary highly available (HA) notary implementations:

* MySQL notary (deprecated)
* JPA notary

{{< warning >}}
Single-node notaries are not suitable for a production deployment.
{{< /warning >}}


For a list of databases supported by the MySQL and JPA notaries, please refer to the [Platform support matrix](../platform-support-matrix.md).

## Single-node notary

To have a regular Corda node provide a notary service you simply need to set appropriate `notary` configuration values as specified in the [node configuration file](../node/setup/corda-configuration-fields.md/)

For clients to be able to use the notary service, its `notary.serviceLegalName` must be added to the network parameters.
If you are using the [network bootstrapper](../network-bootstrapper.md/) the notary service name will be added to the network parameters automatically.


## Notary high-availability mode

The high availability JPA and deprecated MySQL Corda notary services are made up of two components:

* The *notary workers*: A set of Corda nodes configured in HA notary mode. Each node has a separate legal identity, but shares a single
notary identity. These nodes are configured to work together in high-availability mode
* The *notary state database*: A single logical database, itself configured to be highly-available, that all the notary workers connect
to

{{< note >}}
Because each notary worker is a Corda node, in addition to being connected to the notary state database, it requires a standard node
database to store its node state (e.g. its identity information).
{{< /note >}}

We can visualise this set-up as follows, with the regular Corda nodes in green, the Corda notary worker nodes in red, and the standard node
databases and notary state database replicas in blue.

{{< figure alt="ha notary overview2" zoom="../resources/ha-notary-overview2.png" >}}
Nodes requesting notarisation from a highly-available notary will connect to the notary workers in round-robin fashion.

Provided there are multiple notary workers and the notary state database is configured to be highly-available, the overall notary service
will be highly-available. This is because the notary service can continue processing notarisation requests even if individual database
replicas and/or notary workers fail. For example, a three-node notary cluster can tolerate one crash fault.

{{< note >}}
In production you should consider running five nodes or more, in order to be able to tolerate more than one simultaneous crash fault.
Although a single Corda notary worker is enough to serve notarisation requests in practice, its capacity might not be sufficient
depending on your throughput and latency requirements.
{{< /note >}}

If desired, you can choose to run each database server and its Corda notary worker on the same machine:

{{< figure alt="ha notary colocated" zoom="../resources/ha-notary-colocated.png" >}}

## Notary configuration

Nodes are configured as single-node notaries or notary workers via their `node.conf` files. For more information, please refer to
[node configuration file](../node/setup/corda-configuration-fields.md/).


## Legal names and identities

All notaries and notary workers require two legal names:

- A legal name, specified in the node configuration file as `myLegalName`. In a notary cluster, this property is unique to each worker node.
- The notary legal name, specified in the node configuration file as `notary.serviceLegalname`. This is the legal name and identifier of the notary service. In a notary cluster, it is common to all workers in a given notary cluster.

Only the `notary.serviceLegalName` and public key are included in the network parameters.


## Keys and certificates

As described above, every notary worker is configured with both its own legal name and the shared service legal name. These names
correspond to identities that have their own key pair and certificate, which should be accessible by the notary worker.

Both worker identity and notary service keys and certificates are stored in the same way as for regular Corda nodes. That is, if using local
key stores, the worker identity, worker node CA and notary service key pairs and certificates are stored in files within the
`certificates` directory. If an HSM is being used to generate and store the keys then only the certificate chains will be stored in the
local files. You can find out more in the [permissioning](../network/permissioning.md/) document.

{{< note >}}
The key store aliases for the worker identity, worker node CA and notary service are fully configurable. Unique worker identity and node
CA aliases are required for the workers to share the same HA HSM. Although not required for all deployment scenarios, it is recommended
to configure unique worker aliases. See [node configuration file](../node/setup/corda-configuration-fields.md/) for more information.
{{< /note >}}

## Expected data volume

Non-validating notaries store roughly one kilobyte per transaction.
