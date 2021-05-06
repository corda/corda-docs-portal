---
title: Adding structure with CDL
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-adding-structure"
    weight: 30

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
---

# CDL adds structure to Smart Contracts

For many simple CorDapps, including the ones in the Corda example repos, you may not need a special way of representing CorDapp designs. If you have a simple state, with a single implied status and only one or two commands, you can probably just write the contract code, which will fit on one screen, and see exactly what's going on.

However, if you want to do anything beyond a basic proof of concept, things are likely to get more complicated, especially if you are writing production grade CorDapps that need to deal with many different scenarios.

As complexity increase it quickly becomes difficult to 'think in code' and the corresponding risk of making mistakes goes up.  The primary benefit of CDL is that it provides a level of abstraction that allows you to think about more complicated designs without having to hold all the details in your head.

The way the abstraction works is to split the elements of the Smart Contract design into a standard set of considerations, such as:

* What's my state data?
* What different statuses can the data be in?
* Who are the participants for each status?
* How can I move between each status?

By splitting the design process into these different predefined considerations, you can add structure and robustness to your design thinking. Providing a standardised way to represent each of these considerations in a neat single-page view further empowers you to communicate and reason about the design.

Defining standardised ways to implement and test each consideration can increase confidence in the faithful implementation of the design.
