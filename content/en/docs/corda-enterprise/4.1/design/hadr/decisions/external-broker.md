---
aliases:
- /releases/4.1/design/hadr/decisions/external-broker.html
date: '2020-01-08T09:59:25Z'
menu:
- corda-enterprise-4-1
tags:
- external
- broker
title: 'Design Decision: Broker separation'
---


# Design Decision: Broker separation


## Background / Context

A decision of whether to extract the Artemis message broker as a separate component has implications for the design of
                [high availability](../design.md) for nodes.


## Options Analysis


### 1. No change (leave broker embedded)


#### Advantages


* Least change



#### Disadvantages


* Means that starting/stopping Corda is tightly coupled to starting/stopping Artemis instances.


* Risks resource leaks from one system component affecting other components.


* Not pluggable if we wish to have an alternative broker.



### 2. External broker


#### Advantages


* Separates concerns


* Allows future pluggability and standardisation on AMQP


* Separates life cycles of the components


* Makes Artemis deployment much more out of the box.


* Allows easier tuning of VM resources for Flow processing workloads vs broker type workloads.


* Allows later encrypted version to be an enterprise feature that can interoperate with OS versions.



#### Disadvantages


* More work


* Requires creating a protocol to control external bridge formation.



## Recommendation and justification

Proceed with Option 2: External broker


## Decision taken

The broker should only be separated if required by other features (e.g. the float), otherwise not. (RGB, JC, MH agreed).


* [Design Review Board Meeting Minutes](drb-meeting-20171116.md)
    * [Attendees](drb-meeting-20171116.md#attendees)

    * [Minutes](drb-meeting-20171116.md#minutes)
        * [Near-term-target, Medium-term target](drb-meeting-20171116.md#near-term-target-medium-term-target)

        * [Message storage](drb-meeting-20171116.md#id1)

        * [Broker separation](drb-meeting-20171116.md#id2)

        * [Load balancers and multi-IP](drb-meeting-20171116.md#id3)

        * [Crash shell](drb-meeting-20171116.md#id4)





