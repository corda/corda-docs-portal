---
date: '2020-04-07T12:00:00Z'
menu:
    corda-enterprise-4-6:
        parent: corda-enterprise-4-6-running-a-notary-cluster-faq-toctree
tags:
- notary
- load
- balancing
weight: 2
title: Notary Load Balancing
---


# Notary Load Balancing

Load balancing for notaries as mentioned in ha-notary-service-setup.rst is done in a round robin fashion
on the client side by Artemis.


## How are clustered notaries resolved by Artemis?

Notary workers in a cluster which share the same `serviceLegalName` register their IP addresses with the network map under said legal name.
The node, whenever trying to resolve the legal name, will provide all the addresses to Artemis, which will handle forwarding
to the appropriate notary worker.


## Why is the load balancing on the client side?

While server side solutions are possible, client side was chosen for future flexibility. As any notary worker in the
cluster might be an adversary and deny service, the client needs to have the ability to rotate to different notaries and go
through each one, until a non faulty one is discovered.


## What happens if a notary in cluster becomes unavailable and does not respond?

As described in [Notary Failover](notary-failover.md), the client node will retry the flow. That retry goes to Artemis, which because of round
robin style of communication with the cluster, would send the flow to the next notary worker. For example client sends to notary worker 1, which
becomes unavailable, client times out while waiting for respond and retries the flow automatically which now gets sent to notary worker 2. Note that
the retry can also happen in Artemis if notary worker 1 becomes unavailable before acknowledging that it has received the flow message.


## Can a specific notary from the cluster be selected for notarisation?

That is currently impossible.


## In what order are notarisation requests processed?

If one Corda node sends multiple notarisation requests which try to spend the same state, there is no guarantee which will be processed first.
While technically it should be first in first out, in reality it’s quite possible in the case of a HA notary that the first request gets sent
to notary 1 and the second request gets sent to notary 2. If notary 2 processes the request faster the FIFO is not met and the request on notary
1 will error out. Such a race on a state shouldn’t normally be possible unless it’s done intentionally.

