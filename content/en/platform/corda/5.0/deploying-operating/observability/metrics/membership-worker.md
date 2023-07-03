---
date: '2023-06-14'
version: 'Corda 5.0 Beta 4'
title: "Membership Worker"
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    parent: corda5-cluster-metrics
    identifier: corda5-cluster-membership-worker
    weight: 11000
section_menu: corda5
---

# Membership Worker

The membership worker is responsible for the processing of application network functionality either on behalf of an MGM,
a network member, or both. For an MGM, examples of this application functionality include:
* handling incoming registration requests
* network management
* ensuring the network participants are all in sync with the latest network data

For a network member, examples include:
* registering with an MGM to join a network
* managing network data sent from the MGM
* periodically syncing network data with the MGM

The timer metrics of the membership worker focus on the areas mentioned above. Specifically, the timer metrics cover:
* each stage of registration on both the MGM and membership side
* general membership actions (which at the moment only include the distribution of network data by the MGM)
* synchronisation of network data handling on both the MGM and member sides

These metrics are tagged with the name of the handler so that you can observe at a low-level exactly where time is spent
across different processes. These handler names are tagged as the operation name. They are also tagged with the short
hash ID and the group ID of the virtual node the operation is performed on behalf of in order to determine if certain
virtual nodes or groups are taking longer than others to process.

The membership worker also includes a single gauge metric which shows the size of the network member list held in memory
at any point. It is useful to compare any changes in the performance returned by the timer metrics to the size of the
member list at the time to see if timings could be impacted by a growing network. The gauge metrics are also tagged by
virtual node short hash and group ID so that it is possible to see the overall size of the member lists held in memory
but also view it per application network.

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
| `corda_membership_actions_handler_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | The time spent on membership actions. |
| `corda_membership_registration_handler_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | Registration is broken down into a series of stages, each with its own handler. This metric measures the time taken to execute each stage.  |
| `corda_membership_sync_handler_time_seconds` | Timer | <ul><li>`operation_name`</li><li>`group`</li><li>`virtualnode`</li></ul> | Measures how long it takes for each stage of synchronisation to complete. Synchronisation is split between different handler stages. It is processed on the MGM side and the network data package in constructed, and on the member side it is validated and persisted.  |
| `membership_memberlist_cache_size` | Gauge | <ul><li>`group`</li><li>`virtualnode`</li></ul> | Gauge of the member list cache size to monitor how the cache size grows or shrinks. |

Tags:
* `operation_name`: The name of the operation that the metric is related to. For example, `DistributeMemberInfo`,
`StartRegistration`, `QueryMemberInfo`, and so on.
* `group`: The membership group ID of the virtual node performing an operation or being monitored. It can also
appear as `not_applicable` when a membership group identifier is not accessible when the metric was collected.
* `virtualnode`: The virtual node short hash of the virtual node performing an operation or being monitored.
This can also appear as `not_applicable` when a virtual node identifier was not accessible when the metric was collected.
