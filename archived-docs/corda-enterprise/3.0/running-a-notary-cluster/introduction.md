---
aliases:
- /releases/3.0/running-a-notary-cluster/introduction.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-introduction
    parent: corda-enterprise-3-0-toctree
    weight: 1010
tags:
- introduction
title: Highly Available Notary Service Setup
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Highly Available Notary Service Setup


## About the HA Notary Installation

In this chapter you’ll learn how to set up, configure and start a highly
available (HA) Corda Enterprise Notary from scratch.
The bootstrapper allows you to set up a cluster of nodes from
a set of configuration files.

The HA Notary relies on a Percona/XtraDB (Percona) cluster. How to set up Percona
is described below.

This guide assumes you’re running a Debian-based Linux OS.

Double curly braces `{{ }}` are used to represent placeholder values
throughout this guide.


## Overview

![ha notary overview2](/en/ha-notary-overview2.png "ha notary overview2")
The figure above displays the Corda nodes in green on the top, then the Corda
notaries in red in the middle and on the bottom are the Percona nodes in blue.

Corda nodes that request a notarisation by the service name of the Notary,
will connect to the available Notary nodes in a round-robin fashion.

Since our Notary cluster consists of several Percona nodes and several Corda
Notary nodes, we achieve high availability (HA). Individual nodes of the
Percona and Notary clusters can fail, while clients are still able to
notarise transactions. The Notary cluster remains available. A three-node
Percona cluster as shown in the figure above can tolerate one crash fault.

{{< note >}}
In production you should consider running five nodes or more, to be able to
tolerate more than one simultaneous crash fault. One single Corda Notary
replica is enough to serve traffic in principal, although its capacity might
not be sufficient, depending on your throughput and latency requirements.

{{< /note >}}

### Colocating Percona and the Notary Service

![percona colocated](/en/percona-colocated.png "percona colocated")
You can run a Percona DB service and a Corda Notary service on the same machine.


### Summary


* Corda nodes communicate with the Notary cluster via P2P messaging, the messaging layer handles selecting an appropriate Notary replica by the service legal name.
* Corda nodes connect to the Notary cluster members round-robin.
* The notaries communicate with the underlying Percona cluster via JDBC.
* The Percona nodes communicate with each other via group communication (GComm).
* The Percona replicas should only be reachable from each other and from the Notary nodes.
* The Notary P2P ports should be reachable from the internet (or at least from the rest of the Corda network you’re building or joining).
* We recommend running the notaries and the Percona service in a joined private subnet, opening up the P2P ports of the notaries for external traffic.


### Legal Names and Identities

Every Notary replica has two legal names. Its own legal name, specified by
`myLegalName`, e.g `O=Replica 1, C=GB, L=London` and the service legal name
specified in configuration by `notary.serviceLegalName`, e.g. `O=HA Notary,
C=GB, L=London`. Only the service legal name is included in the network
parameters. CorDapp developers should select the Notary service identity from the network map cache.

```kotlin
serviceHub.networkMapCache.getNotary(CordaX500Name("HA Notary", "London", "GB"))
```

Every Notary replica’s keystore contains the private key of the replica and the
private key of the Notary service (with aliases `identity-private-key` and
`distributed-notary-private key` in the keystore). We’re going to create and
populate the node’s keystores later in this tutorial.


## Expected Data Volume

For non-validating notaries the Notary stores roughly one kilobyte per transaction.


## Prerequisites


* Java runtime
* Corda Enterprise JAR
* Bootstrapper JAR
* Root access to a Linux machine or VM to install Percona
* The private IP addresses of your DB hosts (where we’re going to install Percona)
* The public IP addresses of your Notary hosts (in order to advertise these IPs for P2P traffic)

Your Corda distribution should contain all the JARs listed above.


## Security


### Credentials

Make sure you have the following credentials available, create them if necessary and always
keep them safe.


{{< table >}}

|Password or Keystore|Description|
|--------------------------------|------------------------------------------------------------------------------------------------------------|
|database root password|used to create the Corda user, setting up the DB and tables (only required for some installation methods)|
|Corda DB user password|used by the Notary service to access the DB|
|SST DB user password|used by the Percona cluster for data replication (SST stands for state snapshot transfer)|
|Network root truststore password|(not required when using the bootstrapper)|
|Node keystore password|(not required when using the bootstrapper)|
|The network root truststore|(not required when using the bootstrapper)|

{{< /table >}}


### Networking


#### Percona Cluster


{{< table >}}

|Port|Purpose|
|-----|-------------------------------------------------------------------------------------|
|3306|MySQL client connections (from the Corda Notary nodes)|
|4444|SST via rsync and Percona XtraBackup|
|4567|Write-set replication traffic (over TCP) and multicast replication (over TCP and UDP)|
|4568|IST (Incremental State Transfer)|

{{< /table >}}

Follow the [Percona documentation](https://www.percona.com/doc/percona-xtradb-cluster/5.7/security/encrypt-traffic.html)
if you need to encrypt the traffic between your Corda nodes and Percona and between Percona nodes.


#### Corda Node


{{< table >}}

|Port|Example|Purpose|
|---------|-------|------------------------------|
|P2P Port|10002|P2P traffic (external)|
|RPC Port|10003|RPC traffic (internal only)|

{{< /table >}}

Later in the tutorial we’re covering the Notary service configuration in details, in [Setting up the Notary Service](installing-the-notary-service.md).


### Keys and Certificates

Keys are stored the same way as for regular Corda nodes in the `certificates`
directory. If you’re interested in the details you can find out
more in the [Network permissioning](../permissioning.md) document.


## Next Steps



* [Percona, the underlying Database](installing-percona.md)
* [Setting up the Notary Service](installing-the-notary-service.md)
* [Percona Monitoring, Backup and Restore (Advanced)](operating-percona.md)



