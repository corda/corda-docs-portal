---
aliases:
- /releases/release-V3.2/corda-api.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-2:
    identifier: corda-os-3-2-corda-api
    parent: corda-os-3-2-building-a-cordapp-index
    weight: 1080
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


## Internal APIs and stability guarantees

Corda 3.0 provides a stable wire protocol and support for database upgrades. Therefore, you should expect to be able to migrate persisted data from 3.0 to future versions. However, it will be necessary to recompile applications against future versions of the API until we begin offering ABI stability as well.

Additionally, please note the Corda 3.0 release has been security audited at a rudimentary level so to ensure node security is maintained the following best practices should be followed:


* Credentials for RPC users, database connections, and shell users should be created using a secure password generator, preferably from the command line of the node host.
* Nodes should never be deployed using default or development mode credentials.
* Corda nodes should use one of the supported database platforms, in preference to the default H2 database which is intended for development purposes only. Postgres is a supported platform.
* Nodes should be operated within a secure network (such as a DMZ) that restricts inbound and outbound traffic to only the required ports. Specifically, node operators should aim to allow access to peer-to-peer traffic from the internet. RPC and database connections should be internal only.
* The node webserver module is deprecated and should not be deployed in a production environment because it is not built to the same security standards as the Corda node.

Corda artifacts can be required from Java 9 Jigsaw modules.
From within a `module-info.java`, you can reference one of the modules e.g., `requires net.corda.core;`.


{{< warning >}}
While Corda artifacts can be required from `module-info.java` files, they are still not proper Jigsaw modules,
because they rely on the automatic module mechanism and declare no module descriptors themselves. We plan to integrate Jigsaw more thoroughly in the future.

{{< /warning >}}



## Corda stable modules

The following modules have a stable API we commit not to break in following releases, unless an incompatible change is required for security reasons:


* **Core (net.corda.core)**: core Corda libraries such as crypto functions, types for Corda’s building blocks: states, contracts, transactions, attachments, etc. and some interfaces for nodes and protocols
* **Client RPC (net.corda.client.rpc)**: client RPC
* **Client Jackson (net.corda.client.jackson)**: JSON support for client applications
* **Test Utils (net.corda.testing.core)**: generic test utilities
* **Test Node Driver (net.corda.testing.node, net.corda.testing.driver)**: test utilities to run nodes programmatically
* **Http Test Utils (net.corda.testing.http)**: a small set of utilities for making HttpCalls, aimed at demos and tests.
* **DSL Test Utils (net.corda.testing.dsl)**: a simple DSL for building pseudo-transactions (not the same as the wire protocol) for testing purposes.
* **Dummy Contracts (net.corda.testing.contracts)**: dummy state and contracts for testing purposes
* **Mock Services (net.corda.testing.services)**: mock service implementations for testing purposes


## Corda incubating modules

The following modules don’t yet have a completely stable API, but we will do our best to minimise disruption to
developers using them until we are able to graduate them into the public API:


* **net.corda.confidential.identities**: experimental support for confidential identities on the ledger
* **net.corda.finance**: a range of elementary contracts (and associated schemas) and protocols, such as abstract fungible assets, cash, obligation and commercial paper
* **net.corda.client.jfx**: support for Java FX UI
* **net.corda.client.mock**: client mock utilities
* **Cordformation**: Gradle integration plugins


## Corda unstable modules

The following modules are available but we do not commit to their stability or continuation in any sense:


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
* **net.corda.verifier**: allows out-of-node transaction verification, allowing verification to scale horizontally
* **net.corda.webserver**: is a servlet container for CorDapps that export HTTP endpoints. This server is an RPC client of the node
* **net.corda.sandbox-creator**: sandbox utilities
* **net.corda.quasar.hook**: agent to hook into Quasar and provide types exclusion lists


{{< warning >}}
Code inside any package in the `net.corda` namespace which contains `.internal` or in `net.corda.node` for internal use only.
Future releases will reject any CorDapps that use types from these packages.

{{< /warning >}}




## The `@DoNotImplement` annotation

Certain interfaces and abstract classes within the Corda API have been annotated
as `@DoNotImplement`. While we undertake not to remove or modify any of these classes’ existing
functionality, the annotation is a warning that we may need to extend them in future versions of Corda.
Cordapp developers should therefore just use these classes “as is”, and *not* attempt to extend or implement any of them themselves.

This annotation is inherited by subclasses and subinterfaces.

