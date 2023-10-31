---
date: '2023-10-26'
version: 'Corda 5.1'
title: "Task Manager"
menu:
  corda51:
    parent: corda51-cluster-metrics
    identifier: corda51-cluster-task-manager
    weight: 1450
section_menu: corda51
---

# Task Manager

The task manager exposes metrics for underlying thread pools and jobs processing duration and count.

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

| Metric                                                    | Type    | Tags                                                      | Description                                                                            |
| :-------------------------------------------------------- | :------ | :-------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| `corda_taskmanager_executor_active_threads`               | Gauge   | `name`                                                    | The approximate number of threads that are actively executing tasks.                   |
| `corda_taskmanager_executor_completed_tasks_total`        | Counter | `name`                                                    | The approximate number of tasks that have completed execution.                         |
| `corda_taskmanager_executor_idle_seconds_count`           | Counter | `name`                                                    | The number of events that have been observed for the base metric.                   |
| `corda_taskmanager_executor_idle_seconds_max`             | Gauge   | `name`                                                    | The maximum observed value for the base metric.                                                                                       |
| `corda_taskmanager_executor_idle_seconds_sum`             | Counter | `name`                                                    | The total sum of all observed values for the base metric.                           |
| `corda_taskmanager_executor_pool_core_threads`            | Gauge   | `name`                                                    | The core number of threads for the pool.                                               |
| `corda_taskmanager_executor_pool_max_threads`             | Gauge   | `name`                                                    | The maximum allowed number of threads in the pool.                                     |
| `corda_taskmanager_executor_pool_size_threads`            | Gauge   | `name`                                                    | The current number of threads in the pool.                                             |
| `corda_taskmanager_executor_queue_remaining_tasks`        | Gauge   | `name`                                                    | The number of additional elements that this queue can ideally accept without blocking. |
| `corda_taskmanager_executor_queued_tasks`                 | Gauge   | `name`                                                    | The approximate number of tasks that are queued for execution.                         |
| `corda_taskmanager_executor_scheduled_repetitively_total` | Counter | `name`                                                    |                                                                                        |
| `corda_taskmanager_executor_seconds_count`                | Counter | `name`                                                    | The number of events that have been observed for the base metric.                   |
| `corda_taskmanager_executor_seconds_max`                  | Gauge   | `name`                                                    | The maximum observed value for the base metric.                                                                                       |
| `corda_taskmanager_executor_seconds_sum`                  | Counter | `name`                                                    | The total sum of all observed values for the base metric                            |
| `corda_taskmanager_completion_time_count`                  |  Counter  | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> | The time it took to execute a task, including time waiting to be scheduled.            |
| `corda_taskmanager_completion_time_max`                  |  Gauge  | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> | .            |
| `corda_taskmanager_completion_time_sum`                  |  Counter  | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> | .            |
| `task_manager_live_tasks`                                               | Gauge  | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> | The number of live tasks running or scheduled in the task manager.                     |

Tags:

* `name`: The name of the task manager.
* `task.manager.name`: The name of the task manager.
* `task.type`: The task type (`SHORT_RUNNING`, `LONG_RUNNING`, or `SCHEDULED`).
