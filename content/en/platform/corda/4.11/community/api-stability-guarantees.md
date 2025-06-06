---
aliases:
- /head/api-stability-guarantees.html
- /HEAD/api-stability-guarantees.html
- /api-stability-guarantees.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-11:
    identifier: corda-community-4-11-api-stability-guarantees
    parent: corda-community-4-11-versioning-and-upgrades
    weight: 1010
tags:
- api
- stability
- guarantees
title: API stability guarantees
---


Corda makes certain commitments about which parts of the Corda 4 API will preserve stability and which will not. Over time, more of the Corda 4 API will fall under the stability guarantees. Thus, APIs can be categorized in the following two broad categories:


* **public APIs**, for which API/[ABI](https://en.wikipedia.org/wiki/Application_binary_interface) stability guarantees are provided. See: [Public API]({{< relref "#public-api" >}})
* **non-public APIs**, for which no stability guarantees are provided. See: [Non-public API (experimental)]({{< relref "#non-public-api-experimental" >}})

## Public API

The following modules form part of the Corda 4 public API and we commit to API/ABI stability in following releases, unless an incompatible change is required for security reasons:


* **Core (net.corda.core)**: core Corda libraries such as crypto functions, types for Corda’s building blocks: states, contracts, transactions, attachments, etc. and some interfaces for nodes and protocols.
* **Client RPC (net.corda.client.rpc)**: client RPC
* **Client Jackson (net.corda.client.jackson)**: JSON support for client applications
* **DSL Test Utils (net.corda.testing.dsl)**: a simple DSL for building pseudo-transactions (not the same as the wire protocol) for testing purposes.
* **Test Node Driver (net.corda.testing.node, net.corda.testing.driver)**: test utilities to run nodes programmatically
* **Test Utils (net.corda.testing.core)**: generic test utilities
* **Http Test Utils (net.corda.testing.http)**: a small set of utilities for making HttpCalls, aimed at demos and tests.
* **Dummy Contracts (net.corda.testing.contracts)**: dummy state and contracts for testing purposes
* **Mock Services (net.corda.testing.services)**: mock service implementations for testing purposes

Additionally, the **Tokens SDK (com.r3.corda.lib.tokens)** available in [the Tokens GitHub repository](https://github.com/corda/token-sdk)
has a stable API.

## Non-public API (experimental)

The following are not part of the Corda 4 public API and no stability guarantees are provided:


* Incubating modules, for which we will do our best to minimise disruption to developers using them until we are able to graduate them into the public API
* Internal modules, which are not to be used, and will change without notice
* Anything defined in a package containing `.internal` (for example, `net.corda.core.internal` and sub-packages should
not be used)
* Any interfaces, classes or methods whose name contains the word `internal` or `Internal`

The **finance module** was the first CorDapp ever written and is a legacy module. Although it is not a part of our API guarantees, we also
don’t anticipate much future change to it. Users should use the tokens SDK instead.


###  Corda incubating modules


* **net.corda.confidential**: experimental support for confidential identities on the ledger
* **net.corda.client.jfx**: support for Java FX UI
* **net.corda.client.mock**: client mock utilities
* **Cordformation**: Gradle integration plugins


### Corda internal modules

Every other module is internal and will change without notice, even deleted, and should not be used.

Some of the public modules may depend on internal modules, so be careful to not rely on these transitive dependencies. In particular, the
testing modules depend on the node module and so you may end having the node in your test classpath.


## The `@DoNotImplement` annotation

Certain interfaces and abstract classes within the Corda API have been annotated
as `@DoNotImplement`. While we undertake not to remove or modify any of these classes’ existing
functionality, the annotation is a warning that we may need to extend them in future versions of Corda.
Cordapp developers should therefore just use these classes “as is”, and *not* attempt to extend or implement any of them themselves.

This annotation is inherited by subclasses and sub-interfaces.

