---
description: "Review the metrics generated for the ledger uniqueness checker. These metrics are from the perspective of the notarization flow running on a notary virtual node."
date: '2023-06-14'
title: "Ledger Uniqueness Checker Client Service"
menu:
  corda52:
    parent: corda52-cluster-metrics
    identifier: corda52-cluster-ledger-uniqueness
    weight: 1000
---

# Ledger Uniqueness Checker Client Service

The ledger uniqueness checker client service metrics are from the perspective of the notarization {{< tooltip >}}flow{{< /tooltip >}} running on a {{< tooltip >}}notary{{< /tooltip >}} {{< tooltip >}}virtual node{{< /tooltip >}}.

<style>
table th:first-of-type {
    width: 25%;
}
table th:nth-of-type(2) {
    width: 10%;
}
table th:nth-of-type(3) {
    width: 20%;
}
table th:nth-of-type(4) {
    width: 45%;
}
</style>

| Metric | Type | Tags | Description |
| :----------- | :----------- | :----------- | :----------- |
| `corda_ledger_uniqueness_client_run_time_seconds` | Timer | <ul><li>`result_type`</li></ul> | The time taken from requesting a uniqueness check to a response being received. |

Tags:

* `result_type`: This tag is set to the specific type of uniqueness check result that was returned.
