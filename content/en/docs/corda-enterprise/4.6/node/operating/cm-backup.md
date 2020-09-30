---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-corda-nodes-operating-cm
    name: "Change management for nodes"
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- cm
- backup
title: Backup and restoration of a Corda node
weight: 8
---


# Backup and restoration of a Corda node



Various components of the Corda platform read their configuration from the file system, and persist data to a database or into files on disk. Given that hardware can fail, operators of IT infrastructure must have a sound backup strategy in place. Whilst blockchain platforms can sometimes recover some lost data from their peers, it is rarely the case that a node can recover its full state in this way because real-world blockchain applications invariably contain private information (e.g., customer account information). Moreover, this private information must remain in sync with the ledger state. As such, we strongly recommend implementing a comprehensive backup strategy.

The following elements of a backup strategy are recommended:


## Database replication

When properly configured, database replication prevents data loss from occurring in case the database host fails.
In general, the higher the number of replicas, and the further away they are deployed in terms of regions and availability zones, the more a setup is resilient to disasters.
The trade-off is that, ideally, replication should happen synchronously, meaning that a high number of replicas and a considerable network latency will impact the performance of the Corda nodes connecting to the cluster.
Synchronous replication is strongly advised to prevent data loss.


## Database snapshots

Database replication is a powerful technique, but it is very sensitive to destructive SQL updates. Whether malicious or unintentional, a SQL statement might compromise data by getting propagated to all replicas.
Without rolling snapshots, data loss due to such destructive updates will be irreversible.
Using snapshots always implies some data loss in case of a disaster, and the trade-off is between highly frequent backups minimising such a loss, and less frequent backups consuming less resources.
At present, Corda does not offer online updates with regards to transactions.
Should states in the vault ever be lost, partial or total recovery might be achieved by asking third-party companies and/or notaries to provide all data relevant to the affected legal identity.


## File backups

Corda components read and write information from and to the file-system. The advice is to backup the entire root directory of the component, plus any external directories and files optionally specified in the configuration.
Corda assumes the filesystem is reliable. You must ensure that it is configured to provide this assurance, which means you must configure it to synchronously replicate to your backup/DR site.
If the above holds, Corda components will benefit from the following:


* Guaranteed eventual processing of acknowledged client messages, provided that the backlog of persistent queues is not lost irremediably.
* A timely recovery from deletion or corruption of configuration files (e.g., `node.conf`, `node-info` files, etc.), database drivers, CorDapps binaries and configuration, and certificate directories, provided backups are available to restore from.


{{< warning >}}
Private keys used to sign transactions should be preserved with the utmost care. The recommendation is to keep at least two separate copies on a storage not connected to the Internet.

{{< /warning >}}
