---
aliases:
- /releases/3.3/running-a-notary.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    identifier: corda-enterprise-3-3-running-a-notary
    parent: corda-enterprise-3-3-corda-networks-index
    weight: 1020
tags:
- running
- notary
title: Setting up a notary service
---


# Setting up a notary service

Corda comes with several notary implementations built-in:


* **Single-node**: a simple notary service that persists notarisation requests in the node’s database. It is easy to configure
and can be used for testing, or networks that do not have strict availability requirements.
* **Crash fault-tolerant**: a highly available notary service operated by a single party.
* **Byzantine fault-tolerant** *(experimental)*: a decentralised highly available notary service operated by a group of parties.


## Single-node

To have a regular Corda node provide a notary service you simply need to set appropriate `notary` configuration values
before starting it:

```kotlin
notary : { validating : false }
```

For a validating notary service specify:

```kotlin
notary : { validating : true }
```

See [Validation](key-concepts-notaries.md#validation) for more details about validating versus non-validating notaries.

For clients to be able to use the notary service, its identity must be added to the network parameters. This will be
done automatically when creating the network, if using [Network Bootstrapper](network-bootstrapper.md). See [Corda networks](corda-test-networks.md)
for more details.


## Crash fault-tolerant

Corda Enterprise provides a highly available notary service implementation backed by a replicated Percona XtraDB cluster.
This is the recommended implementation for production networks. See [Setting up a HA notary service](running-a-notary-cluster/toctree.md) for detailed
setup steps.


## Byzantine fault-tolerant (experimental)

A prototype BFT notary implementation based on [BFT-Smart](https://github.com/bft-smart/library) is available. You can
try it out on our [notary demo](https://github.com/corda/corda/tree/release-V3.3/samples/notary-demo) page. Note that it
is still experimental and there is active work ongoing for a production ready solution.

We do not recommend using it in any long-running test or production deployments.

