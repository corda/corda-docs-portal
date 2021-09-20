---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-notaries
tags:
- db
- guidelines
title: Highly available database setup guidelines
weight: 2
---


# Highly available database setup guidelines

This document serves to capture general database guidelines to consider when setting up a highly available
database for use with the JPA notary.


## Consistency over availability

The CAP theorem states that no distributed system can simultaneously guarantee consistency, availability and
partition tolerance at the same time. Given that network failures are unavoidable, some form of partition
tolerance must be present in any distributed database setup. Therefore, a notary’s distributed database can
either be consistent or highly available. Consistency is preferred to availability due to the critical nature
of the data stored. A clustered setup will increase availability, depending on the clustering technology used,
but the more important requirement should always be consistency.


## Synchronous replication

Due to the importance of consistency for the data that a notary stores, synchronous replication is required of
any database used with a notary. CockroachDB only supports synchronous replication, one of the reasons it was
chosen for the JPA notary.

Asynchronous replication could result in data loss if data is written to one node which then goes down. For
this reason, it should be avoided in any database used with a notary.


## Impact of latency on performance

It is important to note that latency between database cluster members negatively affects the performance of
the database cluster as a whole. One possible cause of increased latency would be having one or more members
of the cluster were located in geographically separate data centres.

This is ideal from a disaster recovery perspective and is supported by Corda. While performance is negatively
impacted, the prevention of data loss more than makes up for the loss. However, it may be worth bearing this
in mind when performance tuning the notary.


## Transaction isolation

Any database used with the JPA notary should have its transaction isolation level set to no lower than
`READ_COMMITTED`. The JPA notary itself will attempt to use a transaction isolation level of
`READ_COMMITTED`.

