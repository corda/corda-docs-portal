---
date: '2023-05-16'
title: "Notary Plugin CorDapps"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: notary-plugin-cordapps
    parent: corda5-develop-notaries
    weight: 4700
section_menu: corda5
---
# Notary Plugin CorDapps 

In Corda 5, notary functionality is provided in the form of plugin CorDapps. In theory, anyone can write a new notary protocol by implementing their own CorDapps. However, initially, it is expected to only have protocols provided by R3. For a given notary protocol, two CPBs (Corda Package Bundles) are expected to be required:

* A **client**, or **application** CPB, which should be used to generate a CPI (Corda Package Installer) associated with application virtual nodes. At a minimum, this would contain a CPK (Corda Package) that has an initiating flow that is automatically invoked by the Corda 5 flow framework to initiate a notarization request.

* A **notary server** CPB (Corda Package Bundle), which should be used to generate a CPI associated with notary virtual nodes. At a minimum, this would contain a CPK that has a responder flow to what is packaged in the client CPB.

For Corda 5.0, only a single notary protocol is provided, the **non-validating notary protocol**.

## Plugin Packaging
The details of this architecture and the steps you need to take in order to successfully build your CorDapp will be outlined in the following sections. For information on how to deploy a functioning network, see the see the [Onboarding Notaries]({{< relref "../../application-networks/creating/notaries.md" >}}) section.

{{< figure src="c5-non-validating-notary.png" figcaption="The CPKs, CPBs and CPIs involved in getting a functioning network that can run a notary (and by extension, UTXO ledger functionality)" alt="Corda 5 non-validating notary" >}}

## Notary CPKs
There are four modules/CPKs of relevance to the non-validating notary protocol, which are then packaged into two different CPBs. These are:

* **`notary-common`**: This contains useful library functionality that is not specific to a particular notary protocol. For example, it defines the structure of an error that may be returned by a notary protocol. This is an example of something that must be standard cross-protocol, because the UTXO ledger depends on this format to perform processing, and the ledger has no visibility of the specific notary protocol that performs notarisation.

* **`non-validating-notary-api`**: This contains the payload definition that is used to communicate between the non-validating notary client and server CPKs. Extreme caution must be taken when making changes to this module, as backwards compatibility concerns must be taken into account.

* **`non-validating-notary-client`**: This is intended to run on application virtual nodes, and provides a sub-flow that initiates a notarization request to a notary virtual node when requested by the ledger finality flow.

* **`non-validating-notary-server`**: This provides a responder flow to the corresponding initiator flow in the client package, and will perform notarization processing.

The source code for all of these modules can be found under the [notary-plugins area of corda-runtime-os](https://github.com/corda/corda-runtime-os/tree/release/os/5.0/notary-plugins).

## Notary Server CPB

R3 produces a standard non-validating notary server CPB, as this only contains CPKs that are produced by R3 and therefore does not require a developer to build their own CPB using a mixture of R3 and third-party CPKs.

## Application CPB

It is not possible to provide a standard application CPB, because the contents of this depend on the writer of a CorDapp. The writer of a CorDapp must decide which CPKs they will bundle together to provide their application CPB. This will be comprised of one or more CPKs which provide the application functionality. However, the CorDapp developer must also bundle the appropriate CPKs for the notary protocols their CorDapp will support.

The decision on which protocols to support is trivial at present, given there is only a single notary protocol to choose; the decision is purely based on whether the CorDapp is using the UTXO ledger model or not. If it is, then the CorDapp developer must bundle the `notary-common`, `non-validating-notary-api` and `non-validating-notary-client` CPKs when creating their CPB. Otherwise, there is no requirement to bundle any additional CPKs (as the notary is not involved in flow only or consensual ledger based CorDapps).

The easiest way to ensure your CorDapp includes the necessary CPKs is to use the CorDapp dependency functionality of the CPK Gradle plugin. You need to add the following to your Gradle dependency configuration, where `cordaNotaryPluginsVersion` is an appropriate version of `corda-runtime-os`, as the notary plugin currently lives as part of this repository.

```kotlin

cordapp "com.r3.corda.notary.plugin.nonvalidating:notary-plugin-non-validating-client:$cordaNotaryPluginsVersion"

```

{{< note >}}
It is only necessary to specify a dependency on the client CPK; this itself depends on the API and notary common CPKs, so these transitive dependencies will also be pulled in when constructing your application CPB.
{{< /note >}}

The other way to form your application CPB is to use the `corda-cli` tool. However, if you choose to use this, you will need to explicitly specify all three of the required CPKs (`notary-common`, `non-validating-notary-api` and `non-validating-notary-client`).

## CPI Creation

Having two CPBs for the application and notary virtual node roles on the network also extends to needing two different CPIs. This process is unchanged, but ensure the following:
* the notary server CPB signing key is used to create the CPI and and then imported to Corda
* the same group policy file is used when creating both the application and notary CPIs.