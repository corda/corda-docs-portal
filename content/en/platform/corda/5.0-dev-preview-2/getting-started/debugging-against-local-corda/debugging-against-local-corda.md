---
date: '2022-09-20'
title: "Debugging Against Local Corda"
menu:
  corda-5-dev-preview2:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-debugging
    weight: 6000
section_menu: corda-5-dev-preview2
---
The CSDE includes an IntelliJ run-time configuration that allows you to attach IntelliJ’s debugger to the local Corda cluster.
{{< note >}}
Currently there is a time-out issue when debugging Corda. As the local Corda cluster is a real Corda cluster, it behaves like one. Specifically, if the workers stop working, Corda detects it and errors out the flow. Unfortunately, it currently mistakes code held at a debugging point as a processor that has stopped working. As a result, although you can halt at a breakpoint and examine the stack, if you wait too long before resuming the execution of the code, it times out and the CorDapp does not continue to run as expected.     
{{< /note >}}
To debug:
1. [Start the Corda combined worker using the startCorda Gradle helper](../running-your-first-cordapp/run-first-cordapp.html#starting-the-corda-combined-worker), if not already started.
2. [Deploy your CorDapp using deployCordapp](../running-your-first-cordapp/run-first-cordapp.html#deploying-a-cordapp), if not already deployed.
3. Select the `DebugCorDapp` run configuration.
{{< figure src="select-debug-configuration.png" figcaption="CSDE DebugCorDapp run configuration in IntelliJ" >}}
4. Click the **Debug** button.
{{< figure src="click-debug.png" figcaption="Debug button in IntelliJ" >}}
   The following message is displayed to indicate a successful connection:
   {{< figure src="debugger-connected.png" figcaption="DebugCorDapp connection success in IntelliJ" >}}
5. Place a breakpoint next to the place in the code you want to inspect.
   {{< figure src="place-breakpoint.png" figcaption="Breakpoint added in IntelliJ" >}}
6. Start a flow using the Swagger UI; see [Running your first Cordapp section](../running-your-first-cordapp/run-first-cordapp.html).
   The CorDapp stops execution at the breakpoint and you can inspect the stack.
   {{< figure src="pause-at-breakpoint.png" figcaption="Pause at breakpoint in IntelliJ" >}}   
  {{< note >}}
  As described previously, if you wait too long to resume, the flow will fail. The logs will contain one or more of the following messages:

   * `2022-09-20 18:43:20.278 [Thread-94] ERROR net.corda.flow.pipeline.impl.FlowEventPipelineImpl - Flow execution timeout, Flow marked as failed, interrupt attempted`
   * `java.util.concurrent.TimeoutException: null`
   * `net.corda.flow.pipeline.exceptions.FlowEventException: Received a Wakeup for flow [f9a83184-2f83-4587-aca4-e622f4b1bfee] that does not exist`
  {{< /note >}}   
