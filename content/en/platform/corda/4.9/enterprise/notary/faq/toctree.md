---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-running-a-notary-cluster-faq-toctree
    name: "Notary FAQs"
    parent: corda-enterprise-4-9-corda-nodes-notary-operate
title: Frequently-Asked-Questions
weight: 150
---


# Frequently-Asked-Questions

Frequently asked questions for anything notary related:



* [Backpressure Mechanism Overview](eta-mechanism.md)
    * [What is the backpressure mechanism?](eta-mechanism.html#what-is-the-backpressure-mechanism)
    * [How is the backpressure calculated?](eta-mechanism.html#how-is-the-retry-time-calculated)
    * [Why is there a backpressure mechanism?](eta-mechanism.html#why-is-there-a-backpressure-mechanism)
    * [What happens if I just invoke FinalityFlow again after getting told to wait?](eta-mechanism.html#what-happens-if-i-just-invoke-finalityflow-again-after-getting-told-to-wait)
    * [How can I configure backpressure threshold?](eta-mechanism.html#how-can-i-configure-backpressure-threshold)


* [Notary Load Balancing](notary-load-balancing.md)
    * [How are clustered notaries resolved by Artemis?](notary-load-balancing.html#how-are-clustered-notaries-resolved-by-artemis)
    * [Why is the load balancing on the client side?](notary-load-balancing.html#why-is-the-load-balancing-on-the-client-side)
    * [What happens if a notary in cluster becomes unavailable and does not respond?](notary-load-balancing.html#what-happens-if-a-notary-in-cluster-becomes-unavailable-and-does-not-respond)
    * [Can a specific notary from the cluster be selected for notarisation?](notary-load-balancing.html#can-a-specific-notary-from-the-cluster-be-selected-for-notarisation)
    * [In what order are notarisation requests processed?](notary-load-balancing.html#in-what-order-are-notarisation-requests-processed)


* [Notary Failover](notary-failover.md)
    * [How does the timeout work?](notary-failover.html#how-does-the-timeout-work)
    * [What is the backpressure mechanism?](notary-failover.html#what-is-the-backpressure-mechanism)
    * [What happens on multiple successful responses caused by retrying?](notary-failover.html#what-happens-on-multiple-successful-responses-caused-by-retrying)
    * [Is it possible to receive a success and failure because of retrying?](notary-failover.html#is-it-possible-to-receive-a-success-and-failure-because-of-retrying)
    * [If there is a network outage/partition, how does this affect the notary?](notary-failover.html#if-there-is-a-network-outagepartition-how-does-this-affect-the-notary)
