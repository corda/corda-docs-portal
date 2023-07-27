---
title: Corda Community Edition 4.11 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2023-03-30'
menu:
  corda-community-4-11:
    identifier: corda-community-4-11-release-notes
    parent: about-corda-landing-4-11-community
    weight: 10
    name: "Release notes"
tags:
- release
- community
- notes

---

# Corda Community Edition 4.11 release notes

Corda Community Edition 4.11 includes several new features, enhancements, and fixes.

## Platform version change

Corda 4.11 uses platform version 13.

For more information about platform versions, see [Versioning](versioning.md).

## New features and enhancements

### Two Phase Finality
New Two Phase Finality protocol (`FinalityFlow` / `ReceiveFinalityFlow` sub-flows) to improve resiliency and
recoverability of CorDapps using finality. Existing CorDapps will not require any changes to take advantage of this
new improved protocol.

See [Two Phase Finality](two-phase-finality.md)

### Extended SendTransactionFlow
`SendTransactionFlow` has been extended to allow for sending to multiple sessions.
The caller of `SendTransactionFlow` can indicate the type of sessions to send to using the following new constructor arguments:
```
participantSessions: Set<FlowSessions>
observerSessions: Set<FlowSession>
```
These parameters are also used to infer and construct the type of recovery metadata to store on the sender side.
- participant sessions default to using a `StatesToRecord` value of ONLY_RELEVANT
- participant sessions default to using a `StatesToRecord` value of ALL_VISIBLE

### Introduction of an Encryption Service
An AES-key implementation is used to encrypt and decrypt distribution record recovery metadata for sharing and persistence amongst peers.

## Fixed issues

This release includes the following fixes:


### Database schema changes

The following database changes have been applied between 4.10 and 4.11:

Two Phase Finality introduces two new database tables for storage of recovery metadata distribution records:

```bash
    @Entity
    @Table(name = "${NODE_DATABASE_PREFIX}sender_distribution_records")
    data class DBSenderDistributionRecord(
            @EmbeddedId
            var compositeKey: PersistentKey,

            @Column(name = "tx_id", length = 144, nullable = false)
            var txId: String,

            /** PartyId of flow peer **/
            @Column(name = "receiver_party_id", nullable = false)
            val receiverPartyId: Long,

            /** states to record: NONE, ALL_VISIBLE, ONLY_RELEVANT */
            @Column(name = "states_to_record", nullable = false)
            var statesToRecord: StatesToRecord

    )

    @Entity
    @Table(name = "${NODE_DATABASE_PREFIX}receiver_distribution_records")
    data class DBReceiverDistributionRecord(
            @EmbeddedId
            var compositeKey: PersistentKey,

            @Column(name = "tx_id", length = 144, nullable = false)
            var txId: String,

            /** PartyId of flow initiator **/
            @Column(name = "sender_party_id", nullable = true)
            val senderPartyId: Long,

            /** Encrypted recovery information for sole use by Sender. See [HashedDistributionList] **/
            @Lob
            @Column(name = "distribution_list", nullable = false)
            val distributionList: ByteArray
   )
  ```

The above tables use the same persistent composite key type:

```bash
    @Embeddable
    @Immutable
    data class PersistentKey(
            @Column(name = "sequence_number", nullable = false)
            var sequenceNumber: Long,

            @Column(name = "timestamp", nullable = false)
            var timestamp: Instant,

            @Column(name = "timestamp_discriminator", nullable = false)
            var timestampDiscriminator: Int

    )
```

There are two further tables to hold distribution list privacy information (including encryption keys):

```bash
    @Entity
    @Table(name = "${NODE_DATABASE_PREFIX}recovery_party_info")
    data class DBRecoveryPartyInfo(
            @Id
            /** CordaX500Name hashCode() **/
            @Column(name = "party_id", nullable = false)
            var partyId: Long,

            /** CordaX500Name of party **/
            @Column(name = "party_name", nullable = false)
            val partyName: String
    )

    @Entity
    @Table(name = "${NODE_DATABASE_PREFIX}aes_encryption_keys")
    class EncryptionKeyRecord(
            @Id
            @Type(type = "uuid-char")
            @Column(name = "key_id", nullable = false)
            val keyId: UUID,

            @Column(name = "key_material", nullable = false)
            val keyMaterial: ByteArray
    )
```

See node migration scripts:
- `node-core.changelog-v25.xml`: added Sender and Receiver recovery distribution record tables, plus PartyInfo table.
- `node-core.changelog-v26.xml`: added AES encryption keys table.

### Third party component upgrades

