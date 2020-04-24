---
aliases:
- /releases/3.0/design/hadr/decisions/near-term-target.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- near
- term
- target
title: 'Design Decision: Near-term target for node HA'
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Design Decision: Near-term target for node HA


## Background / Context

Designing for high availability is a complex task which can only be delivered over an operationally-significant
timeline. It is therefore important to determine the target state in the near term as a precursor to longer term
outcomes.


## Options Analysis


### 1. No HA


#### Advantages


* Reduces developer distractions.


#### Disadvantages


* No backstop if we miss our targets for fuller HA.
* No answer at all for simple DR modes.


### 2. Hot-cold (see [HA design doc]({{% ref "../design.md" %}}))


#### Advantages


* Flushes out lots of basic deployment issues that will be of benefit later.
* If stuff slips we at least have a backstop position with hot-cold.
* For now, the only DR story we have is essentially a continuation of this mode
* The intent of decisions such as using a loadbalancer is to minimise code changes


#### Disadvantages


* Distracts from the work for more complete forms of HA.
* Involves creating a few components that are not much use later, for instance the mutual exclusion lock.


## Recommendation and justification

Proceed with Option 2: Hot-cold.


## Decision taken

Adopt option 2: Near-term target: Hot Cold (RGB, JC, MH agreed)



* [Design Review Board Meeting Minutes](drb-meeting-20171116.md)
    * [Attendees](drb-meeting-20171116.md#attendees)
    * [Minutes](drb-meeting-20171116.md#minutes)
        * [Near-term-target, Medium-term target](drb-meeting-20171116.md#near-term-target-medium-term-target)
        * [Message storage](drb-meeting-20171116.md#id1)
        * [Broker separation](drb-meeting-20171116.md#id2)
        * [Load balancers and multi-IP](drb-meeting-20171116.md#id3)
        * [Crash shell](drb-meeting-20171116.md#id4)







