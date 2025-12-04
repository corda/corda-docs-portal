---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-11:
    identifier: corda-enterprise-4-11-running-a-notary-cluster-faq-toctree
    name: "Notary FAQs"
    parent: corda-enterprise-4-11-corda-nodes-notary-operate
title: Frequently-Asked-Questions
weight: 150
---


# Frequently-Asked-Questions

Frequently asked questions for anything notary related:



* [Backpressure Mechanism Overview]({{< relref "eta-mechanism.md" >}})
    * [What is the backpressure mechanism?]({{< relref "eta-mechanism.md#what-is-the-backpressure-mechanism" >}})
    * [How is the backpressure calculated?]({{< relref "eta-mechanism.md#how-is-the-retry-time-calculated" >}})
    * [Why is there a backpressure mechanism?]({{< relref "eta-mechanism.md#why-is-there-a-backpressure-mechanism" >}})
    * [What happens if I just invoke FinalityFlow again after getting told to wait?]({{< relref "eta-mechanism.md#what-happens-if-i-just-invoke-finalityflow-again-after-getting-told-to-wait" >}})
    * [How can I configure backpressure threshold?]({{< relref "eta-mechanism.md#how-can-i-configure-backpressure-threshold" >}})


* [Notary load balancing]({{< relref "notary-load-balancing.md" >}})
    * [How are clustered notaries resolved by Artemis?]({{< relref "notary-load-balancing.md#how-are-clustered-notaries-resolved-by-artemis" >}})
    * [Why is the load balancing on the client side?]({{< relref "notary-load-balancing.md#why-is-the-load-balancing-on-the-client-side" >}})
    * [What happens if a notary in cluster becomes unavailable and does not respond?]({{< relref "notary-load-balancing.md#what-happens-if-a-notary-in-cluster-becomes-unavailable-and-does-not-respond" >}})
    * [Can a specific notary from the cluster be selected for notarisation?]({{< relref "notary-load-balancing.md#can-a-specific-notary-from-the-cluster-be-selected-for-notarization" >}})
    * [In what order are notarisation requests processed?]({{< relref "notary-load-balancing.md#in-what-order-are-notarization-requests-processed" >}})


* [Notary failover]({{< relref "notary-failover.md" >}})
    * [How does the timeout work?]({{< relref "notary-failover.md#how-does-the-timeout-work" >}})
    * [What is the backpressure mechanism?]({{< relref "notary-failover.md#what-is-the-backpressure-mechanism" >}})
    * [What happens on multiple successful responses caused by retrying?]({{< relref "notary-failover.md#what-happens-on-multiple-successful-responses-caused-by-retrying" >}})
    * [Is it possible to receive a success and failure because of retrying?]({{< relref "notary-failover.md#is-it-possible-to-receive-a-success-and-failure-because-of-retrying" >}})
    * [If there is a network outage/partition, how does this affect the notary?]({{< relref "notary-failover.md#if-there-is-a-network-outagepartition-how-does-this-affect-the-notary" >}})
