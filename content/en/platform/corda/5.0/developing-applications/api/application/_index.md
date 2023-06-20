---
date: '2023-02-10'
version: 'Corda 5.0 Beta 4'
title: "net.corda.v5.application"
menu:
  corda5:
    identifier: corda5-api-application
    parent: corda5-api
    weight: 1000
section_menu: corda5
---
# net.corda.v5.application
The `corda-application` module provides the fundamental building blocks required to create a [flow]({{< relref "../../../key-concepts/fundamentals/ledger/flows/_index.md" >}}) and so all CorDapps use this module.

`corda-application` sits at a higher level in the module hierachy and exposes the following modules as API dependencies:

- `corda-base`
- `corda-crypto`
- `corda-membership`
- `corda-serialization`

By depending on `corda-application`, your CorDapp does not need to directly depend on the modules listed above.

`corda-application` provides a number of packages. The most significant package for defining flows is <a href="flows.md">`flows`</a>, which contains the interfaces to implement and annotations to use to customize flow behaviour. The remaining packages provide some services for use within a flow. A description of each of these packages is provided in the following sections:
* [crypto](crypto.md)
* [flows](flows.md)
* [marshalling](marshalling.md)
* [membership](membership.md)
* [messaging](messaging.md)
* [persistence](persistence.md)
* [serialization](serialization.md)
