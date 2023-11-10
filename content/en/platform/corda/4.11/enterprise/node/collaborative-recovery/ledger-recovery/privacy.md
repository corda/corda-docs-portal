---
date: '2023-11-08'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-ledger-recovery
tags:
- ledger recovery privacy
title: Privacy
weight: 300
---

# Privacy

The ledger recovery `DistributionList` is now encrypted using AES keys stored in the node's database.
Upon startup a node will create 10 random AES keys and store them in the `node_aes_encryption_keys` table, if there are no keys already present.
The keys themselves are obfuscated, by wrapping them with a deterministic AES key derived from the key's ID and the node's X.500 name.
This is done purely to reduce the impact of an accidental data dump of the keys, and is not meant to be secure.

The `senderRecordedTimestamp` has been moved to a separate header object, and is treated as the authenticated additional
data in the AES-GCM encryption. This allows it to be public, which is necessary as the receiver node needs to be read it
without having access to the encryption key, but also gives a guarantee to the original sender during recovery that it has not been tampered with.
