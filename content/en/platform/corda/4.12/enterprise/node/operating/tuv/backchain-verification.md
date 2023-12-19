---
date: '2023-12-15'
section_menu: corda-enterprise-4-12
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-backchain-verification
    parent: corda-enterprise-4-12-tuv
tags:
- backchain
- tuv
- transaction validator utility
title: Backchain verification
weight: 500
---

# Backchain verification

node's verification method - nodes takes txs from vault, uses verification method

provide datasourse

validation

## Load progress file

Load the register.txt file containing saved validation progress and where the resumed progress will be loaded to.

Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=party_a -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource -l register.txt --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs`

## Re-verify transaction IDs

Re-verify specific transaction IDs provided to the TVU in a text file.

Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=party_a -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs -i Ids.txt`

## Register errors

Register verification/deserialization errors while processing transactions.

Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=party_a -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs`

## Resume validation from the provided time

Load transactions greater than or equal to the provided transaction time.

Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=party_a -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs --load-tx-time 2023-10-10T10:41:39.808179Z`
