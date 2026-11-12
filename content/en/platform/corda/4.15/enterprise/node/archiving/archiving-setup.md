---
date: '2020-12-10T12:00:00Z'
menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-corda-nodes-archive-service
    name: "Archive Service"
    parent: corda-enterprise-4-15-corda-nodes
tags:
- archive
- backup schema
- archive install
- archive transactions

title: Archive Service
weight: 150
---

# The Archive Service

The Archive Service allows you to make an archive of transactions and attachments from the Corda vault which can no longer be part of an ongoing or new transaction flow. This can reduce pressure on your node’s database, and declutter your vault.

You can use Archive service commands to mark archivable items in your vault, archive them, and restore transactions from the archive when necessary.

The Archive Service consists of the following:

* **Archive Service CorDapp** - Contains the necessary flows to mark and archive transactions.
* **Archive Service Client Library** - Provides programmatic access to the archive service, and exposes relevant APIs.
* **Archive Service Command-Line Interface** - Allows you to perform archiving tasks from the command line.

It also makes use of the Application **Entity Manager**, which allows CorDapps to access off-ledger databases using JPA APIs.

{{< note >}}
Corda Enterprise 4.15 requires Archive Service 2.0.1 or later. Earlier Archive Service versions refer to Hibernate 5 classes that the node's Hibernate 7 no longer has, and the node refuses to load them. See the [Archive Service release notes]({{< relref "../../../../../../tools/archiving-service/archiving-release-notes.md#archive-service-201" >}}).
{{< /note >}}

Read the full documentation about [The Archive Service]({{< relref "../../../../../../tools/archiving-service/archiving-service-index.md" >}})
