---
date: 2021-08-24
section_menu: tutorials
menu:
  tutorials:
    parent: corda-5-building-template-cordapp-intro
    name: Modify the state
    weight: 150
    identifier: corda-5-template-cordapp-modify-state
title: Modify the state
---

In Corda, facts on the blockchain are represented as states. States are instances of classes that implement [`ContractState`](https://docs.corda.net/docs/corda-os/4.8/api-states.html#contractstate).  This tutorial shows you how to modify the template state to define a new state type that records probes being sent between two parties.

## Before you start

Before you start modifying the template state, familiarize yourself with:

* [Key concepts: States](XXX)
* [API: States](https://docs.corda.net/docs/corda-os/4.8/api-states.html#contractstate)

<!-- In some places I'm adding full links to 4.8 docs. These must be replaced with relative links before release, but I wanted to note the pages for now.  -->

## Define the `ProbeState`

<!-- Explain in small chunks, with code snippets in each section, how to define the state. I'm following the general steps from 4.8, but this may be different in C5/for this CorDapp. -->

### Add annotations

`@BelongsToContract(ProbeContract::class)`

### Implement the state

### Add private variables

### Add required variables and parameters

### Add the constructor

### Add getters

### Add imports

## Outcome



## Next steps
