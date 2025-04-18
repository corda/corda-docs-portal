---
description: "Review the metrics generated for the Corda task manager. The task manager exposes metrics for underlying thread pools and jobs processing duration and count."
date: '2023-10-26'
title: "Task Manager"
menu:
  corda52:
    parent: corda52-cluster-metrics
    identifier: corda52-cluster-task-manager
    weight: 1450
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
| `corda_taskmanager_executor_active_threads`               | Gauge   | <ul><li>`name`</li></ul>                                                    | The approximate number of threads that are actively executing tasks.                   |
| `corda_taskmanager_executor_completed_tasks_total`        | Counter | <ul><li>`name`</li></ul>                                                    | The approximate number of tasks that have completed execution.                         |
| `corda_taskmanager_executor_idle_seconds_count`           | Counter | <ul><li>`name`</li></ul>                                                    | The number of events that have been observed for the base metric.                   |
| `corda_taskmanager_executor_idle_seconds_max`             | Gauge   | <ul><li>`name`</li></ul>                                                    | The maximum observed value for the base metric.                                                                                       |
| `corda_taskmanager_executor_idle_seconds_sum`             | Counter | <ul><li>`name`</li></ul>                                                    | The total sum of all observed values for the base metric.                           |
| `corda_taskmanager_executor_pool_core_threads`            | Gauge   | <ul><li>`name`</li></ul>                                                    | The core number of threads for the pool.                                               |
| `corda_taskmanager_executor_pool_max_threads`             | Gauge   | <ul><li>`name`</li></ul>                                                    | The maximum allowed number of threads in the pool.                                     |
| `corda_taskmanager_executor_pool_size_threads`            | Gauge   | <ul><li>`name`</li></ul>                                                    | The current number of threads in the pool.                                             |
| `corda_taskmanager_executor_queue_remaining_tasks`        | Gauge   | <ul><li>`name`</li></ul>                                                    | The number of additional elements that this queue can ideally accept without blocking. |
| `corda_taskmanager_executor_queued_tasks`                 | Gauge   | <ul><li>`name`</li></ul>                                                    | The approximate number of tasks that are queued for execution.                         |
| `corda_taskmanager_executor_scheduled_repetitively_total` | Counter | <ul><li>`name`</li></ul>                                                    |                                                                                        |
| `corda_taskmanager_executor_seconds_count`                | Counter | <ul><li>`name`</li></ul>                                                    | The number of events that have been observed for the base metric.                   |
| `corda_taskmanager_executor_seconds_max`                  | Gauge   | <ul><li>`name`</li></ul>                                                    | The maximum observed value for the base metric.                                                                                       |
| `corda_taskmanager_executor_seconds_sum`                  | Counter | <ul><li>`name`</li></ul>                                                    | The total sum of all observed values for the base metric                            |
| `corda_taskmanager_completion_time_count`                  |  Counter  | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> | The number of tasks completed by a task manager.            |
| `corda_taskmanager_completion_time_max`                  |  Gauge  | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> | The maximum time taken to complete a task by a task manager.           |
| `corda_taskmanager_completion_time_sum`                  |  Counter  | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> | The total sum of the time taken to execute all completed tasks by a task manager.           |
| `task_manager_live_tasks`                                               | Gauge  | <ul><li>`task.manager.name`</li><li>`task.type`</li></ul> | The number of live tasks running or scheduled in the task manager.                     |

Tags:

* `name`: The name of the task manager.
* `task.manager.name`: The name of the task manager.
* `task.type`: The task type (`SHORT_RUNNING`, `LONG_RUNNING`, or `SCHEDULED`).
