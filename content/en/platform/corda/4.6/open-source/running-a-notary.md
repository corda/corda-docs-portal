---
aliases:
- /head/running-a-notary.html
- /HEAD/running-a-notary.html
- /running-a-notary.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-running-a-notary
    parent: corda-os-4-6-corda-networks-index
    weight: 1100
tags:
- running
- notary
title: Setting up a notary service
---


# Setting up a notary service

Corda comes with several notary implementations built-in:


* **Single-node**: a simple notary service that persists notarisation requests in the node’s database. It is easy to set up
and is recommended for testing, and production networks that do not have strict availability requirements.
* **Crash fault-tolerant** *(experimental)*: a highly available notary service operated by a single party.
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

See [Validation](key-concepts-notaries.md#key-concepts-notaries-validation) for more details about validating versus non-validating notaries.

For clients to be able to use the notary service, its identity must be added to the network parameters. This will be
done automatically when creating the network, if using [Network Bootstrapper](network-bootstrapper.md). See [Networks](corda-networks-index.md)
for more details.


## Crash fault-tolerant (experimental)

Corda provides a prototype [Raft-based](http://atomix.io/) highly available notary implementation. You can try it out on our
[notary demo](https://github.com/corda/corda/blob/release/os/4.6/samples/notary-demo) page. Note that it has known limitations
and is not recommended for production use.


## Byzantine fault-tolerant (experimental)

A prototype BFT notary implementation based on [BFT-Smart](https://github.com/bft-smart/library) is available. You can
try it out on our [notary demo](https://github.com/corda/corda/blob/release/os/4.6/samples/notary-demo) page. Note that it
is still experimental and there is active work ongoing for a production ready solution. Additionally, BFT-Smart requires Java
serialization which is disabled by default in Corda due to security risks, and it will only work in dev mode where this can
be customised.

We do not recommend using it in any long-running test or production deployments.

