---
title: Corda Community Edition 4.11 release notes
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2023-05-08'
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

For more information about platform versions, see [Versioning]({{< relref "versioning.md" >}}).

## New features and enhancements

### Two Phase Finality

Two Phase Finality protocol (`FinalityFlow` and `ReceiveFinalityFlow` sub-flows) has been added to improve resiliency and recoverability of CorDapps using finality. Existing CorDapps do not require any changes to take advantage of this new improved protocol.

See [Two Phase Finality]({{< relref "two-phase-finality.md" >}}).

### Upgraded dependencies 

The following dependencies have been upgraded to address critical and high-severity security vulnerabilities:
* H2 has been upgraded from 1.4.197 to 2.1.214.
* Hibernate has been upgraded from 5.4.32.Final to 5.6.14.Final.
* Liquibase has been upgraded from 3.6.3 to 4.20.0.

### Consuming transaction IDs added to `vault_state` table 

When a state is consumed by a transaction, Corda now adds the ID of the consuming transaction in the `consuming_tx_id` column of the `vault_state` table. Corda only updates this database column for new transactions; for existing consumed states already in the ledger, the value of `consuming_tx_id` is null.

### Deserializing AMQP data performance improvement

This release includes improvements in the performance of deserializing AMQP data, which may result in performance improvements for LedgerGraph, Archiving and other CorDapps.

## Fixed issues

This release includes the following fixes:

* When a notary worker is shut down, message ID cleanup is now performed as the last shutdown activity, rather than the first; this prevents a situation where the notary worker might still appear to be part of the notary cluster and receiving client traffic while shutting down.

* Flow checkpoint dumps now include a `status` field which shows the status of the flow; in particular, whether it is hospitalized or not.

* Debug logging of the Artemis server has been added.

* A new property, `previousPageAnchor`, has been added to `Vault.Page`. It is used to detect if the vault has changed while pages of a vault query have been loaded. If such a scenario is important to detect, then the property can be used to restart querying.

  An example of how to use this property can be found in [Vault Queries]({{< relref "api-vault-query.md#query-for-all-states-using-a-pagination-specification-and-iterate-using-the-totalstatesavailable-field-until-no-further-pages-available-1" >}}).
  
* A `StackOverflowException` was thrown when an attempt was made to store a deleted party in the vault. This issue has been resolved.

* The certificate revocation checking has been improved with the introduction of a read timeout on the download of the certificate revocation lists (CRLs). The default CRL connect timeout has also been adjusted to better suit Corda nodes. The caching of CRLs has been increased from 30 seconds to 5 minutes.

### Database schema changes

The following database changes have been applied:

Two Phase Finality introduces additional data fields within the main `DbTransaction` table:

```kotlin
  @Column(name = "signatures")
  val signatures: ByteArray?,

  /**
   * Flow finality metadata used for recovery
   */

  /** X500Name of flow initiator **/
  @Column(name = "initiator")
  val initiator: String? = null,

  /** X500Name of flow participant parties **/
  @Column(name = "participants")
  @Convert(converter = StringListConverter::class)
  val participants: List<String>? = null,

  /** states to record: NONE, ALL_VISIBLE, ONLY_RELEVANT */
  @Column(name = "states_to_record")
  val statesToRecord: StatesToRecord? = null
```
See node migration scripts:
- `node-core.changelog-v24.xml`: added transaction signatures.
- `node-core.changelog-v24.xml`: added finality flow recovery metadata.

### Third party component upgrades

The following table lists the dependency version changes between 4.9.5 and 4.10 Community Editions:

| Dependency           | Name           | Version 4.9.5 Community | Version 4.10 Community |
|----------------------|----------------|-------------------------|------------------------|
| com.squareup.okhttp3 | OKHttp         | 3.14.2                  | 3.14.9                 |
| org.bouncycastle	   | Bouncy Castle  | 1.68                    | 1.70                   |
| io.opentelemetry	   | Open Telemetry | -                       | 1.20.1                 |

## Log4j patches
Click [here]({{< relref "./log4j-patches.md" >}}) to find all patches addressing the December 2021 Log4j vulnerability.