---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Uniqueness Checker"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-uniqueness-checker
    weight: 8000
section_menu: corda5
---

# Uniqueness Checker

The uniqueness checker and backing store metrics are from the perspective of uniqueness processing, which runs independently of the flow processing.

The uniqueness checker handles the business logic of uniqueness checking.
The implementation is batched at two levels and three categories of metrics are provided:

* Metrics starting with `uniqueness_checker_batch` relate to “top level” metrics, which apply to a single batch
  processed by the uniqueness checker. As a batch may contain requests from different notary services and/or virtual nodes,
  these metrics provide no context as to the identities of the batch being processed.

* Metrics starting with `uniqueness_checker_subbatch` relate to “sub-batch level” metrics. Each sub-batch represents
  a partition for each notary virtual node identity within a batch. The virtual node identity is captured via the existing `virtualnode.source` tag.

* Metrics starting with `uniqueness_checker_request` relate to metrics applicable to specific requests within a sub-batch,
  such as the result of a request. Like the sub-batch metrics, these are also associated with the `virtualnode.source` tag.

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
| `corda_uniqueness_checker_batch_execution_time_seconds` | Timer | None | The overall time for the uniqueness checker to process a batch, inclusive of all sub-batches. |
| `corda_uniqueness_checker_batch_size` | DistributionSummary | None | The number of requests in a batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_subbatch_execution_time_seconds` | Timer | <ul><li>`virtualnode_source`</li></ul> | The time for the uniqueness checker to process a sub-batch, that is, a partition of a batch segregated by notary virtual node holding identity. |
| `corda_uniqueness_checker_subbatch_size` | DistributionSummary | <ul><li>`virtualnode_source`</li></ul> | The number of requests in a sub-batch processed by the uniqueness checker. |
| `corda_uniqueness_checker_request_count` | Counter | <ul><li>`virtualnode_source`</li><li>`result_type`</li><li>`duplicate`</li></ul> | A count of the number of requests processed. On its own this simply duplicates information that is already captured at the batch and sub-batch levels, but the tags can be used to provide additional context not available in the other metrics. |

Tags:
* `virtualnode_source`: The virtual node identity.
* `result_type`: It can be used to understand the number of successful vs failed requests, and the type of failures.
* `duplicate`: This tag is set to `true` if the uniqueness checker has seen a request for this transaction before, and is therefore simply returning the original result. Otherwise, it is `false`.
