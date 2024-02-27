---
description: "Learn the fundamentals of the Corda 5 notary, Corda’s uniqueness consensus service."
title: "Notaries"
date: 2023-06-08
menu:
  corda52:
    identifier: corda52-fundamentals-ledger-notaries
    parent: corda52-fundamentals-ledger
    weight: 6000
---

# Notaries

The notary is Corda’s uniqueness consensus service. The notary’s primary role is to prevent double-spends by ensuring each transaction contains only unique unconsumed input {{< tooltip >}}states{{< /tooltip >}}. It also acts as the time-stamping authority. Every transaction includes a time window and it can only be notarized during that window.
A notary service is formed by one or more notary workers that together form a notary cluster. The cluster’s signature is obtained once it verifies that a proposed transaction’s input states have not already been consumed by a prior transaction. Upon determining this, the notary cluster will either:

* Sign the transaction in cases where all input states are found to be unique.
* Reject the transaction and flag that a double-spend attempt has occurred in cases where any of the input states are identical to those already encountered in a previous transaction.

Every state has an appointed notary cluster, so the cluster only notarizes a transaction if it is the appointed notary cluster of all of the transaction’s input states. A network can have several notary clusters, all running different consensus algorithms. Backchain resolution verifies that all transactions through the backchain have been notarized by a notary allowed on the network at the time of that transaction’s notarization. This verification is based on the network group parameters, which Corda also distributes with the backchain.

## Notary Protocols

A notary service runs a notary protocol, which dictates the consensus algorithm and additional validation performed. R3 provide the following protocols:

* [Non-validating Notary Protocol](#non-validating-notary-protocol)
* [Contract-Verifying Protocol](#contract-verifying-notary-protocol)

For more information about bundling these in your CPI, see [Notary CorDapps]({{< relref "../../notaries/_index.md" >}})

### Non-Validating Notary Protocol

When Corda receives a new transaction from a participant on the network, it performs the following:

* Checks that all inputs are in the list of unconsumed states.
* Remove the inputs from the list of unconsumed states.
* Add any outputs as new valid states to the list of unconsumed states.
* Signs the transaction and sends the signature back to the requestor of the notarization.

To establish that a state on the ledger is valid, a virtual node must verify the transaction that has the state as output.
The first step is to verify that all states which appear as inputs, if any, to that transaction are are valid by verifying those transactions first.
Once the inputs are valid, Corda can continue verifying the new states, which includes checking the signatures, including the notary signature, and then moving on to running the smart contracts which check that the transaction represents a valid transformation of inputs and outputs on the ledger.

This validity requirement means that in order to verify a transaction, each virtual node must fetch the whole chain of transactions back to issuance. This is called the backchain of a transaction.
For some use cases, for example to trace the origin of a tokenized asset, this can actually be quite useful.
For other cases, where the relevant property is ownership rather than provenance, it is less desirable.
Particularly if transactions can have many inputs and ouputs or states are fungible tokens. In these cases, the backchain can turn into a tangled web of transactions that needs to be downloaded. This leads to the following:

* Decentralized verification. Every virtual node has the required data to run the full set of verifications all the way to the origins, without having to rely on any remote or centralized verification. The role of the notary is limited to ensuring no state is consumed more than once.
* Privacy implications. Every virtual node must fetch and process a large number of transactions that it might not have been involved in, and can see the full history of every token it sees.
* Performance implications. The backchain continues to grow:
  * When a virtual node receives a state or token for which it has not seen the history before, it must download the complete backchain. This must occur before it can accept/sign a transaction and slows down the main functionality of the network. This would be definitely the case for any new joiner to a network.
  * Most virtual nodes will eventually have to store a large part of the global ledger in their database which could be gigabytes of data that is only required to verify new transactions.
  * Archiving the ledger is near impossible, as old transaction might be required to verify the backchain of newly created transactions.

The non-validating notary protocol maintains a degree of privacy by only revealing the information about a transaction that is strictly necessary to perform validation. Below is a summary of which specific transaction components are revealed:

| Transaction Components            | Non-validating Protocol   |
| --------------------------------- | ------------------------- |
| Input states                      | References only [1]       |
| Output states                     | Number of states only [2] |
| Commands (with signer identities) | Hidden                    |
| Time window                       | Fully visible             |
| Notary identity                   | Fully visible             |
| Signatures                        | Hidden                    |
| Transaction metadata              | Fully visible             |

The protocol also records the calling party’s identity in the form of its {{< tooltip >}}X.500{{< /tooltip >}} Distinguished Name.

[1] A state reference is composed of the issuing transaction’s ID and the state’s position in the outputs. It does not reveal what kind of state it is or its contents.
[2] Output states are not revealed, but the total number of output states are communicated to allow the protocol to track unspent states.

### Contract-Verifying Notary Protocol

As outlined in the [Non-Validating Notary Protocol](#non-validating-notary-protocol) section, a backchain verification based UTXO ledger is not suitable for a large scale token network that also needs very high performance, such as a digital currency.
The contract-verifying notary protocol provides an alternative approach to verifying that inputs to a transaction are trustworthy.





## Multiple Notaries

Each Corda network can have multiple notary clusters. This has several benefits:

* **Choice of protocol:** Once multiple notary protocols are implemented, nodes can choose the preferred notary cluster on a per-transaction basis.
* **Load balancing:** Spreading the transaction load over multiple notary clusters allows higher transaction throughput for the platform overall.
* **Low latency:** Latency can be minimized by choosing a notary cluster physically closer to the transacting parties.

## Changing Notaries

A notary cluster will only sign a transaction if it is the appointed notary cluster of all the transaction’s input states. However, there are cases in which it may be necessary to change a state’s appointed notary cluster. These include:

* When a single transaction needs to consume several states that have different appointed notary clusters.
* When a node would prefer to use a different notary cluster for a given transaction due to privacy or efficiency concerns.

Before these transactions can be created, the states must first all be re-pointed to the same notary cluster. This is achieved using a special notary-change transaction. This has not been implemented for this version of Corda.
