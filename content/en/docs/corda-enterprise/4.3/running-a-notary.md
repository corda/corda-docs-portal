---
title: "Setting up a notary service"
date: 2020-01-08T09:59:25Z
---


# Setting up a notary service
Corda Enterprise comes with two notary implementations built-in:


* **Single-node**: a simple notary service that persists notarisation requests in the node’s database. It is easy to configure
                    and can be used for testing, or networks that do not have strict availability requirements.


* **Highly available**: a clustered notary service operated by a single party, able to tolerate crash faults. See
                    [Corda Enterprise notary services]({{< relref "running-a-notary-cluster/toctree" >}})



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
See [Validation]({{< relref "key-concepts-notaries#key-concepts-notaries-validation" >}}) for more details about validating versus non-validating notaries.

For clients to be able to use the notary service, its identity must be added to the network parameters. This will be
                done automatically when creating the network, if using [Network Bootstrapper]({{< relref "network-bootstrapper" >}}). See [Networks]({{< relref "corda-networks-index" >}})
                for more details.


