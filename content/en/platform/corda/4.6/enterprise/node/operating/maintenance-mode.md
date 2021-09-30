---
date: '2020-05-05T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-node-maintenance-mode
    name: "Node Maintenance Mode"
    parent: corda-enterprise-4-6-corda-nodes-operating
    weight: 7
tags:
- maintenance
- mode
title: Node Maintenance Mode
---

# Node Maintenance Mode

The Node Maintenance Mode feature, introduced in Corda Enterprise 4.6, enables you to run certain house-keeping events automatically within Corda at specific times of the day or week, using a "_cron-like_" scheduling algorithm.

Node Maintenance Mode is designed in a scalable way - maintenance tasks are discovered by Corda Enterprise through the use of an internal API.

## Supported maintenance tasks

The following maintenance tasks are currently supported:

- Perform RPC Audit table cleanup
- Run message ID Cleanup

## Configuration of Node Maintenance Mode

Node Maintenance Mode is configured via a new, optional configuration sub-section named `maintenanceMode` within the `enterpriseConfiguration` top-level [configuration section](../setup/corda-configuration-fields.md#enterpriseconfiguration).

By default, no maintenance activities will be performed if the `maintenanceMode` section is not provided. Without the new parameter, Corda will behave as if maintenance mode is not available.

If the `maintenanceMode` configuration sub-section *is* present in the Corda configuration, then **ALL** `maintenanceMode` parameters must be supplied and must also pass configuration validation at start-up.

In addition to the `maintenanceMode` configuration sub-section, the message ID cleanup maintenance task parameters are taken from the configuration sub-section `processedMessageCleanup`(also part of the `enterpriseConfiguration` top-level [configuration section](../setup/corda-configuration-fields.md#enterpriseconfiguration)). This configuration is used for running the message ID cleanup task (also called `NodeJanitor`) at shutdown. `NodeJanitor` is a background process that will clean up old entries from the `NODE_MESSAGE_IDS` [table](node-database-tables.html#node-state-machine). The size should be fairly constant. The same rules will apply for calculation of default values as when the activity runs at shutdown.

The following example shows a sample `maintenanceMode` configuration, including `processedMessageCleanup` parameters:

```
enterpriseConfiguration {
  maintenanceMode {
    schedule = "00 30 14,15 * * 5"
    duration = "10m"
    rpcAuditDataRetentionPeriod = "100d"
  }
  processedMessageCleanup {
    generalRetentionPeriodInDays = 334
    senderRetentionPeriodInDays = 445
  }
}
```

### Configuration parameters

#### `schedule`

This is the *“cron-like”* expression which is used to control at what time(s) the maintenance tasks are run. The format follows the existing cron standards using a 6-part time specification but omits the command line part of the expression as would be present in a Unix cron expression. Times are in **UTC**. A summary of the parts of the schedule follows below:

```
┌─────────────── second (0 - 59)
│ ┌───────────── minute (0 - 59)
│ │ ┌─────────── hour (0 - 23)
│ │ │ ┌───────── day of the month (1 - 31)
│ │ │ │ ┌─────── month (1 - 12)
│ │ │ │ │ ┌───── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │ │                                  
│ │ │ │ │ │
│ │ │ │ │ │
* * * * * *
```

For more information on *cron* (with examples) please see [cron-wiki](https://en.wikipedia.org/wiki/Cron) and note that the examples shown will include the *<command to execute>* part which is not present in the Corda `schedule`. The tasks that get run are not dependent on this configuration item and are determined *within* Corda.
The following example will run maintenance at 14:30 and 15:30 (UTC) on Fridays (‘5’ in final column):

```
schedule = "00 30 14,15 * * 5"
```

#### `duration`

This is the maximum time that a maintenance window is expected to take to run all tasks. At start-up, Corda will check for all maintenance events that occur within the following week. If there is an overlap (due the specified duration being longer than the interval between any two adjacent maintenance windows), Corda will emit a *warning* to the log which will precisely specify the overlap scenario but no further action will be taken. Additionally, if the time that the maintenance tasks *actually* take to run exceeds the specified duration, a warning will be emitted to the log but the maintenance tasks will not be interrupted. The purpose of the duration parameter is to allow the user to check that there are no overlaps and to allow monitoring of overrunning activities via log messaging and monitoring.

The duration is specified in HOCON *duration* format with suffixes of `‘h’ (hours), ‘m’ (minutes) and ‘s’ (seconds)` - for example, `‘1h’` to mean one hour. For additional information on HOCON duration format parsing see [HOCON-duration-format](https://github.com/lightbend/config/blob/master/HOCON.md#duration-format).

#### `rpcAuditDataRetentionPeriod`

This is a parameter to the RPC table maintenance task and specifies how long records should be kept for within the table for.

The parameter is in HOCON *period* format - for example, `‘365d’, ‘1w’`. In general, the following suffixes should be sufficient: `‘d’ (days), ‘w’ (weeks), ‘m’ (months), ‘y’ (years)`.

For more information on the HOCON period format see [HOCON-period-format](https://github.com/lightbend/config/blob/master/HOCON.md#period-format). The end of the retention period will be the current time (in UTC) minus the duration.

## Overrunning maintenance windows

It may be possible that maintenance windows overrun. This could happen due to one of two reasons, as follows:

* The nominal duration specified was insufficient for the tasks to fully complete. In this case Corda Enterprise will emit a log warning (as explained in the duration section in the explanation of parameters above). There is no other effect on the operation of Corda Enterprise.
* The actual duration, which the maintenance window takes to run, ended **after** the start of the next maintenance window. This is a slightly more serious situation in that the next maintenance window will **NOT** be run. Only one maintenance window can run at any one time and maintenance will only start at the **beginning** of its specified window. Therefore, even a slight overrun in a previous maintenance window can prevent a later one from being run. If this happens, Corda Enterprise will emit a log warning, as shown in the example below:

```
[WARN ] 2020-08-28T14:22:41,005Z [pool-12-thread-1] maintenance.MaintenanceScheduler - The maintenance window scheduled to run at 2020-08-28T14:22:38 (UTC) was missed due to an earlier window at 2020-08-28T14:22:31 (UTC) not finishing until 2020-08-28T14:22:41 (UTC)
```
