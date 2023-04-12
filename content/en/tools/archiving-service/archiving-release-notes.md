---
date: '2020-12-10T12:00:00Z'
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
