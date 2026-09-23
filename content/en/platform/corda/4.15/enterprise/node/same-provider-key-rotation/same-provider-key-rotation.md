---
date: '2026-09-09T14:00:00Z'
menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-corda-nodes-same-provider-key-rotation
    name: "Same-provider key rotation"
    parent: corda-enterprise-4-15-corda-nodes
tags:
- key rotation
- hsm
- node
- notary
title: Same-provider key rotation
weight: 179
---

# Same-provider key rotation

Same-provider key rotation reissues a node's or notary's legal identity keys and certificates, using a new key held in the **same** key provider. The provider can be one hardware security module (HSM) or one file-based keystore. The node keeps access to the states and transactions it already holds. It re-registers the node with a new certificate in the Network Map in {{< cenmlatestrelref "cenm/_index.md" "CENM" >}}. It is available in Corda Enterprise 4.7 and later.

To move a key to a **different** key provider, such as from one HSM to another, use [Cross-provider key rotation]({{< relref "../cross-provider-key-rotation/cross-provider-key-rotation.md" >}}) instead.

{{< warning >}}

Key rotation is a system-critical operation. An unsuccessful rotation can leave the affected node unable to access its existing states. Always rehearse the procedure in a test environment, take verified backups, and have a rollback plan before you rotate a key in production.

{{< /warning >}}

{{< warning >}}

You must not change the node's `myLegalName` during certificate rotation. Also, the old key must remain reachable if unconsumed states signed with it exist in the vault. If the old key is not reachable, the node will not be able to consume those states, and they will remain locked in the vault.

{{< /warning >}}

## How it works

A node's legal identity key is the key it uses to sign transactions and prove who it is on the network. Every state the node has ever signed is bound to the key that signed it. Reissuing that key therefore has to preserve the node's ability to keep signing for the states the old key already owns.

Same-provider key rotation always generates a **fresh key pair**. Reissuing a certificate with the original key is a separate, less secure approach that this feature does not support. The process is similar to the initial node registration. The [Node certificate rotation tool]({{< relref "../../ha-utilities.md#node-certificate-rotation-tool" >}}) generates a new node CA key and sends a Certificate Signing Request to the CENM Identity Manager service. It then generates new node identity and TLS certificates around the renewed node CA certificate. From that point on:

* The new key and its certificates are stored under **new aliases** in the keystore or HSM, using the same crypto service configuration as before. Most HSMs do not allow the alias of an existing key to change, so the replacement key is always stored under a new alias.
* The old identity key stays in the keystore so the node can still sign for the states that key already owns. You keep it available by listing its alias in `previousIdentityKeyAliases`.
* The node keeps the same `myLegalName`. When the node starts with its new certificates, it publishes a new `NodeInfo`. The network map replaces the old `NodeInfo` with the new one by X.500 name. The old `NodeInfo` is removed from the network map automatically.

### How this differs from cross-provider key rotation

[Cross-provider key rotation]({{< relref "../cross-provider-key-rotation/cross-provider-key-rotation.md" >}}) moves
a key to a different key provider. It records a key rotation proof that links the old key to the new one, so the
crypto material never has to leave the old provider. Same-provider key rotation is a different operation.
It does not produce a key rotation proof, and it does not support changing the key provider. The old and new node CA and
node identity keys must be reachable through the same crypto service configuration.

## Before you begin

### Compatibility

New node certificates are reissued with the same X.500 name in the subject. The node keeps signing for its existing states with the old key, so the ledger is not altered by a rotation.

Confidential identities generated without certificates, such as those used by the Token SDK, are compatible with same-provider
key rotation. Old-style [confidential identities with certificates]({{< relref "../../cordapps/api-confidential-identity.md" >}}) are
not supported by this tool.

### Limitations

* The key provider cannot be changed.

## Prerequisites

Same-provider key rotation is a system-critical operation. An unsuccessful rotation can leave the affected node or notary unable to access its existing states. Complete every item in this checklist before you rotate any key.

1. Rehearse the complete procedure in a non-production environment that mirrors production, and confirm that the node or notary restarts and can access its states afterwards.
2. Take verified backups of the node directory, the node database, the keystores, and any HSM keys. For a notary rotation, also back up the notary database. Confirm that you can restore these backups before you continue.
3. Plan for downtime and prepare a rollback plan. The affected node must be stopped throughout the rotation, and a notary rotation also requires stopping every other node on the network.
4. Confirm that every node on the network runs a Corda version that supports certificate rotation, and that the network minimum platform version is high enough. Certificate rotation was introduced in Corda 4.7, which requires a network minimum platform version of `9`. To raise the minimum platform version, see [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}).
5. Assign new keystore aliases for the new keys in `node.conf`, and keep the old identity key available for signing. See [Rotating a node key](#rotating-a-node-key).
6. Confirm that all deployed CorDapps are compatible with key rotation.
7. Make `corda-tools-ha-utilities.jar` available in the node or notary directory. For the tool's full command syntax and options, see the [Node certificate rotation tool]({{< relref "../../ha-utilities.md#node-certificate-rotation-tool" >}}) reference.
8. When the node uses an HSM, place the vendor-supplied client-side JAR files in the `drivers` subdirectory of the configured base directory. The HA Utilities JAR does not include them. See [HSM integration]({{< relref "../../operations/deployment/hsm-integration.md" >}}).
9. Enable key rotation in the Identity Manager service. See [Enabling key rotation in the Identity Manager service](#enabling-key-rotation-in-the-identity-manager-service).

### Enabling key rotation in the Identity Manager service

Same-provider key rotation must be explicitly enabled in the CENM Identity Manager service (`cenm-idman`). Enabling it switches on the `/reissuecertificate` endpoint, which the tool uses. In `identitymanager.conf`, add `allowKeyRotation = true` to the existing issuance workflow configuration. Add the single property. Do not replace the surrounding block.

```hocon
workflows = {
  "identity-manager-alias" = {
    allowKeyRotation = true
  }
}
```

For a description of the Identity Manager service, see the {{< cenmlatestrelref "cenm/identity-manager.md" "Identity Manager Service" >}} documentation. For a description of the `allowKeyRotation` parameter, see {{< cenmlatestrelref "cenm/config-identity-manager-parameters.md" "Identity Manager configuration parameters" >}}.

{{< warning >}}

Leaving key rotation enabled after the operation is a security risk. Enable this setting only for the duration of the rotation, and disable it again as soon as the rotation is complete.

{{< /warning >}}

## Rotating a node key

1. Confirm that all [prerequisites](#prerequisites) are met.
2. Make sure that from now on no new flows are launched against the node by other nodes. See [Operational restrictions](#operational-restrictions).
3. Stop the node gracefully.
4. Edit `node.conf` to assign new aliases for the new keys. List the current identity key alias in `previousIdentityKeyAliases`, so the node can still sign for its existing states.

   ```hocon
   enterpriseConfiguration = {
       identityKeyAlias = identity-private-key-new
       clientCaKeyAlias = cordaclientca-new
       tlsKeyAlias = cordaclienttls-new
       previousIdentityKeyAliases = [ identity-private-key ]
   }
   ```

5. Run the key rotation tool. Passing `--old-node-ca-alias` signs the request with the current key, which allows the Identity Manager Workflow to auto-approve the reissuance.

   ```shell
   java -jar corda-tools-ha-utilities.jar node-certificate-rotation --config-file node.conf --old-node-ca-alias cordaclientca
   ```

6. The tool reads the current `certificates` directory and writes the new keystores to `output/certificates`. Copy every file from `output/certificates` into the node's `certificates` directory.
7. Start the node.
8. Wait a few minutes for the new `NodeInfo` to propagate across the network before you launch new flows. Then confirm that the node has started successfully and can access its states, and set `allowKeyRotation` back to `false` in the Identity Manager service.

## Rotating a notary key

Rotating a notary key changes the notary's node information, so this procedure also includes a network parameters update and a flag day. The steps below are the end-to-end sequence. For the details of each network operation, follow the linked pages.

1. Confirm that all [prerequisites](#prerequisites) are met.
2. Shut down all nodes and notaries gracefully.
3. Take a backup of the directories, databases, keystores, and HSM keys for every node, including the notary.
4. Edit `node.conf` for the notary to assign new aliases for the new keys. A notary does not need `previousIdentityKeyAliases`, because its old key is not used for signing after rotation. A notary has a single identity when `notary.serviceLegalName` is not present. In that case, reconfigure it to use two identities. Assign a new value to `myLegalName`, and copy the old value of `myLegalName` to `notary.serviceLegalName`. Keep `notary.serviceLegalName` and `myLegalName` unchanged otherwise.

   ```hocon
   enterpriseConfiguration = {
       identityKeyAlias = identity-private-key-new
       clientCaKeyAlias = cordaclientca-new
       tlsKeyAlias = cordaclienttls-new
       distributedNotaryKeyAlias = distributed-notary-private-key-new
   }
   ```

5. When using an HA notary service, first rotate the HA notary service identity by running the [Notary registration tool]({{< relref "../../ha-utilities.md#notary-registration" >}}) with the `--renew` option.
6. Run the key rotation tool for the notary. Do not pass `--old-node-ca-alias`, because notary reissuance requests are approved manually.

   ```shell
   java -jar corda-tools-ha-utilities.jar node-certificate-rotation --config-file notary.conf
   ```

7. Copy every file from the generated `output/certificates` directory into the notary's `certificates` directory.
8. Remove the `network-parameters` file from every node directory. This is required so the nodes accept the new network parameters while they are offline.
9. Generate a new `NodeInfo` for the notary.

   ```shell
   java -jar corda.jar generate-node-info --config-file=notary.conf
   ```

10. Update the network parameters so the notary whitelist contains both the old and the new notary identities, then sign the new parameters. Keeping both identities lets existing states linked to the old notary identity continue to evolve. For the full workflow, see [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}).
11. Issue the flag day to execute the update, and confirm that every node accepts the update before the deadline. See [Handling flag days]({{< relref "../../notary/handling-flag-days.md" >}}).
12. Start all nodes and notaries. Wait a few minutes for the new `NodeInfo` to propagate before you launch new flows, then set `allowKeyRotation` back to `false` in the Identity Manager service.

## Operational restrictions

### Pending flows

Before you start a rotation, make sure there are no unfinished flows running on the node and that no new incoming flows are initiated. Flow draining mode helps complete the flows the node itself started, but it does not stop other peers from initiating new flows against the node. Those start-flow messages accumulate in the `p2p.inbound.<old key hash>` broker inbox. They are never processed after the node restarts with its new identity, so those flows can get stuck or fail. The simplest way to rotate safely is to shut down every node that can communicate with the node being rotated.

### NodeInfo propagation

It takes some time for the new `NodeInfo` to propagate across the network after a node starts with its new identity. Starting a flow during this interval, either from or to the rotated node, is unsafe. Wait a few minutes after starting the node before you launch any flow activity.

## Recovering from a failed rotation

A rotation has not completed successfully if the node or notary fails to start or cannot access its states. If this happens, do not re-run the tool over the partially rotated files. Instead:

1. Stop the affected node or notary.
2. Restore the node directory, the node database, the keystores, and any HSM keys from the verified backups. For a notary, also restore the notary database.
3. Start the node and confirm that it is healthy before retrying.

## References

* [Node certificate rotation tool]({{< relref "../../ha-utilities.md#node-certificate-rotation-tool" >}}) in the HA Utilities reference, for the full command syntax and options.
* [Cross-provider key rotation]({{< relref "../cross-provider-key-rotation/cross-provider-key-rotation.md" >}}), for moving a key to a different key provider.
