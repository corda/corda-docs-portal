---
date: '2022-09-06'
title: "net.corda.v5.membership"
menu:
  corda-5-dev-preview2:
    identifier: corda-5-dev-preview-api-membership
    parent: corda-5-dev-preview-api
    weight: 6000
section_menu: corda-5-dev-preview2
---
You can view the KDoc documentation for this module [here](/en/api-ref/corda/5.0-dev-preview-2/modules/corda-membership-5.0.0.190-DevPreview-2-javadoc/index.html).

The `corda-membership` module defines interfaces that provide information about a member (a [virtual node](../../introduction/key-concepts.html#virtual-nodes) in a group), and a membership group. The interfaces in this module should not be implemented by CorDapp developers. Instead, instances can be retrieved through lookup services.

This module consists primarily of the following two root classes:
* [MemberInfo](#memberinfo)
* [GroupParameters](#groupparameters)

## `MemberInfo`
The `MemberInfo` interface exposes properties of a virtual node's membership. This includes the x500 name, ledger keys, and status. This information is a combination of information provided during network registration and metadata assigned to the member by the network manager (MGM).

Information provided by the virtual node operator at time of registration is the content of the `MemberContext` and the information provided by the MGM is the source of the `MGMContext` content.

Instances of `MemberInfo` must be retrieved through a lookup API. `MemberLookup` from the `corda-application` module, is the lookup API which provides membership information to CorDapps. This can be used to lookup the information of the member executing a flow or other members available to transact with within the group.

The `MemberInfo` interface extends the `LayeredPropertyMap` interface, which means that membership information is key-value `String` pairs that are parsed and returned through properties. Generally, any properties required for use within a CorDapp are exposed through the `MemberInfo` interface. Other properties may only be relevant internally or at certain layers within the codebase so these are exposed through extension functions.


## `GroupParameters`

The `GroupParameters` interface is also a type of `LayerPropertyMap` which exposes properties of the group as distributed by the network manager (MGM). These properties define the parameters under which all members must operate during transactions.

The current implementation is largely present purely for backwards compatibility in the ledger layer. This is why there is currently no API to expose these group parameters. This feature is to be implemented in the next stage of development, so it is not currently possible to interact with the parameters at this stage.
