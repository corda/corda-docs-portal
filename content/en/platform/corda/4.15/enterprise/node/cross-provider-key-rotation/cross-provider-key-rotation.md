---
date: '2026-08-05T14:00:00Z'
menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-corda-nodes-cross-provider-key-rotation
    name: "Cross-provider key rotation"
    parent: corda-enterprise-4-15-corda-nodes
tags:
- key rotation
- hsm
- node
title: Cross-provider key rotation
weight: 180
---

# Cross-provider key rotation

Cross-provider key rotation lets a node or notary move its legal identity key to a different key provider, such as from one hardware security module (HSM) to another, without losing access to the states and transactions it already holds. It is available in Corda Enterprise 4.15 and later.

This page is written for two audiences:

* **Node operators** who plan and run the rotation. If that is you, read [How it works](#how-it-works) and [Before you begin](#before-you-begin), then follow [Rotating a node key](#rotating-a-node-key) or [Rotating a notary key](#rotating-a-notary-key).
* **CorDapp developers** whose applications must keep working after a rotation. If that is you, read [How it works](#how-it-works) and then [Adapting your CorDapps](#adapting-your-cordapps).

{{< warning >}}

Key rotation is a system-critical operation. An unsuccessful rotation can leave the affected node unable to access its existing states. Always rehearse the procedure in a test environment, take verified backups, and have a rollback plan before you rotate a key in production.

{{< /warning >}}

## How it works

A node's legal identity key is the key it uses to sign transactions and prove who it is on the network. Every state a node has ever signed is bound to the key that signed it. Moving that key to a new provider therefore creates a problem to solve. The node must remain able to spend states that were signed with the old key, even though that key now lives in a different provider.

Cross-provider key rotation solves this with a **key rotation proof**. When you rotate a key, the HA Utilities tool generates a new legal identity key in the new provider and creates a proof, signed by the old key, that links the old key to the new one. From that point on:

* When a transaction consumes a state that was signed with the old key, it carries the relevant key rotation proof. The proof shows any verifier that the new key legitimately controls the identity that signed the original state.
* Verification checks both the transaction signature and every proof in the chain. A transaction is valid only if all of them are valid.
* Each proof adds a small, fixed overhead to the transaction (see [Transaction size and performance](#transaction-size-and-performance)).

For many applications the proofs are temporary. Once every state signed with the old key has been consumed, new transactions no longer need proofs and the overhead disappears. For applications that must preserve the same parties across a state's whole lifetime, such as bilateral agreements, the proofs may be needed indefinitely unless the CorDapp is adapted.

### How this differs from same-provider key rotation

Corda also supports same-provider key rotation, which reissues a node's legal identity key and certificate within the same key provider using the [node certificate rotation tool]({{< relref "../../ha-utilities.md#node-certificate-rotation-tool-node-same-provider-key-rotation-tool" >}}). Cross-provider rotation is a different operation with a different tool and different steps. It generates the new key in a different provider and produces the key rotation proofs described above.

{{< note >}}

Use this page only for moving between providers.

{{< /note >}}

## Before you begin

### Compatibility

Nodes running Corda 4.15 interoperate with earlier Corda versions in exactly the same way as Corda 4.14 did. The API changes that support key rotation do not affect interoperability. This includes interoperability between Corda Open Source and Corda Enterprise.

A Corda Open Source node cannot initiate a cross-provider key rotation, but a Corda Open Source node running 4.15 or later can verify transactions that contain key rotation proofs. A Corda Enterprise node can therefore adopt cross-provider key rotation without breaking compatibility with Corda Open Source nodes on the network.

### Limitations

* Only Corda Enterprise nodes and notaries running Corda 4.15 or later can initiate a rotation.
* A rotation cannot be reversed. After a successful rotation you cannot return to the old key, and moving back to a previous provider requires performing another key rotation.
* Each rotation adds a key rotation proof to the chain, which places a small overhead on affected transactions. Performing several rotations over time lengthens the proof chain and increases that overhead. See [Transaction size and performance](#transaction-size-and-performance).

## Prerequisites

Cross-provider key rotation is a system-critical operation. An unsuccessful rotation can leave the affected node or notary unable to access its existing states, so complete every item in this checklist before you rotate any key:

1. Rehearse the complete procedure in a non-production environment that mirrors production, and confirm that the node or notary restarts and can access its states afterwards. Do not run a rotation in production that you have not first validated in a test environment.
2. Take verified backups of the node database and the entire node directory, including the current `certificates` directory and its Java KeyStore (JKS) files. For a notary rotation, also back up the notary database. Confirm that you can restore these backups before you continue, because they are the only way to roll back a failed rotation.
3. Plan for downtime and prepare a rollback plan. The affected node must be stopped throughout the rotation, and a notary rotation also requires stopping every other node on the network. See [Recovering from a failed rotation](#recovering-from-a-failed-rotation).
4. Confirm that every node on the network runs Corda 4.15 or later, and that the network minimum platform version is `170`. To upgrade, see [Upgrading a node]({{< relref "../../node-upgrade-notes.md" >}}). To raise the minimum platform version, see [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}).
5. Confirm that the new key provider is configured, running, and accessible to the affected node or notary.
6. Confirm that all deployed CorDapps are compatible with key rotation. See [Adapting your CorDapps](#adapting-your-cordapps).
7. Make `corda-tools-ha-utilities.jar` version 4.15 or later available in the node or notary directory. For the tool's full command syntax and options, see the [Node cross-provider key rotation tool]({{< relref "../../ha-utilities.md#node-cross-provider-key-rotation-tool" >}}) reference.
8. When the new provider is an HSM, place the vendor-supplied client-side JAR files in the `drivers` subdirectory of the configured base directory. The HA Utilities JAR does not include them. See [HSM integration]({{< relref "../../operations/deployment/hsm-integration.md" >}}).
9. Enable key rotation in the Identity Manager service. See [Enabling key rotation in the Identity Manager service](#enabling-key-rotation-in-the-identity-manager-service).

### Enabling key rotation in the Identity Manager service

Cross-provider key rotation must be explicitly enabled in the CENM Identity Manager service (`cenm-idman`). In `identitymanager.conf`, add `allowKeyRotation = true` to the existing `identity-manager-alias` workflow configuration. Add the single property. Do not replace the surrounding block:

```hocon
workflows = {
  "identity-manager-alias" = {
    allowKeyRotation = true
  }
}
```

For a description of the Identity Manager service, see the {{< cenmlatestrelref "cenm/identity-manager.md" "Identity Manager Service" >}} documentation. For a description of the `allowKeyRotation` parameter and the surrounding workflow configuration, see {{< cenmlatestrelref "cenm/config-identity-manager-parameters.md#allowkeyrotation" "Identity Manager configuration parameters" >}}.

{{< warning >}}

Leaving key rotation enabled after the operation is a security risk. Enable this setting only for the duration of the rotation, and disable it again as soon as the rotation is complete. Disabling it is the final step of both the [node](#rotating-a-node-key) and [notary](#rotating-a-notary-key) rotation procedures.

{{< /warning >}}

## Platform version safeguards

Corda enforces the minimum platform version requirement with three safeguards:

* The key rotation tool fails if the network minimum platform version is below `170`.
* A Corda 4.15 node fails to start if a key rotation file is present and the network minimum platform version is below `170`.
* A Corda 4.15 transaction builder throws an exception if a command includes a key rotation proof and the network minimum platform version is below `170`.

{{< important >}}

These safeguards catch the most common misconfiguration, but they do not cover every operational error. Verify all prerequisites yourself before you start.

{{< /important >}}

## Rotating a node key

1. Confirm that all [prerequisites](#prerequisites) are met.
2. Stop the node.
3. In the node directory, copy the current configuration file (which points to the old key provider) to `node.conf.previous`.
4. Edit `node.conf` so that it points to the new key provider.
5. Run the key rotation tool:

   ```shell
   java -jar corda-tools-ha-utilities.jar node-cross-provider-key-rotation
   ```

6. The tool creates an `output/certificates` directory. It contains the Java KeyStore (JKS) files with the new certificates and a `key-rotation-proofs.bin` file. The proof file is what lets the node keep consuming states signed with the old key.
7. Copy every file from `output/certificates` into the node's `certificates` directory.
8. Start the node. On startup it loads the proofs from `key-rotation-proofs.bin` and deletes the file once it has processed them.
9. Confirm that the node has started successfully and can access its states. Then set `allowKeyRotation` back to `false` in the Identity Manager service.

{{< warning >}}

Once you copy the new files into `certificates`, the old certificates are gone unless you kept a backup of the previous JKS files. If the rotation fails, recover from a verified backup. See [Recovering from a failed rotation](#recovering-from-a-failed-rotation).

{{< /warning >}}

{{< important >}}

Once a cross-provider key rotation has succeeded and the new key is in use, the change cannot be reversed. Backups can roll back a rotation that has not yet succeeded, but they cannot restore the old key after a successful rotation. Reusing the old key afterwards is not supported, because Corda treats the new key as the node's current identity and reintroducing a rotated key causes undefined behaviour. Any states already signed with the new key would also become permanently inaccessible, because the notary would no longer use the key that owns them. If you later need to move back to the original provider, perform a new cross-provider key rotation rather than reinstating the old key.

{{< /important >}}

## Rotating a notary key

Rotating a notary key changes the notary's node information, so this procedure also includes a network parameters update and a flag day. The steps below are the end-to-end sequence. For the details of each network operation, follow the linked pages.

1. Confirm that all [prerequisites](#prerequisites) are met.
2. Stop the notary, then stop every other node on the network.
3. In the notary directory, copy the current `notary.conf` (which points to the old key provider) to `notary.conf.previous`.
4. Edit `notary.conf` so that it points to the new key provider.
5. Run the key rotation tool:

   ```shell
   java -jar corda-tools-ha-utilities.jar node-cross-provider-key-rotation --config-file notary.conf --config-file-previous notary.conf.previous
   ```

6. Copy every file from the generated `output/certificates` directory into the notary's `certificates` directory.
7. Delete the existing `nodeInfo-*` file from the notary directory, then generate a new one:

   ```shell
   java -jar corda.jar generate-node-info --config-file=notary.conf
   ```

8. On the Network Map Service host, stop the service and delete the notary's old `nodeInfo-*` file from its directory.
9. Update the network parameters with the notary's new node information. Create a `network-parameters-update.conf` file similar to the following:

   ```hocon
   notaries : [
     {
       notaryNodeInfoFile: <PathToNotaryInfoFile>
       validating: <Boolean>
     }
   ]
   minimumPlatformVersion = <VALUE>
   maxMessageSize = <VALUE>
   maxTransactionSize = <VALUE>
   eventHorizonDays = <VALUE>
   parametersUpdate {
     description = <STRING>
     updateDeadline = <DATE_TIME>
   }
   ```

   Apply it, then start the Network Map Service and wait for it to sign the new parameters:

   ```shell
   java -jar networkmap.jar -f networkmap.conf --set-network-parameters=FILE --network-truststore=FILE --truststore-password=<networkTrustStorePassword> --root-alias=<networkRootCertificateAlias>
   ```

   For the full workflow, see [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}).

10. Issue the flag day to execute the update:

    ```shell
    java -jar networkmap.jar -f networkmap.conf --flag-day
    ```

11. Confirm that every node accepts the network parameters update before the deadline. See [Handling flag days]({{< relref "../../notary/handling-flag-days.md" >}}).
12. Restart the notary and the remaining nodes as required by the update. Confirm that they start successfully, then set `allowKeyRotation` back to `false` in the Identity Manager service.

{{< warning >}}

As with a node rotation, the old certificates are unavailable once the new files are in place unless you kept a backup. If the rotation fails, recover from a verified backup. See [Recovering from a failed rotation](#recovering-from-a-failed-rotation).

{{< /warning >}}

{{< important >}}

Once a cross-provider key rotation has succeeded and the new key is in use, the change cannot be reversed. Backups can roll back a rotation that has not yet succeeded, but they cannot restore the old key after a successful rotation. Reusing the old key afterwards is not supported, because Corda treats the new key as the notary's current identity and reintroducing a rotated key causes undefined behaviour. Any states already signed with the new key would also become permanently inaccessible, because the node would no longer use the key that owns them. If you later need to move back to the original provider, perform a new cross-provider key rotation rather than reinstating the old key.

{{< /important >}}

## Recovering from a failed rotation

A rotation has not completed successfully if the node or notary fails to start or cannot access its states. If this happens, do not attempt to re-run the tool over the partially rotated files. Instead:

1. Stop the affected node or notary.
2. Restore the node directory, the node database, and (for a notary) the notary database from the verified backups while following the steps in [prerequisites](#prerequisites).
3. Restore the previous `certificates` directory from backup so that the node uses its original key again.
4. Start the node and confirm that it is healthy before retrying.

## Adapting your CorDapps

Most CorDapps keep working after a key rotation without changes, because the node handles rotated identities transparently. Some do not. This section explains when a CorDapp needs changes and how to make them.

### When a CorDapp needs changes

After a rotation, the `Party` and `PartyAndCertificate` objects for the rotated identity are **not equal** to the objects created before the rotation, because the underlying public key has changed. Any logic that compares a key or certificate directly, including comparisons against values stored in vault states, can therefore break.

The node absorbs most of this automatically:

* Vault queries do not distinguish between states belonging to parties with the same X.500 name.
* The `Party` field is stored as an X.500 name and is always deserialised with the current identity. Storing a `PublicKey` (or its hash) instead of a `Party` can cause compatibility problems.

The risk is concentrated in CorDapps that store party or key details directly in a state and later compare them. For example, a bilateral-agreement CorDapp such as the `negotiation-cordapp` (see [References](#references)) stores party details in its state. Its `ModificationFlow` will not work after a rotation without changes, because those stored details no longer equal the value returned by `ourIdentity`. If a CorDapp cannot be adapted, an alternative is to write dedicated flows that re-sign the affected states with the new keys.

Test every CorDapp for compatibility before you rotate a key.

### Resolving identities from a single, consistent source

The following methods always return the node's current identity from the `NetworkMapCache`, which may differ from the identity recorded in an older state:

* `IdentityService.wellKnownPartyFromX500Name`
* `FlowSession.counterparty`
* `FlowLogic.getOurIdentity`
* `IdentityService.trustRoot` and `IdentityService.trustAnchor` (these return the root of the current legal identity certificate chain)

When a party in an input state must match a party in an output state, follow these rules:

* Copy the party directly from the input state to the output state, or resolve it with `PartyIdentityResolver`.
* Do not read parties directly from the Identity or Key Management services for this purpose. They return the current identity, not the one recorded in the input state.
* Never mix sources in a single comparison. Obtain every party you compare from the same source: all from states, or all from services.
* Where a stored party may be out of date, use `PartyIdentityResolver.resolveToCurrentParty` to resolve it to its current identity in the `NetworkMapCache`.

{{< note >}}

Use `PartyIdentityResolver` only for parties or keys stored in a state, where an old identity should be replaced by the new one once it becomes available, and in contracts where a transaction must keep ownership unchanged. Do not use it to build counterparty identities. Once a stored party or key has been updated to the new identity, never revert it to the old one.

{{< /note >}}

### Signing and validating correctly

When you call `signInitialTransaction(builder: TransactionBuilder, signingPubKeys: Iterable<PublicKey>)`, the keys in `signingPubKeys` must be a subset of the keys the command requires. Asking a node to sign with a new key while the command still requires the old key causes the transaction to fail. If `signingPubKeys` contains both the old and the new key, Corda produces a separate signature for each.

If a CorDapp performs its own transaction validation, it must validate the whole key rotation proof chain, not just the transaction signature. After a key has been rotated, a valid transaction signature alone is no longer sufficient.

{{< important >}}

Do not run a mix of CorDapp versions in which some support key rotation and others do not.

{{< /important >}}

### Including proofs when parties must stay identical

When a transaction requires the parties in its input and output states to remain identical, include the required proof in `Command.keyRotationProofChainMap`. This matters most for CorDapps that implement bilateral agreements.

### Transaction size and performance

Each key rotation proof adds approximately 128 bytes to a transaction, and validating a transaction now also validates every proof in its chain, which adds one cryptographic check per proof.

* **Payment-style CorDapps:** the overhead applies only while transactions still consume states signed with the old key. Once all legacy states are consumed, transaction size and performance return to their previous baseline.
* **Bilateral-agreement CorDapps:** the overhead can apply to all future transactions unless the CorDapp is updated so that proofs are no longer required.

Assess the impact against your required throughput, and measure it in an environment that reflects your production workload. See [Performance testing]({{< relref "../../performance-testing/introduction.md" >}}).

### Upgrade patterns

CorDapps that model bilateral agreements usually need one or both of the following changes:

* **Add key rotation support** so the flow includes the required proofs in `Command.keyRotationProofChainMap` when input and output parties must match. This keeps the CorDapp working with states signed by the old key.
* **Enable proof-free transactions** by updating the contract and flow so that proofs are no longer required going forward. This removes the ongoing size and performance overhead for bilateral-agreement CorDapps.

For a worked example, study the `ModificationFlow` in the `negotiation-cordapp` sample (see [References](#references)).

## References

* [Node cross-provider key rotation tool]({{< relref "../../ha-utilities.md#node-cross-provider-key-rotation-tool" >}}) in the HA Utilities reference, for the full command syntax and options.
* `negotiation-cordapp` sample, [`ModificationFlow.java`](https://github.com/corda/samples-java/blob/release/4.12/Advanced/negotiation-cordapp/workflows/src/main/java/net/corda/samples/negotiation/flows/ModificationFlow.java).
