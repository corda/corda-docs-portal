---
date: '2023-12-15'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tuv
    parent: corda-enterprise-4-12-corda-nodes-operating
tags:
- tuv
- transaction validator utility
title: Transaction Validator Utility
weight: 130
---

# Transaction Validator Utility

Corda 4.12 has been released and is compatible with JDK 17 and Kotlin 1.8. Therefore, migrating to Corda 4.12 means that you must update to a newer JDK and Kotlin version to align with the updated Corda dependencies.

You must also ensure that the transactions committed to the database using the older Corda version are valid, verifiable and deserializable post-migration, before migrating to Corda 4.12. You can do it using Transaction Validator Utility (TVU) introduced as part of the Corda 4.12 release. TVU streams database transactions and performs validation on them. Its useful features include:

* Transaction validation: Can validate (verify and deserialize) transactions by streaming them from the database. The database credentials can be provided by the user as Hikari properties or can be read directly from a node using its node.conf.
* Progress registration: The utility registers its runtime progress with reference to the number of transactions processed.
* Progress reloading: Since the number of transactions can be high (possibly millions), the utility can be paused and resumed at a later point in time.
* Transaction time loading: Since the number of transactions can be high (possibly millions), the utility can start processing transactions from a supplied transaction time.
* ID re-verification: There may be a need to verify only certain transactions, hence the utility can be supplied with a newline-separated transaction ID file. Only transactions with the transaction IDs provided in this file will be processed.
* •	Error registration: The utility can register any errors relating to transaction validation in a `.zip` file. This error `.zip` file stores erroneous transactions’ raw data.
•	Erroneous transaction re-verification: If there is a need to re-validate the erroneous transactions, provide the utility with an error `.zip` file containing those transactions.
•	Transaction processor: Apart from performing validation on transactions, the utility can also act as a transaction processor, performing user-supplied tasks on each transaction. All the functionalities detailed in the previous points, that is, progress registration/reloading, error registration and ID re-verification work for this mode as well.
