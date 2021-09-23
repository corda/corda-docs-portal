---
date: '2021-09-21'
title: "Building your first CorDapp"
menu:
  corda-5-dev-preview:
    identifier: corda-5-dev-preview-1-tutorials-building-cordapp
    parent: corda-5-dev-preview-1-tutorials
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
---

Follow this learning path to build your first CorDapp using step-by-step tutorials. You will learn how to implement the functionality and features needed to get any CorDapp up and running with the Corda 5 Developer Preview. It reinforces [best practices for building CorDapps](xxx).

Code samples for this tutorial are provided in Kotlin.

## Before you start

Before you start building your first CorDapp:

- Read about [Corda key concepts](XXX).
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

1. Mars Express issues a voucher to Peter via a ledger transaction. In your CorDapp, this voucher is called `MarsVoucher` and is a [state](../../../../../platform/corda/4.8/os/key-concepts-states.md) on the [ledger](../../../../../platform/corda/4.8/os/key-concepts-ledger.md). This is the first transaction.

2. When Mars Express prepares the ticket Peter requested, the company self-issues the ticket via a self-issue transaction. This is another state on the ledger - `BoardingTicket`. This is the second transaction.

3. Next, Peter goes to Mars Express to redeem his voucher and pick up his ticket, triggering a transaction on the ledger that consumes the `MarsVoucher` state. Three transactions have now been performed.

4. The `BoardingTicket` state is transferred to Peter when the `MarsVoucher` state is consumed and Mars Express gives Peter his ticket. This is the fourth and final transaction.

All of these transactions are initiated by [flows](XXX).

## Changes from Corda 4

If you’ve previously built CorDapps on Corda 4, you will notice some differences when building CorDapps with the Corda 5 Developer Preview:

* Modular APIs - The new APIs are modular, which lets you include or exclude the modules you need to build your CorDapp.
* Flexibility when building your client - You can create your client in any language you like. You are no longer limited to creating the client in a language targeting the JVM. We’ve also removed dependencies on Corda libraries. Additionally, RPC is now HTTP and JSON-based. You must pass JSON parameters and return types must be JSON representables if you want them to be returned over RPC.
* Corda Services - You now use the `@CordaInject` annotation to add any Corda Service to your CorDapp. This replaces everything that was in `FlowLogic`, `ServiceHub`, and all custom Corda Services.
* Corda package files and Corda package bundles (`.cpk` and `.cpb`) - Corda package files are the standard way to distribute CorDapps for Corda 5 Developer Preview. Corda package bundles are composed of multiple Corda package files. They are bundled in preparation for deployment.
* Testing changes - Integration and unit testing your CorDapp is now easier.

More details about these changes are covered in the tutorial for each topic. Contracts in the Corda 5 Developer Preview are implemented in the same way as in Corda 4.

## Next steps

Follow these tutorials in sequential order to build your CorDapp:

1. [Write states](c5-basic-cordapp-state.md)

2. [Write contracts](c5-basic-cordapp-contract.md)

3. [Write flows](c5-basic-cordapp-flows.md)

4. [Run your CorDapp](XXX)

5. [Conduct integration testing](c5-basic-cordapp-int-test.md)
