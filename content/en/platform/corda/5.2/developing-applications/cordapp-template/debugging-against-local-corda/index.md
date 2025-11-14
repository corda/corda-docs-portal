---
date: '2023-11-01'
title: "Debugging Against Local Corda"
description: Learn how to debug using the CorDapp template.
menu:
  corda52:
    parent: corda52-develop-get-started
    identifier: corda52-debugging
    weight: 6000

---
# Debugging Against Local Corda

The CorDapp template includes an IntelliJ run-time configuration that allows you to attach IntelliJ’s debugger to the local Corda cluster.
{{< note >}}
Currently there is a time-out issue when debugging Corda. As the local Corda cluster is a real Corda cluster, it behaves like one. Specifically, if the workers stop working, Corda detects it and errors out the flow. Unfortunately, it currently mistakes code held at a debugging point as a processor that has stopped working. As a result, although you can halt at a breakpoint and examine the stack, if you wait too long before resuming the execution of the code, it times out and the CorDapp does not continue to run as expected.
{{< /note >}}

To debug:

1. [Start the Corda combined worker using the startCorda Gradle helper]({{< relref  "../running-your-first-cordapp/_index.md#starting-the-corda-combined-worker" >}}), if not already started.
2. [Deploy your CorDapp using deployCordapp]({{< relref "../running-your-first-cordapp/_index.md#deploying-a-cordapp" >}}), if not already deployed.
3. Select the `DebugCorDapp` run configuration.
{{< figure src="debugging.png" width="40%" figcaption="DebugCorDapp run configuration in IntelliJ" >}}
4. Click the **Debug** button.
{{< figure src="click-debug.png" width="50%" figcaption="Debug button in IntelliJ" >}}
   The following message is displayed to indicate a successful connection:
   {{< figure src="debugger-connected.png" width="90%" figcaption="DebugCorDapp connection success in IntelliJ" >}}
5. Place a breakpoint next to the place in the code you want to inspect.
   {{< figure src="place-breakpoint.png" figcaption="Breakpoint added in IntelliJ" >}}
6. Start a flow using the Swagger UI; see [Running your First CorDapp]({{< relref "../running-your-first-cordapp/_index.md" >}}).
   The CorDapp stops execution at the breakpoint and you can inspect the stack.
   {{< figure src="pause-at-breakpoint.png" figcaption="Pause at breakpoint in IntelliJ" >}}

  {{< note >}}
  As described previously, if you wait too long to resume, the flow will fail. The logs will contain one or more of the following messages:

   * `2022-09-20 18:43:20.278 [Thread-94] ERROR net.corda.flow.pipeline.impl.FlowEventPipelineImpl - Flow execution timeout, Flow marked as failed, interrupt attempted`
   * `java.util.concurrent.TimeoutException: null`
   * `net.corda.flow.pipeline.exceptions.FlowEventException: Received a Wakeup for flow [f9a83184-2f83-4587-aca4-e622f4b1bfee] that does not exist`
  {{< /note >}}
