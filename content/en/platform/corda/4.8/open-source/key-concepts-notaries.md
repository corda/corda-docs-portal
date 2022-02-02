---
aliases:
- /head/key-concepts-notaries.html
- /HEAD/key-concepts-notaries.html
- /key-concepts-notaries.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-notaries
    parent: corda-os-4-8-key-concepts
    weight: 1080
tags:
- concepts
- notaries
title: Notaries
---


# Notaries

## Summary

* *Notary clusters prevent “double-spends”*
* *Notary clusters are also time-stamping authorities. If a transaction includes a time-window, it can only be notarized during that window*
* *Notary clusters may optionally also validate transactions, in which case they are called “validating” notaries, as opposed to “non-validating”*
* *A network can have several notary clusters*

## Video

{{% vimeo 214138458 %}}

## Overview

The notary cluster is Corda's uniqueness consensus service. The notary's role is to ensure a
transaction contains only unique input states.

After it examines a proposed transaction's input states, a notary either:

* Signs the transaction, if all the input states are unique.
* Rejects the transaction and flags it as a  double-spend attempt if the input states match any from a previous transaction.

Every state has an appointed notary cluster. The cluster only notarizes transactions if it is the appointed notary cluster for all the transaction’s input states.

## Validation

Notary clusters can provide validity consensus by validating each transaction
before committing it. There are two types of notary deployment:

* The non-validating notary, where the transaction **is not** checked for validity.
* The validating notary, where the transaction **is** checked for validity.

### Data visibility

Specific transaction components must be revealed to each type of notary:

{{< table >}}

|Transaction components|Validating|Non-validating|
|-----------------------------------|---------------|-----------------------|
|Input states|Fully visible|References only \[1\]|
|Output states|Fully visible|Hidden|
|Commands (with signer identities)|Fully visible|Hidden|
|Attachments|Fully visible|Hidden|
|Time window|Fully visible|Fully visible|
|Notary identity|Fully visible|Fully visible|
|Signatures|Fully visible|Hidden|
|Network parameters|Fully visible|Fully visible|

{{< /table >}}

Both types of notaries record the calling party’s identity: the public key and the X.500 Distinguished Name.

<a name="key-concepts-notaries-id1"></a>

\[1\]
A state reference is composed of the issuing transaction’s ID and the state’s position in the outputs. It does not
reveal what kind of state it is or its contents.

## Multiple notaries

Each Corda network can have multiple notary clusters. This has several benefits:

* **Privacy** -  Nodes can choose the most suitable notary cluster for a specific transaction.
* **Load balancing** - spreading the transaction load over multiple notary clusters allows higher transaction
throughput for the platform overall.
* **Low latency** - Nodes can speed up transactions by choosing the closest notary cluster to the transacting parties.

### Changing notaries

Notaries only sign transactions if they are the appointed notary for all the
transaction’s input states. It's possible to change a state’s appointed notary.
You might need to change a state's appointed notary if:

* A single transaction needs to consume several states that have different appointed notary clusters.
* A node would prefer to use a different notary cluster for a given transaction for increased privacy or reduced latency.

Before you create these transactions, you must re-point all the states to the same notary cluster. You can do this 
using a special `notary-change` transaction that takes:

* A single input state
* An output state identical to the input state, except that the appointed notary cluster has been changed

The input state’s appointed notary cluster signs the transaction if it does not constitute a double-spend. The state then has all the properties of the old state, but with a different appointed notary
cluster.
