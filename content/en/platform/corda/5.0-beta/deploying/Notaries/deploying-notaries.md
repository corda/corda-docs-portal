---
date: '2023-01-05'
menu:
  corda-5-beta:
    identifier: corda-5-beta-notary-deployment
    weight: 5000
    parent: corda-5-beta-deploy
section_menu: corda-5-beta
title: "Notary Deployment"
---

Deploying notary virtual nodes to your network follows an almost identical process to deploying regular application virtual nodes to your network, with some small changes:

The appropriate R3 signing keys must be allowed on the network, in addition to any signing keys used to sign application CPKs/CPBs.

Prior to constructing a notary virtual node, you must upload the notary CPI to the application network.

When creating a notary virtual node, you must specify the hash of the notary CPI rather than the application CPI.

When registering the notary virtual node with the MGM, the following additional information must be supplied in the `context` of the registration request:

* `"corda.roles.0" : "notary"` - This flags the virtual node as taking the role of a notary on the network.

* `"corda.notary.service.name" : <x500 name>` - This is a user-specified x500 name for the notary service that this virtual node will represent. This is the name that will be used by CorDapps when specifying which notary to use for notarization.

{{< note >}}
It is currently only possible to have a single notary virtual node associated with a notary service x500 name. The eventual intent is to allow a many to one mapping, similar to the HA notary implementation in Corda 4. This will allow a notary service to be hosted across multiple Corda clusters / regions.
{{< /note >}}

* `"corda.notary.service.plugin" : "net.corda.notary.NonValidatingNotary"` - This attribute replaces the validating Boolean flag in Corda 4. This is effectively the equivalent to setting `validating = false` in Corda 4.

For information on developing notary virtual nodes in Corda 5.0 Beta 1, see the [Developing](../../developing/Notaries/overview.md) section,