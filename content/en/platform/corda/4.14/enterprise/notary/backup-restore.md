---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-corda-nodes-notary-operate
tags:
- backup
- restore
title: Backing up and restoring highly-available notaries
weight: 1
---


# Backing up and restoring highly-available notaries

The HA notary consists of two types of components:


* Worker (Corda) nodes
* Replicated database nodes

The worker nodes do not store any standard notarisation-related data locally, so no backup is strictly required. If a worker node gets corrupted or encounters data loss, it can be decommissioned and replaced with a new worker node. However, it is good practice to at least back up the node CA keys, so no new node registration with the network operator is required.

All notarisation-related data is stored in the shared replicated database. The database should be set up with synchronous replication and strong consistency guarantees across nodes, so that multiple identical copies of the entire data-set is maintained at all times.
Loss of a single machine or hard drive corruption therefore would be tolerated by default.
However, to prevent protocol and human errors; for example, an administrator accidentally dropping a table, periodic backups should be taken.

Additionally, it is critical to have a backup of the Notary Service identity private key, which is shared by all the worker nodes. If lost, all states assigned to the notary will be permanently frozen.

The following diagram highlights in blue which storage components should be backed up.

{{< figure alt="storage components" width=80% zoom="../resources/storage-components.png" >}}
Note that for regular nodes it is very important to back up the Messaging Broker (Artemis) folder and the local database, but for HA notary nodes that are purely used for notarisation purposes that is not needed.

To summarise:

- **For worker nodes:** It is essential to back up the `certificates` directory. `node.conf` can also be backed up for convenience when restoring. To restore a worker node:
  1. Re-create the node directory with the right Corda JAR and drivers.
  2. Place the `certificates` folder and `node.conf` there.
  3. Start the node as normal.
- **For the replicated notary database:** Periodic backups should be setup for the whole data-set. To restore the replicated notary database, follow the database vendor specific instructions.

