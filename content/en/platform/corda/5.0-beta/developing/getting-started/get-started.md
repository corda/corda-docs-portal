---
date: '2023-01-09'
title: "Getting Started"
menu:
  corda-5-beta:
    identifier: corda-5-beta-start
    parent: corda-5-beta-develop
    weight: 1000
section_menu: corda-5-beta
---

{{< note >}}
Development of the Corda 5.0 Beta version of the [CorDapp Standard Development Environment (CSDE)](cordapp-standard-development-environment/csde.html) is ongoing. A new version will be released shortly.
{{< /note >}}

This section guides Developers who are new to Corda 5 from setting up their development environment through to writing, compiling, and running their first basic CorDapp.

## Corda 4 vs Corda 5

Corda 5 is a complete re-write of Corda 4. This was necessary to achieve the massive gains in non-functional performance that Corda 5 offers. When writing CorDapps, some things will seem familiar and some things will feel different. For example, the basic mechanism of flows is similar, whereas the structure of the Corda network, the way flows are tested, and the way flows are instantiated (via REST) have changed significantly. You can read more about these changes in the [Introduction](../../introduction/introduction.html).

This documentation does not assume any prior knowledge of Corda 4.

## Other Sources of Documentation

Aside from this documentation, there is also the [corda-runtime-os Wiki](https://github.com/corda/corda-runtime-os/wiki) which has useful information about working with Corda.
Corda-runtime-os contains the guidance if you want to compile Corda from source.
