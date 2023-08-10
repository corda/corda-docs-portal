---
date: '2023-05-03'
title: "Initial Setup"
version: 'Corda 5.1'
menu:
  corda5:
    identifier: corda51-develop-first-cordapp-setup
    parent: corda51-develop-first-cordapp
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

1. Follow the CSDE [installation instructions]({{< relref "../getting-started/installing/_index.md" >}}) to clone the [Kotlin CSDE repository](https://github.com/corda/CSDE-cordapp-template-kotlin).

2. Update the `workflows` module by performing the following steps:

   a. Update the CorDapp's configuration in the `workflows` module `build.gradle` file to reflect the purpose of your CorDapp:

   ```kotlin
    workflow {
    name "Apples utxo example workflow"
    versionId 1
    vendor "VendorNameHere"
    }
    ```

   b. Create the `com.r3.developers.apples.workflows` package. If using IntelliJ, you can do this by right-clicking
the **kotlin** folder within the **workflows** folder and then selecting **New > Package**.

3. Update the `contracts` module by performing the following steps:

   a. Update the CorDapp's configuration in the `contracts` module `build.gradle` file to reflect the purpose of your CorDapp:
   ```kotlin
    contract {
    name "Apples utxo example contract"
    versionId 1
    vendor "VendorNameHere"
    }
    ```

   b. Create two packages:

   * com.r3.developers.apples.contracts
   * com.r3.developers.apples.states


## Next steps

Follow the [Write States]({{< relref "./state.md" >}}) tutorial to continue on this learning path.
