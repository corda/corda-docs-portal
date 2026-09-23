---
date: '2026-09-23T14:00:00Z'
menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-corda-nodes-key-rotation
    name: "Key rotation"
    parent: corda-enterprise-4-15-corda-nodes
tags:
- key rotation
- hsm
- node
- notary
title: Key rotation
weight: 179
---

# Key rotation

The key rotation tools list below allow you to rotate the keys that a node or notary uses to sign. Key rotation is the
process of replacing a key with a new one, while preserving the node's ability to sign for its existing states and transactions.

Corda Enterprise supports three key rotation operations:

* [Same-provider key rotation]({{< relref "same-provider-key-rotation/same-provider-key-rotation.md" >}}) reissues a node's or notary's legal identity key within the **same** key provider. It generates a fresh key and re-registers the node's certificate with the CENM Identity Manager service while keeping the old key reachable so the node can still sign for its existing states. It does not change the key provider. It is available in Corda Enterprise 4.7 and later.
* [Cross-provider key rotation]({{< relref "cross-provider-key-rotation/cross-provider-key-rotation.md" >}}) reissues a node's or notary's legal identity key to a **different** key provider, such as from one HSM to another. It follows the same core process as same-provider key rotation, and it also records a key rotation proof that links the old key to the new one, so the crypto material never has to leave the old provider. After the rotation, the node no longer signs with the old key. It signs for its existing states with the new key and the proof instead. It is available in Corda Enterprise 4.15 and later.
* [Confidential identity cross-provider key rotation]({{< relref "cross-provider-key-rotation/confidential-identity-cross-provider-key-rotation.md" >}}) moves a node's wrapped **confidential identity** keys to a different key provider. These are the keys a node generates for its transactions, not its legal identity key. It uses the same key rotation proof mechanism as the cross-provider key rotation. It is available in Corda Enterprise 4.15 and later.

{{< warning >}}

Key rotation is a system-critical operation. An unsuccessful rotation can leave the affected node unable to access its existing states. Always rehearse the procedure in a test environment, take verified backups, and have a rollback plan before you rotate a key in production.

{{< /warning >}}
