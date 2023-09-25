---
date: '2023-09-25'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-corda-networks-parameters
    identifier: corda-enterprise-4-11-corda-networks-parameters-available
tags:
- network
- map
title: Available network parameters
weight: 37
---

This topic lists the currently-available network parameters:

* **minimumPlatformVersion**:
The minimum platform version that the nodes must be running. Any node which is below this will
not start.

   {{< note >}}
   To determine which `minimumPlatformVersion` a zone must mandate in order to permit all the features of Corda 4.11, see [Corda versioning]({{< relref "../cordapps/versioning.md" >}}).
   {{< /note >}}

* **notaries**:
List of identity and validation type (either validating or non-validating) of the notaries which are permitted
in the compatibility zone.

* **maxMessageSize**:
Maximum allowed size in bytes of an individual message sent over the wire.

* **maxTransactionSize**:
Maximum allowed size in bytes of a transaction. This is the size of the transaction object and its attachments.

* **modifiedTime**:
The time when the network parameters were last modified by the compatibility zone operator.

* **epoch**:
Version number of the network parameters. Starting from 1, this will always increment whenever any of the
parameters change.

* **whitelistedContractImplementations**:
List of whitelisted versions of contract code.
For each contract class there is a list of SHA-256 hashes of the approved CorDapp jar versions containing that contract.
Read more about *Zone constraints* here api-contract-constraints

* **eventHorizon**:
Time after which nodes are considered to be unresponsive and removed from network map. Nodes republish their
`NodeInfo` on a regular interval. Network map treats that as a heartbeat from the node.

* **packageOwnership**:
List of the network-wide java packages that were successfully claimed by their owners.
Any CorDapp JAR that offers contracts and states in any of these packages must be signed by the owner.
This ensures that when a node encounters an owned contract it can uniquely identify it and knows that all other nodes can do the same.
Encountering an owned contract in a JAR that is not signed by the rightful owner is most likely a sign of malicious behaviour, and should be reported.
The transaction verification logic will throw an exception when this happens.
Read more about package ownership in the [Package namespace ownership]({{< relref "../node/deploy/env-dev.md#package-namespace-ownership" >}}) section.
