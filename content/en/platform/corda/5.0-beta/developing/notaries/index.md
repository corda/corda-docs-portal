---
date: '2022-12-01'
title: "Notaries"
menu:
  corda-5-beta:
    parent: corda-5-beta-develop
    identifier: corda-5-beta-notaries
    weight: 4000
section_menu: corda-5-beta

---

This section outlines what you need to know to get a notary up and running on a Corda 5 application network.

* [Network Member Roles](../notaries/network-member-roles.md)
* [Notary Plugin CorDapps](../notaries/plugin-cordapps-notary.md)
* [CSDE Environment](../notaries/csde.md)

For information on deploying notary virtual nodes in Corda 5.0, see the [Notary Deployment](../../deploying/notaries/notary-deployment.md) section.

## Points to note in the Beta 1 release

* Notary virtual nodes use an additional “uniqueness” database for capturing state data for double spend prevention. This is similar to the existing “crypto” and “vault” DBs. Currently, when auto-provisioning virtual node DBs, we always provision a uniqueness DB, regardless of whether it is a notary virtual node or not. This will be addressed in a future release.

* Notary virtual nodes currently sign successful notarization requests with the ledger key for that virtual node. A separate notary key will be introduced before GA, and this will be used instead. This means that future releases will not be backwards compatible with Beta 1 from the perspective of notary signature verification. To use the notary key (e.g. for signature verification purposes) in your CorDapp, you will need to do something like:

```kotlin
val notaryKey = memberLookup.lookup().first {
    it.memberProvidedContext["corda.notary.service.name"] == notary.name.toString()
}.ledgerKeys.first()
```

* The uniqueness checking within the notary server flow currently uses a naïve database lookup implementation. Performance will be poor under high throughput situations, or when specifying many states in one transaction. This will be improved for Beta 2.