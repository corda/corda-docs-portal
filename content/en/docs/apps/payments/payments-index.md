---
date: '2020-01-08T09:59:25Z'
menu:
  apps:
    identifier: payments
    name: Payments
tags:
- Payments
- ISO20022
- PSP
title: Payments Alpha
weight: 200
---

# Payments and Modulr payment rail

Corda Payments, including payments on the Modulr payment rail, is an early release feature that allows you to create theoretical and experimental payment solutions in Corda - connecting to real Payment Service Providers (PSPs).

There are two main CorDapps in this version of Corda Payments:

* Payments-core - the main CorDapp that enables all flows required to make payments to a chosen PSP.
* Modulr Payment Rail CorDapp - a ready-to-try CorDapp that allows you to create payments using the Modulr PSP.

There are likely to be substantial architectural improvements as development of these features accelerates towards commercial readiness. This is an opportunity for early adopters to test Corda Payments and engage with the concepts before investing in a commercial payments solution.

Create and test a theoretical payments solution using [Payments-core](payments-core-cordapp).

Try the [Modulr Payment Rail CorDapp](modulr-payment-rail) to trial live payments through the Modulr PSP.
