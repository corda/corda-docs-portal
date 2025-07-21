---
aliases:
- /cenm-backup-recommendations.html
date: '2024-06-12'
menu:
  cenm-1-7:
    identifier: cenm-1-7-cenm-backup-recommendations
    parent: cenm-1-7-operations
    weight: 185
tags:
- backup
title: CENM backup recommendations
---

# CENM backup recommendations

Various components of CENM read their configuration from the file system, and persist data to a database or to files on disk.
Given that hardware can fail, operators of IT infrastructure must have a sound backup strategy in place. CENM holds important network information, such as approved and revoked network participants, the network map, and network parameters. This is another reason why R3 strongly recommends implementing a comprehensive backup strategy.

The following elements of a backup strategy are recommended:


### Database replication

When properly configured, database replication prevents data loss from occurring in case the database host fails.
In general, the higher the number of replicas, and the further away they are deployed in terms of regions and availability zones, the more a setup is resilient to disasters.
The trade-off is that, ideally, replication should happen synchronously, meaning that a high number of replicas and a considerable network latency will impact the performance of the CENM services connecting to their databases.
Synchronous replication is strongly advised to prevent data loss.


### Database snapshots

Database replication is a powerful technique, but it is very sensitive to destructive SQL updates. Whether malicious or unintentional, a SQL statement might compromise data by getting propagated to all replicas.
Without rolling snapshots, data loss due to such destructive updates will be irreversible.
Using snapshots always implies some data loss in case of a disaster, and the trade-off is between highly frequent backups minimising such a loss, and less frequent backups consuming less resources.


### File backups

CENM services read and write information to and from the file-system. R3 recommends backing up the entire directory of the service, plus any external directories and files optionally specified in the configuration.
CENM assumes the file system is reliable. You must ensure that it is configured to provide this assurance, which means you must configure it to synchronously replicate to your backup/DR site.
If the above holds, CENM services will benefit from the following:

* Guaranteed eventual processing of acknowledged messages, provided that the backlog of persistent queues is not lost irremediably.
* A timely recovery from deletion or corruption of configuration files (for example, `networkmap.conf`, `network-parameters.conf` files, and so on), database drivers, plugin binaries and configuration, and certificate directories, provided backups are available to restore from.

{{< warning >}}
Private keys used to sign CSRs, CRLs, new network maps and parameters should be preserved with the utmost care. R3 recommends keeping at least two separate copies on a storage not connected to the Internet.
{{< /warning >}}
