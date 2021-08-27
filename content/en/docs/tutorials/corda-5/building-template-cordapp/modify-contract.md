---
date: 2021-08-24
section_menu: tutorials
menu:
  tutorials:
    parent: corda-5-building-template-cordapp-intro
    name: Modify the contract
    weight: 300
    identifier: corda-5-template-cordapp-modify-contract
title: Modify the contract
---

Depending on your use case, you may want to impose constraints on how states evolve over time in your CorDapp. You can do this by adding smart contracts to your application. Like a real-world contract, smart contracts in Corda impose rules on what kinds of transactions are involved. Every contract must implement the [`Contract`](https://docs.corda.net/docs/corda-os/4.8/api-contracts.html#contract) interface.

In this CorDapp, you want to control if probes can be sent to all celestial bodies or just planets in the `ProbeContract`. There are a few additional constraints you will add to the contract to control general inputs and outputs. This tutorial walks you through adding these constraints.

## Before you start

Before you start modifying the template contract, familiarize yourself with:

* [Key concepts: Contracts](XXX)
* [API: Contracts](https://docs.corda.net/docs/corda-os/4.8/api-contracts.html#contract)

<!-- In some places I'm adding full links to 4.8 docs. These must be replaced with relative links before release, but I wanted to note the pages for now.  -->

## Define the `ProbeContract`

### Add the `Create`command

### Implement the `verify` logic

## Outcome

You have now created the `ProbeContract`. Your code should look something like this:

<!-- Insert code sample.-->

## Next steps

Follow the [Modify the flow](modify-flow.md) tutorial to continue on this learning path.
