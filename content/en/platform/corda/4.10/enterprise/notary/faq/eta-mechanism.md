---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-9-running-a-notary-cluster-faq-toctree
tags:
- mechanism
weight: 1
title: Backpressure mechanism overview
---


# Backpressure mechanism overview


## What is the backpressure mechanism?

The backpressure mechanism is a method to ensure that the notary is at no point overwhelmed with information and requests. An overwhelmed
notary is more likely to suffer a detriment to performance. To avoid this, Corda uses a simple backpressure mechanism that is applicable to notaries and nodes
above a minimum platform version of 4. Using a configured retry threshold, we compare the measured throughput and determine if
the request is going to require more than that. If so, we respond with a backpressure message.

## How is the retry time calculated?

By inspecting the number of states in the request queue and comparing that to the throughput (measured in states per minute),
the number of seconds until a new request can be processed is calculated.


## Why is there a backpressure mechanism?

Like any other form of backpressure, this mechanism prevents the queuing of redundant requests which occurs when a request is retried before the expected
handling time for the original. Queuing additional redundant requests creates unnecessary work for the notary service,
and uses up processing resources. These resources could otherwise be used for new requests. Retrying requests
too eagerly prevents the notary from running at peak throughput.


## What happens if I just invoke FinalityFlow again after getting told to wait?

If a Corda node is told to wait, its state machine will handle the wait. Nothing will be visible to the CorDapp.
Even if a client runs a modified Corda node, they will experience a cut-off by the backpressure once again and hardly see any benefit.
While the retry time acts more as an estimate than an accurate timeframe, it is a close approximation of response time.
The backpressure mechanism is in place to maximize the throughput of the notary service - assuming clients wait before retrying
their requests, as intended.


## How can I configure backpressure threshold?

In the notary config - `notaryConfig.etaMessageThresholdSeconds`.

