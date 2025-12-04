---
description: "The steps that TVU goes through when verifying pre-4.12 database of transactions."
date: '2024-11-04'
menu:
  corda-enterprise-4-13:
    identifier: corda-enterprise-4-13-running-tvu
    parent: corda-enterprise-4-13-tvu
tags:
- tvu
- transaction validator utility
title: Running the TVU
weight: 150
---

# Running the TVU

This section describes the requirements to run the Transaction Validator Utility (TVU). The TVU can be used to [validate the transactions in your database and for a number of other features]({{< relref "_index.md" >}}). 

{{< important >}}
The TVU included in the 4.13 release is compatible only with 4.13 database schemas. 
{{</ important >}}

Note that you do not need to create a `legacy-contracts` folder when running the TVU. The TVU will extract what it needs from the database. Before performing the following steps, ensure everything is backed up, as changes will be made to folders as described below.

To verify transactions on a 4.13 database:  

- Place the TVU JAR in your Corda 4.13 node directory.

You can now run the TVU using the command lines described in the [TVU CLI parameters]({{< relref "tvu-cli.md" >}}) section.
