---
aliases:
- /releases/4.3/running-a-notary-cluster/ha-notary-service-overview.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-ha-notary-service-overview
    parent: corda-enterprise-4-3-corda-enterprise
    weight: 1010
tags:
- ha
- notary
- service
- overview
title: Notary Service
---

# Corda Enterprise Notary Service Overview

A highly-available Corda notary service is made up of two components:

* The *notary workers*: A set of Corda notary nodes that each has a separate legal identity but
share a single service identity, and are configured to work together in high-availability mode
* The *notary state DB*: A single logical database that all the notary workers connect to and
that is itself configured to be highly-available

In addition to the shared database for the notary state, each notary worker requires its own
database for its node state (such as its identity), since the notary workers are just standard
Corda nodes that have been configured to operate in notary mode.

The can visualize this as follows, with the Corda client nodes in green on the top, the Corda
notary worker nodes in red in the middle, and the database nodes on the bottom in blue.

![ha notary overview2](/en/ha-notary-overview2.png "ha notary overview2")
Client nodes requesting notarisation from the notary will connect to the available notary workers
in a round-robin fashion. The task of a worker node is to verify the notarisation request, the
transaction timestamp (if present), and resolve and verify the transaction chain (if the notary
service is validating). It then commits the transaction’s input states to the database.

Since the notary pool consists of several database nodes and several notary workers, it is highly
available, allowing it to continue to process notarisation requests even if individual database
nodes and/or notary workers fail. For example, a three-node notary cluster can tolerate one crash
fault.

{{< note >}}
In production you should consider running five nodes or more, to be able to
tolerate more than one simultaneous crash fault. Although a single Corda notary
worker is enough to serve notarisation requests in practice, its capacity might
not be sufficient depending on your throughput and latency requirements.
{{< /note >}}

If desired, you can choose to run each database server and its Corda notary worker on the same
machine:

![ha notary colocated](/en/ha-notary-colocated.png "ha notary colocated")
