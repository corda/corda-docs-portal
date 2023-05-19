---
date: '2022-01-05'
title: "Notaries"
menu:
  corda-5-beta:
    parent: corda-5-beta-develop
    identifier: corda-5-beta-notaries-overview
    weight: 4000
section_menu: corda-5-beta

---

This section outlines what you need to know to get a notary up and running on a Corda 5 application network.

* [Network Member Roles]({{< relref "../notaries/network-member-roles.md" >}})
* [Notary Plugin CorDapps]({{< relref "../notaries/plugin-cordapps-notary.md" >}})
* [CSDE Environment]({{< relref "../notaries/csde.md" >}})

For information on deploying notary virtual nodes to your network, see the [Notary Deployment]({{< relref "../../deploying/notaries/notary-deployment.md" >}}) section.

For information on the metrics that are provided in Corda 5 for notary and uniqueness checking functionality, see the [Notary Uniqueness Metrics]({{< relref "../../operating/notary-uniqueness-metrics.md" >}}) section.

## Points to Note for the Corda 5 Beta Release

* Notary virtual nodes use an additional “uniqueness” database for capturing state data for double-spend prevention. This is similar to the existing “crypto” and “vault” databases. Currently, when auto-provisioning virtual node databases, a uniqueness database is always provisioned, regardless of whether it is a notary virtual node or not. This will be addressed in a future release.
