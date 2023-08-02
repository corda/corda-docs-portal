---
title: "Interoperability CorDapp API"
date: 2023-07-25
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interoperability-cordapp-api
    weight: 1000
section_menu: corda5
---

# Interoperability

This section explains Corda's interoperability features that allow your CorDapp to communicate with external CorDapps
from other application networks. In this document, you will learn about:

* Façades: How façades provide a common interface to enable interoperation between CorDapps while maintaining
  separation.
* Defining façades: The JSON format for specifying façade interfaces along with methods, parameters and return types.
* Mapping façades: Using annotations to map the façade definition to Java or Kotlin interfaces in your CorDapp code.
* Calling façades: Obtaining a proxy and invoking façade methods on a remote CorDapp.
* Implementing façades: Implementing a façade interface in a responder flow and handling requests.
* APIs: An overview of Corda APIs such as `FacadeService` and `ResponderFlow` that facilitate interoperability.
* Steps involved in augmenting your CorDapp with façades for interoperation between Corda application networks.

