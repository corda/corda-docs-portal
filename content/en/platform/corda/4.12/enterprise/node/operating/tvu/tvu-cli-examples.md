---
date: '2023-12-20'
section_menu: corda-enterprise-4-12
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tvu-cli-examples
    parent: corda-enterprise-4-12-tvu-cli
tags:
- tvu cli
- tvu
- transaction validator utility
title: TVU CLI command examples
weight: 100
---

# TVU CLI command examples

The TVU tool streams and validates all the transactions from a provided database. This database can be provided directly by the user using `-d` or `--datasource` CLI option or can be picked up from a `node.conf` file when the node’s base directory is given using the `-b` or `--base-directory` CLI option.

The following section provides you with the examples of how you can use the TVU CLI commands in practice. You can modify and use the provided TVU CLI command examples so they work in your project.

## Verify all transactions in a database

This example shows how to:
* Verify all transactions in a database and record the progress.

Command: `java -jar transaction-validator.jar -d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=postgres -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource -l register.txt --cordapp-dir /Users/cordallp/corda/IdeaProjects/corda/cordapp-template-java/build/libs`

## Verify transactions from a given timestamp

This example shows how to:
* Connect to the node database from reading `node.conf` in `/Users/cordallp/corda/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA` (`-b` option).
* Load transactions having transaction time greater than or equal to `2023-10-10T10:41:39.808179Z` (`--load-tx-time` option).

Command: `java -jar transaction-validator.jar -b /Users/cordallp/corda/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA --load-tx-time 2023-10-10T10:41:39.808179Z`

## Verify specific identified transactions

This example shows how to:
* Verify transactions in a database where database is identified by datasource parameters.

Command: `java -jar transaction-validator.jar -d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=postgres -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource -i /Users/cordallp/corda/IdeaProjects/corda/enterprise/Ids.txt`

## Perform user-supplied task

This example shows how to:
* Connect to the node database from reading `node.conf` in `/Users/cordallp/corda/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA` (`-b` option).
* Do not validate transactions but perform a user-supplied task defined in the `net.corda.tvu.LogTransaction` class for each transaction.

Command: `-b /Users/cordallp/corda/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA -c net.corda.tvu.LogTransaction`
