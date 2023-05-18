---
date: '2023-05-18'
title: "Code Signing"
menu:
  corda5:
    parent: corda5-develop-packaging
    identifier: corda5-develop-packaging-code-signing
    weight: 3000
section_menu: corda5
---

CorDapps are packaged as CPKs, CPBs, and CPIs. Each of these packages must be signed with a Code Sign certificate.
The signatures of these packages are then verified when a CPI is installed. They are verified against the certificates
that are uploaded to the Corda REST API Docs API.

CPK signatures are also verified during backchain verification [insert link to ledger section for verification],
which is why you must carefully consider which certificates to sign with and which certificates to upload to the cluster to establish trust.

CPK and CPB packages can be signed using the Corda Gradle plugin or the Corda CLI, and CPI packages can be signed with the  Corda CLI only.
You can also “re-sign” a package, that is, to take the old signature away and replace it with a new signature.
This is useful in case, for example, you need to replace a pre-production signature that was used for testing,
with a signature based on a production certificate.
