---
date: '2023-11-08'
menu:
  corda-enterprise-4-14:
    parent: corda-enterprise-4-14-corda-ledger-recovery
tags:
- ledger recovery privacy
title: Privacy
weight: 300
---

# Privacy

The ledger recovery `DistributionList` is encrypted using AES keys stored in the node's database.
Upon startup, a node creates ten random AES keys and stores them in the `node_aes_encryption_keys` table, if there are no keys already present.
The keys themselves are obfuscated, by wrapping them with a deterministic AES key derived from the key's ID and the node's X.500 name.
{{< note >}}
This obfuscation only reduces the impact of an accidental data dump of the keys, and is not meant to be secure.
{{< /note >}}

`senderRecordedTimestamp` is in a separate header object, and is treated as the authenticated additional
data in the AES-GCM encryption. This allows it to be public, which is necessary to allow the receiver node to read it
without having access to the encryption key. It also gives a guarantee to the original sender during recovery that it has not been tampered with.
