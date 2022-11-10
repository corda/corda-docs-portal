---
date: '2022-09-19'
title: "Getting Started"
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-start
    weight: 2000
section_menu: corda-5-alpha
---
This section guides Developers who are new to Corda 5 from setting up their development environment through to writing, compiling, and running their first basic CorDapp.

<!--{{< note >}}
Alpha is, as the name suggests, a developer preview. It is not a product released and supported by R3. As a result:
* Do not release anything built on Alpha into Production.
* There is no support for Alpha but we are keen to receive community feedback.
* There are no guarantees around API stability.
* The tooling described in this section is experimental and may or may not be delivered in the GA release of Corda 5.
* There are likely to be bugs. If you raise a bug with us, we will consider them for fixing.
{{< /note >}}-->

## Corda 4 vs Corda 5

Corda 5 is a complete re-write of Corda 4. This was necessary to achieve the massive gains in non-functional performance that Corda 5 offers. When writing CorDapps, some things will seem familiar and some things will feel different. For example, the basic mechanism of flows is similar, whereas the structure of the Corda network, the way flows are tested, and the way flows are instantiated (via REST) have changed significantly. You can read more about these changes in the [Introduction](../introduction/introduction.html).

This documentation does not assume any prior knowledge of Corda 4.

## Ledger

As at the cut for Alpha, the Corda 5 [ledger](../introduction/key-concepts.html#ledger-layer) is not at the stage of development where it can be usefully previewed, hence there is no ledger in Alpha.
There are however some of the ledger building blocks around cryptography, serialization, and persistence and so with a bit of extra work you can still prototype useful distributed ledger applications.

## Other Sources of Documentation

Aside from this documentation, the [corda-runtime-os Wiki](https://github.com/corda/corda-runtime-os/wiki) has some useful information about working with Corda.
Corda-runtime-os contains the guidance if you want to compile Corda from source.
