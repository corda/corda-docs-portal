---
title: "Interoperability CorDapp API"
date: 2023-07-25
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interop-cordapp-api
    parent: corda5-interop
    weight: 2000
section_menu: corda5
---

# Interoperability CorDapp API

This section explains Corda's Interoperability features that allow your CorDapp to communicate with external CorDapps
from other application networks. In this section, you will learn about:

* Corda Façades: How Façades provide a common interface to enable interoperation between CorDapps while maintaining
  separation.
* Defining Façades: The JSON format for specifying Façade interfaces along with methods, parameters and return types.
* Mapping Façades: Using annotations to map the Façade definition to Java or Kotlin interfaces in your CorDapp code.
* Calling Façades: Obtaining a proxy and invoking Façade methods on a remote CorDapp.
* Implementing Façades: Implementing a Façade interface in a responder flow and handling requests.
* APIs: An overview of Corda APIs such as `FacadeService` and `ResponderFlow` that facilitate interoperability.
* Steps involved in augmenting your CorDapp with Façades for interoperation between Corda application networks.

