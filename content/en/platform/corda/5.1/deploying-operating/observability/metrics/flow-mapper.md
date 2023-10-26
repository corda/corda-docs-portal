---
date: '2023-10-26'
version: 'Corda 5.1'
title: "Task Manager"
menu:
  corda51:
    parent: corda51-cluster-metrics
    identifier: corda51-cluster-task-manager
    weight: 500
section_menu: corda51
---

# Task Manager

The task manager exposes metrics for underlying thread pools and jobs processing duration and count.

Jobs processing duration and count.

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

| Metric                                                    | Type    | Tags                                                      | Description                                                          |
| :-------------------------------------------------------- | :------ | :-------------------------------------------------------- | :------------------------------------------------------------------- |
| `corda_taskmanager_executor_active_threads`               | Gauge   | `name`                                                    | The approximate number of threads that are actively executing tasks. |
| `corda_taskmanager_executor_completed_tasks_total`        | Counter | `name`                                                    | The approximate number of tasks that have completed execution.       |
| `corda_taskmanager_executor_idle_seconds_count`           | Counter | `name`                                                    | The number of events that have been observed for the base metric (). |
| `corda_taskmanager_executor_idle_seconds_max`             | Gauge   | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_idle_seconds_sum`             | Counter | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_pool_core_threads`            | Gauge   | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_pool_max_threads`             | Gauge   | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_pool_size_threads`            | Gauge   | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_queue_remaining_tasks`        | Gauge   | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_queued_tasks`                 | Gauge   | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_scheduled_once_total`         | Counter | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_scheduled_repetitively_total` | Counter | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_seconds_count`                | Counter | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_seconds_max`                  | Gauge   | `name`                                                    |                                                                      |
| `corda_taskmanager_executor_seconds_sum`                  | Counter | `name`                                                    |                                                                      |
| `TaskCompletionTime`                                      |         | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> |                                                                      |
| `LiveTasks `                                              |         | `name`                                                    | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul>            |

Tags:
* `name`: The name of the task manager.
* `task.manager.name`: The name of the task manager.
* `task.type`: The task type (`SHORT_RUNNING`, `LONG_RUNNING`, or `SCHEDULED`).
