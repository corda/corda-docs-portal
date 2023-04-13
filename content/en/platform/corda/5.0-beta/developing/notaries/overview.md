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

## Points to Note for the Corda 5 Beta Release

* Notary virtual nodes use an additional “uniqueness” database for capturing state data for double-spend prevention. This is similar to the existing “crypto” and “vault” databases. Currently, when auto-provisioning virtual node databases, a uniqueness database is always provisioned, regardless of whether it is a notary virtual node or not. This will be addressed in a future release.

* Notary virtual nodes currently sign successful notarization requests with the ledger key for that virtual node. A separate notary key will be introduced before GA, and this will be used instead. This means that future releases will not be backward compatible with Beta 1 from the perspective of notary signature verification. To use the notary key (for example for signature verification purposes) in your CorDapp, you will need to do something like:

   ```kotlin
   val notaryKey = memberLookup.lookup().first {
       it.memberProvidedContext["corda.notary.service.name"] == notary.name.toString()
   }.ledgerKeys.first()
   ```

* The uniqueness checking within the notary server flow currently uses a naive database lookup implementation. Performance will be poor under high throughput situations, or when specifying many states in one transaction. This will be improved for Beta 3.