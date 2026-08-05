---
date: '2026-07-29T14:00:00Z'
menu:
  corda-enterprise-4-15:
    identifier: corda-enterprise-4-15-corda-nodes-cross-provider-key-rotation
    name: "Cross-provider Key Rotation"
    parent: corda-enterprise-4-15-corda-nodes
tags:
- key rotation
- hsm
- node
title: Cross-provider key rotation
weight: 180
---

# Cross-provider key rotation

Cross-provider key rotation is available in Corda Enterprise 4.15 and later. It enables a node or notary to move its legal identity key to a different key provider, such as a different hardware security module (HSM), without losing access to existing Corda states and transactions.

{{< warning >}}

Key rotation is a system-critical operation. Plan and test the procedure carefully before using it in production. An unsuccessful rotation can prevent the affected node from accessing existing states.

{{< /warning >}}

## Compatibility and limitations

Nodes running Corda 4.15 continue to interoperate with earlier Corda versions in the same way as Corda 4.15. This includes interoperability between Corda Open Source and Corda Enterprise.

A Corda Open Source node cannot initiate a cross-provider key rotation. However, a Corda Open Source node running Corda 4.15 or later can verify transactions that contain a cross-provider key rotation proof. Consequently, a Corda Enterprise node can use cross-provider key rotation without affecting compatibility with Corda Open Source nodes.

## Platform requirements

Before performing a key rotation:

* All nodes on the network must run Corda 4.15 or later.
* The network minimum platform version must be at least `170`. For guidance, see [Network parameters]({{< relref "../../network/network-parameters.md" >}}).

Corda includes the following safeguards:

* The key rotation tool fails if the network minimum platform version is below `170`.
* A Corda 4.15 node fails to start if a key rotation file is present and the network minimum platform version is below `170`.
* A Corda 4.15 transaction builder throws an exception when a command includes a key rotation proof and the network minimum platform version is below `170`.

These safeguards do not cover every configuration or operational error. Verify all prerequisites before continuing.

## CorDapp considerations

Test existing CorDapps for compatibility before rotating a key. Flow logic may require changes when it involves states signed by the previous legal identity key. Following a key rotation, the `Party` and `PartyAndCertificate` objects for a rotated node identity are not equal to the original objects. Logic that compares a key or certificate directly, including comparisons with vault states, can therefore fail.

In most cases, the vault handles rotated identities transparently:

* Vault queries do not distinguish between states that belong to parties with the same X.500 name.
* The `Party` field is stored as an X.500 name and is therefore deserialised using the current identity. Storing a `PublicKey`, or its hash, instead of a `Party` can cause compatibility issues.

For example, a bilateral-agreement CorDapp that stores party details directly in a state must not compare those details directly with the value returned by `ourIdentity` after rotation, because the underlying public key has changed. If a CorDapp cannot be adapted, create dedicated flows to re-sign the affected states with the new keys.

### Resolving party identities

`IdentityService.wellKnownPartyFromX500Name`, `FlowSession.counterparty`, and `FlowLogic.getOurIdentity` return the node identity that is currently present in the `NetworkMapCache`. `IdentityService.trustRoot` and `IdentityService.trustAnchor` return the root certificate for the current node legal identity certificate chain.

When input and output states must contain the same parties, include the required proof in `Command.keyRotationProofChainMap`. This is particularly important for CorDapps that implement bilateral agreements.

When a party in an input state must match a party in an output state:

* Copy the party directly from the input state to the output state, or resolve it with `PartyIdentityResolver`.
* Do not retrieve parties directly from the Corda Identity or Key Management services. They return the current identity from the `NetworkMapCache`, which can differ from the identity used in the input state.
* Do not compare parties obtained from states with parties obtained directly from Identity or Key Management services. Obtain every party in a comparison from the same source.
* Where appropriate, use `PartyIdentityResolver.resolveToCurrentParty` to resolve a potentially outdated party in a state to its current identity in the `NetworkMapCache`.

Use `PartyIdentityResolver` only for parties or keys stored in a state, where the old identity should be replaced with the new identity when it becomes available. It must not be used to create counterparty identities. Once a party or key in a state has been updated to the new identity, do not revert it to the old identity.

### Signing and validation

When calling `signInitialTransaction(builder: TransactionBuilder, signingPubKeys: Iterable<PublicKey>)`, the supplied signing keys must be a subset of the keys required by the transaction command. Requesting a node to sign with a new key while the command requires the old key causes the transaction to fail.

If `signingPubKeys` contains both the old and new keys, Corda generates a separate signature for each key.

If a CorDapp performs its own transaction validation, it must validate the entire key rotation proof chain. A transaction is valid only when its transaction signature and every signature in its proof chain are valid. When a key has been rotated, validating only the transaction signature is insufficient.

Do not deploy mixed CorDapp versions where only some versions support key rotation.

## Transaction size and performance

After a key rotation, each key rotation proof adds approximately 128 bytes to a transaction.

For payment CorDapps, this overhead applies only while transactions consume states signed with the old key. Once all legacy states have been consumed, the transaction-size and performance impact returns to the previous baseline.

For CorDapps that implement bilateral agreements, the overhead can apply to all future transactions unless the CorDapp is updated so that key rotation proofs are no longer required. Assess this impact against the required throughput. See [Performance testing]({{< relref "../../performance-testing/introduction.md" >}}) for performance-testing guidance.

Transaction validation also validates the proof chain, adding cryptographic verification for each proof in the chain. Test the performance impact in an environment that reflects your production workload.

## Prerequisites

Before starting a cross-provider key rotation, complete the following steps:

1. Back up the node database and node directory. For a notary rotation, also back up the notary database.
2. Confirm that every node runs Corda 4.15 or later and that the network minimum platform version is `170`.
3. Confirm that the new key provider is configured, running, and accessible to the affected node or notary.
4. Confirm that the new provider generates the same type of keys as the existing provider.
5. Confirm that all deployed CorDapps are compatible with key rotation.
6. Make `corda-tools-ha-utilities.jar` version 4.15 or later available in the node or notary directory.
7. When using an HSM, place the vendor-supplied client-side JAR files in the `drivers` subdirectory of the configured base directory. The HA Utilities JAR does not include these files. See [HSM integration]({{< relref "../../operations/deployment/hsm-integration.md" >}}) for more information.
8. Enable key rotation in the Identity Manager service, as described in the next section.

### Enable key rotation in the Identity Manager service

Set `allowKeyRotation` to `true` in the `identity-manager-alias` workflow configuration. Add the property to the existing workflow configuration; do not replace the entire configuration block.

```hocon
workflows = {
  "identity-manager-alias" = {
    allowKeyRotation = true
  }
}
```

Disable this setting after the rotation has completed.

## HA Utilities command

The [HA Utilities]({{< relref "../../ha-utilities.md" >}}) command for cross-provider key rotation is:

```shell
ha-utilities node-cross-provider-key-rotation [-hvV] [--logging-level=<loggingLevel>] [-b=FOLDER] [--config-file=FILE] [--config-file-previous=FILE]...
```

The most relevant options are:

| Option | Description |
| --- | --- |
| `-b`, `--base-directory=FOLDER` | The working directory containing the node or notary files. |
| `-f`, `--config-file=FILE` | The current configuration file, which must reference the new key provider. The default is `node.conf`. |
| `-g`, `--config-file-previous=FILE` | The configuration file that references the previous key provider. The default is `node.conf.previous`. |
| `-n`, `--network-parameters=FILE` | The network parameters file. The default is `network-parameters`. |
| `-t`, `--network-root-truststore=FILE` | The network root truststore obtained from the network operator. |
| `-p`, `--network-root-truststore-password=PASSWORD` | The password for the network root truststore. |
| `--config-obfuscation-passphrase[=<cliPassphrase>]` | The passphrase used to generate an AES key for configuration obfuscation. |
| `--config-obfuscation-seed[=<cliSeed>]` | The seed used to create a salt for configuration obfuscation. |

Use `--help` to view the complete command reference for the installed version of HA Utilities.

## Rotate a node key

1. Verify that all [prerequisites](#prerequisites) are met.
2. Stop the node.
3. From the node directory, copy the existing configuration file, which points to the old key provider, to `node.conf.previous`.
4. Update `node.conf` so that it points to the new key provider.
5. Run the key rotation tool:

   ```shell
   java -jar corda-tools-ha-utilities.jar node-cross-provider-key-rotation --config-file-previous node.conf.previous
   ```

6. The tool creates `output/certificates`, which contains Java KeyStore (JKS) files with the new certificates and a `key-rotation-proofs.bin` file. The proof file allows the node to consume states signed with the old key.
7. Copy every file from `output/certificates` to the node's `certificates` directory.
8. Start the node. At startup, the node loads the proofs from `key-rotation-proofs.bin` and deletes the file after processing it.
9. Confirm that the node starts successfully, then disable `allowKeyRotation` in the Identity Manager service.

{{< warning >}}

After the rotation files have been copied, the old certificates are unavailable unless you have retained a backup of the previous JKS files. If the rotation fails, restore the affected data from a verified backup. Returning to the previous HSM by reusing the old key is not supported; perform a new key rotation instead.

{{< /warning >}}

## Rotate a notary key

The notary procedure includes a network parameters update because the notary node information changes.

1. Verify that all [prerequisites](#prerequisites) are met.
2. Stop the notary and then stop all nodes on the network.
3. From the notary directory, copy the existing `notary.conf`, which points to the old key provider, to `notary.conf.previous`.
4. Update `notary.conf` so that it points to the new key provider.
5. Run the key rotation tool:

   ```shell
   java -jar corda-tools-ha-utilities.jar node-cross-provider-key-rotation --config-file notary.conf --config-file-previous notary.conf.previous
   ```

6. Copy every file from `output/certificates` to the notary's `certificates` directory.
7. Delete the existing `nodeInfo-*` file from the notary directory and generate a new node information file:

   ```shell
   java -jar corda.jar generate-node-info --config-file=notary.conf
   ```

8. Update the network parameters with the new notary node information file. Follow [Updating the network parameters]({{< relref "../../operations/deployment/updating-network-parameters.md" >}}) to submit, advertise, sign, and execute the update.
9. Ensure that every node accepts the network parameters update before its deadline. Then execute the flag day and follow the guidance in [Handling flag days]({{< relref "../../notary/handling-flag-days.md" >}}).
10. Restart the notary and the remaining nodes as required by the network parameters update. Confirm that they start successfully, then disable `allowKeyRotation` in the Identity Manager service.

## Further CorDapp upgrade guidance

CorDapps that model bilateral agreements typically require updates to support cross-provider key rotation. Review the [negotiation CorDapp `ModificationFlow` example](https://github.com/corda/samples-java/blob/release/4.12/Advanced/negotiation-cordapp/workflows/src/main/java/net/corda/samples/negotiation/flows/ModificationFlow.java) when adapting flow logic.
