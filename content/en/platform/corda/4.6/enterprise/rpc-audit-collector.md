---
date: '2020-04-22T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- rpc
- audit
- collector
title: RPC Audit Data Collection Tool
weight: 200
---

# RPC Audit Data Collection Tool

In this section, you will learn how to run the RPC Audit Data Collection Tool in order to collect recorded RPC audit data.

This tool is distributed as part of Corda Enterprise.

The RPC data recorded by the node is explained in detail on the [RPC Audit Data Recording](node/setup/rpc-audit-data-recording.md) page.

## Collecting RPC audit data

To enable the collection of recorded RPC Audit Data, we have provided a new RPC action with options for filtering data collection based on `username`, `action`, and a specific time range (by specifying `startTime` and `endTime`). All of these filters are optional and are not applied if not explicitly enabled.

The action is available on the `AuditDataRPCOps` interface.

{{< tabs name="signature" >}}
{{% tab name="kotlin" %}}

```kotlin
fun collectRPCAuditData(
    format: Format = Format.JSON,
    username: String? = null,
    action: String? = null,
    startTime: Instant? = null,
    endTime: Instant? = null
) : String
```

{{% /tab %}}
{{< /tabs >}}

To use the interface to collect audit data, ensure that the following permissions are set:

- InvokeRpc.collectAuditData
- InvokeRpc.nodeInfo

You can use the `collectAuditData` action with the following parameters:

- `format` - either `JSON` or `CSV` (default: `JSON`)
- `username` - filter by a specific user
- `action` - filter by a specific action
- `startTime` - filter RPC data after the startTime (inclusive)
- `endTime`- filter RPC data before the endTime (exclusive)

### Examples

#### Collecting RPC audit data for all actions over the last 7 days

{{< tabs name="example-1" >}}
{{% tab name="kotlin" %}}

```kotlin
fun collectRpcAuditData(rpc: AuditDataRPCOps): String {
    val startTime = Instant.now() - Duration.ofDays(7)
    val endTime = Instant.now()
    return rpc.collectAuditData(
        Format.JSON,
        startTime = startTime,
        endTime = endTime)
}
```

{{% /tab %}}
{{% tab name="java" %}}

```java
public String collectRpcAuditData(AuditDataRPCOps rpc) {
    Instant startTime = Instant.now() - Duration.ofDays(7)
    Instant endTime = Instant.now()
    return rpc.collectAuditData(
        Format.JSON,
        null,
        null,
        startTime,
        endTime);
}
```

{{% /tab %}}
{{< /tabs >}}

#### Collecting RPC audit data for user "Alice" for the last 7 days

{{< tabs name="example-2" >}}
{{% tab name="kotlin" %}}

```kotlin
fun collectData(rpc: AuditDataRPCOps): String {
    val startTime = Instant.now() - Duration.ofDays(7)
    val endTime = Instant.now()
    return rpc.collectAuditData(
        Format.JSON,
        user = "Alice",
        startTime = startTime,
        endTime = endTime)
```

{{% /tab %}}
{{% tab name="java" %}}

```java
public String collectRpcAuditData(AuditDataRPCOps rpc) {
    Instant startTime = Instant.now() - Duration.ofDays(7)
    Instant endTime = Instant.now()
    return rpc.collectAuditData(
        Format.JSON,
        "Alice",
        null,
        startTime,
        endTime);
}
```

{{% /tab %}}
{{< /tabs >}}

#### Collecting all available RPC data for a particular action

{{< tabs name="example-3" >}}
{{% tab name="kotlin" %}}

```kotlin
fun collectData(rpc: AuditDataRPCOps): String {
    return rpc.collectAuditData(
        Format.JSON,
        action = "startDynamicFlow")
}
```

{{% /tab %}}
{{% tab name="java" %}}

```java
public String collectRpcAuditData(AuditDataRPCOps rpc) {
    return rpc.collectAuditData(
        Format.JSON,
        null,
        "startDynamicFlow",
        null,
        null);
}
```

{{% /tab %}}
{{< /tabs >}}

## Purging RPC audit data

You can purge older audit logs that you don't need (although the collection of RPC audit data usually results in a fairly small amount of disk space). To remove older audit data, use the following action on the `AuditDataRPCOps` interface:

```kotlin
/**
 * Removes any past audit data
 * NOTE: Exercise caution if you are allowing users access to this function.
 */
fun clearRPCAuditDataBefore(
    before: Instant
)
```

You can use the `clearRPCAuditDataBefore` action with the following parameter:

- `before` - the cut-off time to keep audit data from - all audit data recorded before that time will be cleared (exclusive)

### Example

#### Clearing all RPC audit data over a week old

{{< tabs name="example-4" >}}
{{% tab name="kotlin" %}}

```kotlin
fun clearWeekOldAuditData(rpc: AuditDataRPCOps) {
    val oneWeekAgo = Instant.now() - Duration.ofDays(7)
    rpc.clearAuditDataBefore(oneWeekAgo)
}
```

{{% /tab %}}
{{% tab name="java" %}}

```java
public void clearWeekOldAuditData(AuditDataRPCOps rpc) {
    Instant oneWeekAgo = Instant.now() - Duration.ofDays(7);
    rpc.clearAuditDataBefore(oneWeekAgo);
}
```

{{% /tab %}}
{{< /tabs >}}
