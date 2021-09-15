---
date: 2021-09-15
section_menu: tutorials
section_menu: tutorials
menu:
  tutorials:
    parent: tutorials-corda-5
    name: Building your first basic CorDapp
    weight: 1010
    identifier: corda-corda-5.0-dev-preview-1-os-tutorial-c5-basic-cordapp-intro
title: Building your first basic CorDapp
---

Follow this learning path to build your first CorDapp with a step-by-step guide. This set of tutorials teaches you how to implement the functionality and features you will need to get any CorDapp up and running with the Corda 5 Developer Preview. It reinforces [best practices for building CorDapps](xxx).

Code samples for this tutorial are provided in Kotlin.

## Before you start

Before you start building your first CorDapp:

- Read about [Corda key concepts](../../../../../platform/corda/4.8/os/key-concepts.html). <!-- Added link to C4 key concepts. Same in other key concepts references throughout doc. XXX -->
- [Get set up for CorDapp development](XXX).
- [Deploy a local Corda 5 network](XXX).
- [Run a sample CorDapp](../run-demo-cordapp.md).
- Take a look at the Corda 5 Developer Preview [CorDapp template](XXX).

## The story

This example showcases a delivery versus payment (DvP) scenario. You are building a CorDapp for a space travel company that wants to offer a way for customers to purchase a voucher that they will later redeem for a ticket to go to Mars.

There are two parties involved in this transaction:

- The space travel company - Mars Express.
- A customer - let's call him Peter.

Your CorDapp must follow this process:

1. Mars Express issues a voucher to Peter for the ticket he wishes to buy.

2. Mars Express prepares the ticket that Peter requested.

3. Peter goes to the launch site to redeem his voucher and collect his ticket.

4. The voucher is marked as spent and Mars Express gives Peter his ticket.

An important feature of this CorDapp is that the voucher cannot be used more than once. It must be considered invalid after it is redeemed.

## How will it work on Corda?

1. Mars Express issues a voucher to Peter via a ledger transaction. In your CorDapp this voucher is called `MarsVoucher` and is a [state](../../../../../platform/corda/4.8/os/key-concepts-states.md) on the [ledger](../../../../../platform/corda/4.8/os/key-concepts-ledger.md). One transaction has been performed so far.

2. When Mars Express prepares the ticket Peter requested, the company self-issues the ticket via a self-issue transaction. This is another state on the ledger - `BoardingTicket`. Two transactions have been performed so far.

3. Next, Peter goes to Mars Express to redeem his voucher and pick up his ticket, triggering a transaction on the ledger that consumes the `MarsVoucher` state. Three transactions have been performed so far.

4. The `BoardingTicket` state is transferred to Peter when the `MarsVoucher` state is consumed and Mars Express gives Peter his ticket.

All of these transactions are initiated by [flows](../../../../../platform/corda/4.8/os/key-concepts-flows.md).

## Changes from Corda 4

If you’ve previously built CorDapps on Corda 4, you will notice some differences when building CorDapps with the Corda 5 Developer Preview:

* Modular APIs - The new APIs are modular, which lets you include or exclude the modules you need to build your CorDapp. For example, maybe your CorDapp doesn’t require smart contracts - then you can feel free to leave this module out.
* Flow interface - The flow interface changes the way you call flows in your CorDapp.
* Flexibility building the client - You can create your client in any language you like. You are no longer limited to creating the client in a language targeting the JVM. We’ve also removed dependencies on Corda libraries.
* Corda Services - You now use the `@CordaInject` annotation to add any Corda Service to your CorDapp. This replaces everything that was in `FlowLogic`, `ServiceHub`, and all custom Corda Services.
* RPCClient - RPC is now HTTP and JSON-based. You must pass JSON parameters and return types must be JSON representables if you want them to be returned over RPC.
Corda package files and Corda package bundles (`.cpk` and `.cpb`) - Corda package files are the standard way to distribute CorDapps for Corda 5 Developer Preview. Corda package bundles are composed of multiple Corda package files. They are bundled in preparation for deployment.
* Testing changes - Integration and unit testing your CorDapp is now easier.

These changes will be covered in more detail in the tutorial for each topic.

## Next steps

Follow these tutorials in sequential order to build your CorDapp:

<!---These will all link to the new tutorials when they are added.--->

1. [Write states](c5-basic-cordapp-state.md)

2. [Write contracts](c5-basic-cordapp-contract.md)

3. [Write flows](c5-basic-cordapp-flows.md)

4. Conduct unit testing

5. Conduct integration testing

6. Run your CorDapp
