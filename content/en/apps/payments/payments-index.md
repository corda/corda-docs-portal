---
date: '2020-01-08T09:59:25Z'
section_menu: apps
menu:
  apps:
    identifier: payments
    name: Corda Payments
    weight: 1000
title: Corda Payments Technical Preview
weight: 100
---

Corda Payments Technical Preview allows you make payments between members of a Corda network in a local environment, via an external Payment Service Provider (PSP). Communication with the PSP is managed by the Payments Agent-a trusted member of the network, such as the Business Network Operator (BNO).

Using Modulr as the PSP, you can demonstrate and experiment with making payments between accounts using the Modulr sandbox. As payments are processed in the Modulr sandbox, they are synchronised on the ledger in your local network. All funds paid between these sample accounts are fictional - no real money is required.

Using these documents, you can:

1. Add the Payments SDK dependencies to an existing CorDapp. This gives the CorDapp access to the Payments API which allows payment requests and account amendments to be sent to the network's Payments Agent.
2. Deploy and configure the Payments Agent CorDapp to a local node.
3. Simulate payments on a local network that connects to Modulr's sandbox environment.

## The Payments Agent

Payments on a Corda network are facilitated by the designated Payments Agent-this is a trusted party on the network such as the Business Network Operator (BNO). Using the Payments Agent CorDapp, the Payments Agent is able to communicate payments requests from network members to the external PSP via an API. As the payments are processed, the Payments Agent relays updates back to the relevant parties, and updates the ledger accordingly.

In this Technical Preview, you can use the Payments Agent Cordapp and node to facilitate payments requested on a local network, via the Modulr sandbox.

## The Payments SDK

To trigger payments on a Corda network, you must have a payments-enabled CorDapp, which you can create using the Corda Payments SDK. The SDK gives you access to the Corda Payments API, which contains the methods required to trigger payment requests to the Payments Agent, track the progress, and update your vault accordingly.

In this Technical Preview, you can use the sample Payments CorDapp, which is already programmed to send payment requests on your local network.

For example, Bob wants to pay Alice $100. Both parties have CorDapps that have been enabled with the Corda Payments SDK to send and receive payments. The BNO of their network has an operational Payments Agent CorDapp set up with active accounts for both Alice and Bob.

1. Bob triggers a payment request using a payments flow.

2. The request is sent to the network's Payments Agent (the BNO).

3. The Payments Agent contacts the PSP, Modulr with a request to pay $100 from Bob's account to Alice's account.

4. The payment request is processed by Modulr and is tracked by the Payment Agent via Modulr's API.

5. The payment is complete. The ledger shows, and both Bob and Alice's vault reflect that Bob has paid $100 to Alice.

## Before you start

In order to start trialling payments on Corda, you need to:

1. Set up a sandbox account with Modulr.
2. Install the Corda Payments Technical Preview.

## Getting the most from the Corda Payments Technical Preview

This preview demonstrates how payments can be initiated by members of a Corda network, leading to money being paid outside of Corda by a traditional PSP, while the payment is tracked and recorded on the Corda ledger. This retains the integrity of the Corda network, but empowers network members.

To see this in action quickly, use the ready-made CorDapps, Payments Agent and network to make payments via Modulr.

To see how easy it can be to enable payments on existing CorDapps, get to grips with the Payments SDK. Once your modifciations are complete, you can use the local network and Payments Agent to trial it.
