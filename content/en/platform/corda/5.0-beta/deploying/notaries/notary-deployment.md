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

* The appropriate R3 signing keys must be allowed on the network, in addition to any signing keys used to sign application CPKs (Corda Packages)/CPBs (Corda Package Bundles).

* Prior to constructing a notary virtual node, you must upload the notary CPI (Corda Package Installer) to the application network.

* When creating a notary virtual node, you must specify the hash of the notary CPI rather than the application CPI.

* When registering the notary virtual node with the MGM, the following additional information must be supplied in the `context` of the registration request:

  - `"corda.roles.0" : "notary"` - This flags the virtual node as taking the role of a notary on the network.

  - `"corda.notary.service.name" : <x500 name>` - This is a user-specified X.500 name for the notary service that this virtual node will represent. This is the name that will be used by CorDapps when specifying which notary to use for notarization.

  - `"corda.notary.service.flow.protocol.name" : "com.r3.corda.notary.plugin.nonvalidating"` - This attribute replaces the validating Boolean flag in Corda 4. This is effectively the equivalent to setting `validating = false` in Corda 4.

  - `"corda.notary.service.flow.protocol.version.0" : "1"` - This must be specified and must be set to version 1 for now. The 0 on the end of the name reflects the fact that in future there may be multiple versions supported, which would be reflected in the MGM standard way using 1, 2, 3 for each additional version supported.

  {{< note >}}
  It is currently only possible to have a single notary virtual node associated with a notary service X.500 name. The eventual intent is to allow a many-to-one mapping, similar to the HA notary implementation in Corda 4. This will allow a notary service to be hosted across multiple Corda clusters/regions.
  {{< /note >}}


For information on developing notary plugin CorDapps in Corda 5.0 Beta, see the [Developing]({{< relref "../../developing/notaries/overview.md" >}}) section.