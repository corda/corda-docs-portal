---
date: '2021-07-15'
menu:
  corda-enterprise-4-8:
    identifier: corda-enterprise-4-8-cordapps-debugging
    name: "Debugging and testing CorDapps"
    parent: corda-enterprise-4-8-cordapps
tags:
- debugging
- cordapp
title: Debug a CorDapp
weight: 120
---

# Debug a CorDapp

There are several ways you can debug your CorDapp.

## Method 1: Use a `MockNetwork`

You can attach the [IntelliJ IDEA debugger](https://www.jetbrains.com/help/idea/debugging-code.html) to a
`MockNetwork` to debug your CorDapp.


1. Define your [flow tests]({{< relref "../../../../../../en/platform/corda/4.8/enterprise/cordapps/api-testing.md" >}}).
2. Set `threadPerNode` to `false` in your `MockNetwork`.
3. Set your breakpoints.
4. Run the flow tests using the debugger. When the tests hit a breakpoint, execution will pause.


## Method 2: Use the node driver

Attach the [IntelliJ IDEA debugger](https://www.jetbrains.com/help/idea/debugging-code.html) to nodes
running via the node driver to debug your CorDapp. You can debug the CorDapp:
* While the nodes are in-process
* Using remote debugging


### Debug with the nodes in-process

1. [Define a network using the node driver]({{< relref "../get-started/tutorials/supplementary-tutorials/tutorial-integration-testing.md" >}}).
2. Check your `DriverParameters` and make sure that `startNodesInProcess` is set to `true`.
3. Run the driver using the debugger.
4. Set your breakpoints.
5. Interact with your nodes.  If the execution hits a breakpoint, it will pause.

{{< note >}}
The debugger cannot attach to the node's webservers - they always run in a separate process.
{{< /note >}}


### Debug remotely

1. [Define a network using the node driver]({{< relref "../get-started/tutorials/supplementary-tutorials/tutorial-integration-testing.md" >}}).
2. Check your `DriverParameters` and make sure that `startNodesInProcess` is set to `false` and `isDebug` is set to
`true`.
3. Run the driver. The remote debug ports for each node are generated automatically and printed to the terminal.

   For example:

```none
[INFO ] 11:39:55,471 [driver-pool-thread-0] (DriverDSLImpl.kt:814) internal.DriverDSLImpl.startOutOfProcessNode -
    Starting out-of-process Node PartyA, debug port is 5008, jolokia monitoring port is not enabled {}
```

4. Attach the debugger to the relevant node's debug port:
    1. In IntelliJ IDEA, create a new run/debug configuration of type `Remote`.
    2. Set the run/debug configuration’s `Port` to the debug port.
    3. Start the run/debug configuration in debug mode.

5. Set your breakpoints.
6. Interact with your node. If the execution hits a breakpoint, it will pause.

{{< note >}}
The debugger cannot attach to the node's webservers - they always run in a separate process.
{{< /note >}}


## Method 3: Enable remote debugging on a node


See [Enabling remote debugging](../../../../../../en/platform/corda/4.8/enterprise/node/node-commandline.html#enabling-remote-debugging).

