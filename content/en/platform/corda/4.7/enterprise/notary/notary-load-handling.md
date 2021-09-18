---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    parent: corda-enterprise-4-7-corda-nodes-notary-operate
tags:
- notary
- load
- handling
- backpressure
- eta
title: Notary backpressure and load handling
weight: 5
---


# Notary backpressure and load handling

In high traffic networks, a notary can receive a large number of notarisation requests very quickly. Once the number of requests is more than the notary has capacity to handle, the notarisation response time will increase.

To avoid a notarisation request being lost in the event of a temporary notary worker outage or failure, Corda nodes will retry requests if no response is received. This means that if a node does not receive a response within a predefined time period, the node will resend the notarisation request. If the notary takes longer to complete each request than the retry timer, the notarisation queue will grow, potentially overloading the notary. The backpressure mechanism has been designed to offer responsive retry timers based on the current load of the notary, and prevent successive waves of retry attempts hindering notary performance.

The backpressure mechanism ensures that the retry timer is variable, and based on the timeout configuration settings `timeout` and `backoffBase`, the number of previous retry attempts for the notarisation request (capped at a maximum defined by the `maxRestartCount` configuration setting), and an additional jitter factor. The jitter factor  introduces a degree of randomness to the calculation, helping to protect the notary against sudden increases in notarisation requests causing a subsequent increase in retry attempts.

## Flow Engine Behaviour

When a node makes a notarisation request it receives an estimated completion time. This value represents an upper bound value for time that it should take to process the request, based on the current throughput of the cluster. Once the notarisation request has been processed the node will receive the response, however if no response has been received before the estimated processing time is up then the the node will retry the request.

This mechanism means that requests should always be processed in the event of a notary worker failure, whilst notaries under heavy load do not receive premature, redundant retry requests.

{{< note >}}
The backpressure mechanism is built into the notarisation flow logic within nodes running Corda version >= 4.
{{< /note >}}

## Artemis Messaging Layer Behaviour

A less common scenario that can occur is the notary workers get sent a very large amount of requests which causes the Artemis message broker to become overloaded. For example, if the notary worker receives messages at a greater rate than the maximum rate its Artemis message broker can consume messages from the queue then message processing delays can start to occur.

If running a HA notary cluster then scaling up the worker cluster size will help negate this problem. See [Scaling A Notary Cluster](scaling-a-notary-cluster.md) for more information. The backpressure within the flow engine should also help to prevent this scenario.

