---
description: Learn about the R3 notary protocols.
date: '2024-02-27'
title: "Notary Protocols"
menu:
  corda52:
    identifier: corda52-develop-notary-protocols
    parent: corda52-develop-notaries
    weight: 1000
---
# Notary Protocols

Notary functionality is provided in the form of plugin CorDapps. A notary protocol requires two {{< tooltip >}}CPBs{{< /tooltip >}}:

* A **client**, or **application** CPB, which is used to generate a {{< tooltip >}}CPI{{< /tooltip >}} associated with application virtual nodes. At a minimum, this contains a {{< tooltip >}}CPK{{< /tooltip >}} that has an initiating {{< tooltip >}}flow{{< /tooltip >}} that is automatically invoked by the Corda 5 flow framework to initiate a notarization request.
* A **notary server** CPB, which is used to generate a CPI associated with notary virtual nodes. At a minimum, this contains a CPK that has a responder flow to what is packaged in the client CPB.

Two notary protocols are currently available:

* [Non-validating notary protocol]({{< relref "non-validating-notary/_index.md" >}}) - each virtual node checks the whole chain of transactions back to issuance.
* [Contract-verifying notary protocol]({{< relref "../enhanced-ledger-privacy.md" >}}) - the notary checks the contracts applicable to transactions.

To help you select a protocol, see the [Considerations section]({{< relref "../enhanced-ledger-privacy.md#considerations" >}})  of the [Transaction Privacy Enhancements page]({{< relref "../enhanced-ledger-privacy.md" >}}) page.
