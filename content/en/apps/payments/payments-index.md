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

Corda Payments Technical Preview is an early release of Corda Payments, a solution that allows you to initiate and manage payments from within a Corda network via an external Payment Service Provider (PSP).

This technical preview allows you to create a local environment on which you can generate payment requests from a node, have the request picked up by a Payments Agent CorDapp attached to another node, and passed to the chosen external PSP—Modulr. The Modulr sandbox environment simulates the payment off-ledger, which is tracked and recorded on your Corda network.

Using these documents, you can:

1. Add the Payments SDK dependencies to an existing CorDapp. This gives the CorDapp access to the Payments flows used to generate payment requests and account amendments to be picked up by the network's Payments Agent.
2. Deploy and configure the Payments Agent CorDapp to a local node.
3. Simulate payments on a local network that connects to Modulr's sandbox environment.

## The Payments Agent

Payments on a Corda network are facilitated by the designated Payments Agent. This must be a trusted party on the network, such as the Business Network Operator (BNO). Using the Payments Agent CorDapp, the Payments Agent is able to communicate payment requests from network members to the external PSP via an API. As the payments are processed, the Payments Agent relays updates back to the relevant parties, and updates the ledger accordingly.

In this Technical Preview, you can play the role of the Payments Agent to facilitate payments requested on a local network, via the Modulr sandbox.

If you are considering setting up a payments network, read more about the [Payments Agent flows](payments-agent.md) to see the actions you can perform.

## The Payments SDK

To trigger payments on a Corda network, you must have a payments-enabled CorDapp, which you can create using the Corda Payments SDK. The SDK gives you access to the Corda Payments API, which contains the methods required to trigger payment requests to the Payments Agent, track the progress, and update your vault accordingly.

In this Technical Preview, you can use the sample Payments CorDapp, which is already programmed to send payment requests on your local network.

For example, Bob wants to pay Alice £100. Both parties have CorDapps that have been enabled with the Corda Payments SDK to send and receive payments. The BNO of their network has an operational Payments Agent CorDapp set up with active accounts for both Alice and Bob.

1. Bob triggers a payment request using a payments flow.

2. A payment state is created on the ledger for the Payments Agent to process.

3. The Payments Agent contacts the PSP, Modulr, with a request to pay £100 from Bob's account to Alice's account.

4. The payment request is processed by Modulr via the appropriate payment rail—UK Faster Payments, and is tracked by the Payments Agent via Modulr's API.

5. The payment is complete. The ledger shows, and both Bob and Alice's vault reflect that Bob has paid £100 to Alice.

## Before you start

In order to start trialling payments on Corda, you need to:

1. Set up a sandbox account with Modulr. To run the Payments Agent, you must have a **Partner Account** for your Modulr Sandbox. This involves contacting Modulr by email. You can follow the Modulr instructions to do this here: https://secure-sandbox.modulrfinance.com/sandbox/onboarding.

Once you have registered, Modulr will communicate your API key and secret. The Payments Agent holds these keys. Customers of the Payments Agent (anyone on the network who wants to use Corda Payments) do not require Modulr accounts with API key or secret.

2. Install the Corda Payments Technical Preview.


To see this in action quickly, use the ready-made CorDapps, Payments Agent and network to make payments via Modulr.
