---
date: '2023-01-11'
title: "Building Your First Basic CorDapp"
menu:
  corda-5-beta:
    parent: corda-5-beta-tutorials-develop
    identifier: corda-5-beta-tutorial-develop-building-your-first-basic-cordapp
    weight: 1000
section_menu: corda-5-beta
---

Follow this learning path to build your first CorDapp with a step-by-step guide. This set of tutorials teaches you how to implement the functionality and features you will need to get any CorDapp up and running. It reinforces [best practices for building CorDapps](../../../../platform/corda/4.8/open-source/writing-a-cordapp.md).

<!---The solution for this CorDapp is available in [Java](https://github.com/corda/samples-java/tree/master/Basic/tutorial-applestamp) and [Kotlin](https://github.com/corda/samples-kotlin/tree/master/Basic/tutorial-applestamp). This tutorial walks you through the Java version of the Apple Stamp CorDapp.--->

## Before you start

Before you start building your first CorDapp:

- Read about [Corda key concepts](../../../introduction/key-concepts.md).
- [Get set up for CorDapp development](../../getting-started/get-started.md).
- [Run the sample CorDapp](../../getting-started/running-your-first-cordapp/run-first-cordapp.md).

## The story

This example showcases a delivery versus payment (DvP) scenario. You are building a CorDapp for an apple orchard that wants to offer a way for customers to purchase a voucher that they will later redeem for a bushel of apples.

There are two parties involved in this transaction:

- The owner of the orchard - Farmer Bob.
- A customer - let's call him Peter.

Your CorDapp must follow this process:

1. Farmer Bob creates and issues a voucher to Peter for the apples he wishes to buy.

2. Farmer Bob prepares the amount of apples Peter requested.

3. Peter goes to the orchard to pick up his apples and redeems his voucher.

4. The voucher is marked as spent and Farmer Bob gives Peter his apples.

An important feature of this CorDapp is that the voucher cannot be used more than once. It must be considered invalid after it is redeemed.

## How will it work on Corda?

1. Farmer Bob issues a voucher to Peter via a ledger transaction. In your CorDapp this voucher is called `AppleStamp` and is a [state](../../ledger/states.md) on the [ledger](../../ledger/ledger.md). One transaction has been performed so far.

2. When Farmer Bob prepares the apples Peter requested, he self-issues a bushel of apples via a self-issue transaction. This is another state on the ledger - `BasketofApples`. Two transactions have been performed so far.

3. Next, Peter goes to the orchard to pick up his apples and redeems his voucher, triggering a transaction on the ledger that consumes the `AppleStamp` state. Three transactions have been performed so far.

4. The `BasketofApples` state is transferred to Peter when the `AppleStamp` state is consumed and Farmer Bob gives Peter his apples.

All of these transactions are initiated by [flows](../../ledger/flows.md).

## Next steps

Follow these tutorials in sequential order to build your CorDapp:

<!---These will all link to the new tutorials when they are added.--->

1. [Initial Setup](basic-cordapp-setup.md)

2. [Write States](basic-cordapp-state.md)

3. [Write Contracts](basic-cordapp-contract.md)

4. [Write Flows](basic-cordapp-flows.md)
