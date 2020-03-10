---
aliases:
- /releases/3.3/design/hadr/decisions/ip-addressing.html
date: '2020-01-08T09:59:25Z'
menu:
- corda-enterprise-3-3
tags:
- ip
- addressing
title: 'Design Decision: IP addressing mechanism (near-term)'
---


# Design Decision: IP addressing mechanism (near-term)


## Background / Context

End-to-end encryption is a desirable potential design feature for the [high availability support](../design.md).


## Options Analysis


### 1. Via load balancer


#### Advantages


* Standard technology in banks and on clouds, often for non-HA purposes.
* Intended to allow us to wait for completion of network map work.


#### Disadvantages


* We do need to support multiple IP address advertisements in network map long term.
* Might involve small amount of code if we find Artemis doesn’t like the health probes. So far though testing of the Azure Load balancer doesn’t need this.
* Won’t work over very large data centre separations, but that doesn’t work for HA/DR either


### 2. Via IP list in Network Map


#### Advantages


* More flexible
* More deployment options
* We will need it one day


#### Disadvantages


* Have to write code to support it.
* Configuration more complicated and now the nodes are non-equivalent, so you can’t just copy the config to the backup.
* Artemis has round robin and automatic failover, so we may have to expose a vendor specific config flag in the network map.


## Recommendation and justification

Proceed with Option 1: Via Load Balancer


## Decision taken

The design can allow for optional load balancers to be implemented by clients. (RGB, JC, MH agreed)



* [Design Review Board Meeting Minutes](drb-meeting-20171116.md)
    * [Attendees](drb-meeting-20171116.md#attendees)
    * [Minutes](drb-meeting-20171116.md#minutes)
        * [Near-term-target, Medium-term target](drb-meeting-20171116.md#near-term-target-medium-term-target)
        * [Message storage](drb-meeting-20171116.md#id1)
        * [Broker separation](drb-meeting-20171116.md#id2)
        * [Load balancers and multi-IP](drb-meeting-20171116.md#id3)
        * [Crash shell](drb-meeting-20171116.md#id4)







