---
aliases:
- /head/debugging-a-cordapp.html
- /HEAD/debugging-a-cordapp.html
- /debugging-a-cordapp.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-debugging-a-cordapp
    parent: corda-community-4-10-building-a-cordapp-index
    weight: 1070
tags:
- debugging
- cordapp
title: Debugging a CorDapp
---


# Debugging a CorDapp


There are several ways to debug your CorDapp.


## Using a `MockNetwork`

You can attach the [IntelliJ IDEA debugger](https://www.jetbrains.com/help/idea/debugging-code.html) to a
`MockNetwork` to debug your CorDapp:


1. Define your flow tests as per [API: Testing](api-testing.md):

    * In your `MockNetwork`, ensure that `threadPerNode` is set to `false`.

2. Set your breakpoints.
3. Run the flow tests using the debugger. When the tests hit a breakpoint, execution will pause.


## Using the node driver

You can also attach the [IntelliJ IDEA debugger](https://www.jetbrains.com/help/idea/debugging-code.html) to nodes
running via the node driver to debug your CorDapp.


### With the nodes in-process

1. Define a network using the node driver as per [Integration testing](../../../../tutorials/corda/4.10/community/supplementary-tutorials/tutorial-integration-testing.md).
2. In your `DriverParameters`, ensure that `startNodesInProcess` is set to `true`.
3. Run the driver using the debugger.
4. Set your breakpoints.
5. Interact with your nodes. When execution hits a breakpoint, execution will pause.

{{< note >}}
The nodes’ webservers always run in a separate process, and cannot be attached to by the debugger.
{{< /note >}}

### With remote debugging


1. Define a network using the node driver as per [Integration testing](../../../../tutorials/corda/4.10/community/supplementary-tutorials/tutorial-integration-testing.md).

2. In your `DriverParameters`, ensure that `startNodesInProcess` is set to `false` and `isDebug` is set to `true`.

3. Run the driver. The remote debug ports for each node will be automatically generated and printed to the terminal.
For example:

```none
[INFO ] 11:39:55,471 [driver-pool-thread-0] (DriverDSLImpl.kt:814) internal.DriverDSLImpl.startOutOfProcessNode -
    Starting out-of-process Node PartyA, debug port is 5008, jolokia monitoring port is not enabled {}
```

4. Attach the debugger to the node of interest on its debug port.
5. In IntelliJ IDEA, create a new run/debug configuration of type `Remote`.
6. Set the run/debug configuration’s `Port` to the debug port.
7. Start the run/debug configuration in debug mode.
8. Set your breakpoints.
9. Interact with your node. When execution hits a breakpoint, execution will pause.

{{< note >}}
The nodes’ webservers always run in a separate process, and cannot be attached to by the debugger.
{{< /note >}}


## Enabling remote debugging on a node

See [Enabling remote debugging](node-commandline.html#enabling-remote-debugging).
