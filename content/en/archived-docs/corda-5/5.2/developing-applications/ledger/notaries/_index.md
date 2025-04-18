---
description: Learn about Corda's uniqueness consensus service.
date: '2024-02-27'
title: "Notaries"
menu:
  corda52:
    identifier: corda52-develop-notaries
    parent: corda52-fundamentals-ledger
    weight: 5025
---
# Notaries

The notary is Corda’s uniqueness consensus service. The notary’s primary role is to prevent double-spends by ensuring each transaction contains only unique unconsumed input {{< tooltip >}}states{{< /tooltip >}}. It also acts as the time-stamping authority. Every transaction includes a time window and it can only be notarized during that window.
A notary service is formed by one or more notary workers that together form a notary cluster. The cluster’s signature is obtained once it verifies that a proposed transaction’s input states have not already been consumed by a prior transaction. Upon determining this, the notary cluster will either:

* Sign the transaction in cases where all input states are found to be unique.
* Reject the transaction and flag that a double-spend attempt has occurred in cases where any of the input states are identical to those already encountered in a previous transaction.

Every state has an appointed notary cluster, so the cluster only notarizes a transaction if it is the appointed notary cluster of all of the transaction’s input states. A network can have several notary clusters, all running different consensus algorithms.

## Multiple Notaries

Each Corda network can have multiple notary clusters. This has several benefits:

* **Choice of protocol:** Nodes can choose the preferred notary cluster on a per-transaction basis.
* **Load balancing:** Spreading the transaction load over multiple notary clusters allows higher transaction throughput for the platform overall.
* **Low latency:** Latency can be minimized by choosing a notary cluster physically closer to the transacting parties.
