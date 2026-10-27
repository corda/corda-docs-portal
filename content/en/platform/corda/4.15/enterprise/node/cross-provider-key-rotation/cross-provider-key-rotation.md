---
date: '2026-08-05T14:00:00Z'
menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-corda-nodes-cross-provider-key-rotation
    name: "Cross-provider key rotation"
    parent: corda-enterprise-4-15-corda-nodes-key-rotation
tags:
- key rotation
- hsm
- node
title: Cross-provider key rotation
weight: 180
---

# Cross-provider key rotation

Cross-provider key rotation moves a node's or notary's legal identity key from one key provider to another without
losing access to the states and transactions that it already holds. It is available in Corda Enterprise 4.15 and later.

This page is written for two audiences:

* **Node operators** who plan and run the rotation. If that is you, read [How it works](#how-it-works) and [Before you begin](#before-you-begin), then follow [Rotating a node key](#rotating-a-node-key) or [Rotating a notary key](#rotating-a-notary-key).
* **CorDapp developers** whose applications must keep working after a rotation. If that is you, read [How it works](#how-it-works) and then [Adapting your CorDapps](#adapting-your-cordapps).

{{< warning >}}

Key rotation is a system-critical operation. An unsuccessful rotation can leave the affected node unable to access its existing states. Always rehearse the procedure in a test environment, take verified backups, and have a rollback plan before you rotate a key in production.

{{< /warning >}}

## How it works

A node's legal identity key is the key it uses to sign transactions and prove who it is on the network. Every state a node has ever signed is bound to the key that signed it. Moving that key to a new provider therefore creates a problem to solve. The node must remain able to spend states that were signed with the old key, even though that key now lives in a different provider.

Cross-provider key rotation solves this with a **key rotation proof**. When you rotate a key, the [HA Utilities]({{< relref "../../ha-utilities.md" >}}) tool generates a new legal identity key in the new provider. It then creates a proof, signed by the old key, that links the old key to the new one. From that point on:

* When a transaction consumes a state that was signed with the old key, it carries the relevant key rotation proof. The proof shows any verifier that the new key legitimately controls the identity that signed the original state.
* Verification checks both the transaction signature and every proof in the chain. A transaction is valid only if the signature and every proof are valid.
* Each proof adds a small, fixed overhead to the transaction (see [Transaction size and performance](#transaction-size-and-performance)).

For many applications the proofs are temporary. Once every state signed with the old key has been consumed, new transactions no longer need proofs and the overhead disappears. Some applications must preserve the same parties across a state's whole lifetime, such as bilateral agreements. For these, the proofs may be needed indefinitely unless the CorDapp is adapted.

## Before you begin

### Compatibility

Nodes running Corda 4.15 interoperate with earlier Corda versions in exactly the same way as Corda 4.14 did. The API changes that support key rotation do not affect interoperability. This includes interoperability between Corda Open Source and Corda Enterprise.

A Corda Open Source node cannot initiate a cross-provider key rotation. If it runs Corda 4.15 or later, it can still verify transactions that contain key rotation proofs. A Corda Enterprise node can therefore adopt cross-provider key rotation without breaking compatibility with Corda Open Source nodes on the network.

### Supported key providers

The following migrations are supported:

| From (previous provider) | To (new provider) |
|--------------------------|---|
| File-based keystore      | HSM |
| HSM                      | File-based keystore |
| HSM                      | Another HSM |

### Limitations

* Only Corda Enterprise nodes and notaries running Corda 4.15 or later can initiate a rotation.
* A rotation cannot be reversed. Moving back to a previous provider requires performing another rotation.
* Each rotation adds a key rotation proof to the chain, which places a small overhead on affected transactions. Performing several rotations over time lengthens the proof chain and increases that overhead. See [Transaction size and performance](#transaction-size-and-performance).
* Raft, BFT-SMaRt, and Solana notaries cannot be rotated across key providers. The tool refuses to run when either configuration uses one of these notary implementations.

## Prerequisites

Cross-provider key rotation is a system-critical operation. An unsuccessful rotation can leave the affected node or notary unable to access its existing states. Complete every item in this checklist before you rotate any key:

1. Rehearse the complete procedure in a non-production environment that mirrors production. Confirm that the node or notary restarts and can access its states afterwards. Do not run a rotation in production that you have not first validated in a test environment.
2. Take verified backups of the node database and the entire node directory, including the current `certificates` directory and its Java KeyStore (JKS) files. For a notary rotation, also back up the notary database. Confirm that you can restore these backups before you continue, because they are the only way to roll back a failed rotation.
3. Plan for downtime and prepare a rollback plan. The affected node must remain stopped throughout the rotation. Rotating a standalone notary also requires stopping every other node on the network. For a notary cluster, each worker needs to be stopped only while the tool runs and restarted once after flag day. The rest of the network can remain running. See [Recovering from a failed rotation](#recovering-from-a-failed-rotation).
4. Confirm that every node on the network runs Corda 4.15 or later. To upgrade, see [Upgrading a node]({{< relref "../../node-upgrade-notes.md" >}}).
5. Confirm that the network minimum platform version is `170`. To raise the minimum platform version, see [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}).
6. Confirm that the new key provider is configured, running, and accessible to the affected node or notary.
7. Confirm that all deployed CorDapps are compatible with key rotation. See [Adapting your CorDapps](#adapting-your-cordapps).
8. Make `corda-tools-ha-utilities.jar` version 4.15 or later available in the node or notary directory. For the tool's full command syntax and options, see the [Node cross-provider key rotation tool]({{< relref "../../ha-utilities.md#node-cross-provider-key-rotation-tool" >}}) reference.
9. When the new provider is an HSM, place the vendor-supplied client-side JAR files in the `drivers` subdirectory of the configured base directory. The HA Utilities JAR does not include them. See [HSM integration]({{< relref "../../operations/deployment/hsm-integration.md" >}}).
10. Enable key rotation in the Identity Manager service. See [Enabling key rotation in the Identity Manager service](#enabling-key-rotation-in-the-identity-manager-service).

### Enabling key rotation in the Identity Manager service

Cross-provider key rotation must be explicitly enabled in the CENM Identity Manager service (`cenm-idman`). In `identitymanager.conf`, add `allowKeyRotation = true` to the existing `identity-manager-alias` workflow configuration. Add the single property. Do not replace the surrounding block:

```hocon
workflows = {
  "identity-manager-alias" = {
    allowKeyRotation = true
  }
}
```

For a description of the Identity Manager service, see the {{< cenmlatestrelref "cenm/identity-manager.md" "Identity Manager Service" >}} documentation. For a description of the `allowKeyRotation` parameter and the surrounding workflow configuration, see {{< cenmlatestrelref "cenm/config-identity-manager-parameters.md" "Identity Manager configuration parameters" >}}.

{{< warning >}}

Leaving key rotation enabled after the operation is a security risk. Enable this setting only for the duration of the rotation, and disable it again as soon as the rotation is complete. Disabling it is the final step of both the [node](#rotating-a-node-key) and [notary](#rotating-a-notary-key) rotation procedures.

{{< /warning >}}

## Platform version safeguards

Corda enforces this requirement. If the network minimum platform version is below `170`, the following safeguards apply:

* The key rotation tool fails.
* A Corda 4.15 node fails to start when a key rotation file is present.
* A Corda 4.15 transaction builder throws an exception when a command includes a key rotation proof.

{{< important >}}

These safeguards catch the most common misconfiguration, but they do not cover every operational error. Verify all prerequisites yourself before you start.

{{< /important >}}

## Rotating a node key

1. Confirm that all [prerequisites](#prerequisites) are met.
2. Make sure that from now on no new flows are launched against the node by other nodes, then stop the node. See [Operational restrictions](#operational-restrictions).
3. In the node directory, copy the current configuration file (which points to the old key provider) to `node.conf.previous`.
4. Edit `node.conf` so that it points to the new key provider.
5. Run the key rotation tool:

   ```shell
   java -jar corda-tools-ha-utilities.jar node-cross-provider-key-rotation
   ```

6. The tool creates an `output/certificates` directory. It contains the Java KeyStore (JKS) files with the new certificates and a `key-rotation-proofs.bin` file. The proof file is what lets the node keep consuming states signed with the old key.
7. Copy every file from `output/certificates` into the node's `certificates` directory.
8. Start the node. On startup, it loads the proofs from `key-rotation-proofs.bin`, records any that are not already in its database, and deletes the file once it has processed them. Re-processing the same file, for example one restored from a backup, has no effect, because a proof already recorded is skipped.
9. Confirm that the node has started successfully and can access its states. Then set `allowKeyRotation` back to `false` in the Identity Manager service.

{{< warning >}}

Once you copy the new files into `certificates`, the old certificates are gone unless you kept a backup of the previous JKS files. If the rotation fails, recover from a verified backup. See [Recovering from a failed rotation](#recovering-from-a-failed-rotation).

{{< /warning >}}

{{< important >}}

Once a cross-provider key rotation has succeeded and the new key is in use, the change cannot be reversed. Backups can roll back a rotation that has not yet succeeded, but they cannot restore the old key after a successful rotation. Reusing the old key afterwards is not supported. Corda treats the new key as the node's current identity, so reintroducing a rotated key causes undefined behaviour. Any states already signed with the new key would also become permanently inaccessible. The node no longer uses the key that owns them. If you later need to move back to the original provider, perform a new cross-provider key rotation rather than reinstating the old key.

{{< /important >}}

## Rotating a notary key

A notary node has two identities, each backed by keys held in the notary's key provider. One is the notary's own legal identity, named by `myLegalName`. The other is the notary service identity, named by `notary.serviceLegalName`, whose signing key is held under the alias `enterpriseConfiguration.distributedNotaryKeyAlias`. The notary service identity key is the one listed in the network parameters and the one that signs notarised transactions. In a notary cluster, it is shared by every worker. Moving a notary to a new key provider also requires a new notary service key in that provider, because the rotation does not transfer the existing key.

How that new key is created depends on the kind of notary. Keep `distributedNotaryKeyAlias` unchanged in `notary.conf` and `notary.conf.previous` in both cases.

* **A single notary** does not share the key with any other notary. `node-cross-provider-key-rotation` creates the new notary service identity as part of the rotation. It generates the key with the new key provider, obtains a certificate for it from the Identity Manager, and stores the certificate in the new node key store, exactly as `initial-registration` does for a new notary.
* **A notary cluster** shares the key between its workers, so it is created once, for the cluster, before any worker is rotated. This is the same two-step procedure as the registration of an HA notary (see [Registering a HA notary]({{< relref "../../notary/ha-notary-service-setup.md#registering-a-ha-notary" >}})). The tool `notary-registration --renew`, run against the new key provider, generates the key and obtains its certificate. The key store it writes is then copied to every worker, and each worker's rotation finds the notary service identity in place and rotates only the worker's own identity. Keep in mind that the tool does not create the notary service identity for a cluster worker. Without the new key store it stops, before submitting anything, with an error message.

In both cases the request for the new notary service certificate is a re-issuance request which an operator must approve manually. `allowKeyRotation` must be enabled in the Identity Manager for the duration of the rotation (see [Prerequisites](#prerequisites)).

No key rotation proof is produced for the notary service key, and none is needed to keep earlier transactions usable. A state records the notary identity, X.500 name and public key, that was current when it was created. A transaction notarised by the notary's new identity can consume such a state, because the platform only requires the notary of each input state and the notary of the transaction to have the same X.500 name, which does not change during a rotation. The network parameters check, however, is made on the public key. Every notary identity that a transaction refers to, including those of its input states, must be listed in the network parameters. The previous notary identity must therefore stay in the network parameters until no unconsumed state refers to it. The previous private key plays no part in this. After the rotation, the new key signs every notarisation, including those that consume states created under the previous identity. Because the notary list in the network parameters changes, rotating a notary always includes a network parameters update and a flag day.

In both procedures below, the new notary identity is added to the network parameters **alongside** the previous one, and the previous one is removed in a later update, once no unconsumed state refers to it (see [Retiring the previous notary identity](#retiring-the-previous-notary-identity)). The procedures differ in what keeps running. A single notary is rotated with the notary and all nodes stopped. A cluster keeps serving: each worker is stopped only while the tool runs on it, then restarted on its previous configuration, so the cluster keeps signing with the previous key until the flag day, and the other nodes stay up. The CENM services keep running in both cases.

### Rotating a single notary

1. Confirm that all [prerequisites](#prerequisites) are met.
2. Stop the notary, then stop every other node on the network.
3. In the notary directory, copy the current `notary.conf` (which points to the old key provider) to `notary.conf.previous`.
4. Edit `notary.conf` so that it points to the new key provider. Keep `myLegalName`, `notary.serviceLegalName` and `enterpriseConfiguration.distributedNotaryKeyAlias` unchanged.
5. Run the key rotation tool:

   ```shell
   java -jar corda-tools-ha-utilities.jar node-cross-provider-key-rotation --config-file notary.conf --config-file-previous notary.conf.previous
   ```

6. Copy every file from the generated `output/certificates` directory into the notary's `certificates` directory.
7. Generate the notary's node info from the rotated configuration. The new file carries the new notary service identity and has the same name as the previous one, because Corda derives the name from the notary's legal name, so it overwrites the previous file in the notary directory. In the Network Map Service's directory, keep the previous node info under another name before copying the new one there. The parameters update in the next step needs both files:

   ```shell
   java -jar corda.jar generate-node-info --config-file=notary.conf
   ```

8. Update the network parameters so that the notary list contains **both** the previous and the new notary identity under the same notary name. The previous entry is the node info the current parameters were built from, and the new entry is the one generated in the previous step. The previous identity must remain listed while unconsumed states created under it exist. Create a `network-parameters-update.conf` file similar to the following:

   ```hocon
   notaries : [
     {
       notaryNodeInfoFile: <PathToPreviousNotaryInfoFile>
       validating: <Boolean>
     },
     {
       notaryNodeInfoFile: <PathToNewNotaryInfoFile>
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

   Both node info files must be available to the Network Map Service. Apply the update, then start the Network Map Service and wait for it to sign the new parameters:

   ```shell
   java -jar networkmap.jar -f networkmap.conf --set-network-parameters=FILE --network-truststore=FILE --truststore-password=<networkTrustStorePassword> --root-alias=<networkRootCertificateAlias>
   ```

   For the full workflow, including the equivalent CENM command-line interface commands (`netmap netparams update submit`, `advertise` and `execute`), see [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}).

9. Issue the flag day to execute the update:

    ```shell
    java -jar networkmap.jar -f networkmap.conf --flag-day
    ```

10. Delete the cached `network-parameters` file from the notary directory and from every node directory that was stopped during the update. A node that was offline during the flag day still holds the previous parameters in that file and refuses to start with `Node is using network parameters with hash ... but the network map is advertising ...`. Without the file, it downloads the current parameters from the Network Map Service when it starts. Nodes that stayed online and accepted the update do not need this. See [Handling flag days]({{< relref "../../notary/handling-flag-days.md" >}}).
11. Start the notary and the remaining nodes. Confirm that they start successfully and that the notary's log does not warn that its identity is not in the whitelist, then set `allowKeyRotation` back to `false` in the Identity Manager service.

### Rotating a notary cluster

The new notary service key and certificate are created once, before the workers are rotated. The workers are then rotated one at a time, in any order, so that the rest of the cluster keeps serving, and each returns to serving on its previous configuration until the flag day, because the tool writes only under `output/`. After the flag day every worker is switched to its rotated files and restarted once. The other nodes of the network stay up throughout.

Procedure:

1. Confirm that all [prerequisites](#prerequisites) are met.
2. On one worker, prepare the new configuration: copy the current `notary.conf` to `notary.conf.previous`, then edit `notary.conf` so that it points to the new key provider, keeping `myLegalName`, `notary.serviceLegalName` and `enterpriseConfiguration.distributedNotaryKeyAlias` unchanged. The worker can keep running on its previous configuration meanwhile.
3. On that worker, create the new notary service identity with the registration tool, sending its output to a new file. The tool generates the notary service key with the new key provider, obtains its certificate chain from the Identity Manager, and writes the chain (and the key, if the new key provider is a file-based key store) to the output key store:

   ```shell
   java -jar corda-tools-ha-utilities.jar notary-registration --renew --config-file notary.conf --output-keystore output/certificates/nodekeystore.jks --network-root-truststore certificates/network-root-truststore.jks --network-root-truststore-password <password>
   ```

   If the output key store already holds an entry under `distributedNotaryKeyAlias` (such as the current `certificates/nodekeystore.jks`), the tool reports that the certificate already exists and does nothing. An empty key store left by an earlier failed run is fine.

4. Copy `output/certificates/nodekeystore.jks` to every other worker, at the same path under the worker's directory. The tool wrote this keystore with the node key store password from the configuration of the worker that ran the renewal. Nothing requires the other workers to use that password. If a worker uses a different node key store password, change the password of its copy to match, rather than re-running the renewal, which would create a second notary service key. Change the store password with `keytool -storepasswd`. When the key provider is file-based, the private key is held in the keystore, so also change the key password with `keytool -keypasswd`.
5. Rotate the workers one at a time, in any order:

   a. Stop the worker.

   b. Prepare its new configuration as in step 2, with the worker's own `identityKeyAlias` and `clientCaKeyAlias`.

   c. Run the key rotation tool. The worker's own identity is rotated into `output/certificates`, next to the notary service certificate installed in step 4:

      ```shell
      java -jar corda-tools-ha-utilities.jar node-cross-provider-key-rotation --config-file notary.conf --config-file-previous notary.conf.previous
      ```

   d. Start the worker again on its **previous** configuration and certificates: nothing under `certificates` or `notary.conf.previous` has changed, and the previous identity is still the one in the network parameters, so the worker keeps serving until the flag day.

6. Generate the new node info on one worker. `generate-node-info` must use the keystores generated during the key rotation. So stop the worker, back up its current `certificates` directory, then copy `nodekeystore.jks`, `sslkeystore.jks` and `truststore.jks` from `output/certificates` into `certificates`. Finally, run the command.
   Afterwards, restore the backup over `certificates` so the worker keeps serving on its previous identity, or leave the worker stopped until the flag day. The new node info has the same file name as the previous one, because Corda derives the name from the notary's legal name. Keep a copy of the previous node info under another name, where the Network Map Service can read it, since the parameters update needs both:

   {{< warning >}}

   Do not copy `key-rotation-proofs.bin`. A node loads that file on every start and records the rotation in its database, so it must not be present while the worker is still on its previous identity. Were it present, the worker could no longer sign or accept the network parameters update with its previous key.

   {{< /warning >}}

   ```shell
   java -jar corda.jar generate-node-info --config-file=notary.conf
   ```

7. Update the network parameters so that the notary list contains **both** the previous and the new notary identity under the same notary name. The previous entry is the node info the current parameters were built from, and the new entry is the one generated in the previous step. Keeping the previous identity is what lets the workers keep serving until the flag day and lets existing states that name it continue to evolve. Advertise the update, have the running nodes and workers accept it, and execute the flag day. For the commands, see step 8 of [Rotating a single notary](#rotating-a-single-notary) and [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}).

   ```hocon
   notaries : [
     {
       notaryNodeInfoFile: <PathToPreviousNotaryInfoFile>
       validating: <Boolean>
     },
     {
       notaryNodeInfoFile: <PathToNewNotaryInfoFile>
       validating: <Boolean>
     }
   ]
   ```

8. After the flag day, switch each worker to its rotated files. Stop it, copy every file from `output/certificates` into `certificates`, delete the cached `network-parameters` file (the worker was on the previous parameters at the flag day, see step 10 of the single-notary procedure), and start it on the new `notary.conf`. Copying into the existing directory keeps the files the tool does not write, such as `network-root-truststore.jks` and, for file-based wrapped confidential identities, `wrappingkeystore.pkcs12`. Confirm that its log does not warn that its identity is not in the whitelist, then confirm with a transaction from a node that the cluster notarises. If the notary uses the JPA backing store, its request log (`notary_request_log`, column `worker_node_x500_name`) records which worker served each request.
9. Once every worker runs on the new key provider, set `allowKeyRotation` back to `false` in the Identity Manager service.

### Retiring the previous notary identity

Both procedures leave the previous notary identity in the network parameters. Nodes do not select it for new transactions, because the network map only holds the notary's new node info, but it must remain listed while unconsumed states created under it exist. Every notary identity that a transaction refers to, including those of its input states, is checked against the network parameters. Retire it when no unconsumed state names it by submitting a network parameters update that lists only the new node info, and revoking the previous notary service certificate in the Identity Manager service.

The previous private key is not needed to consume those states. After the rotation, the new key signs every notarisation. Keep `notary.conf.previous` and the previous `certificates` directory only until the notary, or every worker of a cluster, has been switched to the new key provider. They are the rollback until then.

{{< warning >}}

As with a node rotation, the old certificates are unavailable once the new files are in place unless you kept a backup. If the rotation fails, recover from a verified backup. See [Recovering from a failed rotation](#recovering-from-a-failed-rotation).

{{< /warning >}}

{{< important >}}

Once a cross-provider key rotation has succeeded and the new key is in use, the change cannot be reversed. Backups can roll back a rotation that has not yet succeeded, but they cannot restore the old key after a successful rotation. Reusing the old key afterwards is not supported. Corda treats the new key as the notary's current identity, so reintroducing a rotated key causes undefined behaviour.

{{< /important >}}

## Operational restrictions

### Pending flows

Before you start a rotation, make sure there are no unfinished flows running on the node and that no new incoming flows are initiated. Flow draining mode helps complete the flows the node itself started, but it does not stop other peers from initiating new flows against the node. Those start-flow messages accumulate in the `p2p.inbound.<old key hash>` broker inbox. They are never processed after the node restarts with its new identity, so those flows can get stuck or fail. The simplest way to rotate safely is to shut down every node that can communicate with the node being rotated.

### NodeInfo propagation

It takes some time for the new `NodeInfo` to propagate across the network after a node starts with its new identity. Starting a flow during this interval, either from or to the rotated node, is unsafe. Wait a few minutes after starting the node before you launch any flow activity.

## Recovering from a failed rotation

A rotation has not completed successfully if the node or notary fails to start or cannot access its states. If this happens, do not attempt to re-run the tool over the partially rotated files. Instead:

1. Stop the affected node or notary.
2. Restore the node directory, the node database, and (for a notary) the notary database from the verified backups you took in the [prerequisites](#prerequisites).
3. Restore the previous `certificates` directory from backup so that the node uses its original key again.
4. Start the node and confirm that it is healthy before retrying.

## Adapting your CorDapps

Most CorDapps keep working after a key rotation without changes, because the node handles rotated identities transparently. Some do not. This section explains when a CorDapp needs changes, which changes to make, and walks through the two patterns using the `negotiation-cordapp` sample.

### When a CorDapp needs changes

After a rotation, the `Party` and `PartyAndCertificate` objects for the rotated identity are **not equal** to the objects created before the rotation. The underlying public key has changed. Any logic that compares a key or certificate directly, including comparisons against values stored in vault states, can therefore break.

The node absorbs most of this automatically:

* Vault queries do not distinguish between states belonging to parties with the same X.500 name.
* The `Party` field is stored as an X.500 name and is always deserialised with the current identity. Storing a `PublicKey` (or its hash) instead of a `Party` can cause compatibility problems.
* `initiateFlow` accepts a `Party` that holds an old key. The session is established with the counterparty's current identity.
* `CollectSignaturesFlow`, `FinalityFlow` and signature verification accept a signature made with a rotated key in place of the original key, as long as the key rotation proof is available in the transaction.

The risk is concentrated in CorDapps that store party or key details directly in a state and later compare them. A bilateral-agreement CorDapp such as the `negotiation-cordapp` (see [References](#references)) stores party details in its state and its `ModificationFlow` does not work after a rotation without changes, because those stored details no longer equal the value returned by `ourIdentity`. The [sample](#sample-the-negotiation-cordapp) below shows exactly where it breaks and the two ways to fix it. If a CorDapp cannot be adapted, an alternative is to write dedicated flows that re-sign the affected states with the new keys.

Test every CorDapp for compatibility before you rotate a key. See [Testing a CorDapp against a rotated key](#testing-a-cordapp-against-a-rotated-key).

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

Use `PartyIdentityResolver` for parties or keys stored in a state, where an old identity should be replaced by the new one once it becomes available. Also use it in contracts where a transaction must keep ownership unchanged. Do not use it to build counterparty identities. Once a stored party or key has been updated to the new identity, never revert it to the old one.

{{< /note >}}

### Signing and validating correctly

When you call `signInitialTransaction(builder: TransactionBuilder, signingPubKeys: Iterable<PublicKey>)`, the keys in `signingPubKeys` must be a subset of the keys the command requires. Asking a node to sign with a new key while the command still requires the old key causes the transaction to fail. If `signingPubKeys` contains both the old and the new key, Corda produces a separate signature for each.

If a CorDapp performs its own transaction validation, it must validate the whole key rotation proof chain, not just the transaction signature. After a key has been rotated, a valid transaction signature alone is no longer sufficient.

{{< important >}}

Do not run a mix of CorDapp versions in which some support key rotation and others do not.

{{< /important >}}

### Where the proof is stored

A key rotation proof is needed whenever a transaction consumes a state that names a rotated key, because the transaction must be signed for that key and the node no longer holds it. The node signs with its new key, and the proof links the new key to the old one. The proof can travel in two places, and which one depends on how the CorDapp was adapted:

* **In the signature.** The node attaches the proof chain to the metadata of its own signature. The platform does this for you: `signInitialTransaction`, `SignTransactionFlow`, `CollectSignaturesFlow` and signature verification all understand it. The contract never sees this proof. This is enough when the output state keeps naming the old key.
* **In the command.** The flow puts the proof chain in `Command.keyRotationProofChainMap`. This is the only place a contract can read a proof from, so it is required whenever the output state replaces the old key by the new one and the contract must verify that both keys belong to the same party.

Once a state names only current keys, consuming it needs no proof at all.

### Transaction size and performance

Key rotation proofs add a few hundred bytes per proof, plus a one-off schema overhead per transaction. Validating a transaction now also validates every proof in its chain, which adds one cryptographic check per proof.

* **Payment-style CorDapps:** the overhead applies only while transactions still consume states signed with the old key. Once all legacy states are consumed, transaction size and performance return to their previous baseline.
* **Bilateral-agreement CorDapps:** the overhead can apply to all future transactions unless the CorDapp is updated so that proofs are no longer required.

If performance is paramount, always assess the impact against your required throughput,
and measure it in an environment that reflects your production workload. See [Performance testing]({{< relref "../../performance-testing/introduction.md" >}}).

### Sample: the negotiation CorDapp

The `negotiation-cordapp` sample models a bilateral agreement. A `ProposalState` names the `buyer`, the `seller`, the `proposer` and the `proposee`. Only the proposee can modify or accept a proposal, and whoever modifies becomes the new proposer. The sample repositories contain the original CorDapp and two adapted copies (see [References](#references)):

| Sample | Pattern | Where the proof is stored | Proof needed |
|--------|---------|---------------------------|--------------|
| `negotiation-cordapp` | Original. | Nowhere: the flow fails after a rotation. | n/a |
| `negotiation-cordapp-key-rotation-support` | Add key rotation support. | In the signature of the node that rotated. | On every transaction that consumes a state naming the old key, indefinitely. |
| `negotiation-cordapp-key-rotation-proof-free` | Enable proof-free transactions. | In the command (or in the signature when the counterparty starts the transaction). | Once per state that references an old key. Later transactions carry no proof. |

#### Why the original flow breaks

The original `ModificationFlow` works out which party it is by comparing `ourIdentity` with the proposer stored in the input state, builds the output around `ourIdentity`, and requires the signatures of the keys named by the input:

{{< tabs name="original-modification-flow" >}}
{{% tab name="Kotlin" %}}
```kotlin
val counterparty = if (ourIdentity == input.proposer) input.proposee else input.proposer
val output = input.copy(amount = newAmount, proposer = ourIdentity, proposee = counterparty)

val requiredSigners = listOf(input.proposee.owningKey, input.proposer.owningKey)
val command = Command(ProposalAndTradeContract.Commands.Modify(), requiredSigners)
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
Party counterparty = (getOurIdentity().equals(input.getProposer())) ? input.getProposee() : input.getProposer();
ProposalState output = new ProposalState(newAmount, input.getBuyer(), input.getSeller(), getOurIdentity(), counterparty, input.getLinearId());

List<PublicKey> requiredSigners = ImmutableList.of(input.getProposee().getOwningKey(), input.getProposer().getOwningKey());
Command command = new Command(new ProposalAndTradeContract.Commands.Modify(), requiredSigners);
```
{{% /tab %}}
{{< /tabs >}}

After the node that made the proposal rotates its key, `ourIdentity` holds the new key while `input.proposer` holds the old one, so the comparison is false and the flow picks the wrong counterparty. The output then mixes a current key (`ourIdentity`) with old keys,
and the contract, which checks that buyer and seller are unchanged with `==`, rejects the transaction. The responder has the same problem in `checkTransaction`, where it compares the proposee stored in the state with `counterpartySession.counterparty`.

#### Pattern 1: add key rotation support

This pattern keeps the states exactly as they are. No key is ever replaced in a state, the contract remains unchanged, and the proof is stored in the rotated node’s signature. This is the smallest possible change, at the cost of requiring a proof on every transaction that consumes a state referencing the old key.

The initiator resolves the proposer stored in the state to its current identity **only for comparison** with `ourIdentity`, then continues working with the parties as they are named in the input:

{{< tabs name="support-modification-flow" >}}
{{% tab name="Kotlin" %}}
```kotlin
// A party read from a state may hold a key that has since been rotated, while ourIdentity always holds the
// current key. Resolve the stored party to its current identity before comparing the two. Nothing is replaced
// in the output, so resolveToCurrentParty (which does not need a proof) is sufficient.
val proposerParty = resolveToCurrentParty(input.proposer, serviceHub.identityService)
val myPartyFromInput = if (ourIdentity == proposerParty) input.proposer else input.proposee
val counterpartyFromInput = if (myPartyFromInput == input.proposer) input.proposee else input.proposer

// The output keeps the parties exactly as the input names them.
val output = input.copy(amount = newAmount, proposer = myPartyFromInput, proposee = counterpartyFromInput)

// The required signers are the keys named by the input. The node that rotated no longer holds that key: it
// signs with its new key and the platform attaches the key rotation proof to the signature, which satisfies
// the old key during verification. No proof map is needed in the command.
val requiredSigners = listOf(input.proposee.owningKey, input.proposer.owningKey)
val command = Command(ProposalAndTradeContract.Commands.Modify(), requiredSigners)

// ... build and sign the transaction as before ...

// The counterparty stored in the state may hold an old key. initiateFlow resolves it to the node's current identity.
val counterpartySession = initiateFlow(counterpartyFromInput)
val fullyStx = subFlow(CollectSignaturesFlow(partStx, listOf(counterpartySession)))
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
// A party read from a state may hold a key that has since been rotated, while getOurIdentity() always holds the
// current key. Resolve the stored party to its current identity before comparing the two. Nothing is replaced
// in the output, so resolveToCurrentParty (which does not need a proof) is sufficient.
Party proposerParty = PartyIdentityResolver.Companion.resolveToCurrentParty(input.getProposer(), getServiceHub().getIdentityService());
Party myPartyFromInput = (getOurIdentity().equals(proposerParty)) ? input.getProposer() : input.getProposee();
Party counterpartyFromInput = (myPartyFromInput.equals(input.getProposer())) ? input.getProposee() : input.getProposer();

// The output keeps the parties exactly as the input names them.
ProposalState output = new ProposalState(newAmount, input.getBuyer(), input.getSeller(), myPartyFromInput, counterpartyFromInput, input.getLinearId());

// The required signers are the keys named by the input. The node that rotated no longer holds that key: it
// signs with its new key and the platform attaches the key rotation proof to the signature, which satisfies
// the old key during verification. No proof map is needed in the command.
List<PublicKey> requiredSigners = ImmutableList.of(input.getProposee().getOwningKey(), input.getProposer().getOwningKey());
Command command = new Command(new ProposalAndTradeContract.Commands.Modify(), requiredSigners);

// ... build and sign the transaction as before ...

// The counterparty stored in the state may hold an old key. initiateFlow resolves it to the node's current identity.
FlowSession counterpartySession = initiateFlow(counterpartyFromInput);
SignedTransaction fullyStx = subFlow(new CollectSignaturesFlow(partStx, ImmutableList.of(counterpartySession)));
```
{{% /tab %}}
{{< /tabs >}}

The responder applies the same rule the other way round. `counterpartySession.counterparty` is a current identity, so the proposee stored in the state
must be resolved before the two are compared:

{{< tabs name="support-responder" >}}
{{% tab name="Kotlin" %}}
```kotlin
override fun checkTransaction(stx: SignedTransaction) {
    val input = stx.toLedgerTransaction(serviceHub, false).inputsOfType<ProposalState>().single()

    // counterpartySession.counterparty always holds the current identity, so the party stored in the state must
    // be resolved to its current identity before the two can be compared.
    val proposee = resolveToCurrentParty(input.proposee, serviceHub.identityService)
    if (proposee != counterpartySession.counterparty) {
        throw FlowException("Only the proposee can modify a proposal.")
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
@Override
protected void checkTransaction(@NotNull SignedTransaction stx) throws FlowException {
    LedgerTransaction ledgerTx = stx.toLedgerTransaction(getServiceHub(), false);
    ProposalState input = ledgerTx.inputsOfType(ProposalState.class).get(0);

    // counterpartySession.getCounterparty() always holds the current identity, so the party stored in the state
    // must be resolved to its current identity before the two can be compared.
    Party proposee = PartyIdentityResolver.Companion.resolveToCurrentParty(input.getProposee(), getServiceHub().getIdentityService());
    if (!proposee.equals(counterpartySession.getCounterparty())) {
        throw new FlowException("Only the proposee can modify a proposal.");
    }
}
```
{{% /tab %}}
{{< /tabs >}}

`AcceptanceFlow` receives the same two changes. The contract is untouched: input and output still name the same keys, so its equality checks keep passing.

With this pattern, after node A rotates, every proposal modification and the final acceptance carry A's proof chain in A's signature, whether A or B starts the transaction, and the trade is still recorded against A's original key. The counterparty needs no prior knowledge of the rotation. The proof arrives with the signature.

#### Pattern 2: enable proof-free transactions

This pattern replaces a rotated key by the current one in the output state the first time the node that rotated consumes a state naming its old key. That transaction carries the proof in the command so the contract can verify the replacement. Afterward, the state names only current keys and no further proof is needed. It costs a few more lines in the flow and a contract change, and removes the permanent overhead.

The initiator resolves every party stored in the state through a `PartyIdentityResolver` backed by the Identity Service, builds the output from the resolved parties, and puts the resulting proof map in the command:

{{< tabs name="proof-free-modification-flow" >}}
{{% tab name="Kotlin" %}}
```kotlin
// Resolve every party stored in the state. The resolver consults the Identity Service: if the node holds a
// proof for a party, the resolution carries that party's current identity; otherwise it carries the stored one.
// A node always holds the proofs for its own rotations; it learns a counterparty's proof from the first
// transaction the counterparty signs after rotating.
val resolver = PartyIdentityResolver(serviceHub.identityService)
val buyerKeyResolution = resolver.resolve(input.buyer)
val sellerKeyResolution = resolver.resolve(input.seller)
val proposerKeyResolution = resolver.resolve(input.proposer)
val proposeeKeyResolution = resolver.resolve(input.proposee)

// Builds the proof map for every party whose resolved identity differs from the stored one, keyed by the
// original key. Returns null when no key changed, so the command is identical to one without any rotation.
// Proposer and proposee are always the buyer and the seller, so those two resolutions are enough.
val proofMap = generateProofChainMap(buyerKeyResolution, sellerKeyResolution)

// Compare ourIdentity (current) with a resolved party (current where a proof is known), never with the
// party stored in the state. originalOrCurrentParty is the current identity when a proof is known and the stored one otherwise.
val ourIdentityFromInput = if (ourIdentity == proposerKeyResolution.originalOrCurrentParty) {
    proposerKeyResolution.originalOrCurrentParty
} else {
    proposeeKeyResolution.originalOrCurrentParty
}
val counterpartyFromInput = if (ourIdentity == proposerKeyResolution.originalOrCurrentParty) {
    proposeeKeyResolution.originalOrCurrentParty
} else {
    proposerKeyResolution.originalOrCurrentParty
}

// The output is built from the resolved parties, so a rotated key is replaced wherever a proof is known and
// kept otherwise. Use the same resolutions for the output and for the required signers: never mix a node's
// old and new keys in one transaction.
val output = ProposalState(
    amount = newAmount,
    buyer = buyerKeyResolution.originalOrCurrentParty,
    seller = sellerKeyResolution.originalOrCurrentParty,
    proposer = ourIdentityFromInput,
    proposee = counterpartyFromInput,
    linearId = input.linearId
)
val requiredSigners = listOf(proposeeKeyResolution.owningKey, proposerKeyResolution.owningKey)

// The proof map goes into the command, which is the only place the contract can read it from.
val command = Command(ProposalAndTradeContract.Commands.Modify(), requiredSigners, proofMap)
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
// Resolve every party stored in the state. The resolver consults the Identity Service: if the node holds a
// proof for a party, the resolution carries that party's current identity; otherwise it carries the stored one.
// A node always holds the proofs for its own rotations; it learns a counterparty's proof from the first
// transaction the counterparty signs after rotating.
PartyIdentityResolver resolver = new PartyIdentityResolver(getServiceHub().getIdentityService());
PartyIdentityResolved buyerKeyResolution = resolver.resolve(input.getBuyer());
PartyIdentityResolved sellerKeyResolution = resolver.resolve(input.getSeller());
PartyIdentityResolved proposerKeyResolution = resolver.resolve(input.getProposer());
PartyIdentityResolved proposeeKeyResolution = resolver.resolve(input.getProposee());

// Builds the proof map for every party whose resolved identity differs from the stored one, keyed by the
// original key. Returns null when no key changed, so the command is identical to one without any rotation.
// Proposer and proposee are always the buyer and the seller, so those two resolutions are enough.
SortedMap<PublicKey, KeyRotationProofChain> proofMap = PartyIdentityResolver.Companion.generateProofChainMap(buyerKeyResolution, sellerKeyResolution);

// Compare getOurIdentity() (current) with a resolved party (current where a proof is known), never with the
// party stored in the state. getOriginalOrCurrentParty() is the current identity when a proof is known and the stored one otherwise.
Party ourIdentityFromInput = (getOurIdentity().equals(proposerKeyResolution.getOriginalOrCurrentParty()))
        ? proposerKeyResolution.getOriginalOrCurrentParty() : proposeeKeyResolution.getOriginalOrCurrentParty();
Party counterpartyFromInput = (getOurIdentity().equals(proposerKeyResolution.getOriginalOrCurrentParty()))
        ? proposeeKeyResolution.getOriginalOrCurrentParty() : proposerKeyResolution.getOriginalOrCurrentParty();

// The output is built from the resolved parties, so a rotated key is replaced wherever a proof is known and
// kept otherwise. Use the same resolutions for the output and for the required signers: never mix a node's
// old and new keys in one transaction.
ProposalState output = new ProposalState(newAmount,
        buyerKeyResolution.getOriginalOrCurrentParty(), sellerKeyResolution.getOriginalOrCurrentParty(),
        ourIdentityFromInput, counterpartyFromInput, input.getLinearId());
List<PublicKey> requiredSigners = ImmutableList.of(proposeeKeyResolution.getOwningKey(), proposerKeyResolution.getOwningKey());

// The proof map goes into the command, which is the only place the contract can read it from.
Command command = new Command(new ProposalAndTradeContract.Commands.Modify(), requiredSigners, proofMap);
```
{{% /tab %}}
{{< /tabs >}}

Because the output may now name a different key from the input for the same party, the contract can no longer compare parties with `==`. It builds a `PartyIdentityResolver` from the proof map in the command and uses it for every comparison:

{{< tabs name="proof-free-contract" >}}
{{% tab name="Kotlin" %}}
```kotlin
is Commands.Modify -> requireThat {
    // ... structural checks unchanged ...
    val input = tx.inputsOfType<ProposalState>().single()
    val output = tx.outputsOfType<ProposalState>().single()

    // A resolver backed by the proof map in the command. With no proof map it falls back to plain equality,
    // so transactions without any rotation verify exactly as before.
    val resolver = PartyIdentityResolver(cmd.keyRotationProofChainMap)

    "The amount is modified in the output" using (output.amount != input.amount)

    // isSameParty accepts an output party that differs from the input party only by a proven key rotation.
    "The buyer is unmodified in the output" using (resolver.isSameParty(input.buyer, output.buyer))
    "The seller is unmodified in the output" using (resolver.isSameParty(input.seller, output.seller))

    // isRequiredSigner accepts the party's current key among the signers when the proof map links it to the stored key.
    "The proposer is a required signer" using (resolver.isRequiredSigner(cmd.signers, input.proposer))
    "The proposee is a required signer" using (resolver.isRequiredSigner(cmd.signers, input.proposee))
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
} else if (command.getValue() instanceof Commands.Modify) {
    requireThat(require -> {
        // ... structural checks unchanged ...
        ProposalState input = tx.inputsOfType(ProposalState.class).get(0);
        ProposalState output = tx.outputsOfType(ProposalState.class).get(0);

        // A resolver backed by the proof map in the command. With no proof map it falls back to plain equality,
        // so transactions without any rotation verify exactly as before.
        PartyIdentityResolver resolver = new PartyIdentityResolver(command.getKeyRotationProofChainMap());

        require.using("The amount is modified in the output", output.getAmount() != input.getAmount());

        // isSameParty accepts an output party that differs from the input party only by a proven key rotation.
        require.using("The buyer is unmodified in the output", resolver.isSameParty(input.getBuyer(), output.getBuyer()));
        require.using("The seller is unmodified in the output", resolver.isSameParty(input.getSeller(), output.getSeller()));

        // isRequiredSigner accepts the party's current key among the signers when the proof map links it to the stored key.
        require.using("The proposer is a required signer", resolver.isRequiredSigner(command.getSigners(), input.getProposer()));
        require.using("The proposee is a required signer", resolver.isRequiredSigner(command.getSigners(), input.getProposee()));
        return null;
    });
}
```
{{% /tab %}}
{{< /tabs >}}

The `Accept` branch of the contract and `AcceptanceFlow` receive the same treatment, and the responder's `checkTransaction` is the same as in pattern 1.

With this pattern, after node A rotates, the behaviour depends on who starts the first transaction. If A modifies the proposal, A knows its own rotation: the output names A's new key, the command carries A's proof chain, and no signature carries a proof. If B modifies it first, B has not yet seen A's proof: the output keeps A's old key, the command carries no proof map, and A proves the rotation in its signature. B learns the proof from that transaction and A's next modification moves the state to the new key. Either way, once the proposal names only current keys, every later modification and the acceptance carry no proof anywhere, and the trade is recorded against A's new key.

{{< note >}}

A forged proof does not help an attacker take over a party: `KeyRotationProofChain.isValid` returns `false` for a chain that is not signed by the original key, so the contract rejects the transaction with "The seller is unmodified in the output" (or the buyer equivalent) and the state stays with its rightful owner.

{{< /note >}}

#### Testing a CorDapp against a rotated key

Both adapted samples ship tests that rotate a node's key in the middle of a negotiation and check where the proof appears. They use the same test infrastructure as the Corda Enterprise key rotation tests, not the public `MockNetwork`, for two reasons: `MockNetwork` nodes run the Corda Open Source flows, which cannot produce a rotated signature, and only `InternalMockNetwork` can rotate a node's key.

{{< tabs name="key-rotation-test-network" >}}
{{% tab name="Kotlin" %}}
```kotlin
// Every node is an Enterprise node: createKeyRotationMockNode gives it the Enterprise CollectSignaturesFlow and FinalityFlow.
// Key rotation needs network minimum platform version 170.
network = InternalMockNetwork(
        notarySpecs = listOf(MockNetworkNotarySpec(CordaX500Name("Notary", "London", "GB"))),
        cordappsForAllNodes = setOf(
                TestCordapp.findCordapp("net.corda.samples.negotiation.flows") as TestCordappInternal,
                TestCordapp.findCordapp("net.corda.samples.negotiation.contracts") as TestCordappInternal
        ),
        initialNetworkParameters = NetworkParameters(170, emptyList(), 10485760, 10485760 * 50, Instant.now(), 1, emptyMap()),
        defaultFactory = ::createKeyRotationMockNode
)
a = network.createPartyNode(CordaX500Name("Node A", "London", "GB"))
b = network.createPartyNode(CordaX500Name("Node B", "New York", "US"))

// Rotates the node's legal identity key: a new key is generated, the old key signs the new one (the proof) and the
// node restarts on the new key. The returned node replaces the old one; re-register the responder flows on it.
a = network.rotateKey(a, null)
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
// Every node is an Enterprise node: createKeyRotationMockNode gives it the Enterprise CollectSignaturesFlow and FinalityFlow.
// Key rotation needs network minimum platform version 170.
NetworkParameters networkParameters = new NetworkParameters(170, Collections.emptyList(), 10485760, 10485760 * 50, Instant.now(), 1, Collections.emptyMap());
network = new InternalMockNetwork(
            Collections.emptyList(),
            new MockNetworkParameters(),
            false,
            false,
            new InMemoryMessagingNetwork.ServicePeerAllocationStrategy.Random(),
            ImmutableList.of(new MockNetworkNotarySpec(CordaX500Name.parse("O=Notary,L=London,C=GB"))),
            Paths.get("build", "mock-network", DriverDSLImplKt.getTimestampAsDirectoryName()),
            networkParameters,
            InternalMockNetwork.Companion::createKeyRotationMockNode,
            ImmutableList.of(
                (TestCordappInternal) TestCordapp.findCordapp("net.corda.samples.negotiation.flows"),
                (TestCordappInternal) TestCordapp.findCordapp("net.corda.samples.negotiation.contracts")
            ),
            true);
a = network.createPartyNode(new CordaX500Name("Node A", "London", "GB"));
b = network.createPartyNode(new CordaX500Name("Node B", "New York", "US"));

// Rotates the node's legal identity key: a new key is generated, the old key signs the new one (the proof) and the
// node restarts on the new key. The returned node replaces the old one; re-register the responder flows on it.
a = network.rotateKey(a, null);
```
{{% /tab %}}
{{< /tabs >}}

The tests then run the sample's flows and inspect the resulting `SignedTransaction`: `stx.tx.commands.single().keyRotationProofChainMap` for a proof in the command, and `signature.signatureMetadata.proofChain` on each entry of `stx.sigs` for a proof in a signature, checking the chain with `KeyRotationProofChain.isValid(originalKey, rotatedKey)`. `InternalMockNetwork`, `createKeyRotationMockNode` and `rotateKey` are in `corda-node-driver`. Because their signatures mention node-internal types, the test compile classpath also needs `corda-node`, `corda-node-api` and `corda-extensions-api` as `testCompileOnly` dependencies.

## References

* [Node cross-provider key rotation tool]({{< relref "../../ha-utilities.md#node-cross-provider-key-rotation-tool" >}}) in the HA Utilities reference, for the full command syntax and options.
* [negotiation-cordapp](https://github.com/corda/samples-java/tree/release/4.15/Advanced/negotiation-cordapp) (Java) and its [Kotlin version](https://github.com/corda/samples-kotlin/tree/release/4.15/Advanced/negotiation-cordapp): the original bilateral-agreement sample that does not survive a key rotation.
* [negotiation-cordapp-key-rotation-support](https://github.com/corda/samples-java/tree/release/4.15/Advanced/negotiation-cordapp-key-rotation-support) (Java) and its [Kotlin version](https://github.com/corda/samples-kotlin/tree/release/4.15/Advanced/negotiation-cordapp-key-rotation-support): pattern 1, proofs in the signature.
* [negotiation-cordapp-key-rotation-proof-free](https://github.com/corda/samples-java/tree/release/4.15/Advanced/negotiation-cordapp-key-rotation-proof-free) (Java) and its [Kotlin version](https://github.com/corda/samples-kotlin/tree/release/4.15/Advanced/negotiation-cordapp-key-rotation-proof-free): pattern 2, proofs in the command and proof-free transactions afterwards.
