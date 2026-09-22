---
date: '2026-08-21T14:00:00Z'
menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-corda-nodes-confidential-identity-cross-provider-key-rotation
    name: "Confidential identity cross-provider key rotation"
    parent: corda-enterprise-4-15-corda-nodes
tags:
- key rotation
- hsm
- confidential identity
- node
title: Confidential identity cross-provider key rotation
weight: 181
---

# Confidential identity cross-provider key rotation

Confidential identity (CI) cross-provider key rotation lets a node move its **confidential identity keys** from one key provider to another.
For example, between a file-based keystore and a hardware security module (HSM) in either direction, or between two HSMs, without losing the
ability to sign for the states those keys already own. It is available in Corda Enterprise 4.15 and later.

The tool rotates the confidential identity keys a node generates for its transactions. These keys are held wrapped under a master key in a crypto service or HSM (see [Using an HSM with confidential identities]({{< relref "../../node/operating/confidential-identities-hsm.md#wrapped-mode" >}})). To move a node's **legal identity** key instead, use [Cross-provider key rotation]({{< relref "cross-provider-key-rotation.md" >}}).

{{< note >}}

This tool rotates only the anonymous, certificate-less confidential identity keys. It does **not** rotate the older, certificate-based confidential identities created with `SwapIdentitiesFlow` (see [Confidential identities]({{< relref "../../cordapps/api-confidential-identity.md" >}})).

{{< /note >}}

{{< important >}}

**Wrapped certificate-based (CERT) confidential identity keys become permanently unsignable after the provider switch.** This tool does not rotate CERT keys, so once the node switches to the new provider these CERT keys can no longer be signed with, and every unconsumed state still owned by one is permanently stuck. This cannot be recovered by re-running the tool or by rotating again.

Consume or reissue every state owned by a CERT key before you rotate. The tool refuses to run when it finds CERT keys.
Unless you pass `--ignore-cert-keys-check` to proceed anyway, which accepts that any unconsumed states still owned by
those CERT keys will be permanently lost.

{{< /important >}}

{{< warning >}}

Key rotation is a system-critical operation that writes directly to the node database. An unsuccessful rotation can leave the node unable to sign for its existing states. Always rehearse the procedure in a test environment, take verified backups, and have a rollback plan before you rotate keys in production.

{{< /warning >}}

## Which keys it rotates

The tool rotates a node's **wrapped** confidential identity keys. These are the confidential identity private keys stored encrypted under a master (wrapping) key held in a crypto service or HSM, generated when `freshIdentitiesConfiguration` is configured. See [Using an HSM with confidential identities]({{< relref "../../node/operating/confidential-identities-hsm.md#wrapped-mode" >}}).

The tool moves these keys from one provider to another. In every case, the replacement key is generated **wrapped on the new provider**.

The tool supports the following provider migrations:

| From (previous provider) | To (new provider) |
|--------------------------|---|
| File-based keystore      | HSM |
| HSM                      | File-based keystore |
| HSM                      | Another HSM |

The new provider must have `freshIdentitiesConfiguration` enabled, and the replacement key is always generated wrapped on it.

## How it works

Every confidential identity key a node holds may own unconsumed states that the node must still be able to sign for. Moving the key to a new provider therefore creates a problem to solve. The node must remain able to sign for those states even though the key now lives in a different provider, and a well-behaved HSM will not let you export and re-import private key material.

The tool solves this with a **key rotation proof**. For every confidential identity key that needs rotating, the tool does three things:

1. It generates a new wrapped key on the **new** provider.
2. It uses the **old** key to sign the new key's public key. This signature is the proof that the owner of the old key authorised the replacement.
3. It stores the proof in the node database, copies the old key's identity mapping onto the new key so the new key belongs to the same party, and marks the old key as rotated.

From then on, whenever the node is asked to sign with the old confidential identity key, it follows the proof to the new key and signs with the new key on the new provider.
Nothing is moved or deleted. The old key stays in place linked to the new key by the proof. Each further rotation simply extends the proof chain.

Because "already rotated" is defined purely by the presence of a proof, the operation is idempotent and resumable. Re-running the tool skips keys that are already done, and an interrupted run continues where it left off.

## Before you begin

### Compatibility

Nodes running Corda 4.15 interoperate with earlier Corda versions in exactly the same way as Corda 4.14 did. Including interoperability between Corda Open Source and Corda Enterprise. A Corda Open Source node running 4.15 or later can verify transactions that contain key rotation proofs but cannot initiate a rotation.

### Limitations

* Only Corda Enterprise nodes running Corda 4.15 or later can initiate a rotation.
* A rotation cannot be reversed. Moving back to a previous provider requires performing another rotation.
* Each rotation adds a key rotation proof to the chain, which places a small, fixed overhead on affected transactions. See [Transaction size and performance]({{< relref "cross-provider-key-rotation.md#transaction-size-and-performance" >}}).
* The tool rotates confidential identity keys only. It does not rotate the node's legal identity key.

## Prerequisites

Complete every item in this checklist before you rotate any key:

1. Rehearse the complete procedure in a non-production environment that mirrors production, and confirm that the node restarts and can consume existing states afterwards.
2. Take a verified backup of the node database and the entire node directory. Confirm that you can restore it before you continue because it is the only way to roll back a failed rotation.
3. Plan for downtime. The node must be stopped throughout the rotation.
4. Confirm that every node on the network runs Corda 4.15 or later. And that the network minimum platform version is `170` or later. To upgrade, see [Upgrading a node]({{< relref "../../node-upgrade-notes.md" >}}). To raise the minimum platform version, see [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}).
5. Confirm that the new key provider is configured, running, and accessible to the node.
6. Confirm that all deployed CorDapps are compatible with key rotation. See [Adapting your CorDapps]({{< relref "cross-provider-key-rotation.md#adapting-your-cordapps" >}}).
7. Make `corda-tools-ha-utilities.jar` version 4.15 or later available in the node directory. For the tool's full command syntax and options, see the [Node confidential identity cross-provider key rotation tool]({{< relref "../../ha-utilities.md#node-confidential-identity-cross-provider-key-rotation-tool" >}}) reference.
8. When the new provider is an HSM, place the vendor-supplied client-side JAR files in the `drivers` subdirectory of the configured base directory. The HA Utilities JAR does not include them. For more details see [HSM integration]({{< relref "../../operations/deployment/hsm-integration.md" >}}).

## Rotating confidential identity keys

1. Confirm that all [prerequisites](#prerequisites) are met.
2. Stop the node.
3. In the node directory, copy the current configuration file (which points to the old key provider) to `node.conf.previous`.
4. Edit `node.conf` so that it points to the new key provider. The new configuration must have `freshIdentitiesConfiguration` enabled, because replacement keys are always generated wrapped on the new provider.
5. Run the key rotation tool. Both configuration files must point to the same node database:

   ```shell
   java -jar corda-tools-ha-utilities.jar node-confidential-identity-cross-provider-key-rotation
   ```

   To preview the keys that would be rotated without writing any changes, add `--dry-run`.

6. Confirm the tool reported zero failures and exited successfully. The summary reports the total, the number rotated, and the number that failed. If any key failed, the rotation is incomplete, so do not start the node on the new provider. Fix the cause and re-run the tool until it reports zero failures.
7. Start the node and confirm that it can sign for its states.

{{< important >}}

Once a rotation has succeeded and a new key is in use, the change cannot be reversed. Backups can roll back a rotation that has not yet succeeded, but they cannot restore an old key after a successful rotation. If you later need to move back to the original provider, perform a new rotation rather than reinstating the old key.

{{< /important >}}

## Behaviour and options

* **Selection.** The tool rotates every used confidential identity key that has not already been rotated, including keys that no longer own any unconsumed vault state.
* **Certificate keys.** The tool refuses to run when the node has wrapped certificate-based (CERT) confidential identity keys, because it does not rotate them and they would become permanently unsignable after the switch. Pass `--ignore-cert-keys-check` to rotate anyway, accepting that any unconsumed states still owned by those CERT keys will be permanently lost.
* **Batching.** Keys are rotated in batches, one database transaction per batch, controlled by `--batch-size` (default `500`). If a key fails, the tool rolls back that batch and retries it by rotating each key individually, which may cause a temporary slowdown while the batch is reprocessed. Once every key in the batch has been processed, the tool goes back to rotating the keys in batches.
* **Resilience.** A key that fails to rotate does not stop the others. The tool logs each failure, continues with the remaining keys, and prints a final summary of the total, rotated, and failed counts. If any key fails, the tool exits with a non-zero status and reports that the rotation is incomplete. Do not switch the node to the new key provider while any key is still unrotated. Fix the cause and re-run the tool to retry the outstanding keys. Re-running is idempotent, so keys already rotated onto the new provider are skipped.
* **No-op guard.** If the new and previous configurations resolve to the same provider, the tool makes no changes. It decides this by comparing a hash of the key provider configuration, rather than by probing the provider. Because the hash is computed over the configuration’s raw bytes, reformatting or rewriting the previous configuration for the same HSM changes the hash, so the tool treats it as a new provider and performs a full, unnecessary rotation. Change only what is needed to point at the new provider, and otherwise leave the provider configuration unchanged.
* **Dry run.** `--dry-run` reports exactly which keys would be rotated without writing anything.

{{< note >}}

When a key fails to rotate, the whole batch fails and every key in that batch that had already been rotated must be rotated again.
The database changes are rolled back, but the key pairs already created in the new key provider are not, because `generateWrappedKeyPair` is not transactional.
If a single key fails in a batch of N keys, the other potentially N-1 keys may already have had new key pairs generated in the key provider.
Those key pairs become orphaned, because the overall transaction failed and the rotation must be retried. Whether this happens depends on the key provider being used.

{{< /note >}}

For the full command syntax and every option, see the [Node confidential identity cross-provider key rotation tool]({{< relref "../../ha-utilities.md#node-confidential-identity-cross-provider-key-rotation-tool" >}}) reference.

## Recovering from a failed rotation

A rotation has not completed successfully if the node fails to start or cannot sign for its states. If this happens, do not re-run the tool over the partially rotated database. Instead:

1. Stop the node.
2. Restore the node directory and the node database from the verified backups taken in [Prerequisites](#prerequisites).
3. Start the node and confirm that it is healthy before retrying.

## Adapting your CorDapps

Confidential identity keys use the same key rotation proof mechanism as legal identity keys, so the same CorDapp considerations apply. The node follows proofs transparently for most applications, but CorDapps that store and later compare party or key details, or that perform their own transaction validation, may need changes. Because confidential identities are typically short-lived, the proof overhead usually disappears once the states they own are consumed.

For the full guidance on resolving identities from a single source, signing and validating correctly, including proofs when parties must stay identical, and transaction size and performance, see [Adapting your CorDapps]({{< relref "cross-provider-key-rotation.md#adapting-your-cordapps" >}}) on the legal identity page.

## References

* [Node confidential identity cross-provider key rotation tool]({{< relref "../../ha-utilities.md#node-confidential-identity-cross-provider-key-rotation-tool" >}}) in the HA Utilities reference, for the full command syntax and options.
* [Cross-provider key rotation]({{< relref "cross-provider-key-rotation.md" >}}), for rotating a node's or notary's legal identity key.
