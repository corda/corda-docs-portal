---
aliases:
- /head/versioning-and-upgrades.html
- /HEAD/versioning-and-upgrades.html
- /versioning-and-upgrades.html
- /releases/release-V4.4/versioning-and-upgrades.html
- /docs/corda-os/head/versioning-and-upgrades.html
- /docs/corda-os/versioning-and-upgrades.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-4:
    identifier: corda-os-4-4-versioning-and-upgrades
    parent: corda-os-4-4-development
    weight: 150
tags:
- versioning
- upgrades
title: Versioning and upgrades
---


# Versioning and upgrades


*Change is inevitable, except from a vending machine*
– Abraham Lincoln


This section of the guide covers how CorDapps are versioned and how to manage upgrades in a decentralised network. It should be read when
you’re at a stage of your development that requires planning for post-launch iteration. You will learn:


* How the ledger expresses to what extent business logic can be changed and by who.
* How change is managed in a world where there are no privileged administrators who can force upgrades.

It’s worth planning for versioning and upgrades from the start, especially if you plan for your CorDapp to itself provide APIs to other
apps. Apps extending the platform with industry-specific data models is a common case, and ensuring you can evolve your data model as
the world changes is a key part of any professionally built software.



* [API stability guarantees](api-stability-guarantees.md)
* [Public API](api-stability-guarantees.md)
* [Non-public API (experimental)](api-stability-guarantees.md)
* [The @DoNotImplement annotation](api-stability-guarantees.html#corda-internal-modules)
* [Versioning](versioning.md)
* [Release new CorDapp versions](upgrading-cordapps.md)
* [CorDapp constraints migration](cordapp-constraint-migration.md)
* [CorDapp Upgradeability Guarantees](cordapp-upgradeability.md)
