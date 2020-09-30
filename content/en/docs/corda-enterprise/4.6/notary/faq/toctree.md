---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-running-a-notary-cluster-faq-toctree
    name: "Notary FAQs"
    parent: corda-enterprise-4-6-corda-nodes-notary-operate
title: Frequently-Asked-Questions
weight: 150
---


# Frequently-Asked-Questions

Frequently asked questions for anything notary related:



* [ETA Mechanism Overview](eta-mechanism.md)
    * [What is the ETA mechanism?](eta-mechanism.md#what-is-the-eta-mechanism)
    * [How is the ETA calculated?](eta-mechanism.md#how-is-the-eta-calculated)
    * [Why is there an ETA mechanism?](eta-mechanism.md#why-is-there-an-eta-mechanism)
    * [What happens if I just invoke FinalityFlow again after getting told to wait?](eta-mechanism.md#what-happens-if-i-just-invoke-finalityflow-again-after-getting-told-to-wait)
    * [How can I configure ETA threshold?](eta-mechanism.md#how-can-i-configure-eta-threshold)


* [Notary Load Balancing](notary-load-balancing.md)
    * [How are clustered notaries resolved by Artemis?](notary-load-balancing.md#how-are-clustered-notaries-resolved-by-artemis)
    * [Why is the load balancing on the client side?](notary-load-balancing.md#why-is-the-load-balancing-on-the-client-side)
    * [What happens if a notary in cluster becomes unavailable and does not respond?](notary-load-balancing.md#what-happens-if-a-notary-in-cluster-becomes-unavailable-and-does-not-respond)
    * [Can a specific notary from the cluster be selected for notarisation?](notary-load-balancing.md#can-a-specific-notary-from-the-cluster-be-selected-for-notarisation)
    * [In what order are notarisation requests processed?](notary-load-balancing.md#in-what-order-are-notarisation-requests-processed)


* [Notary Failover](notary-failover.md)
    * [How does the timeout work?](notary-failover.md#how-does-the-timeout-work)
    * [What is the back off mechanism?](notary-failover.md#what-is-the-back-off-mechanism)
    * [What happens on multiple successful responses caused by retrying?](notary-failover.md#what-happens-on-multiple-successful-responses-caused-by-retrying)
    * [Is it possible to receive a success and failure because of retrying?](notary-failover.md#is-it-possible-to-receive-a-success-and-failure-because-of-retrying)
    * [If there is a network outage/partition, how does this affect the notary?](notary-failover.md#if-there-is-a-network-outage-partition-how-does-this-affect-the-notary)
