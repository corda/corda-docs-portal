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

This topic lists the currently-available network parameters, in alphabetical order:

## `confidentialIdentityMinimumBackupInterval`

The `confidentialIdentityMinimumBackupInterval` network parameter is an optional parameter of type `Duration`. It specifies the minimum age of a generated Confidential Identity key before it can be used. This can be overridden in the node configuration or if a more recent database backup is indicated via RPC/shell.

This parameter is optional in both the network parameters and the node configuration. If no value is specified for either, then it is assumed to be zero.

For example:

```
confidentialIdentityMinimumBackupInterval = 5d
```

or

```
confidentialIdentityMinimumBackupInterval = 30d
```

## `epoch`

The version number of the network parameters. Starting from 1, this will always increment whenever any of the
parameters change.

## `eventHorizon`

The time after which nodes are considered to be unresponsive and removed from the network map. Nodes republish their
`NodeInfo` on a regular interval. The network map treats that as a heartbeat from the node.

## `maxMessageSize`

The maximum allowed size in bytes of an individual message sent over the wire.

## `maxTransactionSize`

The maximum allowed size in bytes of a transaction. This is the size of the transaction object and its attachments.

## `minimumPlatformVersion`

The minimum platform version that the nodes must be running. Any node which is below this will not start.

   {{< note >}}
   To determine which `minimumPlatformVersion` a zone must mandate in order to permit all the features of Corda 4.11, see [Corda versioning]({{< relref "../cordapps/versioning.md" >}}).
   {{< /note >}}

## `modifiedTime`

The time when the network parameters were last modified by the compatibility zone operator.

## `notaries`

The list of identity and validation types (either validating or non-validating) of the notaries which are permitted
in the compatibility zone.

## `recoveryMaximumBackupInterval`

The `recoveryMaximumBackupInterval` network parameter is an optional parameter of type `Duration`, and is used by [Ledger Recovery]({{< relref "../node/collaborative-recovery/ledger-recovery/overview.md" >}}). It specifies how far back in time the recovery process should consider. When attempting a recovery, a node will only restore to a database backup more recent than this value.

This value can be overridden by specifying an override in the flow. It can also be overridden for a particular node if the same parameter is specified in the node configuration; the node configuration takes precedence over the network configuration. An override to the flow takes priority over values in either the network configuration or node configuration.

The parameter is optional in both the network parameters and the node configuration. However, if no values are set then it needs to be specified in the flow.

For example:

```
recoveryMaximumBackupInterval = 5d
```
or
```
recoveryMaximumBackupInterval = 30d
```

## `packageOwnership`

The list of the network-wide Java packages that were successfully claimed by their owners.
Any CorDapp JAR that offers contracts and states in any of these packages must be signed by the owner.
This ensures that when a node encounters an owned contract, it can uniquely identify it and knows that all other nodes can do the same.
Encountering an owned contract in a JAR that is not signed by the rightful owner is most likely a sign of malicious behavior, and should be reported.
The transaction verification logic will throw an exception when this happens.
Read more about package ownership in the [Package namespace ownership]({{< relref "../node/deploy/env-dev.md#package-namespace-ownership" >}}) section.

## `whitelistedContractImplementations`

The list of whitelisted versions of contract code.
For each contract class there is a list of SHA-256 hashes of the approved CorDapp JAR versions containing that contract.
For more information about zone constraints, see [Contract constraints]({{< relref "../cordapps/api-contract-constraints.md" >}}).







