---
aliases:
- /releases/3.3/design/hadr/decisions/db-msg-store.html
date: '2020-01-08T09:59:25Z'
menu:
- corda-enterprise-3-3
tags:
- db
- msg
- store
title: 'Design Decision: Message storage'
---


# Design Decision: Message storage


## Background / Context

Storage of messages by the message broker has implications for replication technologies which can be used to ensure both
                [high availability](../design.md) and disaster recovery of Corda nodes.


## Options Analysis


### 1. Storage in the file system


#### Advantages


* Out of the box configuration.


* Recommended Artemis setup


* Faster


* Less likely to have interaction with DB Blob rules



#### Disadvantages


* Unaligned capture time of journal data compared to DB checkpointing.


* Replication options on Azure are limited. Currently we may be forced to the ‘Azure Files’ SMB mount, rather than the ‘Azure Data Disk’ option. This is still being evaluated



### 2. Storage in node database


#### Advantages


* Single point of data capture and backup


* Consistent solution between VM and physical box solutions



#### Disadvantages


* Doesn’t work on H2, or SQL Server. From my own testing LargeObject support is broken. The current Artemis code base does allow some pluggability, but not of the large object implementation, only of the SQL statements. We should lobby for someone to fix the implementations for SQLServer and H2.


* Probably much slower, although this needs measuring.



## Recommendation and justification

Continue with Option 1: Storage in the file system


## Decision taken

Use storage in the file system (for now)


* [Design Review Board Meeting Minutes](drb-meeting-20171116.md)
    * [Attendees](drb-meeting-20171116.md#attendees)

    * [Minutes](drb-meeting-20171116.md#minutes)
        * [Near-term-target, Medium-term target](drb-meeting-20171116.md#near-term-target-medium-term-target)

        * [Message storage](drb-meeting-20171116.md#id1)

        * [Broker separation](drb-meeting-20171116.md#id2)

        * [Load balancers and multi-IP](drb-meeting-20171116.md#id3)

        * [Crash shell](drb-meeting-20171116.md#id4)





