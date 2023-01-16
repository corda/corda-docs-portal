---
aliases:
- /releases/4.2/running-a-notary.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-running-a-notary
    parent: corda-enterprise-4-2-corda-networks-index
    weight: 1130
tags:
- running
- notary
title: Setting up a notary service
---


# Setting up a notary service

Corda Enterprise comes with two notary implementations built-in:


* **Single-node**: a simple notary service that persists notarisation requests in the node’s database. It is easy to configure
and can be used for testing, or networks that do not have strict availability requirements.
* **Highly available**: a clustered notary service operated by a single party, able to tolerate crash faults.


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
done automatically when creating the network, if using [Network Bootstrapper](network-bootstrapper.md). See [Networks](corda-networks-index.md)
for more details.


## Highly available

Corda Enterprise provides a highly available notary service implementation backed by a replicated Percona XtraDB cluster.
This is the recommended implementation for production networks. See [Setting up a HA notary service](running-a-notary-cluster/toctree.md) for detailed
setup steps.


{{< warning >}}
Upgrading an existing single-node notary to be highly available is currently unsupported.

{{< /warning >}}


