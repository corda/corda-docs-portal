---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes-notaries
tags:
- running
- notary
title: Setting up a notary service
weight: 1
---


# Setting up a notary service

Corda Enterprise comes with two notary implementations built-in:


* **Single-node**: a simple notary service that persists notarisation requests in the node’s database. It is easy to configure
and can be used for testing, or networks that do not have strict availability requirements.
* **Highly available**: a clustered notary service operated by a single party, able to tolerate crash faults.


{{< warning >}}
Upgrading an existing single-node notary to be highly available is currently unsupported.

{{< /warning >}}



## Single-node notary

To have a regular Corda node provide a notary service you simply need to set appropriate `notary` configuration values
before starting it:

```kotlin
notary : { validating : false }
```

For a validating notary service specify:

```kotlin
notary : { validating : true }
```

For clients to be able to use the notary service, its identity must be added to the network parameters. This will be
done automatically when creating the network, if using [Network Bootstrapper](../network-bootstrapper.md). 
