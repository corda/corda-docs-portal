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
# Notaries

This section outlines how to get a notary up and running on a Corda application network.

* [Network Member Roles]({{< relref "../notaries/network-member-roles.md" >}})
* [Notary Plugin CorDapps]({{< relref "../notaries/notary-plugin-cordapps.md" >}})


{{< note >}} 
Notary virtual nodes use an additional “uniqueness” database for capturing state data for double-spend prevention. This is similar to the existing “crypto” and “vault” databases. Currently, when auto-provisioning virtual node databases, a uniqueness database is always provisioned, regardless of whether it is a notary virtual node or not. This will be addressed in a future release.
{{< /note >}} 
