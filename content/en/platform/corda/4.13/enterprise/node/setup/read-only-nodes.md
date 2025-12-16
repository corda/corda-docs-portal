---
date: '2025-10-20'
menu:
  corda-enterprise-4-13:
    parent: corda-enterprise-4-13-corda-nodes-configuring
tags:
- corda
- configuration
- file
title: Read-only nodes
weight: 100
---

# Read-only nodes

This topic describes read-only nodes, why they might be required, and how to configure a node to be read-only.

Making a node read-only is a feature that is used for many reasons, including the following:

- [Making nodes read-only for regulatory reasons]({{< relref "#making-nodes-read-only-for-regulatory-reasons" >}})
- [Making nodes real-only for scalable reporting solutions]({{< relref "#making-nodes-real-only-for-scalable-reporting-solutions" >}})

## Making nodes read-only for regulatory reasons

Sometimes you may want to configure a node on a network so that it has no more involvement in new transactions, but there is still a regulatory requirement to keep its data available for further use. Corda ledger data is not easily interpreted outside of a Corda node because it is stored as binary blobs in an AMQP encoding. It is possible to interpret that data externally, but we currently provide no such tooling. Keeping the node online in the network is not a good option, as it continues to be an active participant in the network and could participate in new transactions on the ledger.

It is possible to re-configure a node as read-only, with no ability to mutate data or participate with peers, but continue to perform vault queries or other reporting operations (read-only flows) to aid with data extraction or regulatory investigations.

## Making nodes real-only for scalable reporting solutions

Using a read-only node can be a way to provide a scalable reporting solution. 

One node handles transactions, while one node is dedicated to handling database queries for reporting purposes. The database for the reporting node is replicated to a read-only database replica, and the reporting node that queries the read-only database replica is set to be read-only. 

The purpose of this is so the database queries, which may take a long time, do not block the database transactions traffic; this might happen if only one node was used for transactions and for reporting. This scenario keeps reporting workloads fully segregated from transactional workloads, and is an easy route to getting additional scalability.

## Impact of being a read-only node

Read-only nodes have the following restrictions versus normal nodes:

- A read-only node is not visible on the peer-to-peer network. 
- It does not open its related port.
- It does not register on the network. 
- It does not advertise itself.
- it does not get updates from the network.
- All of its knowledge about the network and its participants comes from its configuration and database, as well as the network map cache.
- Although if its database is a replication of a live node, it can get fresh information about the network through the database.
- It is not accessible to other nodes.
- All initiateFlow operations are disabled.
- Its JDBC connection is in read-only mode.
- All signing with private keys or key pair generation is disabled.
- The following RPC operations are disabled:
   - clearRPCAuditDataBefore
   - collectRPCAuditData
   - collectRPCAuditDataWithPaging
   - acceptNewNetworkParameters
   - networkParametersFeed
   - addVaultTransactionNote
   - uploadAttachment
   - uploadAttachmentWithMetadata
   - refreshNetworkMapCache
   - setFlowsDrainingModeEnabled
   - terminate with drainingMode = true
   - recoverFinalityFlow
   - recoverFinalityFlows
   - recoverAllFinalityFlows
   - recoverFinalityFlowByTxnId
   - recoverFinalityFlowByTxnIds
   - recoverFinalityFlowsMatching
   - acknowledgeDatabaseBackup
   - markAllKeysUsed

- The [clearNetworkMapCache]({{< relref "../../network/network-map.md#cleaning-the-network-map-cache" >}}) operation clears only the in-memory network map cache, leaving the database intact. In read-only mode, the network map cache's entries expire in 5 minutes to let the node pick up fresh information replicated into its database from live nodes, if there is any.
- The [RPC audit functionality]({{< relref "rpc-audit-data-recording.md" >}}) writes its audit entries into the node's logs, instead of the database. The related log entries come from `ReadOnlyAuditServiceImpl` class. Also, related RPC operations are disabled.
- The node vault's produced states cache is disabled to prevent any stale data from being stored in memory.
- The node's internal checkpoint storage has been replaced by an in-memory one, which does not persist. That also means that flows cannot be restored, continued across restarts.
- Freshly installed CorDapps are not registered in the database, but only in memory.
- The Token SDK [in-memory selection]({{< relref "../../cordapps/token-selection.md#move-tokens-using-in-memory-selection" >}}) cannot be used.

## Read-only node disabled functionality

Read-only nodes have the following functionalities disabled:

- Draining mode
- Notary
- Metering
- Scheduler
- Maintenance functionalities
- System flows
- Ledger recovery
- Key pair pre-generator
- Schema sync, database migrations, upgrades
- Mutual exclusions

## Making a node read-only

To make a node read-only, perform the following steps:

1. [Prepare the node database](#prepare-the-node-database)
2. Either: 
   - [Configure readOnlyMode to true]({{< relref "#configure-readonlymode-to-true" >}}), *or*
   - [Run the node in read-only mode from the CLI]({{< relref "#running-the-node-in-read-only-mode-from-cli" >}} )
   
### Prepare the node database

To make a node read-only, first its database must be preinitialised. This preinitialization can happen when:

- Restoring the database from a backup
- Replicating a normal node's database
- Configuring a normal node to a read-only node while keeping its database intact

The node's network map cache in the database must have an entry matching the node's `myLegalName` configuration option. The previous options all satisfy this, assuming the read-only node's `myLegalName` stays the same as the original node's one.

The node will not run any mutating operations on the database; however, the CorDapps installed by end-users may contain mutating queries.
To restrict any unintentional mutating operations, it is recommended to ensure the read-only state of the database by either:

- Restricting the database user specified in the configuration's [dataSourceProperties]({{< relref "corda-configuration-fields.md#datasourceproperties" >}}) section from having any mutating privileges, *or*
- Setting the database itself to run in read-only mode.

The Corda node will turn on the `readOnly` property of the database connection, but some database servers treat this only as a hint, and they do not restrict mutating operations. For example, SQL Server does not support this flag.

### Removing nodekeystore and HSH keystore

It is recommended to remove the [node keystore]({{< relref "../../network/permissioning.md#key-pair-and-certificate-formats" >}}) and the related [HSH keystore]({{< relref "../operating/cryptoservice-configuration.md" >}}) from the read-only node's configuration. A read-only node needs an SSL keystore whose key will be used for the internal TLS server. These keys may differ from the original node's SSL keys.

### Configure readOnlyMode to true

In the node configuration, set *[readOnlyMode]({{< relref "corda-configuration-fields.md#readonlymode" >}})* to true as shown in the following example:

```
enterpriseConfiguration {
    readOnlyMode=true
}
```
   
### Running the node in read-only mode from CLI

Instead of changing the node configuration, you can start a node in read-only mode by using the `--readonly-mode` flag.

## Read-only node output

A read-only node will display the following line when started in read-only mode:

`Read-only mode is set to true.`

Also, instead of the normal message `Running P2PMessaging loop`, the node displays the following message when it is ready:

`Blocking main thread until stop() is called`

### Checking a node is read-only

The `isReadOnlyNode` [RPC operation]({{<  relref "../operating/clientrpc.md" >}}) allows you to check the read-only status of a node. `isReadOnlyNode` returns true if the node is configured read-only, otherwise false.
