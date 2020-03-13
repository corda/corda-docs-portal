---
aliases:
- /releases/3.3/design/hadr/decisions/crash-shell.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- crash
- shell
title: 'Design Decision: Node starting & stopping'
---


# Design Decision: Node starting & stopping


## Background / Context

The potential use of a crash shell is relevant to high availability capabilities of nodes.


## Options Analysis


### 1. Use crash shell


#### Advantages


* Already built into the node.
* Potentially add custom commands.


#### Disadvantages


* Won’t reliably work if the node is in an unstable state
* Not practical for running hundreds of nodes as our customers already trying to do.
* Doesn’t mesh with the user access controls of the organisation.
* Doesn’t interface to the existing monitoring and control systems i.e. Nagios, Geneos ITRS, Docker Swarm, etc.


### 2. Delegate to external tools


#### Advantages


* Doesn’t require change from our customers
* Will work even if node is completely stuck
* Allows scripted node restart schedules
* Doesn’t raise questions about access control lists and audit


#### Disadvantages


* More uncertainty about what customers do.
* Might be more requirements on us to interact nicely with lots of different products.
* Might mean we get blamed for faults in other people’s control software.
* Doesn’t coordinate with the node for graceful shutdown.
* Doesn’t address any crypto features that target protecting the AMQP headers.


## Recommendation and justification

Proceed with Option 2: Delegate to external tools


## Decision taken

Restarts should be handled by polite shutdown, followed by a hard clear. (RGB, JC, MH agreed)



* [Design Review Board Meeting Minutes](drb-meeting-20171116.md)
    * [Attendees](drb-meeting-20171116.md#attendees)
    * [Minutes](drb-meeting-20171116.md#minutes)
        * [Near-term-target, Medium-term target](drb-meeting-20171116.md#near-term-target-medium-term-target)
        * [Message storage](drb-meeting-20171116.md#id1)
        * [Broker separation](drb-meeting-20171116.md#id2)
        * [Load balancers and multi-IP](drb-meeting-20171116.md#id3)
        * [Crash shell](drb-meeting-20171116.md#id4)







