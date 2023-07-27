---
title: Corda Enterprise Edition 4.11 release notes
date: '2023-03-30'

menu:
  corda-enterprise-4-11:
    identifier: corda-enterprise-4-11-release-notes
    parent: about-corda-landing-4-11-enterprise
    name: "Release notes"
tags:
- release
- notes
- enterprise

weight: 10
---

# Corda Enterprise Edition 4.11 release notes

Corda Enterprise Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.11 uses platform version 13.

For more information about platform versions, see [Versioning](cordapps/versioning.md).

## New features and enhancements

### Two Phase Finality
New Two Phase Finality protocol (`FinalityFlow` / `ReceiveFinalityFlow` sub-flows) to improve resiliency and
recoverability of CorDapps using finality. Existing CorDapps will not require any changes to take advantage of this
new improved protocol.

See [Two Phase Finality](two-phase-finality.md)

### Improved Double Spend exception handling
Two Phase Finality will automatically delete an un-notarised transaction from the DBTransaction table when a Double Spend
is detected upon attempting notarisation by the Initiator of `FinalityFlow`.

Furthermore, if the new optional `ReceiveFinalityFlow` `handlePropagatedNotaryError` constructor parameter is set to `true` (default: `false`),
then the Double Spend error (NotaryError.Conflict) will propagate back to the 2PF initiator allowing it to automatically remove the
associated un-notarised transaction from its DBTransaction table.
If a CorDapp is compiled against 4.11 (e.g. its TPV = 13) then Double Spend handling is enabled by default.

### Finality Recovery Tooling
- RPC extension operations (additions to the FlowRPCOps interface) which allow for Finality Flow recovery at both
  Initiator and Receiver(s)
- Node Shell commands to allow operations teams to perform Finality Flow recovery.

See [Finality Flow Recovery](finality-flow-recovery.md)

### Ledger Recovery
A new ledger recovery flow (`LedgerRecoveryFlow`) enables a node to identify and recover transactions from
peer recovery nodes to which it was a party (initiator, receiver) and which are missing from its own ledger.

See [Ledger Recovery Flow](ledger-recovery-flow.md)

### Confidential Identity key-pair generator
Introduction of a new service that pre-generates Confidential Identity keys to be used when using CI's in transactions.
This pre-generated CI's are subsequently used for backup recovery purposes.

### Ledger Recovery and CI Pre-generation configuration
Additional network map and associated node configuration parameters:
```
recoveryMaximumBackupInterval: Duration? = null
confidentialIdentityMinimumBackupInterval: Duration? = null
```

## Fixed issues

This release includes the following fixes:

### Database schema changes

The following database changes have been applied between 4.10 and 4.11:

```bash
   @Entity
    @Table(name = "${NODE_DATABASE_PREFIX}our_key_pairs")
    class PersistentKey(
            @Suppress("Unused")
            @Id
            @Column(name = "public_key_hash", length = MAX_HASH_HEX_SIZE, nullable = false)
            var publicKeyHash: String,
            @Lob
            @Column(name = "public_key", nullable = false)
            var publicKey: ByteArray = EMPTY_BYTE_ARRAY,
            @Lob
            @Column(name = "private_key", nullable = true)
            var privateKey: ByteArray? = EMPTY_BYTE_ARRAY,
            @Lob
            @Column(name = "private_key_material_wrapped", nullable = true)
            var privateWrappedKey: ByteArray?,
            @Column(name = "scheme_code_name", nullable = true)
            var schemeCodeName: String?,

            // Version of the encoding scheme for the wrapped key material
            @Column(name = "version", nullable = true)
            var version: Int? = null
            var version: Int? = null,

            @Enumerated(EnumType.ORDINAL)
            @Column(name = "key_type", nullable = false)
            var keyType: KeyType = CI,

            @Column(name = "crypto_config_hash", length = MAX_HASH_HEX_SIZE, nullable = true)
            var cryptoConfigHash: String? = null,

            @Enumerated(EnumType.ORDINAL)
            @Column(name = "status", nullable = false)
            var status: Status = CREATED,

            @Column(name = "generate_tm", nullable = false)
            var insertionDate: Instant = Instant.now()
    )
```

See node migration scripts:
- `node-core.changelog-v25.xml`: added pre-generated CI key pairs table.

### Third party component upgrades
