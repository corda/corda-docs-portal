---
date: '2023-02-23'
title: "Getting Started Using the CSDE"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-get-started
    parent: corda5-develop
    weight: 5000
section_menu: corda5
---

This section guides Developers who are new to Corda 5 from setting up their development environment through to writing, compiling, and running their first basic CorDapp.

## The CorDapp Standard Development Environment (CSDE) 

The CorDapp Standard Development Environment (CSDE) makes the process of prototyping CorDapps more straight-forward.
The CSDE is obtained by cloning our `CSDE-cordapp-template-kotlin` or `CSDE-cordapp-template-java` repository to your local machine. The CSDE provides:
* a prepared CorDapp project that you can use as a starting point to develop your own prototypes.
* a base Gradle configuration that brings in the dependencies you need to write and test a Corda 5 CorDapp.
* a set of Gradle helper tasks which speed up and simplify the development and deployment process; these are effectively wrappers over the [Corda CLI](../installing-corda-cli.html).
* debug configuration for debugging a local Corda cluster.
* the `MyFirstFlow` code which forms the basis of the Getting Started documentation.
* the `utxoexample` Chat CorDapp, which provides a basic, working UTXO Ledger CorDapp.
* the ability to configure the members of the local Corda network.

## Corda 4 vs Corda 5

Corda 5 is a complete re-write of Corda 4. This was necessary to achieve the massive gains in non-functional performance that Corda 5 offers. When writing CorDapps, some things will seem familiar and some things will feel different. For example, the basic mechanism of flows is similar, whereas the structure of the Corda network, the way flows are tested, and the way flows are instantiated (via REST) have changed significantly. You can read more about these changes in the [Introduction]({{< relref "../../introduction/_index.md" >}}).

This documentation does not assume any prior knowledge of Corda 4.

## Other Sources of Documentation

Aside from this documentation, there is also the [corda-runtime-os Wiki](https://github.com/corda/corda-runtime-os/wiki) which has useful information about working with Corda.
Corda-runtime-os contains the guidance if you want to compile Corda from source.