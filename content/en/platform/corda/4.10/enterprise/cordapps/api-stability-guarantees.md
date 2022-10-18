---
date: '2021-08-16'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-9-cordapps-versioning
tags:
- api
- stability
- guarantees
title: API stability guarantees
weight: 1
---


# API stability guarantees

Corda maintains the stability of specific APIs. APIs are categorized as:

* **Public APIs**, which are APIs/application binary interfaces (ABIs) that are backwards compatible. See [public API](#public-api) for more information.
* **Non-public APIs**. These APIs are not guaranteed to be backwards compatible. See [non-public API (experimental)](#non-public-api-experimental) for more information.

## Public API

The following modules form part of Corda’s public API. These will be backwards compatible for future releases, unless an incompatible change is required for security reasons:

* **Core (net.corda.core)**: Core Corda libraries such as crypto functions, types for Corda’s building blocks (such as states, contracts, transactions, and attachments), and some interfaces for nodes and protocols.
* **Client RPC (net.corda.client.rpc)**.
* **Client Jackson (net.corda.client.jackson)**: JavaScript Object Notation (JSON) support for client applications.
* **DSL Test Utils (net.corda.testing.dsl)**: a simple domain-specific language (DSL) for building pseudo-transactions (this is not the same as the wire protocol) for testing purposes.
* **Test Node Driver (net.corda.testing.node, net.corda.testing.driver)**: test utilities to run nodes programmatically.
* **Test Utils (net.corda.testing.core)**: generic test utilities.
* **Http Test Utils (net.corda.testing.http)**: a small set of utilities for making HTTP calls, aimed at demos and tests.
* **Dummy Contracts (net.corda.testing.contracts)**: dummy state and contracts for testing purposes.
* **Mock Services (net.corda.testing.services)**: mock service implementations for testing purposes.

The **Tokens SDK (com.r3.corda.lib.tokens)** available in the [Tokens GitHub repository](https://github.com/corda/token-sdk)
also has a stable API.

## Non-public API (experimental)

Corda does *not* guarantee  backwards compatibility for:

* Incubating modules (where possible, disruption to developers will be minimized). See [Corda incubating modules](#corda-incubating-modules) for more information.
* **The finance module**: a legacy module. Use the Tokens SDK `com.r3.corda.lib.tokens` (available in the [Tokens GitHub repository](https://github.com/corda/token-sdk) instead.

{{< warning >}}

Do not use the following as they may be changed or deleted without notice.
* Internal modules.
* Package and/or sub-package containing `.internal` (for example, `net.corda.core.internal`).
* Any interfaces, classes or methods whose name contains the word `internal` or `Internal`.

{{< /warning >}}


### Corda incubating modules

Incubating modules are under development, and are subject to change until they graduate to the public API.

* **net.corda.confidential**: experimental support for confidential identities on the ledger.
* **net.corda.client.jfx**: support for Java FX UI.
* **net.corda.client.mock**: client mock utilities.
* **Cordformation**: Gradle integration plugins.


### Corda internal modules

Some public modules may depend on internal modules, so be careful not to rely on these transitive dependencies. In particular, the
testing modules depend on the node module, and so you may end having the node in your test classpath.

## The `@DoNotImplement` annotation

Certain interfaces and abstract classes within the Corda API have been annotated
as `@DoNotImplement`. Removal or modification of these classes’ existing
functionality will be avoided. However, the annotation is a warning that they may be extended in future versions of Corda.
You should only use these classes “as is”, and *not* attempt to extend or implement any of them.

This annotation is inherited by subclasses and sub-interfaces.
