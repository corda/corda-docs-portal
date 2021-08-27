---
date: 2021-08-24
section_menu: tutorials
menu:
  tutorials:
    parent: corda-5-building-template-cordapp-intro
    name: Modify the flow
    weight: 400
    identifier: corda-5-template-cordapp-modify-flow
title: Modify the flow
---

<!-- These are notes of some of the big changes from C4 to C5 in flows. This list is not exhaustive.
## Changes from Corda 4

* Flow Interface
* Corda Services - This and Flow Interface are mentioned on the intro page, but worth it to point them out specifically here and go into more detail. 
* `@Suspendable` annotation - This is now an annotation defined in Corda. You don't need to include Quasar in your `build.gradle` file anymore as it's no longer a dependency.
*`signInitialTransaction` has been renamed to `sign`.
* `SignedTransactionDigest` - A new class that returns transaction IDs, signatures, and states in a JSON format, which lets you send it over RPC.
* `mapOfParams` - JSON parameters are parsed into a map, and then these parameters are validated to make sure the flow has everything it needs. This happened under the hood in Corda 4.-->

A flow encodes a sequence of steps that a node can perform to achieve a specific ledger update. Adding new flows on a node allows the node to handle new business processes.

In this tutorial you will modify the template flow to define the `LaunchProbeFlow`. This flow will lets you send a probe from one celestial body to another, which issues a `ProbeState` onto the ledger.

## Before you start

## Define the `LaunchProbeFlow`

## Outcome

## Next steps
