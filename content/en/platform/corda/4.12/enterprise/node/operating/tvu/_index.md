---
cascade:
  version: 'Enterprise 4.12'
  project: Corda
  section_menu: corda-enterprise-4-12
description: "Learn what the Transaction Validator Utility is and its different uses."
title: "Transaction Validator Utility"
date: '2023-12-15'
menu:
  corda-enterprise-4-12:
    identifier: corda-enterprise-4-12-tvu
    parent: corda-enterprise-4-12-corda-nodes-operating
weight: 130
tags:
- tvu
- transaction validator utility
---

# Transaction Validator Utility

{{< important >}}
Why must you run the Transaction Validator Utility (TVU) when upgrading?

If you are upgrading from a 4.11 Corda network, you must run the TVU on your 4.11 node database to verify that your transactions will successfully deserialize and verify using JDK17. Some classes within the JDK or your dependencies may serialize differently on JDK17 compared to JDK8. The purpose of this tool is to certify that this is **not** the case, and that your ledger is compatible with Corda 4.12. In the rare event that an issue arises, we will collaborate with you to develop a solution that facilitates the upgrade to Corda 4.12.

If you are upgrading from a pre-4.11 Corda network, and the result will be a mixed network of pre-4.11 and 4.12 nodes, you must perform validation steps on the older nodes to ensure compatibility with the upgraded nodes. See [Validating Corda 4.10 and earlier nodes]({{< relref "../../../upgrade-guide.md#validating-corda-410-and-earlier-nodes" >}}).
{{< /important >}}

To avoid post-migration errors when upgrading to Corda 4.12, you must first validate transactions committed to the database. You can do this by running TVU on your current Corda database. If no errors are detected during the inspection of your backchain, you can proceed with the migration.


TVU's useful features include:

* **Transaction validation:** Can validate (verify and deserialize) transactions by streaming them from the database. Database credentials are read directly from the `node.conf` file. See [transaction validation CLI example]({{< relref "tvu-cli-examples.md#transaction-validation" >}}).
* **Progress registration:** Registers its runtime progress with reference to the number of transactions processed. See [progress registration CLI example]({{< relref "tvu-cli-examples.md#progress-registration" >}}).
* **Progress reloading:** Can be paused and resumed at a later point in time. This is particularly useful because the number of transactions can be high (possibly millions). See [progress reloading CLI example]({{< relref "tvu-cli-examples.md#progress-reloading" >}}).
* **Transaction time loading:** Can start processing transactions from a supplied transaction time. This is particularly useful because the number of transactions can be high (possibly millions). See [transaction time loading CLI example]({{< relref "tvu-cli-examples.md#transaction-time-loading" >}}).
* **Reverification using transaction ID:** Can verify only certain transactions specified in a newline-separated transaction ID text file. The utility only processes transactions with the transaction IDs in these files. See [reverification using transaction ID CLI example]({{< relref "tvu-cli-examples.md#reverification-using-transaction-id" >}}).
* **Error registration:** Can register any errors relating to transaction validation in a `.zip` file. This error `.zip` file stores erroneous transactions’ raw data. See [error registration CLI example]({{< relref "tvu-cli-examples.md#error-registration" >}}).
* **Erroneous transaction reverification:** Can revalidate the erroneous transactions specified in an error `.zip` file. See [erroneous transaction reverification CLI example]({{< relref "tvu-cli-examples.md#erroneous-transaction-reverification" >}}).
* **Transaction processor:** Can act as a transaction processor, performing user-supplied tasks on each transaction. All the functionalities detailed in the previous points, that is, progress registration/reloading, error registration, and ID re-verification work for this mode as well. See [transaction processor CLI example]({{< relref "tvu-cli-examples.md#transaction-processor" >}}).
