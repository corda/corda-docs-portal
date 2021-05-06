---
aliases:
- /releases/release-V2.0/running-a-notary.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-2-0:
    identifier: corda-os-2-0-running-a-notary
    parent: corda-os-2-0-tutorials-index
    weight: 1110
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

To have a node run a notary service, you need to set appropriate configuration values before starting it
(see [Node configuration](corda-configuration-file.md) for reference).

For `SimpleNotaryService`, simply add the following service id to the list of advertised services:

```kotlin
extraAdvertisedServiceIds : [ "net.corda.notary.simple" ]
```

For `ValidatingNotaryService`, it is:

```kotlin
extraAdvertisedServiceIds : [ "net.corda.notary.validating" ]
```

Setting up a Raft notary is currently slightly more involved and is not recommended for prototyping purposes. There is
work in progress to simplify it. To see it in action, however, you can try out the notary-demo.

