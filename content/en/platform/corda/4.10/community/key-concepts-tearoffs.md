---
aliases:
- /head/key-concepts-tearoffs.html
- /HEAD/key-concepts-tearoffs.html
- /key-concepts-tearoffs.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-key-concepts-tearoffs
    parent: corda-community-4-9-key-concepts
    weight: 1130
tags:
- concepts
- tearoffs
title: Transaction tear-offs
---


# Transaction tear-offs

## Summary

* [Transaction](key-concepts-transactions.md) tear-offs hide components of the transaction for privacy purposes.
* Use them to make sure [oracles](key-concepts-oracles.md) and non-validating [notaries](key-concepts-notaries.md) can only see transaction components relevant to them.

## Use cases

You may want to limit some entities interacting with a transaction to specific parts of it to preserve privacy. For example:
* An [oracle](key-concepts-oracles.md) only needs to see the commands specific to it.
* A [non-validating notary](key-concepts-notaries.md) only needs to see a transaction’s [input states](key-concepts-states.md).

You can achieve this using **Merkle trees**. These let the node proposing the transaction “tear off” any parts of the transaction that the oracle or notary doesn’t need to see before presenting it to them for signing. Merkel trees are a cryptographic scheme that provides proofs of inclusion and data integrity. They guarantee that the parts of the transaction you tore off cannot later be changed without invalidating the oracle’s digital signature. Merkle trees are widely used in peer-to-peer networks, blockchain systems, and Git.



### Merkle trees on Corda

Merkle trees split transactions into "leaves". Each leaf contains
either an input, an output, a command, or an attachment. The final nested tree structure also contains the
other fields of the transaction, such as the time window, the notary, and the required signers. The only component type that requires two trees instead of one is the command, which is split into
command data and required signers for visibility purposes.
{{< figure alt="merkleTreeFull" width=80% zoom="/en/images/merkleTreeFull.png" >}}

Corda uses one nested Merkle tree per component type. A component sub-tree
is generated for each component type (for example, inputs, outputs, or attachments). The roots of these sub-trees
form the leaves of the top Merkle tree, and the root of the tree represents the transaction ID.

Corda also deterministically generates an independent **nonce** for each component. This is a unique number added to the [hash](https://www.investopedia.com/terms/h/hash.asp). Then, it uses the nonces and their corresponding components to calculate the component hash, which is the actual Merkle tree leaf. Nonces protect against brute force attacks that otherwise would reveal the content of hashed values that can't generate much randomness, such as a single-word text attachment.

After computing the leaves, each Merkle tree is built by hashing the concatenation of nodes’ hashes
together. You can see this in the diagram, where `H` denotes sha256 function, “+” - concatenation.

The transaction has three input states, two output states, two commands, one attachment, a notary, and a time window.
If a tree is not a full binary tree, its leaves are padded to the nearest
power of 2 with zero hash (since finding a pre-image of sha256(x) == 0 is a hard computational task). The hash of the root is the identifier of the transaction. This is used for signing and
verification of data integrity. Any change in a transaction on a leaf level changes its identifier.

### Hiding data

To hide data and provide proof that it formed a part of a transaction, you can construct partial Merkle trees,
or **Merkle branches**. A Merkle branch is a set of hashes, that given the leaves’ data, is used to calculate the
root’s hash. Then, you can compare that hash with the hash of a whole transaction. If they match, it means that the data
obtained belongs to that particular transaction.

In this example, assume that only the first command should be visible to the oracle. You must provide guarantees that all
the commands the oracle needs to sign are visible to the oracle entity, but no other data. The transaction would be represented in the Merkle tree structure like this:

{{< figure alt="SubMerkleTree Oracle" width=80% zoom="/en/images/SubMerkleTree_Oracle.png" >}}

The blue nodes and `H(c2)` are provided to the oracle service, while the black ones are omitted. The oracle needs `H(c2)` so it can compute `H(commandData)` without being to able to see the second command. At the same time, this
ensures that `CommandData1` is part of the transaction. All signers are visible as
proof that no related command has been maliciously filtered out. Additionally, hashes of
sub-trees (violet nodes) are provided in the current Corda protocol. These are required for special cases, such as if the oracle needs to know if a component group is empty or not.

You can use this data to calculate the root of the top tree and compare it with original
transaction identifier. Then, you have proof that the command and time window belong to the transaction.

To send the same transaction to a non-validating notary, hide all components
apart from input states, time window, and the notary information. This data is enough for the notary to know which
input states to check for double-spending, if the time-window is valid, and if the transaction is being notarized by the correct notary.

{{< figure alt="SubMerkleTree Notary" width=80% zoom="/en/images/SubMerkleTree_Notary.png" >}}
