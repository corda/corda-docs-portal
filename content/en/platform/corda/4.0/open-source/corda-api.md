---
aliases:
- /releases/release-V4.0/corda-api.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-0:
    identifier: corda-os-4-0-corda-api
    weight: 40
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
* **Test Utils (net.corda.testing.core)**: generic test utilities
* **Test Node Driver (net.corda.testing.node, net.corda.testing.driver)**: test utilities to run nodes programmatically
* **Http Test Utils (net.corda.testing.http)**: a small set of utilities for making HttpCalls, aimed at demos and tests.
* **DSL Test Utils (net.corda.testing.dsl)**: a simple DSL for building pseudo-transactions (not the same as the wire protocol) for testing purposes.
* **Dummy Contracts (net.corda.testing.contracts)**: dummy state and contracts for testing purposes
* **Mock Services (net.corda.testing.services)**: mock service implementations for testing purposes



## Non-public API (experimental)

The following modules are not part of the Corda’s public API and no backwards compatibility guarantees are provided. They are further categorized in 2 classes:


* the incubating modules, for which we will do our best to minimise disruption to developers using them until we are able to graduate them into the public API
* the unstable modules, which are available but we do not commit to their stability or continuation in any sense


### Corda incubating modules


* **net.corda.confidential**: experimental support for confidential identities on the ledger
* **net.corda.finance**: a range of elementary contracts (and associated schemas) and protocols, such as abstract fungible assets, cash, obligation and commercial paper
* **net.corda.client.jfx**: support for Java FX UI
* **net.corda.client.mock**: client mock utilities
* **Cordformation**: Gradle integration plugins


### Corda unstable modules


* **net.corda.buildSrc**: necessary gradle plugins to build Corda
* **net.corda.node**: core code of the Corda node (eg: node driver, node services, messaging, persistence)
* **net.corda.node.api**: data structures shared between the node and the client module, e.g. types sent via RPC
* **net.corda.samples.network.visualiser**: a network visualiser that uses a simulation to visualise the interaction and messages between nodes on the Corda network
* **net.corda.samples.demos.attachment**: demonstrates sending a transaction with an attachment from one to node to another, and the receiving node accessing the attachment
* **net.corda.samples.demos.bankofcorda**: simulates the role of an asset issuing authority (eg. central bank for cash)
* **net.corda.samples.demos.irs**: demonstrates an Interest Rate Swap agreement between two banks
* **net.corda.samples.demos.notary**: a simple demonstration of a node getting multiple transactions notarised by a distributed (Raft or BFT SMaRt) notary
* **net.corda.samples.demos.simmvaluation**: A demo of SIMM valuation and agreement on a distributed ledger
* **net.corda.samples.demos.trader**: demonstrates four nodes, a notary, an issuer of cash (Bank of Corda), and two parties trading with each other, exchanging cash for a commercial paper
* **net.corda.node.smoke.test.utils**: test utilities for smoke testing
* **net.corda.node.test.common**: common test functionality
* **net.corda.tools.demobench**: a GUI tool that allows to run Corda nodes locally for demonstrations
* **net.corda.tools.explorer**: a GUI front-end for Corda
* **net.corda.tools.graphs**: utilities to infer project dependencies
* **net.corda.tools.loadtest**: Corda load tests
* **net.corda.webserver**: is a servlet container for CorDapps that export HTTP endpoints. This server is an RPC client of the node
* **net.corda.sandbox-creator**: sandbox utilities
* **net.corda.quasar.hook**: agent to hook into Quasar and provide types exclusion lists


{{< warning >}}
Code inside any package in the `net.corda` namespace which contains `.internal` or in `net.corda.node` for internal use only.
Future releases will reject any CorDapps that use types from these packages.

{{< /warning >}}



{{< warning >}}
The web server module will be removed in future. You should call Corda nodes through RPC from your web server of choice e.g., Spring Boot, Vertx, Undertow.

{{< /warning >}}



## The `@DoNotImplement` annotation

Certain interfaces and abstract classes within the Corda API have been annotated
as `@DoNotImplement`. While we undertake not to remove or modify any of these classes’ existing
functionality, the annotation is a warning that we may need to extend them in future versions of Corda.
Cordapp developers should therefore just use these classes “as is”, and *not* attempt to extend or implement any of them themselves.

This annotation is inherited by subclasses and sub-interfaces.
