---
description: "Learn what is Transaction Validator Utility and its different uses."
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

To avoid post-migration errors when upgrading to Corda 4.12, you must validate transactions committed to the database first. You can do this by running the Transaction Validator Utility (TVU) on your current Corda database. If no errors are detected during the inspection of your backchain, you can proceed with the migration. However, if you find issues, you must investigate and resolve them to ensure an error-free upgrade.

TVU's useful features include:

* **Transaction validation:** Can validate (verify and deserialize) transactions by streaming them from the database. Database credentials are read directly from the `node.conf` file. See [transaction validation CLI example]({{< relref "tvu-cli-examples.html#transaction-validation" >}}).
* **Progress registration:** Registers its runtime progress with reference to the number of transactions processed. See [progress registration CLI example]({{< relref "tvu-cli-examples.html#progress-registration" >}}).
* **Progress reloading:** Can be paused and resumed at a later point in time. This is particularly useful because the number of transactions can be high (possibly millions). See [progress reloading CLI example]({{< relref "tvu-cli-examples.html#progress-reloading" >}}).
* **Transaction time loading:** Can start processing transactions from a supplied transaction time. This is particularly useful because the number of transactions can be high (possibly millions). See [transaction time loading CLI example]({{< relref "tvu-cli-examples.html#transaction-time-loading" >}}).
* **Reverification using transaction ID:** Can verify only certain transactions specified in a newline-separated transaction ID text file. The utility only processes transactions with the transaction IDs in these files. See [reverification using transaction ID CLI example]({{< relref "tvu-cli-examples.html#reverification-using-transaction-id" >}}).
* **Error registration:** Can register any errors relating to transaction validation in a `.zip` file. This error `.zip` file stores erroneous transactions’ raw data. See [error registration CLI example]({{< relref "tvu-cli-examples.html#error-registration" >}}).
* **Erroneous transaction reverification:** Can revalidate the erroneous transactions specified in an error `.zip` file. See [erroneous transaction reverification CLI example]({{< relref "tvu-cli-examples.html#erroneous-transaction-reverification" >}}).
* **Transaction processor:** Can act as a transaction processor, performing user-supplied tasks on each transaction. All the functionalities detailed in the previous points, that is, progress registration/reloading, error registration, and ID re-verification work for this mode as well. See [transaction processor CLI example]({{< relref "tvu-cli-examples.html#transaction-processor" >}}).
