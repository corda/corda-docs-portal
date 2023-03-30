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

## Fixed issues

This release includes the following fixes:


### Database schema changes

The following database changes have been applied between 4.10 and 4.11:

Two Phase Finality introduces additional data fields within the main `DbTransaction` table:

```bash
  @Column(name = "signatures")
  val signatures: ByteArray?,

  /**
   * Flow finality metadata used for recovery
   * TODO: create association table solely for Flow metadata and recovery purposes.
   * See https://r3-cev.atlassian.net/browse/ENT-9521
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

