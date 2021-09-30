---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-notary-operate
tags:
- notary
- load
- handling
title: Behaviour under excessive load
weight: 5
---


# Behaviour under excessive load

In high traffic networks, a notary can receive a large amount of notarisation requests in a short time window. Once this
number starts approaching the capacity the the notary can quickly handle, the notarisation response time will increase.

To avoid a notarisation request being lost in the event of a notary worker temporarily going down, retry functionality is built into Corda.
If the node does not receive a response from the notary in a predefined period of time, the node will resend the notarisation request.
Having this retry period fixed would mean that if the time to process a request starts starts to exceed the retry period, the notary will
get inundated with requests. Hence to ensure the notary does not become overloaded the retry value is variable and based on the backpressure
mechanism.


## Flow Engine Behaviour

When a node makes a notarisation request it will receive back an estimated time to completion. This value represents an upper bound value
for time that it should take to process the request, based on the current throughput of the cluster. Once the notarisation request has been
processed the node will receive the response, however if no response has been received before the estimated processing time is up then the
the node will retry the request.

This mechanism means that requests should always be processed in the event of a notary worker failure, whilst notaries under heavy load do
not receive premature, redundant retry requests.

{{< note >}}
The backpressure mechanism is built into the notarisation flow logic within nodes running Corda version >= 4.

{{< /note >}}

## Artemis Messaging Layer Behaviour

A less common scenario that can occur is the notary workers get sent a very large amount of requests which causes the Artemis message broker
to become overloaded. For example, if the notary worker receives messages at a greater rate than the maximum rate its Artemis message broker
can consume messages from the queue then message processing delays can start to occur.

If running a HA notary cluster then scaling up the worker cluster size will help negate this problem. See [Scaling A Notary Cluster](scaling-a-notary-cluster.md)
for more information. The backpressure within the flow engine should also help to prevent this scenario.

