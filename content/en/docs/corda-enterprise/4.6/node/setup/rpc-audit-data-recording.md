---
date: '2020-05-03T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-configuring
tags:
- rpc
- audit
- recording
title: Recording of RPC audit data
weight: 4
---

# Recording of RPC audit data

In this section, you will learn how the node records [Remote Procedural Command (RPC)](../../api-rpc.md) audit data.

This feature is distributed as part of Corda Enterprise.

## RPC audit data

RPC actions play a vital part in the process of triggering commands and flows on a node. In a variety of cases you will need to track the usage of RPC actions - for example, when there are security and regulatory concerns. To do so, you can use the Corda Enterprise node's capability to record audit information about RPC actions as they are received, prior to executing each action.

The data recorded by the node is listed below:

- `username` - the specific user who executed the action (limited to 130 characters)
- `interface` - the specific type of RPC on which the action was called (limited to 130 characters)
- `action` - the action that the user intended to invoke (limited to 130 characters)
- `parameters` - for non-flow actions, the parameter list which was passed with the action (limited to 255 characters)
- `invocationtime` - the time whethatn the action was recorded by the node and invoked
- `invocationid` - the unique invocation id of the action
- `allowed` - a boolean field indicating if the `user` was allowed to call the `action`

## Overview of the RPC audit data recording process

To enable collection of RPC actions, we have provided a configuration option in the `enterpriseConfiguration.auditService` section of the `node.conf` file, as follows:

```conf
enterpriseConfiguration = {
    ...

    auditService = {
        eventsToRecord = NONE
    }

    ...
}
```

The current `AuditService` configuration supports the following audit types:

- `NONE` - nothing will be recorded (default)
- `RPC` - RPC actions will be recorded
- `ALL` - all audit services will be recorded (note that only RPC is supported at this time)

## Collecting RPC audit data

In addition to recording RPC Audit Data it will also be useful to collect information on any data recorded.  See the [RPC Audit Data Collector](../../rpc-audit-collector.md) page for details on this.
