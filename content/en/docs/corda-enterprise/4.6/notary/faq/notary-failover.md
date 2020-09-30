---
date: '2020-04-07T12:00:00Z'
menu:
    corda-enterprise-4-6:
        parent: corda-enterprise-4-6-running-a-notary-cluster-faq-toctree
tags:
- notary
- failover
weight: 3
title: Notary Failover
---


# Notary Failover

Corda has built in features that would retry flows on specific cases of failure. See node-flow-hospital for information
that applies to all flows.

The FinalityFlow contains notary specific logic which can initiate a backpressure aware subflow since minimum platform version 4.
The backpressure aware subflow has configured timeout and retry with specific logic relating
to the [ETA mechanism](eta-mechanism.md).


## How does the timeout work?

It is based on the `flowTimeout` section of the node configuration. Flows to HA notaries will be retried after the configured
time. Information can be found in corda-configuration-file.


## What is the back off mechanism?

The back off mechanism is described in [ETA Mechanism Overview](eta-mechanism.md).


## What happens on multiple successful responses caused by retrying?

The first successful response will get mapped to the correct flow and proceed, while the second will be discarded as there will
be no flow to map to anymore. A warning will be logged into the console that a response has nothing to go to, but it is expected
behaviour.


## Is it possible to receive a success and failure because of retrying?

Notarisation requests are idempotent and can be retried, the same request should lead to the same response when retried.
Previously notarised transactions are saved so that future repeated requests can be answered appropriately.


## If there is a network outage/partition, how does this affect the notary?

We are prioritizing consistency over availability. Therefore the service will halt on the minority side of a network partition.

