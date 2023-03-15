---
date: '2020-04-07T12:00:00Z'
menu:
    corda-enterprise-4-8:
        parent: corda-enterprise-4-8-running-a-notary-cluster-faq-toctree
tags:
- notary
- failover
weight: 3
title: Notary Failover
---


# Notary failover

Corda has built-in features to allow for the retrying of flows in specific cases of failure.
See [Flow Hospital](content/en/platform/corda/4.8/enterprise/node/node-flow-hospital.md) for information that applies
to all flows.

The FinalityFlow contains notary-specific logic which can initiate a backpressure-aware sub-flow since minimum platform version 4.
The backpressure aware subflow has configured timeout and retry with specific logic relating
to the [backpressure mechanism](eta-mechanism.md).


## How does the timeout work?

It is based on the `flowTimeout` section of the node configuration. Flows to HA notaries will be retried after the configured
time. Information can be found in the [Corda configuration file]({{< relref "../../node/setup/corda-configuration-file.md" >}}).


## What is the backpressure mechanism?

The backpressure mechanism is described in [backpressure mechanism overview](eta-mechanism.md).


## What happens on multiple successful responses caused by retrying?

The first successful response will be mapped to the correct flow and proceed, while the second will be discarded, as the flow that it is
attempting to map to no longer exists. A warning will be logged into the console that a response has nothing to go to, but that
is expected behaviour.


## Is it possible to receive a success and failure because of retrying?

Notarization requests are idempotent and can be retried, the same request should lead to the same response when retried.
Previously notarized transactions are saved so that future repeated requests can be answered appropriately.


## If there is a network outage/partition, how does this affect the notary?

We are prioritizing consistency over availability. Therefore the service will halt on the minority side of a network partition.

