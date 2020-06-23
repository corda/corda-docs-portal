---
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes-operating
tags:
- shell
- node
- query
- flow
title: Querying flow data
weight: 6
---

# Querying flow data

You can query a node to retrieve flow checkpoint data that can be useful for troubleshooting flows.

A checkpoint is a record of flow data taken at key points during a flow's operation, typically whenever the flow is
suspended and waiting for a response or message.

To query the node for flow data, you must use the [Corda Shell](shell.md).

## Query formatting

A query contains the following elements:

- A query command: `checkpoint`.
- Filtering fields: `queryBy <fields>`. Filtering fields define what checkpoints are returned by the query.
- Reporting fields: `reportBy <fields>`. Reporting fields define what data is returned from each returned checkpoint.

A complete query might look like this:

`checkpoint queryBy flowClass=CashIssueAndPaymentFlow,flowStartMethod=RPC reportBy flowId,flowStartTimeBefore`

In this example:
 - `flowClass` and `flowStartMethod` are filtering fields - checkpoints that match **all** of the filtering fields will be returned.
 - `flowId` and `flowStartTimeBefore` are reporting fields - only the `flowId` and `flowStartTimeBefore` data from each checkpoint will be returned.

{{< note >}}
All the filtering fields can be used as reporting fields. However, the `flowStartContext`, `checkpointSize`, `flowParameters`, `callStack`, `checkpointSeqNum`, and `json` fields can only be used as reporting fields.
{{< /note >}}

## Queryable fields


All dates and timestamps must be formatted as per the [ISO 8601 standard](https://www.iso.org/iso-8601-date-and-time-format.html/) using the following pattern `yyyy-MM-dd'T'HH:mm:ss.SSSZ`.
For example, 2001-07-04 12:08:56 local time in the U.S. Pacific Time time zone is represented as `2001-07-04T12:08:56.235-07:00`.


{{< table >}}

| Field name | Description | Format | Filtering or reporting field |
|---------|----------|---------|---------|
| flowId  |  Unique string identifying the flow.  |  String  |  Both |
| flowClass  |  Shortened classname of the flow.  |  String  |  Both |
| flowStartTimeBefore  |  If used as a filtering field, returns all flows started before the given time. If used as a reporting field, returns the exact time when the flow was started.  |  Timestamp  |  Both |
| flowStartTimeAfter  |  If used as a filtering field, returns all flows started after the given time. If used as a reporting field, returns the exact time when the flow was started.  |  Timestamp  |  Both |
| checkpointTimeBefore  |   If used as a filtering field, returns all checkpoints created before the given time. If used as a reporting field, returns the exact time when the checkpoint was created.  |  Timestamp  |  Both |
| checkpointTimeAfter  |  If used as a filtering field, returns all checkpoints created after the given time. If used as a reporting field, returns the exact time when the checkpoint was created.  |  Timestamp  |  Both |
| platformVersion  |  Corda [platform version](../../cordapps/versioning.html#platform-version) used to process the flow.  |  Positive Integer  |  Both |
| corDappName  |  The name of the CorDapp to which the flow belongs.  |  String  |  Both |
| corDappVersion  |  The version of the CorDapp to which flow belongs.  |  String  |  Both |
| flowStatus  |  The status of the flow at the time the checkpoint was created  |  String  |  Both |
| checkpointCreationReason  |  The reason why the checkpoint was created. For example, `send` or `sendAndReceive`.  |  String  |  Both |
| pendingParty  |  The X.500 name of the party the checkpoint is waiting on. Empty if the checkpoint is not waiting for a party.  |  X.500 string  |  Both |
| flowStartMethod  |  The method used to start the flow. For example, RPC, SubFlow, Initiated.  |  String  |  Both |
| compatible  |  If used as a filtering field, returns compatible or incompatible checkpoints. If used as a reporting field, returns the compatibility of returned checkpoints as a boolean.  |  Boolean String  |  Both |
| progressTrackerStep  |  Last known progress tracker step. If there is no known progress tracker step, an empty string will be returned.  |  String  |  Both |
| flowStartContext  |  Specifies the creator of the flow: RPC user, parent, or initiating flow ID for initiated flows.  |  String  |  Reporting |
| checkpointSize  |  The size of the checkpoint binary, returned as a string.  |  String  |  Reporting |
| flowParameters  |  The parameters passed into the flow, returned as a string.  |  String  |  Reporting |
| callStack  |  The invocation stack at the time the checkpoint was created, returned as a string.  |  String  |  Reporting |
| checkpointSeqNum  |  Checkpoint sequence number.  |  Positive Integer  |  Reporting |
| json  |  Returns a long JSON string representing the whole checkpoint. |  Long JSON string  |  Reporting |

{{< /table >}}
