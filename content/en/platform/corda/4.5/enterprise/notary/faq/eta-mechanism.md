---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-running-a-notary-cluster-faq-toctree
tags:
- mechanism
weight: 1
title: Backpressure mechanism overview
---


# Backpressure mechanism overview


## What is the backpressure mechanism?

It is a simple backpressure mechanism that is applicable to notaries and nodes above minimum platform version 4. Using a
configured retry threshold we compare the measured throughput and determine if the request is going to take more than that,
which if true - we respond with a backpressure message.


## How is the retry time calculated?

By inspecting the amount of states in the request queue and comparing that to the throughput measured in states per minute,
the number of seconds until a new request can be processed is calculated.


## Why is there a backpressure mechanism?

Like any other form of backpressure, it is to prevent queuing redundant requests by retrying requests before the expected
time of handling the original request. Queuing additional redundant requests creates unnecessary work for the notary service
using up resources for processing these redundant requests that could otherwise be used for new requests. Retrying the requests
too eagerly prevents the notary from running at peak throughput.


## What happens if I just invoke FinalityFlow again after getting told to wait?

If a Corda node is told to wait, its state machine will handle the wait and nothing will be visible to the CorDapp.
Even if a client runs a modified Corda node he’ll get cut off by the ETA once again and hardly see any benefit.
While the ETA can hardly be accurate, it is a close approximation of the time when response will arrive.
The backpressure mechanism is in place to maximize the throughput of the notary service assuming clients wait before retrying
their requests as intended.


## How can I configure backpressure threshold?

In the notary config - `notaryConfig.etaMessageThresholdSeconds`.

