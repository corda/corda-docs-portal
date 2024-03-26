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

By default, Corda runs the ledger repair process every ten minutes for transactions from five days in the past to ten minutes in the past, for no more than ten minutes. For more information about changing these default values, see the [configuration fields]({{< relref ".././../deploying-operating/config/fields/ledger-utxo.md" >}}) section.

To manually run the repair process, start the `com.r3.corda.notary.plugin.common.repair.NotarizedTransactionRepairFlow` flow, setting the following properties:

* `from` — the number of milliseconds in the past that the repair functionality processes transactions from. This value must be greater than `until`.
* `until` — the number of milliseconds in the past that the repair functionality processes transactions until. This value must be less than `from`.
* `duration` — the maximum time in seconds that the repair process runs for.

For example:

```
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
