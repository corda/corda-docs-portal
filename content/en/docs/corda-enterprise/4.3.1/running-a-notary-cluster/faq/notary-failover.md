---
aliases:
- /releases/4.3.1/running-a-notary-cluster/faq/notary-failover.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3-1:
    identifier: corda-enterprise-4-3-1-notary-failover
    parent: corda-enterprise-4-3-1-ha-notary-service-overview
    weight: 700
tags:
- notary
- failover
title: Notary Failover
---


# Notary Failover

Corda has built in features that would retry flows on specific cases of failure. See node-flow-hospital for information that applies to all flows.

The FinalityFlow contains notary specific logic which can initiate a back-pressure aware subflow since minimum platform version 4.
The backpressure aware subflow has configured timeout and retry with specific logic relating
to the [ETA mechanism](eta-mechanism.md).

## How does the timeout work?

It is based on the `flowTimeout` section of the node configuration. Flows to HA notaries will be retried after the configured
time. Information can be found in the [Corda configuration](../../corda-configuration-file.md).

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
