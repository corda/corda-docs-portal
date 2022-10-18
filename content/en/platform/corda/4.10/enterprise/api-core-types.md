---
date: '2021-07-07T12:00:00Z'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-9-cordapps
tags:
- api
- core
- types
title: 'Core types in the Corda API'
weight: 190
---

# API: Core types

Corda provides several core classes as part of its API.

## Glossary

**Hash**

A mathematical function that takes a variable-length input string and converts it into a fixed-length binary sequence.

**Public key cryprography**

A system that uses a pair of keys: a public key and private key. Anyone can encrypt a message using the receiver’s public key, but the message can only be decrypted with the receiver’s private key.

**Crytographic primitive**

A low-level algorithm used to build cryptographic protocols for a security system. They are building blocks designed to do one specific task reliably.


**Tree**

Trees organize values (in the form of nodes) into nonlinear, hierarchical data structures. The tree originates from a single root node, then branches into levels of parent and child nodes. The last node on a branch is called the *leaf*.

## SecureHash

Use the `SecureHash` class to uniquely identify objects, such as transactions and attachments, by their hash.
Implement the `NamedByHash` interface for any object that needs to be identified by its hash:

{{< tabs name="tabs-1" >}}
{{< /tabs >}}

`SecureHash` is a sealed class that only defines a single subclass, `SecureHash.SHA256`. You can use utility methods
to create and parse `SecureHash.SHA256` objects.



## CompositeKey

Corda supports complex signing scenarios for the authorization of a state object transition. For example,
if *either* Alice **and** Bob *or* Charlie need to sign a transaction.

You could facilitate this policy with a `CompositeKey`. A `CompositeKey` composes cryptographic public keys into a
tree. The tree stores the public key primitives in its leaves and
the composition logic in its intermediary nodes. Every intermediary node specifies a threshold of how many child
signatures it requires.

An illustration of an *“either Alice and Bob, or Charlie”* composite key:

{{< figure alt="composite key" width=80% zoom="./resources/composite-key.png" >}}
To allow further flexibility, each child node can have an associated custom *weight* (the default is 1). The *threshold*
then specifies the minimum total weight of all children required. Our previous example can also be expressed as:

{{< figure alt="composite key 2" width=80% zoom="./resources/composite-key-2.png" >}}
Signature verification is performed in two stages:



* Given a list of signatures, each signature is verified against the expected content.
* The public keys corresponding to the signatures are matched against the leaves of the relevant composite key tree.
The total combined weight of all children is calculated for every intermediary node. If all thresholds are satisfied,
the composite key requirement is met.




