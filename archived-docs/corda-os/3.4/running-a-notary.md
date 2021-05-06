---
aliases:
- /releases/release-V3.4/running-a-notary.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-4:
    identifier: corda-os-3-4-running-a-notary
    parent: corda-os-3-4-tutorials-index
    weight: 1120
tags:
- running
- notary
title: Running a notary service
---


# Running a notary service

At present we have several prototype notary implementations:


* `SimpleNotaryService` (single node) – commits the provided transaction input states without any validation.
* `ValidatingNotaryService` (single node) – retrieves and validates the whole transaction history
(including the given transaction) before committing.
* `RaftNonValidatingNotaryService` (distributed) – functionally equivalent to `SimpleNotaryService`, but stores
the committed states in a distributed collection replicated and persisted in a Raft cluster. For the consensus layer
we are using the [Copycat](http://atomix.io/copycat/) framework
* `RaftValidatingNotaryService` (distributed) – as above, but performs validation on the transactions received

To have a node run a notary service, you need to set appropriate `notary` configuration before starting it
(see [Node configuration](corda-configuration-file.md) for reference).

For `SimpleNotaryService` the config is simply:

```kotlin
notary : { validating : false }
```

For `ValidatingNotaryService`, it is:

```kotlin
notary : { validating : true }
```

Setting up a Raft notary is currently slightly more involved and is not recommended for prototyping purposes. There is
work in progress to simplify it. To see it in action, however, you can try out the notary-demo.

Use the *–bootstrap-raft-cluster* command line argument when starting the first node of a notary cluster for the first
time. When the flag is set, the node will act as a seed for the cluster that other members can join.

