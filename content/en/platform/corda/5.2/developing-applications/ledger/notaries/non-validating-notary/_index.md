---
description: Learn about the R3 non-validating notary protocol.
title: "Non-Validating Notary Protocol"
date: 2023-06-08
menu:
  corda52:
    identifier: corda52-fundamentals-ledger-notaries
    parent: corda52-develop-notaries
    weight: 2000
---

# Non-Validating Notary Protocol

To support the UTXO ledger model, R3 provides a non-validating [notary]({{< relref "../../notaries/_index.md" >}}) protocol. This protocol implements the following when Corda receives a new transaction from a participant on the network:

* Checks that all inputs are in the list of unconsumed states.
* Remove the inputs from the list of unconsumed states.
* Add any outputs as new valid states to the list of unconsumed states.
* Signs the transaction and sends the signature back to the requestor of the notarization.

{{<
  figure
	 src="non-validating-notary.jpg"
   width=70%
	 figcaption="The CPKs, CPBs, and CPIs involved in getting a functioning network that can run a non-validating notary (and by extension, UTXO ledger functionality)"
	 alt="Corda 5 non-validating notary"
>}}

## Validity

To establish that a state on the ledger is valid, a virtual node must verify the transaction that has the state as output.
The first step is to verify that all states which appear as inputs, if any, to that transaction are valid by verifying those transactions first.
Once the inputs are valid, Corda can continue verifying the new states. This includes checking the signatures, including the notary signature, and then moving on to running the smart contracts which check that the transaction represents a valid transformation of inputs and outputs on the ledger.

## Backchain

This validity requirement means that in order to verify a transaction, each virtual node must fetch the whole chain of transactions back to issuance. This is called the backchain of a transaction.
For some use cases (for example, to trace the origin of a tokenized asset), this can actually be quite useful.
For other cases, where the relevant property is ownership rather than provenance, it is less desirable, particularly if transactions can have many inputs and outputs or states are fungible tokens. In these cases, the backchain can turn into a tangled web of transactions that needs to be downloaded. This leads to the following:

* Decentralized verification. Every virtual node has the required data to run the full set of verifications all the way to the origins, without having to rely on any remote or centralized verification. The role of the notary is limited to ensuring no state is consumed more than once.
* Privacy implications - Every virtual node must fetch and process a large number of transactions that it might not have been involved in, and can see the full history of every token it sees.
* Performance implications - The backchain continues to grow:
  * When a virtual node receives a state or token for which it has not seen the history before, it must download the complete backchain. This must occur before it can accept/sign a transaction and slows down the main functionality of the network. This would be definitely the case for any new joiner to a network.
  * Most virtual nodes will eventually have to store a large part of the global ledger in their database, which could be gigabytes of data that is only required to verify new transactions.
  * Archiving the ledger is near impossible, as old transactions might be required to verify the backchain of newly created transactions.

For these cases, R3 provides an alternative notary protocol. For more information, see [Contract-Verifying Notary Protocol](../../notaries/contract-verifying-notary.md).

## Privacy

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
