---
description: Learn about the ledger repair functionality.
date: '2024-02-27'
title: "Ledger Repair"
menu:
  corda52:
    identifier: corda52-develop-ledger-repair
    parent: corda52-fundamentals-ledger
    weight: 6000
---

# Ledger Repair

The Corda ledger repair functionality resolves scenarios where, due to some unexpected error, a notary notarizes a transaction but the members involved in finalizing the transaction do not store the notarized transaction. Such a scenario may result in the members repeatedly attempting to spend consumed states and their flows constantly failing with notarization failures.

The ledger repair functionality checks each member’s vault for transactions that might have been notarized, sends any such transactions to the notary to check whether they were previously seen, and updates the member’s vault if the transactions were notarized.

By default, Corda runs the ledger repair process every ten minutes for all virtual node's transactions from five days in the past to ten minutes in the past, for no more than ten minutes. For more information about changing these default values, see the [deployment]({{< relref "../../deploying-operating/deployment/deploying/_index.md#ledger-repair" >}}) and [configuration fields]({{< relref "../../deploying-operating/config/fields/ledger-utxo.md" >}}) sections.

To manually run the repair process for a particular node, start the `com.r3.corda.notary.plugin.common.repair.NotarizedTransactionRepairFlow` flow, setting the following properties:

* `from` — the time in epoc milliseconds from which the repair functionality processes transactions. This value must be less than `until`.
* `until` — the time in epoc milliseconds until which the repair functionality processes transactions. This value must be greater than `from`.
* `duration` — the maximum time in seconds that the repair process runs for.

For example:

```kotlin
{
    "clientRequestId": "<request id>",
    "flowClassName": "com.r3.corda.notary.plugin.common.repair.NotarizedTransactionRepairFlow",
    "requestBody": {
        "from": <epoc milliseconds>,
        "until": <epoc milliseconds>,
        "duration": <seconds>,
    }
}
```
