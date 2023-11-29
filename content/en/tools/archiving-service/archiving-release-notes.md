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

The Archive Service compatibility with Corda Enterprise:

| Archive Service version      | Corda Enterprise version    |
|------------------------------|-----------------------------|
| 1.0.x                        | 4.10 and below              |
| 1.1.x                        | 4.11 and above              |

{{< note >}}
If you deviate from the above compatibility guidelines, for example, using the Archive Service 1.1.x with Corda Enterprise 4.10, the Archive Service will not work.
{{< /note >}}

## Corda Enterprise 4.11 and above

### Archive Service 1.1

In this release:

* Version 1.1 is a compatibility release of the Archive Service. This and all future 1.1.x releases will only work with Corda 4.11 and above and will not be compatible with Corda Enterprise 4.10.x and below. Use the latest Archive Service 1.0.x for Corda Enterprise 4.10.x and below.
* In Corda Enterprise 4.11 a new column has been added to the node transactions table for additional signatures. The new Archive Service release includes this new column in its snapshot data.

## Corda Enterprise 4.10 and below

### Archive Service 1.0.5

In this release:

* Previously, an issue occurred where the Archive Service misunderstood reference states. This would prevent a transaction from being archivable if it referenced an unconsumed transaction and did not have any unconsumed transactions that referenced it.

  Now, a transaction that only has outbound references (to unconsumed transactions) and no inbound references (from unconsumed transactions) will be marked as archivable by the Archive Service. Any inbound references will still make a transaction unarchivable.

### Archive Service 1.0.4

In this release:

* Previously, when using a Microsoft SQL Server database, an error was generated when using the `vault-states` filter with a positive value specified for the `retentionDays` parameter; this issue has been resolved.

### Archive Service 1.0.3

In this release:

* A new configuration option has been added which allows the Archive Service to skip transactions that have legacy contract states that cause exceptions during a JSON snapshot export. This configuration option is: `ignoreSnapshotExportFailures: true`.

By default, this value is false and the behaviour of the Archive Service is unchanged. However, if you are experiencing a `TransactionDeserializationException` or a `JsonMappingException` during the export of a JSON snapshot, this configuration option can be added to skip these transactions for a successful export. These transactions won’t be included in the export, but if a binary export is also created, all transactions can be preserved.

### Archive Service 1.0.2

In this release:

* Improved Archiving support of tokens when they are moved between more than one party and then redeemed.
* Logging of the Archiving tool has been increased to aid in troubleshooting.
* The Archiving client can now connect to nodes which are set up to use RPC SSL connection settings.
* Tables are now ordered by table name length in descending order to prevent foreign key constraints from being violated when deleting rows.

### Archive Service 1.0.1

In this release:

* The Archive Service is compatible with [Ledger Graph V1.2.1 On Demand function]({{< relref "archiving-service-index.html#archiving-and-ondemand-ledgergraph" >}}).
