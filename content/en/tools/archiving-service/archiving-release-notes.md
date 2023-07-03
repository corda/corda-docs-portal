---
date: '2023-06-14'
menu:
  tools:
    identifier: release-notes-archiving
    parent: tools-archiving
    name: "Release notes"
title: Archive Service release notes
weight: 705
---

# Archive Service release notes

The Archive Service is a standalone service that operates on a different release cadence to the Corda platform.

## Archive Service 1.0.5

In this release:

* Previously, an issue occurred where the Archive Service misunderstood reference states. This would prevent a transaction from being archivable if it referenced an unconsumed transaction and did not have any unconsumed transactions that referenced it.

 Now, a transaction that only has outbound references (to unconsumed transactions) and no inbound references (from unconsumed transactions) will be marked as archivable by the Archive Service. Any inbound references will still make a transaction unarchivable.

## Archive Service 1.0.4

In this release:

* Previously, when using a Microsoft SQL Server database, an error was generated when using the `vault-states` filter with a positive value specified for the `retentionDays` parameter; this issue has been resolved.

## Archive Service 1.0.3

In this release:

* A new configuration option has been added which allows the Archive Service to ignore transactions that cause failures when exporting a JSON snapshot. For more information, see the [Archive Service]({{< relref "archiving-service-index.md#new-in-v103" >}}) documentation.

## Archive Service 1.0.2

In this release:

* Improved Archiving support of tokens when they are moved between more than one party and then redeemed.
* Logging of the Archiving tool has been increased to aid in troubleshooting.
* The Archiving client can now connect to nodes which are set up to use RPC SSL connection settings.
* Tables are now ordered by table name length in descending order to prevent foreign key constraints from being violated when deleting rows.
