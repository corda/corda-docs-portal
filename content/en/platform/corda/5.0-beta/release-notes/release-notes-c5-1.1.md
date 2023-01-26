---
date: '2023-01-26'
title: "Corda 5.0 Beta 1.1 Release Notes"
menu:
  corda-5-beta:
    parent: corda-5-beta-release-notes
    identifier: corda-5-beta-release-notes-1.1
    weight: 1000
section_menu: corda-5-beta
---

Corda 5.0 Beta is a pre-release version for testing purposes only.
{{< note >}}
If you are not part of the current beta program, the Corda 5.0 Beta documentation is for information only.
Please contact R3 if you are interested in joining the Beta program.
{{< /note >}}

## Enhancements

This section describes the new features in Corda 5.0 Beta 1.1.

### CSDE 

#### Beta 1.1 API

The [CorDapp Standard Development Environment (CSDE)](cordapp-standard-development-environment/csde.html) has been upgraded to use the Corda 5.0 Beta 1.1 API. 

#### Example UTXO Ledger CorDapp

The CSDE now includes an [example  UTXO (unspent transaction output) ledger CorDapp](....). This simple chat application  is available in both the [CSDE-cordapp-template-kotlin](https://github.com/corda/CSDE-cordapp-template-kotlin) and [CSDE-cordapp-template-java](https://github.com/corda/CSDE-cordapp-template-java) repositories.

#### Gradle Helpers

The CSDE gradle helpers have been renamed and grouped into new directories to improve usability.

## Resolved Issues

This section describes the issues resolved in Corda 5.0 Beta 1.1.

### UTXO Ledger


#### Transaction Failures
Input states to a UTXO transaction were marked as consumed when the transaction was first persisted, before it was completely signed and notarised. If counter-signing or notarisation failed, states were incorrectly marked as consumed in the initiating's node vault and were no longer available as inputs.

## Known Limitations and Issues

* Corda 4 CorDapps will not run on Corda 5; it is a different set of incompatible APIs.
* Upgrade from Corda 4 to Corda 5 is not supported; a future version will provide migration guidance and tooling.
* There is no support for the Corda 4 Accounts SDK.
* There is no support for the Corda 4 Tokens SDK.
* There is no support for upgrades from the early access beta versions.

 

#### State Relevancy Flag???????????
Context: When building a transaction, newly created states (outputs) MUST be marked as relevant once the transaction is finalized.

Issue: The State relevancy flag can be inconsistently set due to a difference in the way transactions are finalized between `UtxoReceivedFinalityFlow` and `UtxoFinalityFlow`.
`UtxoReceivedFinalityFlow` on the counterparty side correctly persists State relevancy when the transaction is verified. `UtxoFinalityFlow` on the initiating side incorrectly persists State relevancy when the transaction is still unverified.

Impact: For the initiating participant on a transaction, a Relevant State could be flagged as available when the State should still be flagged as unavailable.
This also has a knock-on effect on the feed into the token selection mechanism.