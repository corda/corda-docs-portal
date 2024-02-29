---
date: '2023-11-01'
description: Learn how to set up a CorDapp development environment, including writing, compiling, and running a first basic CorDapp using the CorDapp template.
title: "CorDapp Template"
menu:
  corda52:
    weight: 5075
    identifier: corda52-develop-get-started
    parent: corda52-develop 
---
# CorDapp Template

This section guides CorDapp Developers from setting up their development environment through to writing, compiling, and running their first basic {{< tooltip >}}CorDapp{{< /tooltip >}} using the CorDapp template.

The CorDapp template simplifies the process of prototyping CorDapps.
This template is obtained by cloning our `cordapp-template-kotlin` or `cordapp-template-java` repository to your local machine and checking out the `release-V5.2` branch. These templates provide:

* a prepared CorDapp project that you can use as a starting point to develop your own prototypes.
* a base Gradle configuration that brings in the dependencies you need to write and test a Corda 5 CorDapp.
* a set of Gradle helper tasks which speed up and simplify the development and deployment process; these are effectively wrappers over the {{< tooltip >}}Corda CLI{{< /tooltip >}}.
* debug configuration for debugging a local Corda cluster.
* the `MyFirstFlow` code, which forms the basis of the [First Flow documentation]({{< relref "./first-flow/_index.md" >}}).
* the `utxoexample` Chat CorDapp, which provides a basic, working {{< tooltip >}}UTXO{{< /tooltip >}} Ledger CorDapp.
* the ability to configure the members of the local Corda network.
