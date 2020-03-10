---
aliases:
- /releases/4.4/notary/ha-notary-service-overview.html
date: '2020-01-08T09:59:25Z'
menu:
- corda-enterprise-4-4
tags:
- ha
- notary
- service
- overview
title: Corda Enterprise notary service overview
---


# Corda Enterprise notary service overview

A high-availability Corda notary service is made up of two components:

> 
> 
> * The *notary workers*: A set of Corda notary nodes that each has a separate legal identity but
> share a single service identity, and are configured to work together in high-availability mode
> * The *notary state DB*: A single logical database that all the notary workers connect to and
> that is itself configured to be high-availability


In addition to the shared database for the notary state, each notary worker requires its own
database for its node state (such as its identity), since the notary workers are just standard
Corda nodes that have been configured to operate in notary mode.

The can visualise this as follows, with the Corda client nodes in green on the top, the Corda
notary worker nodes in red in the middle, and the database nodes on the bottom in blue.

![ha notary overview2](notary/resources/ha-notary-overview2.png "ha notary overview2")
Client nodes requesting notarisation from the notary will connect to the available notary workers
in a round-robin fashion. The task of a worker node is to verify the notarisation request, the
transaction timestamp (if present), and resolve and verify the transaction chain (if the notary
service is validating). It then commits the transaction’s input states to the database.

Since the notary pool consists of several database nodes and several notary workers, it is high-availability, allowing
it to continue to process notarisation requests even if individual database nodes and/or notary workers fail. For
example, a three node notary cluster can tolerate one crash fault.

{{< note >}}
In production you should consider running five nodes or more, to be able to
tolerate more than one simultaneous crash fault. Although a single Corda notary
worker is enough to serve notarisation requests in practice, its capacity might
not be sufficient depending on your throughput and latency requirements.

{{< /note >}}
If desired, you can choose to run each database server and its Corda notary worker on the same
machine:

![ha notary colocated](notary/resources/ha-notary-colocated.png "ha notary colocated")

## Notary implementations

Corda Enterprise contains more than one notary implementation. These implementations serve different operational
requirements. Ensure that the correct notary implementation is selected according to the requirements.

The table below lists the available notary implementations in Corda Enterprise:


{{< table >}}

|Notary Implementation|Supports high-availability mode|Notary state connection|
|-------------------------|---------------------------------|-----------------------------|
|Simple notary|No|Shares the node’s database
connection|
|MySQL notary (Legacy)|Yes|Separate connection|
|JPA notary|Yes|Separate connection|

{{< /table >}}

For a list of databases supported by each of the above notary implementations, please refer to the [Platform support matrix](../platform-support-matrix.md)

{{< note >}}
Due to its lack of resiliency, a simple notary is not suited to a production environment. Furthermore, a simple notary cannot be cannot
be upgraded to a JPA notary. For these reasons it is strongly recommended to deploy a JPA notary in all non-testing environements.

{{< /note >}}

## Notary configuration

Notary workers use `node.conf` files but must include additional properties. For more information, please refer to
../node-configuration-file.


## Legal names and identities

In a simple notary, each notary only requires its own legal name, specified in the node’s configuration file.

In a high-availability notary implementation, every notary worker node must be configured with two legal names:


* Its own legal name, specified in the node’s configuration file as `myLegalName` (e.g `O=Worker 1, C=GB, L=London`). This is worker
specific.
* The service legal name, specified in the node’s configuration file by `notary.serviceLegalName` (e.g. `O=HA Notary,C=GB, L=London`).
This is shared by all workers in the notary cluster.

Only the service legal name is included in the network parameters. CorDapp developers should select the notary service identity from the
network map cache, for example:

```kotlin
serviceHub.networkMapCache.getNotary(CordaX500Name("HA Notary", "London", "GB"))
```


## Keys and certificates

As described above, every notary worker is configured with its own legal name and the shared service legal name. These names correspond to
identities that have their own key pair and certificate, which should be accessible by the notary worker.

Both worker identity and notary service keys and certificates are stored in the same way as for regular Corda nodes. That is, if using local
key stores, the worker identity, worker node CA and notary service key pairs and certificates are stored in files within the
`certificates` directory. If an HSM is being used to generate and store the keys then only the certificate chains will be stored in the
local files. You can find out more in the ../permissioning document.

{{< note >}}
The key store aliases for the worker identity, worker node CA and notary service are fully configurable. Unique worker identity and node
CA aliases are required for the workers to share the same HA HSM. Although not required for all deployment scenarios, it is recommended
to configure unique worker aliases. See ../corda-configuration-file for more information.

{{< /note >}}

## Expected data volume

Non-validating notaries store roughly one kilobyte per transaction.

