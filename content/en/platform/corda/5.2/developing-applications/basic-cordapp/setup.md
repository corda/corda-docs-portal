---
description: "Learn how to configure your environment for your first basic Corda 5 CorDapp."
date: '2023-05-03'
title: "Initial Setup"
menu:
  corda52:
    identifier: corda52-develop-first-cordapp-setup
    parent: corda52-develop-first-cordapp
    weight: 1000
---

# Initial Setup

After you have completed this tutorial, you will have modified the {{< tooltip >}}CSDE{{< /tooltip >}} environment to make it ready for building your {{< tooltip >}}CorDapp{{< /tooltip >}}.
You will have also created three packages within the existing CSDE project structure.

{{< note >}}
The packages are not required but they define a suggested structure for you to follow.
{{< /note >}}

## Initial Setup of Your CorDapp

In this tutorial, you will use the CSDE repository as a template and build on top of it.
This project already contains some example flows, contracts, and {{< tooltip >}}states{{< /tooltip >}}.

1. Follow the CSDE [installation instructions]({{< relref "../runtime-plugin/installing/_index.md" >}}) to clone the [Kotlin CSDE repository](https://github.com/corda/CSDE-cordapp-template-kotlin).

2. Create the `com.r3.developers.apples.workflows` package. If using IntelliJ, you can do this by right-clicking
the **kotlin** folder within the **workflows** folder and then selecting **New > Package**.

3. Update the `contracts` module by creating the following packages:

   * `com.r3.developers.apples.contracts`
   * `com.r3.developers.apples.states`

## Next steps

Follow the [Write States]({{< relref "./state.md" >}}) tutorial to continue on this learning path.
