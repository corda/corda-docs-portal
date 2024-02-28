---
description: Learn how to implement a notary for a Corda 5 application network.
date: '2024-02-27'
title: "Notary CorDapps"
menu:
  corda52:
    identifier: corda52-develop-notary-cordapps
    parent: corda52-develop-notaries
    weight: 3000
---
# Notary CorDapps

The following sections describe the details of the architecture and the steps to take to successfully build your CorDapp. For information on how to deploy a functioning network, see the [Onboarding Notaries]({{< relref "../../../application-networks/creating/notaries.md" >}}) section.

{{< toc >}}

{{< note >}}
Notary virtual nodes use an additional `uniqueness` database for capturing state data for double-spend prevention. This is similar to the existing `crypto` and `vault` databases. Currently, when auto-provisioning virtual node databases, a uniqueness database is always provisioned, regardless of whether it is a notary virtual node or not. This will be addressed in a future release.
{{< /note >}}

## Notary CPKs

Each protocol is composed of the following modules/CPKs, which are packaged into two different CPBs:

* **`notary-common`** —  contains useful library functionality that is not specific to a particular notary protocol. For example, it defines the structure of an error that may be returned by a notary protocol. This is an example of something that must be standard cross-protocol, because the UTXO ledger depends on this format to perform processing, and the ledger has no visibility of the specific notary protocol that performs notarization.
* **`<notary-type>-api`** — contains the payload definition that is used to communicate between the non-validating notary client and server CPKs. Extreme caution must be taken when making changes to this module, as backwards compatibility concerns must be taken into account.
* **`<notary-type>-client`** — intended to run on application virtual nodes, and provides a sub-flow that initiates a notarization request to a notary {{< tooltip >}}virtual node{{< /tooltip >}} when requested by the ledger finality flow.
* **`<notary-type>-server`** — provides a responder flow to the corresponding initiator flow in the client package, and performs notarization processing.

The source code for these modules is in the [notary-plugin-non-validating](https://github.com/corda/corda-runtime-os/tree/release/os/5.2/notary-plugins/notary-plugin-non-validating) and [notary-plugin-contract-verifying](https://github.com/corda/corda-runtime-os/tree/release/os/5.2/notary-plugins/notary-plugin-contract-verifying) folders in the [notary-plugins area of corda-runtime-os](https://github.com/corda/corda-runtime-os/tree/release/os/5.2/notary-plugins).

## Notary Server CPB

### Non-Validating Notary Protocol

R3 provides a [non-validating notary protocol]({{< relref "non-validating-notary/_index.md">}})  CPB. This is available from the [Corda GitHub release page](https://github.com/corda/corda-runtime-os/releases/).

### Contract-Verifying Notary Protocol

You must build a contract-verifying notary protocol CPB for [Transaction Privacy Enhancements]({{< relref "../enhanced-ledger-privacy.md">}}) that contains the relevant contract CPKs, along with the contract-verifying notary server logic supplied with Corda. These contracts are those used on the specific network that the notary is intended for and are required to enable the notary to run and verify the contracts to notarize transactions. A different CPB must be built for each application network, and must be rebuilt and upgraded along with the application.

To build the notary CPB, add a gradle module to your CorDapp project that builds the notary whenever the application is built. For example, in `ledger-utxo-demo-app` the project layout looks as follows:

{{<
  figure
	 src="contract-verifying-example.png"
   width=40%
	 figcaption="Example contract-verifying notary project"
	 alt="Contract-verifying notary project"
>}}

The `ledger-utxo-demo-app` project (contains the workflows) and the `ledger-utxo-demo-contract` project (contains the contracts) are unchanged. The `ledger-utxo-demo-verifying-notary` project was added to build the contract-verifying notary for this specific application. It contains no code, just a `build.gradle` file as it just needs to bring together the notary server CPK and the contract CPKs for this application. The `build.gradle` file looks as follows:

```gradle
plugins {
    id 'org.jetbrains.kotlin.jvm'
    id 'net.corda.plugins.cordapp-cpb2'
}

cordapp {
    targetPlatformVersion 50200
    minimumPlatformVersion 50200 
    workflow {
        name "Utxo demo verifying notary"
        versionId 1
        vendor "R3"
    }
}

dependencies {
    cordaProvided platform("net.corda:corda-api:$cordaApiVersion")
    cordaProvided 'org.jetbrains.kotlin:kotlin-osgi-bundle'
    cordaProvided 'net.corda:corda-ledger-utxo'

    # cordapp dependency on the app contract (built locally)
    cordapp project(':apps:ledger-utxo-demo-contract')

    # cordapp dependency on the contract verifying server CPK (pulled in via Maven)
    cordapp "com.r3.corda.notary.plugin.contractverifying:notary-plugin-contract-verifying-server:$notaryPluginVersion"
}
```

This is a standard workflow project that pulls in the contracts and the notary server CPK as dependencies. Building a CPB from this project creates a working notary CPB.

## Application CPB

It is not possible to provide a standard application CPB, because the contents of this depend on the functionality of your CorDapp. You must decide which CPKs to bundle together to provide your application functionality. However, you must also bundle the `notary-common`, `<notary-type>-api`, and `<notary-type>-client` CPKs to provide the notary protocols your CorDapp will support.

{{< note >}}
If implementing the contract-verifying notary protocol, workflows and contracts must be packaged in separate CPKs. This ensures that the notary only has contracts and none of the workflows.
{{< /note >}}

The easiest way to ensure your CorDapp includes the necessary CPKs is to use the CorDapp dependency functionality of the CPK Gradle plugin. Add one of the following to your Gradle dependency configuration, where `cordaNotaryPluginsVersion` is an appropriate version of `corda-runtime-os`:

* Contract-verifying protocol:

   ```kotlin
   cordapp "com.r3.corda.notary.plugin.nonvalidating:notary-plugin-non-validating-client:$cordaNotaryPluginsVersion"
   ```
* Non-validating notary protocol:

   ```kotlin
   cordapp "com.r3.corda.notary.plugin.contractverifying:notary-plugin-contract-verifying-client:$cordaNotaryPluginsVersion"
   ```

{{< note >}}
It is only necessary to specify a dependency on the client CPK; this itself depends on the API and notary common CPKs, so these transitive dependencies will also be pulled in when constructing your application CPB.
{{< /note >}}

Alternatively, you can form your application CPB using the [Corda CLI]({{< relref "../../../reference/corda-cli/package.md" >}}). However, if you choose to use this, you need to explicitly specify all three of the required CPKs.

## CPI Creation

Having two CPBs for the application and notary virtual node roles on the network also extends to needing two different CPIs. This process is unchanged, but ensure the following:

* the notary server CPB signing key is used to create the CPI and then imported to Corda
* the same {{< tooltip >}}group policy{{< /tooltip >}} file is used when creating both the application and notary CPIs, for more information see the [Onboarding Notaries]({{< relref "../../../application-networks/creating/notaries.md" >}}) section
