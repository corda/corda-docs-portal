---
date: '2023-02-21'
title: "Corda 5.0 Beta 3.0 Release Notes"
menu:
  corda-5-beta:
    parent: corda-5-beta-release-notes
    identifier: corda-5-beta-release-notes-3.0
    weight: 900
section_menu: corda-5-beta
--- 

## New Features and Enhancements


<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Domain                     | Specific Change                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cluster Administration** | **Kubernetes Ingress** — The Corda REST worker now supports Kubernetes Ingress. This provides the REST worker with HTTP load balancing and enables optional annotations for additional integration.                                                                                                                                                                                                                                                                                                                                                      |
| **CorDapp Development**    | **Corda Gradle plugins** — The latest Corda Gradle plugins for Corda 5 is version 7.0.3.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Network Operation**      | **Signed Notary Server CPB** — The notary server CPB is now signed. For information about building and uploading a CPI using the test key used in this beta release, see [Notary Server CPB]({{< relref "../developing/notaries/plugin-cordapps-notary.md#notary-server-cpb" >}}). <br><br> **Notary Uniqueness Metrics** —  Metrics have been added to provide an insight into the uniqueness checking functionality. For a full list of available metrics see [Notary Uniqueness Metrics]({{< relref "../operating/notary-uniqueness-metrics.md" >}}). |

## Resolved Issues

| Domain                  | Specific Change                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CorDapp Development** | **createTransactionBuilder** — The `getTransactionBuilder()` function in `utxoLedgerService` mapped to a `transactionBuilder` property in Kotlin. As of this release, this function has been renamed `createTransactionBuilder`. Any existing CorDapps that use the ledger must be updated. <br><br>**Identifying Notaries** — The `Party` class was only used to identify notaries, but its existence suggested an identity model that does not exist in Corda 5.0. Therefore, this class has been removed to clear API space for a proper identity model in a later version. Notaries are identified by `MemberX500Name` and `PublicKey`. |

## Known Limitations and Issues

During the Beta process, R3 do not guarantee the stability of our user APIs. As a result, seemless upgrade between Beta versions is not supported.
