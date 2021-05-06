---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-notary-operate
tags:
- backup
- restore
title: Highly-available notary backup and restore
weight: 1
---


# Highly-available notary backup and restore

The HA Notary consists of two types of components:


* Worker (Corda) nodes
* Replicated database nodes

The worker nodes (1) don’t store any standard notarisation-related data locally, so no backup is strictly required – if a worker node gets corrupted or encounters data loss it can be decommissioned and replaced with a new worker node. However, it is good practice to at least back up the node CA keys, so no new node registration with the network operator is required.

All notarisation-related data is stored in the shared replicated database (2). The database should be set up with synchronous replication and strong consistency guarantees across nodes, so that multiple identical copies of the entire data-set is maintained at all times.
Loss of a single machine or hard drive corruption therefore would be tolerated by default.
However, to prevent protocol and human errors, e.g. an administrator accidentally dropping a table, periodic backups should be taken.

Additionally, it is critical to have a backup of the Notary Service identity private key, which is shared by all the worker nodes. If lost, all states assigned to the notary will be permanently frozen.

The following diagram highlights in blue which storage components should be backed up.

{{< figure alt="storage components" zoom="../resources/storage-components.png" >}}
Note that for regular nodes it is very important to back up the Messaging Broker (Artemis) folder and the local Database, but for HA notary nodes that are purely used for notarisation purposes that is not needed.

To summarise:


* For worker nodes: it is essential to back up the `certificates` directory, `node.conf` can also be backed up for convenience when restoring. To restore a worker node, re-create the node directory with the right Corda jar and drivers, and place the `certificates` folder and `node.conf`. Start the node as normal.
* For the replicated notary database: periodic backups should be setup for the whole data-set. To restore the replicated notary database, follow the database vendor specific instructions.

