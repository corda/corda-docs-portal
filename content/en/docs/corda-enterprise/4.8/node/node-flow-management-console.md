---
title: "Flow management console"
linkTitle: "Flow management console"
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-corda-nodes-operating
tags:
- node
- flow
- hospital
title: Flow management console
weight: 155
---
# Flow management console

The flow management console allows you to see the state of the flows running on a node and perform some operations on them. It runs as part of the [Gateway Service](gateway-service.md).

It has a front end written in React, and a REST service written in Kotlin, which makes RPC calls to Corda Enterprise.

It consists of two `.jar` files:

* The flow management plug-in: `flow-management-plugin-<release>.jar`.
* The permissions `.jar` for the plug-in: `auth-baseline-flow-management-<release>.jar`.

These files can be downloaded from Artifactory: [`corda-gatewayplugins`](https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-gateway-plugins).

## Installation

1. Put `flow-management-plugin-<release>.jar` into the `plugins` directory in the Gateway Service.
2. Put `auth-baseline-flow-management-<release>.jar` into the `plugins` directory in the Auth Service.
3. Restart the Gateway Service and the Auth Service.

## Configuration

You need to set the following values in the Gateway Service configuration file:

* RPC username.
* RPC password.
* RPC port, which can be specified either as a literal string or by the `NODE_PORT` environment variable.
* The host name or IP address of the node you wish to monitor, which can be specified either as a literal string or by the `NODE_HOST` environment variable.

These are set in `flow.hospital.middleware` as shown below.

```
flow.hospital.middleware {
     rpcUsername ="u"
     rpcPassword ="p"
     rpcHost = ${NODE_HOST}
     rpcPort = ${NODE_PORT}
}
```

## Accessing the flow management console

To access the flow management console, visit the Gateway service plug-in launcher page, `http://<gateway-service-ip>:<port>/launcher`.

The flow management console has two tabs: the **Dashboard** tab and the **Query flows** tab. The **Dashboard** tab is selected by default, and is at `http://<gateway-service-ip>:<port>/flow-management/dashboard`.

{{< warning >}}
If a flow does **not** have a client ID attached to it, it will not be visible in the `COMPLETED`, `FAILED`, or `KILLED` states, but it will be visible in the `PAUSED`, `RUNNABLE`, and `HOSPITALIZED` states.
{{< /warning >}}

## Dashboard tab

The **Dashboard** tab displays two charts:

* A pie chart that shows the breakdown of flows by flow state (`FAILED`, `KILLED`, `HOSPITALIZED`, `PAUSED`, `RUNNABLE`, or `COMPLETED`).
 * Clicking on a pie chart _section_ redirects you to the query flows tab with a filter applied for that flow state.
* A bar chart which lists flows by suspension duration, starting with the longest duration on the left. Clicking on a flow redirects you to the query flows page filtered on that specific flow. This chart has options for choosing how many flows to display and to filter out flows that have not been suspended for a specified amount of time (for example, only display flows that have been suspended for at least 20 minutes).

## Query flows tab

The **Query flows** tab shows the flows on the node and allows you to filter them. The filter options are shown on the left-hand side and the results panel on the right. If you do not have permission to view this tab, you will see a message that says you do not have permission to view it. For more information on the filter options, see [Specifying the query criteria](operating/querying-flow-data.html#specifying-the-query-criteria).

In the results panel, a table shows the flows that match the filter (or all the flows if no filter is set). Each entry can be expanded to show more information about the flow and show the commands panel.

{{< note >}}
When you use a `FLOW START FROM` filter, the results show a `FROM` value, but when you use a `FLOW START TO` filter, the results *do not* show a `TO` value.
{{< /note >}}

The commands panel has three commands: pause flow, retry flow, and kill flow. If a command is not applicable (for example, a killed flow cannot be paused) or if you do not have permissions to run the command, it will be disabled (greyed out).

## Permissions

A user can have either read-only permissions, or admin permissions. Permissions are set using the User Admin tool, `http://<gateway-service-ip>:<port>/admin`.

{{% note %}}
Unless a tab or other functionality is specifically restricted, it is available to an unprivileged user.
{{% /note%}}
