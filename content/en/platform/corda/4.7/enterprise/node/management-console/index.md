---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    parent: corda-enterprise-4-7-corda-nodes
tags:
- node
- administration
title: Node management console
weight: 76
---

# Node management console

The Node management console allows you to see information about a node and perform some operations on it. It runs as a plug-in for the [Gateway Service](../gateway-service.md).

The node management console allows you to see the following information about the node:

* General node information, including:
  * Platform version.
  * Corda version.
  * Revision (git hash).
  * Whether node draining is enabled.
  * Status (such as `RUNNING` or `DISCONNECTED`).
* Node configuration file.
* Logging (log4j) configuration file.
* The most recent 500 log events.
* The installed CorDapps.
* The list of available drivers.

You can also interact with the node in the following ways:

* Toggle draining mode.
* Gracefully stop the node.
* Kill the node (without draining first).

It has a front end written in React, and a REST service written in Kotlin, which makes RPC calls to Corda Enterprise.

The plug-in consists of two `.jar` files:

* The node management plug-in: `node-management-plugin-<release>.jar`.
* The permissions `.jar` for the plug-in: `auth-baseline-node-management-<release>.jar`.

These files can be downloaded from Artifactory: [`corda-gatewayplugins`](https://software.r3.com/artifactory/webapp/#/artifacts/browse/tree/General/corda-gateway-plugins).

## Installation

1. Put `node-management-plugin-<release>.jar` into the `plugins` directory in the Gateway Service.
2. Put `auth-baseline-node-management-<release>.jar` into the `plugins` directory in the Auth Service.
3. Restart the Gateway Service and the Auth Service.

## Configuration

You need to set the following values in the Gateway Service configuration file:

* RPC username.
* RPC password.
* RPC port, which can be specified either as a literal string or by the `NODE_PORT` environment variable.
* The host name or IP address of the node you wish to monitor, which can be specified either as a literal string or by the `NODE_HOST` environment variable.

These are set in `node.admin.middleware` as shown below.

```
node.admin.middleware {
     rpcUsername ="u"
     rpcPassword ="p"
     rpcHost = ${NODE_HOST}
     rpcPort = ${NODE_PORT}
}
```

## Accessing the node management console

The node management plug-in is accessed through the node management console. To access the flow management console, visit the Gateway service plug-in launcher page, `http://<gateway-service-ip>:<port>/launcher`.

### Permissions

A user can have either read-only permissions, or admin permissions. Permissions are set using the User Admin tool, `http://<gateway-service-ip>:<port>/admin`.

{{% note %}}
Unless a tab or other functionality, such as killing a node, is specifically restricted, it is available to an unprivileged user.
{{% /note%}}

## Viewing general node information

General node information is displayed on the **Status** tab. To access the **Status** tab:

1. Log on to the node management console.
2. Navigate to **Status** tab.

{{% figure zoom="management-console/node-management-console_status.png" alt="Node management console status tab" figcaption="Node management console status tab"%}}

## Viewing the node configuration file

1. Log on to the node management console.
2. Navigate to **NODE** tab under **Configuration**.

{{% figure zoom="management-console/node-management-console_node-configuration.png" alt="Node management console node configuration tab" figcaption="Node management console node configuration tab" %}}

## Viewing the log4j configuration file

1. Log on to the node management console.
2. Navigate to **Configuration** tab.
3. Select the **Logging** tab above the text editor display.

Logging configuration will be displayed in the text editor. The editor can be configured via footer bar to set language, theme, and font size. The editor will be in read-only mode, so no changes may be made.

{{% figure zoom="management-console/node-management-console_log-configuration.png" alt="Node management console configuration tab" figcaption="Node management console logging configuration tab" %}}

### Failure conditions

If the file cannot be found, an error panel will be displayed in place of the text editor.

### Permission

If you do not have permission to perform this action and you click the tab, a message will be displayed that tells you that you do not have permission to view this page.

## Viewing the node logs

1. Log on to the node management console.
2.  Navigate to **Logs** tab.

The most recent 500 log events are displayed. Note that this list is static: it does not change. Click **Refresh** to see the most recent 500 log events. This list does *not* contain the startup logs.

{{% figure zoom="management-console/node-management-console_logs.png" alt="Node management console logs tab" figcaption="Node management console logs tab" %}}

### Failure conditions

If the logs are not in the expected location, a message informs you that the logs could not be found.

### Permission

If you do not have permission to perform this action and you click the tab, a message will be displayed that tells you that you do not have permission to view this page.

## Viewing the installed CorDapps

1. Log on to the node management console.
2. Navigate to **CorDapps** tab.

The installed CorDapps will be shown in a table format.

The table will list the `short name`, `type`, and `vendor` for each CorDapp. The table is sortable by these fields.

To view more information about a particular CorDapp, click on an entry in the table and
the entry expands to show a more comprehensive list of properties for that CorDapp.

{{% figure zoom="management-console/node-management-console_cordapps.png" alt="Node management console CorDapps tab" figcaption="Node management console CorDapps tab" %}}

### Empty state

If there are no installed CorDapps, a message informs you that no CorDapps are installed on the node.

### Permission

If you do not have permission to perform this action and you click the tab, a message will be displayed that tells you that you do not have permission to view this page.

### Further information

* The CorDapp fields are retrieved as a `CordappInfo` object from the Corda API.
    * View the [API documentation](https://api.corda.net/api/corda-os/4.7/html/api/kotlin/corda/net.corda.core.cordapp/-cordapp-info/index.html).

## Viewing available drivers

1. Log on to the node management console.
2. Navigate to **Drivers** tab.

A table shows the names of the drivers on the node.

{{% figure zoom="management-console/node-management-console_drivers.png" alt="Node management console drivers tab" figcaption="Node management console drivers tab" %}}

### Empty state

If there are no available drivers, a message informs you that there are no available drivers.

### Permission

If you do not have permission to perform this action and you click the tab, a message will be displayed that tells you that you do not have permission to view this page.

## Toggling draining mode

1. Log on to the node management console.
2. Navigate to **Status** tab.
3. Click the **Draining mode** toggle to turn draining mode on or off.

{{% figure zoom="management-console/node-management-console_status.png" alt="Node management console status tab" figcaption="Node management console status tab"%}}

## Shutting down a node gracefully

Shutting down a node gracefully enables draining mode, waits for in-flight flows to complete, and then stops the node.

1. Log on to the node management console.
2. Navigate to **Status** tab.
3. Click **Gracefully stop**. A prompt will be shown asking you to confirm.
4. Click **Yes**.

Draining mode is turned on, and the draining mode toggle and the buttons for **Gracefully Stop** and **Kill Node** are disabled.

Then a popup message states that graceful stop has begun.

Once the node has been stopped:

* The status label changes from **RUNNING** to **DISCONNECTED**.
* A popup message states that graceful stop was successful.

When the node management console is reloaded, the node diagnostic info is unavailable, therefore:

* The buttons and toggle do not display.
* The unavailable node information shows as `---`.

{{% note %}}
If you stop a node from the command line, the node will still appear in the console because Corda does not poll the node to see if it is still connected. Refresh the page to show the correct status.
{{% /note %}}

{{% figure zoom="management-console/node-management-console_status.png" alt="Node management console status tab" figcaption="Node management console status tab"%}}

### Permission

If you do not have permission to perform these actions:

* The buttons will be greyed out.
* A tool tip will state that you do not have permission to perform the action.

### Further information
* The Status fields are retrieved as a `NodeDiagnosticInfo` object from the Corda API.
    * View the [API documentation](https://api.corda.net/api/corda-os/4.7/html/api/kotlin/corda/net.corda.core.node/-node-diagnostic-info/index.html)
* The calls to gracefully stop or kill a node, or to toggle drainage mode:
    * Make a REST call to the Node Management REST service.
    * The REST service connects to the node via a `CordaRPCService` connection to execute the command.

## Killing a node

Killing a node stops the node without draining it first.

1. Log on to the node management console.
2. Navigate to **Status** tab.
3. Click **Advanced actions**.
4. Click **Kill node**. A prompt will be shown asking you to confirm.
5. Click **Yes**.

The draining mode toggle and the buttons for **Gracefully Stop** and **Kill Node** are disabled.

Then a popup message states that the killing of the node was successful.

Once the node has been killed:

* The status label changes from **RUNNING** to **DISCONNECTED**.
* A popup message states that the killing of the node was successful.

When the node management console is reloaded, the node diagnostic info is unavailable, therefore:

* The buttons and toggle do not display.
* The unavailable node information shows as `---`.

### Permission

If you do not have permission to perform these actions:

* The buttons will be greyed out.
* A tool tip will state that you do not have permission to perform the action.



## Status code 500 errors

A status code 500 error indicates that the node cannot be reached, perhaps because it has been shut down.
