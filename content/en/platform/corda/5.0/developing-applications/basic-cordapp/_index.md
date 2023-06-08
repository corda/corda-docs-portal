---
date: '2023-05-03'
title: "Building Your First CorDapp"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-first-cordapp
    parent: corda5-develop
    weight: 6000
section_menu: corda5
---

# Building Your First CorDapp

Follow this learning path to build your first CorDapp with a step-by-step guide. This set of tutorials teaches you how to implement the functionality and features you need to get any CorDapp up and running.

## Before You Start

Before you start building your first CorDapp:
- Read about [Corda key concepts]({{< relref "../../key-concepts/_index.md" >}}).
- Install the required [prerequisites]({{< relref "../tooling/_index.md" >}}).
- Read the CorDapp Standard Development Environment (CSDE) [installation instructions]({{< relref "../getting-started/cordapp-standard-development-environment/_index.md" >}}).

## The Story

This example showcases a delivery versus payment (DvP) scenario. You are building a CorDapp for an apple orchard that wants to offer a way for customers to purchase a voucher that they can later redeem for a bushel of apples.

There are two parties involved in this transaction:

- The owner of the orchard - Farmer Bob.
- A customer named Dave.

Your CorDapp must follow this process:

1. Farmer Bob creates and issues a voucher to Dave for the apples he wishes to buy.
2. Farmer Bob prepares the amount of apples Dave requested.
3. Dave goes to the orchard to pick up his apples and redeems his voucher.
4. The voucher is marked as spent and Farmer Bob gives Dave his apples.

An important feature of this CorDapp is that the voucher cannot be used more than once. It must be considered invalid after it is redeemed.

## Corda Implementation

1. Farmer Bob issues a voucher to Dave via a ledger transaction. In your CorDapp this voucher is called `AppleStamp` and is a [state]({{< relref "../components/ledger/states.md" >}}) on the [ledger]({{< relref "../components/ledger/_index.md" >}}). One transaction has been performed so far.
2. When Farmer Bob prepares the apples Dave requested, he self-issues a bushel of apples via a self-issue transaction. This is another state on the ledger - `BasketofApples`. Two transactions have been performed so far.
3. Next, Dave goes to the orchard to pick up his apples and redeems his voucher, triggering a transaction on the ledger that consumes the `AppleStamp` state. Three transactions have been performed so far.
4. The `BasketofApples` state is transferred to Dave when the `AppleStamp` state is consumed and Farmer Bob gives Dave his apples.

All of these transactions are initiated by [flows]({{< relref "../components/ledger/flows.md" >}}).

## Next Steps

Follow these tutorials in sequential order to build your CorDapp:

1. [Initial Setup]({{< relref "./setup.md">}})
2. [Write States]({{< relref "./state.md">}})
3. [Write Contracts]({{< relref "./contract.md">}})
4. [Write Flows]({{< relref "./flows.md">}})
5. [Test Your CorDapp]({{< relref "./testing.md">}})
