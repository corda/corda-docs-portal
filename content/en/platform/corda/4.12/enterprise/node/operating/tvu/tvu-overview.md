---
date: '2023-12-15'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tvu
    parent: corda-enterprise-4-12-corda-nodes-operating
tags:
- tvu
- transaction validator utility
title: Transaction Validator Utility
weight: 130
---

# Transaction Validator Utility

Corda 4.12 has been released on and is compatible with JDK 17 and Kotlin 1.8. Therefore, upgrading to Corda 4.12 from a previous version of Corda means that you must update to a newer JDK and Kotlin version to align with the updated Corda dependencies.

Before migrating to Corda 4.12, you must also ensure that the transactions committed to the database using the older Corda version are valid, verifiable and deserializable post-migration. You can do it using Transaction Validator Utility (TVU) which streams and performs validation on database transactions. TVU's useful features include:

* Transaction validation: Can validate (verify and deserialize) transactions by streaming them from the database. You can provide the database credentials as Hikari properties and they can also be read directly from a node using its `node.conf`.
* Progress registration: The utility registers its runtime progress with reference to the number of transactions processed.
* Progress reloading: Since the number of transactions can be high (possibly millions), the utility can be paused and resumed at a later point in time.
* Transaction time loading: Since the number of transactions can be high (possibly millions), the utility can start processing transactions from a supplied transaction time.
* Reverification using transaction ID: If you need to verify only certain transactions, you can supply the utility with a newline-separated transaction ID file. Only transactions with the transaction IDs provided in this file will be processed.
* Error registration: The utility can register any errors relating to transaction validation in a `.zip` file. This error `.zip` file stores erroneous transactions’ raw data.
* Erroneous transaction re-verification: If there is a need to re-validate the erroneous transactions, provide the utility with an error `.zip` file containing those transactions.
* Transaction processor: Apart from performing validation on transactions, the utility can also act as a transaction processor, performing user-supplied tasks on each transaction. All the functionalities detailed in the previous points, that is, progress registration/reloading, error registration and ID re-verification work for this mode as well.
