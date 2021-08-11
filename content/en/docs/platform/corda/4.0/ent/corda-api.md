---
aliases:
- /releases/4.0/corda-api.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-corda-api
    weight: 75
tags:
- corda
- api
title: Corda API
---


# Corda API

The following are the core APIs that are used in the development of CorDapps:



* [API: States](api-states.md)
* [API: Persistence](api-persistence.md)
* [API: Contracts](api-contracts.md)
* [API: Contract Constraints](api-contract-constraints.md)
* [API: Vault Query](api-vault-query.md)
* [API: Transactions](api-transactions.md)
* [API: Flows](api-flows.md)
* [API: Identity](api-identity.md)
* [API: ServiceHub](api-service-hub.md)
* [API: RPC operations](api-rpc.md)
* [API: Core types](api-core-types.md)
* [API: Testing](api-testing.md)



Before reading this page, you should be familiar with the [key concepts of Corda](key-concepts.md).



## API stability guarantees

Corda makes certain commitments about what parts of the API will preserve backwards compatibility as they change and
which will not. Over time, more of the API will fall under the stability guarantees. Thus, APIs can be categorized in the following 2 broad categories:


* **public APIs**, for which API/[ABI](https://en.wikipedia.org/wiki/Application_binary_interface) backwards compatibility guarantees are provided. See: [Public API](#public-api)
* **non-public APIs**, for which no backwards compatibility guarantees are provided. See: [Non-public API (experimental)](#non-public-api)



## Public API

The following modules form part of Corda’s public API and we commit to API/ABI backwards compatibility in following releases, unless an incompatible change is required for security reasons:


* **Core (net.corda.core)**: core Corda libraries such as crypto functions, types for Corda’s building blocks: states, contracts, transactions, attachments, etc. and some interfaces for nodes and protocols
* **Client RPC (net.corda.client.rpc)**: client RPC
* **Client Jackson (net.corda.client.jackson)**: JSON support for client applications
* **DSL Test Utils (net.corda.testing.dsl)**: a simple DSL for building pseudo-transactions (not the same as the wire protocol) for testing purposes.
* **Test Node Driver (net.corda.testing.node, net.corda.testing.driver)**: test utilities to run nodes programmatically
* **Test Utils (net.corda.testing.core)**: generic test utilities
* **Http Test Utils (net.corda.testing.http)**: a small set of utilities for making HttpCalls, aimed at demos and tests.
* **Dummy Contracts (net.corda.testing.contracts)**: dummy state and contracts for testing purposes
* **Mock Services (net.corda.testing.services)**: mock service implementations for testing purposes



## Non-public API (experimental)

The following modules are not part of the Corda’s public API and no backwards compatibility guarantees are provided. They are further categorized in 2 classes:


* the incubating modules, for which we will do our best to minimise disruption to developers using them until we are able to graduate them into the public API
* the internal modules, which are not to be used, and will change without notice


### Corda incubating modules


* **net.corda.confidential**: experimental support for confidential identities on the ledger
* **net.corda.finance**: a range of elementary contracts (and associated schemas) and protocols, such as abstract fungible assets, cash, obligation and commercial paper
* **net.corda.client.jfx**: support for Java FX UI
* **net.corda.client.mock**: client mock utilities
* **Cordformation**: Gradle integration plugins


### Corda internal modules

Everything else is internal and will change without notice, even deleted, and should not be used. This also includes any package that has
`.internal` in it. So for example, `net.corda.core.internal` and sub-packages should not be used.

Some of the public modules may depend on internal modules, so be careful to not rely on these transitive dependencies. In particular, the
testing modules depend on the node module and so you may end having the node in your test classpath.



## The `@DoNotImplement` annotation

Certain interfaces and abstract classes within the Corda API have been annotated
as `@DoNotImplement`. While we undertake not to remove or modify any of these classes’ existing
functionality, the annotation is a warning that we may need to extend them in future versions of Corda.
Cordapp developers should therefore just use these classes “as is”, and *not* attempt to extend or implement any of them themselves.

This annotation is inherited by subclasses and sub-interfaces.
