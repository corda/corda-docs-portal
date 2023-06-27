---
title: "Notaries"
date: 2023-06-08
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-fundamentals-ledger-notaries
    parent: corda5-fundamentals-ledger
    weight: 6000
section_menu: corda5
---

# Notaries

The notary is Corda’s uniqueness consensus service. The notary’s primary role is to prevent double-spends by ensuring each transaction contains only unique unconsumed input states. It also acts as the time-stamping authority. Every transaction includes a time window and it can only be notarized during that window.   
A notary service is formed by one or more notary workers that together form a notary cluster. The cluster’s signature is obtained once it verifies that a proposed transaction’s input states have not already been consumed by a prior transaction. Upon determining this, the notary cluster will either:

* Sign the transaction in cases where all input states are found to be unique.
* Reject the transaction and flag that a double-spend attempt has occurred in cases where any of the input states are identical to those already encountered in a previous transaction.

Every state has an appointed notary cluster, so the cluster will only notarize a transaction if it is the appointed notary cluster of all the transaction’s input states. A network can have several notary clusters, all running different consensus algorithms.

A notary service runs a notary protocol, which dictates the consensus algorithm and additional validation performed. In Corda 5.0, only the non-validating notary protocol is supported, which performs minimal additional checks beyond double-spend and time-window validation. 

## Data Visibility

The non-validating notary protocol maintains a degree of privacy by only revealing the information about a transaction that is strictly necessary to perform validation. Below is a summary of which specific transaction components are revealed:


| Transaction components            | Non-validating protocol   |
| --------------------------------- | ------------------------- |
| Input states                      | References only [1]       |
| Output states                     | Number of states only [2] |
| Commands (with signer identities) | Hidden                    |
| Attachments                       | Hidden                    |
| Time window                       | Fully visible             |
| Notary identity                   | Fully visible             |
| Signatures                        | Hidden                    |
| Transaction metadata              | Fully visible             |

The protocol also records the calling party’s identity in the form of its X.500 Distinguished Name.

[1] A state reference is composed of the issuing transaction’s ID and the state’s position in the outputs. It does not reveal what kind of state it is or its contents.

[2] Output states are not revealed, but the total number of output states are communicated to allow the protocol to track unspent states.

## Pluggable Notaries

The notary is implemented as a special app on the application network, consisting of a client plug-in included with an application workflow app, and a server component that needs to be installed as a notary member with its own virtual node.

The client plug-in and the server component define the protocol used by this notary.

## Multiple Notaries

Each Corda network can have multiple notary clusters. This has several benefits:

* **Choice of protocol:** Once multiple notary protocols are implemented, nodes can choose the preferred notary cluster on a per-transaction basis.
* **Load balancing:** Spreading the transaction load over multiple notary clusters allows higher transaction throughput for the platform overall.
* **Low latency:** Latency can be minimized by choosing a notary cluster physically closer to the transacting parties.

## Changing Notaries

A notary cluster will only sign a transaction if it is the appointed notary cluster of all the transaction’s input states. However, there are cases in which it may be necessary to change a state’s appointed notary cluster. These include:

* When a single transaction needs to consume several states that have different appointed notary clusters.
* When a node would prefer to use a different notary cluster for a given transaction due to privacy or efficiency concerns.

Before these transactions can be created, the states must first all be re-pointed to the same notary cluster. This is achieved using a special notary-change transaction. This has not been implemented for Corda 5 Beta yet.