---
date: '2023-05-18'
version: 'Corda 5.0'
title: "Code Signing"
menu:
  corda5:
    parent: corda5-develop-packaging
    identifier: corda5-develop-packaging-code-signing
    weight: 3000
section_menu: corda5
---

# Code Signing

CorDapps are packaged as {{< tooltip >}}CPKs{{< /tooltip >}}, {{< tooltip >}}CPBs{{< /tooltip >}}, and {{< tooltip >}}CPIs{{< /tooltip >}}. Each of these packages must be signed with a Code Signing certificate.
The signatures are then verified when a CPI is installed. They are verified against the certificates uploaded to Corda using the REST API.

CPK signatures are also verified during [backchain verification]({{< relref "../../ledger/transactions/_index.md" >}}), which is why you must carefully consider which certificates to sign with and which certificates to upload to the cluster to establish trust.

CPK and CPB packages can be signed using the Corda Gradle plugin or the Corda CLI, while CPI packages can only be signed with the Corda CLI.
You can also “re-sign” a package; that is, replace the old signature with a new one.
This is useful in case you need to replace a pre-production signature that was used for testing
with a signature based on a production certificate.
