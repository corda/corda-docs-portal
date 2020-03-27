---
aliases:
- /releases/3.1/design/hadr/decisions/medium-term-target.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- medium
- term
- target
title: 'Design Decision: Medium-term target for node HA'
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Design Decision: Medium-term target for node HA


## Background / Context

Designing for high availability is a complex task which can only be delivered over an operationally-significant
timeline. It is therefore important to determine whether an intermediate state design (deliverable for around March
2018) is desirable as a precursor to longer term outcomes.


## Options Analysis


### 1. Hot-warm as interim state


#### Advantages


* Simpler master/slave election logic
* Less edge cases with respect to messages being consumed by flows.
* Naive solution of just stopping/starting the node code is simple to implement.


#### Disadvantages


* Still probably requires the Artemis MQ outside of the node in a cluster.
* May actually turn out more risky than hot-hot, because shutting down code is always prone to deadlocks and resource leakages.
* Some work would have to be thrown away when we create a full hot-hot solution.


### 2. Progress immediately to Hot-hot


#### Advantages


* Horizontal scalability is what all our customers want.
* It simplifies many deployments as nodes in a cluster are all equivalent.


#### Disadvantages


* More complicated especially regarding message routing.
* Riskier to do this big-bang style.
* Might not meet deadlines.


## Recommendation and justification

Proceed with Option 1: Hot-warm as interim state.


## Decision taken

Adopt option 1: Medium-term target: Hot Warm (RGB, JC, MH agreed)



* [Design Review Board Meeting Minutes](drb-meeting-20171116.md)
    * [Attendees](drb-meeting-20171116.md#attendees)
    * [Minutes](drb-meeting-20171116.md#minutes)
        * [Near-term-target, Medium-term target](drb-meeting-20171116.md#near-term-target-medium-term-target)
        * [Message storage](drb-meeting-20171116.md#id1)
        * [Broker separation](drb-meeting-20171116.md#id2)
        * [Load balancers and multi-IP](drb-meeting-20171116.md#id3)
        * [Crash shell](drb-meeting-20171116.md#id4)







