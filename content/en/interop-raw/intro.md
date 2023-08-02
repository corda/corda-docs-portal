---
date: '2023-08-02'
version: 'Corda 5.2'
title: "What is Interoperability"
menu:
  corda5:
    identifier: corda5-interoperability-cordapp-api-intro
    parent: corda5-interoperability-cordapp-api
    weight: 1000
section_menu: corda5
---
# What is Interoperability

Interoperability is a capability of Cordapps to communicate and coordinate activities with peers from
other Application Networks. These interactions between two different application networks often involve modifying their
respective ledgers to achieve shared objectives. For instance, one example of interoperability is atomic swap. Atomic
exchange of one asset inside Application Network for another asset in the other Application Network.
Atomic swaps represent just one of the various business use cases enabled by interoperability, which are further
explored in here [TODO link].
This document focuses on the API that empowers Cordapps with Interoperability capabilities. To achieve this, Cordapp
code needs to be aware of peers (identities) outside its own application network. Additionally, the Cordapp must be
capable of communicating or invoking actions on a different Cordapp that does not share a common codebase.
[TODO this is not the final diagram and the right scale]

![Application Networks and Interop Groups](interopgroup.png "Application Networks and Interop Groups")

The Interoperability API addresses these requirements, built on the principle of minimizing the exposure of code between
two different Cordapps. This is achieved through the introduction of Façade and Façade Proxy objects and Corda services
for used in Corda flows.
The Façade API acts as a bridge, facilitating seamless and secure communication between distinct Cordapps. It enables
them to interact and exchange data while maintaining a clear separation of concerns. The Façade serves as a common
interface definition, abstracting away the implementation details from the underlying Cordapps.
By incorporating Façade Proxy objects alongside other Corda APIs, developers can leverage the power of Interoperability
while maintaining a consistent and familiar development experience.
In the subsequent sections, we delve into the Façade API, exploring its components, functionality, and usage in depth.
We aim to provide a comprehensive guide that empowers developers to harness the full potential of Interoperability in
Cordapps, facilitating cross-network interactions and supporting diverse use cases.
