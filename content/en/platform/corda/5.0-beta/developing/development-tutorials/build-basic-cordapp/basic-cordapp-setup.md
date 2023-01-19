---
date: '2023-01-11'
title: "Initial setup"
menu:
  corda-5-beta:
    parent: corda-5-beta-tutorial-develop-building-your-first-basic-cordapp
    identifier: corda-5-beta-tutorial-develop-initial-setup
    weight: 1100
section_menu: corda-5-beta
---

## Learning Objectives

After you have completed this tutorial, you will know how to create two modules containing the required setup to build your CorDapp. You will create the following modules:

* `ledger-utxo-example-apples-app` - This is where you will write your application logic.
* `ledger-utxo-example-apples-contract` - This is where your object definitions will be placed.

{{< note >}}
The packages are not required but they allow to define a suggested structure for the users to follow.
{{< /note >}}


## Perform Initial Setup of Your CorDapp

Create two modules in the project's root directory.

1. Create the `ledger-utxo-example-apples-app` module by performing the following steps:

a. Include the following `build.gradle`:

```kotlin
plugins {
    id 'net.corda.plugins.cordapp-cpb2' version '7.0.1-Fox'
}

cordapp {
    targetPlatformVersion 999
    minimumPlatformVersion 999
    workflow {
        name "Apples utxo example app"
        versionId 1
        vendor "R3"
    }
}

dependencies {
    cordaProvided 'net.corda:corda-ledger-utxo:5.0.0.523-Fox1.0'

    cordapp project(':testing:cpbs:ledger-apples-example:ledger-utxo-apples-example-contract')

    // Common and API packages pulled in as transitive dependencies through client
    cordapp 'com.r3.corda.notary.plugin.nonvalidating:notary-plugin-non-validating-client:5.0.0.0-Fox1.0'
}
```

b. Create the `net.cordapp.utxo.apples.flows` package.

2. Create the `ledger-utxo-example-apples-contract` module by performing the following steps:

a. Include the following `build.gradle`:

```kotlin
plugins {
    id 'net.corda.plugins.cordapp-cpb2' version '7.0.1-Fox'
}

cordapp {
    targetPlatformVersion 999
    minimumPlatformVersion 999
    contract {
        name "Apples utxo example contract"
        versionId 1
        vendor "R3"
    }
}

dependencies {
    cordaProvided 'net.corda:corda-ledger-utxo:5.0.0.523-Fox1.0'
}
```

b. Create two packages: `net.cordapp.utxo.apples.contracts` and `net.cordapp.utxo.apples.states`.

## Next steps

Follow the [Write States](basic-cordapp-state.md) tutorial to continue on this learning path.
