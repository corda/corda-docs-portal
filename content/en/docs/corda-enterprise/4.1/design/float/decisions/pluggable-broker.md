+++
date = "2020-01-08T09:59:25Z"
title = "Design Decision: Pluggable Broker prioritisation"
aliases = [ "/releases/4.1/design/float/decisions/pluggable-broker.html",]
menu = [ "corda-enterprise-4-1",]
tags = [ "pluggable", "broker",]
+++


# Design Decision: Pluggable Broker prioritisation


## Background / Context

A decision on when to prioritise implementation of a pluggable broker has implications for delivery of key messaging
                components including the [float](../design.md).


## Options Analysis


### 1. Deliver pluggable brokers now


#### Advantages


* Meshes with business opportunities from HPE and Solace Systems.


* Would allow us to interface to existing Bank middleware.


* Would allow us to switch away from Artemis if we need higher performance.


* Makes our AMQP story stronger.



#### Disadvantages


* More up-front work.


* Might slow us down on other priorities.



### 2. Defer development of pluggable brokers until later


#### Advantages


* Still gets us where we want to go, just later.


* Work can be progressed as resource is available, rather than right now.



#### Disadvantages


* Have to take care that we have sufficient abstractions that things like CORE connections can be replaced later.


* Leaves HPE and Solace hanging even longer.



### 3. Never enable pluggable brokers


#### Advantages


* What we already have.



#### Disadvantages


* Ties us to ArtemisMQ development speed.


* Not good for our relationship with HPE and Solace.


* Probably limits our maximum messaging performance longer term.



## Recommendation and justification

Proceed with Option 2 (defer development of pluggable brokers until later)


## Decision taken


* [Design Review Board Meeting Minutes](drb-meeting-20171116.md)
    * [Attendees](drb-meeting-20171116.md#attendees)

    * [Minutes](drb-meeting-20171116.md#minutes)
        * [TLS termination](drb-meeting-20171116.md#id1)

        * [E2E encryption](drb-meeting-20171116.md#id2)

        * [AMQP vs. custom protocol](drb-meeting-20171116.md#id3)

        * [Pluggable broker prioritisation](drb-meeting-20171116.md#id4)

        * [Inbound only vs. inbound & outbound connections](drb-meeting-20171116.md#inbound-only-vs-inbound-outbound-connections)

        * [Overall design and implementation plan](drb-meeting-20171116.md#overall-design-and-implementation-plan)




Proceed with Option 2 - Defer support for pluggable brokers until later, except in the event that a requirement to do so emerges from higher priority float / HA work. (RGB, JC, MH agreed)


