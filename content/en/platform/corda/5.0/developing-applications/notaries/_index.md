---
date: '2023-02-23'
title: "Notaries"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-notaries
    parent: corda5-develop
    weight: 4500
section_menu: corda5
---

This section outlines what you need to know to get a notary up and running on a Corda 5 application network.

* Network Member Roles
* Notary Plugin CorDapps
* CSDE Environment


## Points to Note

* Notary virtual nodes use an additional “uniqueness” database for capturing state data for double-spend prevention. This is similar to the existing “crypto” and “vault” databases. Currently, when auto-provisioning virtual node databases, a uniqueness database is always provisioned, regardless of whether it is a notary virtual node or not. This will be addressed in a future release.