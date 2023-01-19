---
aliases:
- /releases/release-V2.0/api-index.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-2-0:
    identifier: corda-os-2-0-api-index
    parent: corda-os-2-0-building-a-cordapp-index
    weight: 1050
tags:
- api
title: API
---


# API

This section describes the APIs that are available for the development of CorDapps:



* [API: States](api-states.md)
* [API: Persistence](api-persistence.md)
* [API: Contracts](api-contracts.md)
* [API: Vault Query](api-vault-query.md)
* [API: Transactions](api-transactions.md)
* [API: Flows](api-flows.md)
* [API: Identity](api-identity.md)
* [API: ServiceHub](api-service-hub.md)
* [API: RPC operations](api-rpc.md)
* [API: Core types](api-core-types.md)



Before reading this page, you should be familiar with the [key concepts of Corda](key-concepts.md).


## Internal APIs and stability guarantees


{{< warning >}}
For Corda 1.0 we do not currently provide a stable wire protocol or support for database upgrades.
Additionally, the JSON format produced by the client-jackson module may change in future.
Therefore, you should not expect to be able to migrate persisted data from 1.0 to future versions.

Additionally, it may be necessary to recompile applications against future versions of the API until we begin offering
ABI stability as well. We plan to do this soon after the release of Corda 1.0.

Finally, please note that the 1.0 release has not yet been security audited. You should not run it in situations
where security is required.

{{< /warning >}}


As of Corda 1.0, the following modules export public API that we promise to maintain backwards compatibility for,
unless an incompatible change is required for security reasons:


* core
* client-rpc
* client-jackson

The following modules don’t yet have a completely stable API, but we will do our best to minimise disruption to
developers using them until we are able to graduate them into the public API:


* the Gradle plugins (cordformation)
* node-driver
* confidential-identities
* test-utils
* client-jfx, client-mock
* finance
* anything under the experimental directory (sub-components here may never graduate)

We hope to graduate the node-driver, test-utils and confidential-identities modules in the next feature release
after 1.0. The bulk of the Corda API is found in the core module. Other modules should be assumed to be fully internal.

The web server module will be removed in future: you should build web front-ends for CorDapps using standard frameworks
like Spring Boot, J2EE, Play, etc.

Code that falls into the following packages namespaces are for internal use only and not for public use:


* Any package in the `net.corda` namespace which contains `.internal`
* `net.corda.node`

In the future releases the node upon starting up will reject any CorDapps which uses classes from these packages.

