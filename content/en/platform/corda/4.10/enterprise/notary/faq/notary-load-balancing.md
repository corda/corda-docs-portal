---
date: '2020-04-07T12:00:00Z'
menu:
    corda-enterprise-4-10:
        parent: corda-enterprise-4-9-running-a-notary-cluster-faq-toctree
tags:
- notary
- load
- balancing
weight: 2
title: Notary Load Balancing
---


# Notary load balancing

Load balancing for notaries as mentioned in ha-notary-service-setup.rst is done in a round-robin fashion
on the client side by Artemis.


## How are clustered notaries resolved by Artemis?

Notary workers in a cluster which share the same `serviceLegalName` register their IP addresses with the network map under said legal name.
The node, whenever trying to resolve the legal name, will provide all the addresses to Artemis, which will handle forwarding
to the appropriate notary worker.


## Why is the load balancing on the client side?

While server-side solutions are possible, client side was chosen for future flexibility. As any notary worker in the
cluster might be an adversary, and so deny service, the client needs to have the ability to rotate to different notaries and
cycle through them until a non-faulty one is discovered.


## What happens if a notary in cluster becomes unavailable and does not respond?

As described in [Notary failover](notary-failover.md), the client node will retry the flow. That retry goes to Artemis, which because of the round-robin
style of communication with the cluster, would send the flow to the next notary worker. For example, a client node sends the flow to notary worker 1, which
becomes unavailable, so the client times out while waiting for a response and retries the flow automatically. The flow now gets sent to notary worker 2.
{{< note >}}

The retry can also occur in Artemis if notary worker 1 becomes unavailable before acknowledging that it has received the flow message.

{{< /note >}}



## Can a specific notary from the cluster be selected for notarization?

This is not currently a Corda feature.


## In what order are notarization requests processed?

If one Corda node sends multiple notarization requests which try to spend the same state, there is no guarantee about which of these will be processed first.
Technically, it should be 'first in, first out'. In reality, it’s quite possible in the case of a HA notary that the first request gets sent
to notary 1 and the second request gets sent to notary 2. If notary 2 processes the request faster, the FIFO is not met, and the request on notary
1 will error out. Such a race on a state should not normally be possible - unless done intentionally.

