---
date: '2022-09-19'
title: "Getting started"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-start
    weight: 2000
section_menu: corda-5-dev-preview
---
This section guides Developers who are new to Corda 5 from setting up their development environment through to writing, compiling, and running their first basic CorDapp.

<!--It includes:

The prerequisites for working with Cordapps

Downloading and using the Cordapp Standard Development Environment (CSDE) Template

Writing and running simple flows.

Testing and debugging Cordapps using the (Corda) Simulator.

Deploying Cordapps to a local Corda Cluster (Combined Worker).-->

{{< note >}}
Developer Preview 2 is, as the name suggests, a developer preview. It is not a product released and supported by R3. As a result:
* Do not release anything built on Developer Preview 2 into Production.
* There is no support For Developer Preview 2 but we are keen to receive community feedback.
* There are no guarantees around API stability.
* The tooling described in this section is experimental and may or may not make it in to the GA release of Corda 5.
* There are going to be bugs. If you raise a bug with us, we will consider them for fixing.
{{< /note >}}

## Developer Preview 1 vs Developer Preview 2

Developer Preview 1 was effectively a taster for the Corda 5 API. It was however, mostly based on Corda 4 under the hood. Developer Preview 2 is the real deal, based entirely on the new Corda 5 code base with possibly material differences in the API. As a result, code written for Developer Preview 1 is unlikely to work with Developer Preview 2 without modification. You can not use any artefacts released from Developer Preview 1 for Developer Preview 2.  

## Kotlin vs Java

The getting started documentation and templates are currently only in Kotlin. We are working to provide Java versions as soon as possible, but it may be a short time after the release of DP2.

To Java Developers used to working with Corda 4, or those who have some familiarity with Kotlin, it should be possible to work out how to implement the examples in Java without too many problems.

## Corda 4 vs Corda 5

Corda 5 is a complete re-write of Corda 4. This was necessary to achieve the massive gains in non-functional performance that Corda 5 offers. When writing CorDapps, some things will appear familiar and some things will feel different. For example, the basic mechanism of flows is similar, whereas the structure of the Corda network, the way flows are tested, and the way flows are instantiated (via REST) have changed significantly. You can read more about these changes in the [Introduction](../introduction/introduction.html).

This documentation does not assume any prior knowledge of Corda 4.

## Ledger

As at the cut for Developer Preview 2, the Corda 5 [ledger](../introduction/key-concepts.html#ledger-layer) is not at the stage of development where it can be usefully previewed, hence there is no ledger in Developer Preview 2.
There are however some of the ledger building blocks around cryptography, serialization, and persistence and so with a bit of extra work you can still prototype useful distributed ledger applications.

## Other sources of documentation

Aside from this documentation, there is also the [corda-runtime-os Wiki](https://github.com/corda/corda-runtime-os/wiki) which has useful information about working with Corda.
Corda-runtime-os contains the guidance if you want to compile Corda from source.
