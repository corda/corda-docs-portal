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

You must build the contract-verifying notary protocol CPB for [Transaction Privacy Enhancements]({{< relref "../enhanced-ledger-privacy.md">}}) for your application network to contain the relevant contract CPKs. For more information, see the [implementation section]({{< relref "../enhanced-ledger-privacy.md#implementation">}}).

## Application CPB

It is not possible to provide a standard application CPB, because the contents of this depend on the functionality of your CorDapp. You must decide which CPKs to bundle together to provide your application functionality. However, you must also bundle the `notary-common`, `<notary-type>-api`, and `<notary-type>-client` CPKs to provide the notary protocols your CorDapp will support.

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
