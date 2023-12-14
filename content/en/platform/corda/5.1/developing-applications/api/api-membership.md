---
date: '2022-09-06'
version: 'Corda 5.1'
title: "membership"
menu:
  corda51:
    identifier: corda51-api-membership
    parent: corda51-api
    weight: 6000
section_menu: corda51
---
# net.corda.v5.membership
The `corda-membership` package defines interfaces that provide information about a {{< tooltip >}}member{{< /tooltip >}} and a {{< tooltip >}}membership group{{< /tooltip >}}. The interfaces in this module should not be implemented by {{< tooltip >}}CorDapp{{< /tooltip >}} Developers. Instead, instances can be retrieved through lookup services.
For more information, see the documentation for the package in the <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/membership/package-summary.html" target=" blank">Java API documentation</a>.

This package consists primarily of the following two root classes:
* [MemberInfo](#memberinfo)
* [GroupParameters](#groupparameters)

## `MemberInfo`
The `MemberInfo` interface exposes properties of a virtual node's membership. This includes the {{< tooltip >}}X.500{{< /tooltip >}} name, {{< tooltip >}}ledger keys{{< /tooltip >}}, and status. This information is a combination of information provided during network registration and metadata assigned to the member by the {{< tooltip >}}MGM{{< /tooltip >}}.

Information provided by the virtual node operator at time of registration is the content of the `MemberContext` and the information provided by the MGM is the source of the `MGMContext` content.

Instances of `MemberInfo` must be retrieved through a lookup API. `MemberLookup` from the <a href="application/membership.md">`corda-application` module</a>, is the lookup API which provides membership information to CorDapps. This can be used to look up the information of the member executing a {{< tooltip >}}flow{{< /tooltip >}} or other members available to transact with within the group.

The `MemberInfo` interface extends the `LayeredPropertyMap` interface, which means that membership information is key-value `String` pairs that are parsed and returned through properties. Generally, any properties required for use within a CorDapp are exposed through the `MemberInfo` interface. Other properties may only be relevant internally or at certain layers within the codebase so these are exposed through extension functions.


## `GroupParameters`

The `GroupParameters` interface is also a type of `LayeredPropertyMap` which exposes properties of the group as distributed by the network manager (MGM). These properties define the parameters under which all members must operate during transactions and are exposed for Network Operators by GET methods. For more information, see [Updating Group Parameters]({{< relref "../../application-networks/managing/group-parameters/_index.md">}}).

The `GroupParametersLookup` interface allows flows to access `GroupParameters` for further verification.