---
cascade:
  version: 'Enterprise 4.14'
  project: Corda
  section_menu: corda-enterprise-4.14
description: "Learn what the Transaction Validator Utility is and its different uses."
title: "Transaction Validator Utility"
date: '2023-12-15'
menu:
  corda-enterprise-4.14:
    identifier: corda-enterprise-4.14-tvu
    parent: corda-enterprise-4.14-corda-nodes-operating
weight: 130
tags:
- tvu
- transaction validator utility
---

# Transaction Validator Utility

{{< note >}}
In version 4.12, the Transaction Validator Utility was required when performing [an upgrade from 4.11 to 4.12]({{< relref "../../../../../4.12/enterprise/upgrade-guide.md" >}}). However, for an upgrade from 4.13 to 4.14, the tool is not required. Its purpose in 4.14 is to offer the following features.
{{< /note >}}

TVU's useful features include:

* **Transaction validation:** Can validate (verify and deserialize) transactions by streaming them from the database. Database credentials are read directly from the `node.conf` file. See [transaction validation CLI example]({{< relref "tvu-cli-examples.md#transaction-validation" >}}).
* **Progress registration:** Registers its runtime progress with reference to the number of transactions processed. See [progress registration CLI example]({{< relref "tvu-cli-examples.md#progress-registration" >}}).
* **Progress reloading:** Can be paused and resumed at a later point in time. This is particularly useful because the number of transactions can be high (possibly millions). See [progress reloading CLI example]({{< relref "tvu-cli-examples.md#progress-reloading" >}}).
* **Transaction time loading:** Can start processing transactions from a supplied transaction time. This is particularly useful because the number of transactions can be high (possibly millions). See [transaction time loading CLI example]({{< relref "tvu-cli-examples.md#transaction-time-loading" >}}).
* **Reverification using transaction ID:** Can verify only certain transactions specified in a newline-separated transaction ID text file. The utility only processes transactions with the transaction IDs in these files. See [reverification using transaction ID CLI example]({{< relref "tvu-cli-examples.md#reverification-using-transaction-id" >}}).
* **Error registration:** Can register any errors relating to transaction validation in a `.zip` file. This error `.zip` file stores erroneous transactions’ raw data. See [error registration CLI example]({{< relref "tvu-cli-examples.md#error-registration" >}}).
* **Erroneous transaction reverification:** Can revalidate the erroneous transactions specified in an error `.zip` file. See [erroneous transaction reverification CLI example]({{< relref "tvu-cli-examples.md#erroneous-transaction-reverification" >}}).
* **Transaction processor:** Can act as a transaction processor, performing user-supplied tasks on each transaction. All the functionalities detailed in the previous points, that is, progress registration/reloading, error registration, and ID re-verification work for this mode as well. See [transaction processor CLI example]({{< relref "tvu-cli-examples.md#transaction-processor" >}}).
