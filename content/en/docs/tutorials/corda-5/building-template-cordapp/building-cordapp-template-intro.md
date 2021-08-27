---
date: 2021-08-24
section_menu: tutorials
menu:
  tutorials:
    parent: tutorials-corda-5
    name: Building a CorDapp using a template
    weight: 200
    identifier: corda-5-building-template-cordapp-intro
title: Building a CorDapp using a template
linkTitle: Building a CorDapp using a template
---


Now that you've gotten the [demo CorDapp up and running](XXX), let's look at how to build this CorDapp by following the Corda 5 Developer Preview CorDapp template. This learning path walks you through modifying the template to create the Solar System CorDapp.

Follow these steps to build a CorDapp using the template:

1. [Get the template](get-template.md)
2. [Modify the state](modify-state.md)
3. [Modify the contract](modify-contract.md)
4. [Modify the flow](modify-flow.md)
5. [Run your CorDapp](run-cordapp.md)

## Changes from Corda 4

If you've previously built CorDapps on Corda 4, there are a few differences you will notice when building CorDapps with the Corda 5 Developer Preview:

* [Modular APIs](XXX) - The new APIs are modular, which lets you include or exclude the modules you need to build your CorDapp. For example, maybe your CorDapp doesn't require smart contracts - then you can feel free to leave this module out.
* [Flow interface](XXX) - The flow interface changes the way you call flows in your CorDapp.
* Flexibility building the client - You can create your client in any language you like. You are no longer limited to creating the client in a language targeting the JVM. We've also removed dependencies on Corda libraries.
* Corda Services - You now use the `@CordaInject` annotation to add any Corda Service to your CorDapp. This replaces everything that was in `FlowLogic`, `ServiceHub`, and all custom Corda Services.
* RPCClient - RPC is now HTTP and JSON-based. You must pass JSON parameters and return types must be JSON representables if you want them to be returned over RPC.
* [Corda package files](XXX) and [Corda package bundles](XXX) (`.cpk` and `.cpb`) - Corda package files are the standard way to distribute CorDapps for Corda 5 Developer Preview. Corda package bundles are composed of multiple Corda package files. They bundled in preparation for deployment.

You'll see how these features are implemented in the tutorials for this learning path.

## Before you start

Before you dive into the tutorial steps, you should:

* Familiarize yourself with [CorDapps](XXX) and how they work.
* [Set up a local network](XXX).
* [Set up Corda CLI](XXX).
* [Set up CorDapp Builder](XXX).
* [Set up Corda Node CLI](XXX).
* [Run the Solar System sample CorDapp](XXX).

## Use case

If you've already [run the Solar System CorDapp](../run-demo-cordapp.md), then you have an idea of the use case. You need to build a CorDapp that will send probes to celestial bodies in the solar system. The solar system is your local network. The celestial bodies are the nodes on your network.

In most CorDapps you create, you will define:

* States - The facts that are written to the ledger.
* Flows - The procedures for carrying out ledger updates.
* Contracts - The constraints that govern how states of a given type can evolve over time.

In this CorDapp, you define the following components:

### `ProbeState`

`ProbeState` is the state you use to record the probe being sent between the two celestial bodies. It must have the following parameters:

* `launcher` - The party sending the probe.
* `target` - The party being visited by the probe and returning data.
* `message` - The message to be delivered by the probe.
* `planetaryOnly` - An optional smart contract features that specifies if the probe can only travel to planets, or if it can visit any celestial body.

### `LaunchProbeFlow`

This flow lets two celestial bodies (the `launcher` and the `target`) send a message to each other via the `ProbeState`.

<!-- Maybe add a diagram here to demonstrate steps of the flow.-->

### `ProbeContract`

`ProbeContract` is a basic smart contract you will implement in the CorDapp. It enforces rules regarding the the creation of a valid `ProbeState`.

The `ProbeState` contract checks that:

* No input states are consumed when a probe is launched.
* Only one output state is created.
* The launcher and target of the probe are not the same entity.
* All participants are signers.
* The message has content and is not empty.
* If the probe is a planetary probe, it is being sent to a planet.

If any of these contracts checks fail, the CorDapp throws an exception.

This contract should be optional in the CorDapp.

## Next steps

Go to the first tutorial in this learning path, [Get the CorDapp template](get-template.md), to download the project and get started.
