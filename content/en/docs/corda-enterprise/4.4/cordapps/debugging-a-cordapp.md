---
aliases:
- /releases/4.4/cordapps/debugging-a-cordapp.html
- /docs/corda-enterprise/head/cordapps/debugging-a-cordapp.html
- /docs/corda-enterprise/cordapps/debugging-a-cordapp.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    identifier: corda-enterprise-4-4-cordapps-debugging
    name: "Debugging and testing CorDapps"
    parent: corda-enterprise-4-4-cordapps
tags:
- debugging
- cordapp
title: Debugging a CorDapp
weight: 11
---

# Debugging a CorDapp

There are several ways to debug your CorDapp.

## Using a `MockNetwork`

You can attach the [IntelliJ IDEA debugger](https://www.jetbrains.com/help/idea/debugging-code.html) to a
`MockNetwork` to debug your CorDapp:


* Define your flow tests as per [API: Testing](api-testing.md).

    * In your `MockNetwork`, ensure that `threadPerNode` is set to `false`.

* Set your breakpoints.
* Run the flow tests using the debugger. When the tests hit a breakpoint, execution will pause.


## Using the node driver

You can also attach the [IntelliJ IDEA debugger](https://www.jetbrains.com/help/idea/debugging-code.html) to nodes
running via the node driver to debug your CorDapp.


### With the nodes in-process


* Define a network using the node driver as described in [Integration Testing](../../../corda-os/4.4/tutorial-integration-testing.md).

* In your `DriverParameters`, ensure that `startNodesInProcess` is set to `true`.

* Run the driver using the debugger.

* Set your breakpoints.

* Interact with your nodes. When execution hits a breakpoint, execution will pause.

{{< note >}}
The nodes’ webservers always run in a separate process, and cannot be attached to by the debugger.
{{< /note >}}


### With remote debugging


* Define a network using the node driver as described in [Integration Testing](../../../corda-os/4.4/tutorial-integration-testing.md).
* In your `DriverParameters`, ensure that `startNodesInProcess` is set to `false` and `isDebug` is set to
`true`.
* Run the driver. The remote debug ports for each node will be automatically generated and printed to the terminal.

  For example:

```none
[INFO ] 11:39:55,471 [driver-pool-thread-0] (DriverDSLImpl.kt:814) internal.DriverDSLImpl.startOutOfProcessNode -
    Starting out-of-process Node PartyA, debug port is 5008, jolokia monitoring port is not enabled {}
```

* Attach the debugger to the node of interest on its debug port:

  * In IntelliJ IDEA, create a new run/debug configuration of type `Remote`.
  * Set the run/debug configuration’s `Port` to the debug port.
  * Start the run/debug configuration in debug mode.

* Set your breakpoints.
* Interact with your node. When execution hits a breakpoint, execution will pause.

{{< note >}}
The nodes’ webservers always run in a separate process, and cannot be attached to by the debugger.
{{< /note >}}


## By enabling remote debugging on a node

See [Enabling remote debugging](../node/node-commandline.md#enabling-remote-debugging).
