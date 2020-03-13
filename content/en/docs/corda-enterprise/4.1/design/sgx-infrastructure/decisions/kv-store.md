---
aliases:
- /releases/4.1/design/sgx-infrastructure/decisions/kv-store.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- kv
- store
title: 'Design Decision: Key-value store implementation'
---

[![fg005 corda b](https://www.corda.net/wp-content/uploads/2016/11/fg005_corda_b.png "fg005 corda b")](https://www.corda.net/wp-content/uploads/2016/11/fg005_corda_b.png)


# Design Decision: Key-value store implementation

This is a simple choice of technology.


## Options Analysis


### A. ZooKeeper


#### Advantages


* Tried and tested
* HA team already uses ZooKeeper


#### Disadvantages


* Clunky API
* No HTTP API
* Hand-rolled protocol


### B. etcd


#### Advantages


* Very simple API, UNIX philosophy
* gRPC
* Tried and tested
* MVCC
* Kubernetes uses it in the background already
* “Successor” of ZooKeeper
* Cross-platform, OSX and Windows support
* Resiliency, supports backups for disaster recovery


#### Disadvantages


* HA team uses ZooKeeper


### C. Consul


#### Advantages


* End to end discovery including UIs


#### Disadvantages


* Not very well spread
* Need to store other metadata as well
* HA team uses ZooKeeper


## Recommendation and justification

Proceed with Option B (etcd). It’s practically a successor of ZooKeeper, the interface is quite simple, it focuses on
primitives (CAS, leases, watches etc) and is tried and tested by many heavily used applications, most notably
Kubernetes. In fact we have the option to use etcd indirectly by writing Kubernetes extensions, this would have the
advantage of getting readily available CLI and UI tools to manage an enclave cluster.

