---
date: '2023-12-15'
section_menu: corda-enterprise-4-12
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-backchain-verification
    parent: corda-enterprise-4-12-tvu
tags:
- backchain
- tvu
- transaction validator utility
title: Backchain verification
weight: 500
---

# Backchain verification

The following section walks you through the backchain verification process using the TVU CLI commands. The Corda node itself performs transaction verification when downloading transactions in a back chain.

1. Load the `register.txt` file containing saved validation progress and where the resumed progress will be loaded to.

    Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=party_a -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource -l register.txt --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs`

2. Re-verify specific transaction IDs provided to the TVU in a text file.

    Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=party_a -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs -i Ids.txt`

3. Register verification/deserialization errors while processing transactions.

    Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=party_a -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs`

4. Load transactions greater than or equal to the provided transaction time.

    Command: `-d dataSource.url=jdbc:postgresql://localhost:5432/postgres -d dataSource.user=party_a -d dataSource.password=my_password -d dataSourceClassName=org.postgresql.ds.PGSimpleDataSource --cordapp-dir /Users/suhas.srivastava/IdeaProjects/corda/cordapp-template-java/build/libs --load-tx-time 2023-10-10T10:41:39.808179Z`
