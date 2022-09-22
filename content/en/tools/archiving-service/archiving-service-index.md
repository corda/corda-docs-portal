---
date: '2021-04-24T00:00:00Z'
section_menu: tools
menu:
  tools:
    name: The Archive Service
    weight: 700
    identifier: tools-archiving
title: The Archive Service
---

# The Archive Service

The Archive Service allows you to make an archive of transactions and attachments from the Corda vault which can no longer be part of an ongoing or new transaction flow. This can reduce pressure on your node’s database, and declutter your vault.

You can use Archive service commands to mark archivable items in your vault, archive them, and restore transactions from the archive when necessary.

The Archive Service consists of the following:

* **Archive Service CorDapp** - Contains the necessary flows to mark and archive transactions.
* **Archive Service Client Library** - Provides programmatic access to the archive service, and exposes relevant APIs.
* **Archive Service Command-Line Interface** - Allows you to perform archiving tasks from the command line.

It also makes use of the Application **Entity Manager**, which allows CorDapps to access off-ledger databases using JPA APIs.

Read the full documentation about [The Archive Service](../../../en/platform/corda/4.8/enterprise/node/archiving/archiving-setup.md).
