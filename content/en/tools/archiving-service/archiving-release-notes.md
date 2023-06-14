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

* Fixed an issue where the Archive Service would misunderstand reference states when part of transactions. The Archive Service will now correctly allow a transaction to be archived even if it still has unconsumed outbound references; that is, it references a transaction that is still unconsumed. The behavior will still be the same for any unconsumed transaction that references the transaction (inbound): in this scenario, it will still be unarchivable.

## Archive Service 1.0.4

In this release:

* Previously, when using a Microsoft SQL Server database, an error was generated when using the `vault-states` filter with a positive value specified for the `retentionDays` parameter; this issue has been resolved.

## Archive Service 1.0.3

In this release:

* A new configuration option has been added which allows the Archive Service to ignore transactions that cause failures when exporting a JSON snapshot. For more information, see the [Archive Service]({{< relref "archiving-service-index.md#new-in-v103" >}}) documentation.

## Archive Service 1.0.2

### Fixed issues

In this release:

* Improved Archiving support of tokens when they are moved between more than one party and then redeemed.
* Logging of the Archiving tool has been increased to aid in troubleshooting.
* The Archiving client can now connect to nodes which are set up to use RPC SSL connection settings.
* Tables are now ordered by table name length in descending order to prevent foreign key constraints from being violated when deleting rows.
