---
aliases:
- /releases/4.3.1/running-a-notary-cluster/ha-notary-service-setup.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3-1:
    identifier: corda-enterprise-4-3-1-ha-notary-service-setup
    parent: corda-enterprise-4-3-1-ha-notary-service-overview
    weight: 500
tags:
- ha
- notary
- service
- setup
title: Notary Service Set-up
---

# Corda Enterprise Notary Service Set-up

Double curly braces `{{ }}` are used to represent placeholder values throughout this guide.

## Notary implementations

Corda Enterprise contains more than one notary implementation. These multiple implementations exist to
serve different operational requirements. Ensure that the correct notary implementation is selected
according to the requirements.

The table below lists the available notary implementations in Corda Enterprise:

{{< table >}}

|Notary Implementation|Supports highly available mode|Notary state connection|
|-------------------------|--------------------------------|-----------------------------|
|Simple notary|No|Shares the node’s database connection|
|MySQL notary (Legacy)|Yes|Separate connection|
|JPA notary|Yes|Separate connection|

{{< /table >}}

For a list of databases supported by each of the above notary implementations, please refer to the [Platform support matrix](../platform-support-matrix.md)

## HA notaries

The Corda Enterprise notary service can be configured in highly available (HA) mode. Note that for the
Corda Enterprise notary service to operate in HA mode, a highly available database is required.

Running the Corda Enterprise notary service in highly available mode requires the following:

* One of the notary implementations that supports highly available mode
* A database supported by the notary implementation, configured in highly available mode

## Prerequisites

* Java runtime
* Corda Enterprise `jar`
* Notary Health-Check `jar`
* Bootstrapper `jar` (only required when setting up network without doorman and network map)
* Network Registration tool (only required when setting up a network with doorman and network map)
* Root access to a Linux machine or VM to install the selected database
* The private IP addresses of your database hosts
* The public IP addresses of your notary hosts
* The database driver in the form of a JAR file, located inside the “drivers” folder

Your Corda Enterprise distribution should contain all the JARs listed above.

## Networking

Client nodes communicate with the notary cluster via P2P messaging, with the messaging layer
selecting an appropriate notary worker node by the service legal name. The notary worker P2P ports
should be reachable from the internet (or at least from the rest of the Corda network you’re
building or joining).

Each notary worker needs access to its individual node database. It also communicates with the
underlying database cluster via JDBC.

Load balancing is currently done in *round robin* fashion on the client nodes by providing a custom
policy to the Artemis server locator. When the policy is provided artemis starts automatically
executing the round robin logic for messages completely transparently, because all the workers in the HA setup
share the same legal identity in turn registering multiple IP addresses under it.

{{< note >}}
In very extreme cases, where a plethora of nodes are powered up and all send requests for notarisation
at the same time the ETA mechanism might be triggered on only one worker.
{{< /note >}}

The notary might provide back pressure to the client node, namely the ETA mechanism, which assumes equal load on all HA workers
and in turn forcing the node to wait for some time before retrying the flow.

A case might occur where the same transaction is submitted multiple times, which in turn should yield
the same result. Said idempotence is assured in an HA cluster because the database cluster is shared
and all notaries commit transactions, so that even if transaction X is sent to notary A and notary B,
if notary A processes the transaction first, notary B will be aware of the processing as it will check
the database.

{{< note >}}
The node will continue retrying notarisation requests automatically until it hears back from the notary. The round
robin logic should redirect retry attempts to different notary workers.
{{< /note >}}

## Legal names and identities

Every notary worker node has two legal names:

* Its own legal name, specified in the node’s configuration file as `myLegalName` (e.g `O=Worker 1, C=GB, L=London`)
* The service legal name, specified in the node’s configuration file by `notary.serviceLegalName` (e.g. `O=HA Notary,C=GB, L=London`)

Only the service legal name is included in the network parameters. CorDapp developers should
select the notary service identity from the network map cache, for example:

```kotlin
serviceHub.networkMapCache.getNotary(CordaX500Name("HA Notary", "London", "GB"))
```

Every notary worker’s keystore contains the private key of both the node itself and the
private key of the notary service (with aliases `identity-private-key` and
`distributed-notary-private-key` in the keystore).

{{< note >}}
If you want to connect to a Corda network with a doorman and network map service,
use the registration tool to create your service identity. In you want to set up a test network
for development or a private network without using a doorman or network map, using the
bootstrapper is recommended.
{{< /note >}}

## Expected data volume

Non-validating notaries store roughly one kilobyte per transaction.

## Security

### Credentials

Make sure you have the following credentials available, creating them if necessary and always
keeping them safe.

{{< table >}}

|Password or Keystore|Description|
|--------------------------------|------------------------------------------------------------------------------------------------------------|
|database root password|used to create the Corda user, setting up the DB and tables (only required for some installation methods)|
|Corda DB user password|used by the notary service to access the DB|
|SST DB user password|used by the Percona cluster for data replication (SST stands for state snapshot transfer)|
|Network root truststore password|(not required when using the bootstrapper)|
|Node keystore password|(not required when using the bootstrapper)|
|The network root truststore|(not required when using the bootstrapper)|

{{< /table >}}

## Keys and certificates

Notary keys are stored in the same way as for regular Corda nodes in the `certificates`
directory. You can find out more in the [Network certificates](../permissioning.md) document.
