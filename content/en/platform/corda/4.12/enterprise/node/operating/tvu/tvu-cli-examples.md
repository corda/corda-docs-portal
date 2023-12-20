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

## Deserialize transactions using a CorDapp

Intent:
* Connect to the datasource given (`-d` option).
* Register and reload progress from the `register.txt` file (`-l` option).
* Use CorDapp in `/Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs` directory to deserialize transactions (`--cordapp-dir` option).

Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=postgres -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource -l register.txt --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs`

## Load transactions for a given timestamp

Intent:
* Connect to the node database from reading `node.conf` in `/Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA` (`-b` option).
* Load transactions having transaction time greater than or equal to `2023-10-10T10:41:39.808179Z` (`--load-tx-time` option).

Command: `-b /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA --load-tx-time 2023-10-10T10:41:39.808179Z`

## Load transactions from a specific file

Intent:
* Connect to the node database from reading `node.conf` in `/Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA` (`-b` option).
* Only load transactions given in `/Users/suhas.srivastava/IdeaProjects/corda/enterprise/Ids.txt` file (`-i` option).

Command: `-b /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA  -i /Users/suhas.srivastava/IdeaProjects/corda/enterprise/Ids.txt`

## Perform user-supplied task

Intent:
* Connect to the node database from reading `node.conf` in `/Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA` (`-b` option).
* Do not validate transactions but perform a user-supplied task defined in the `net.corda.tvu.LogTransaction` class for each transaction.

Command: `-b /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/nodes/PartyA -c net.corda.tvu.LogTransaction`
