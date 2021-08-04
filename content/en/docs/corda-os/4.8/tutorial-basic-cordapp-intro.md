---
date: '2021-07-26'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-tutorial-basic-cordapp-intro
    parent: corda-os-4-8-tutorials-index
    weight: 1020
tags:
- tutorial
- cordapp
title: Building your first basic CorDapp
---

Follow this learning path to build your first CorDapp with a step-by-step guide to show you the way. This set of tutorials teaches you how to implement the functionality and features you will need to get any CorDapp up and running. It reinforces best practices for building CorDapps.

Code samples for this tutorial will be provided in both Kotlin and Java.

## Before you start

Before you continue on this learning path:

- Read about [Corda key concepts](key-concepts.md).
- [Get set up for CorDapp development](getting-set-up.md).
- [Run the sample CorDapp](cordapp-tutorial.md).
- [Modify a CorDapp template](writing-a-cordapp-using-a-template.md).

## The story

This example showcases a delivery versus payment (DvP) scenario. You are building a CorDapp for an apple orchard that wants to offer a way for customers to purchase a voucher that they will later redeem for a bushel of apples.

There are two parties involved in this transaction:

- The owner of the orchard - Farmer Bob
- A customer - let's call him Peter

Your CorDapp must follow this process:

1. Farmer Bob issues a voucher to Peter for the apples he wishes to buy.

2. Farmer Bob prepares the amount of apples Peter requested.

3. Peter goes to the orchard to pick up his apples and redeems his voucher.

4. The voucher is marked as spent and Farmer Bob gives Peter his apples.

An important feature of this CorDapp is that the voucher cannot be used more than once. It must be considered invalid after it is redeemed.

## How will it work on Corda?

1. Farmer Bob issues a voucher to Peter via a ledger transaction. In your CorDapp this voucher is called `AppleStamp` and is a [state](key-concepts-states.md) on the [ledger](key-concepts-ledger.md). One transaction has been performed so far.

2. When Farmer Bob prepares the apples Peter requested, he self-issues a bushel of apples via a self-issue transaction. This is another state on the ledger - `BasketofApples`. Two transactions have been performed so far.

3. Next, Peter goes to the orchard to pick up his apples and redeems his voucher, triggering a transaction on the ledger that consumes the `AppleStamp` state. Three transactions have been performed so far.

4. The `BasketofApples` state is transferred to Peter when the `AppleStamp` state is consumed and Farmer Bob gives Peter his apples.

All of these transactions are initiated by [flows](key-concepts-flows.md).

## Next steps

Follow these tutorials in sequential order to build your CorDapp:

<!---These will all link to the new tutorials when they are added.--->

1. Write the states

2. Write the contract

  1. Build transactions

  2. Write contract tests

3. Write flows

  1. Write flow tests

4. Conduct integration testing

5. Run your CorDapp

6. Debug and test your CorDapp

7. Use the CordaRPCClient to run your CorDapp
