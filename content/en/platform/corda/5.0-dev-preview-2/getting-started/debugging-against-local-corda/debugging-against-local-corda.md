---
date: '2022-09-20'
title: "Your first flow"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-start
    identifier: corda-5-dev-preview-debugging
    weight: 6000
section_menu: corda-5-dev-preview
---
The CSDE includes an IntelliJ run-time configuration which allows you to attach IntelliJ’s debugger to the local Corda cluster.

Caveat, currently there is a time out issue when debugging Corda. As the local Corda custer is a real Corda cluster it behaves like one, specifically if the workers stop working Corda will detect it and error out the flow. Unfortunately, it currently mistakes code held at a debugging point with a processor that has stopped working. Hence, although you can halt at a breakpoint and examine the stack, if you wait too long before resuming the execution of the code it will time out and the program will not continue to run as expected.     

To debug:
1. Start corda using the startCorda Gradle Helper (if not already started).
2. Deploy your CorDapp using deployCordapp (if not already deployed).
3. Select the DebugCorDapp run configuration.
{{< figure src="debugging-against-local-corda.png" figcaption="CSDE DebugCorDapp run configuration in IntelliJ" >}}
4. Click the debug button.
{{< figure src="click-debug.png" figcaption="Debug button in IntelliJ" >}}
   The following message is displayed to indicate a successful connection:
   {{< figure src="debugger-connected.png" figcaption="DebugCorDapp connection success in IntelliJ" >}}
5. Place a breakpoint next to the place in the code you want to inspect the running program.
   {{< figure src="place-breakpoint.png" figcaption="Breakpoint added in IntelliJ" >}}
6. Start a flow using the swagger UI (see Running your first Cordapp section)
   The CorDapp stops execution at the breakpoint and you can inspect the stack.
   {{< figure src="pause-at-breakpoint.png" figcaption="Pause at breakpoint in IntelliJ" >}}   
  {{< note >}}
  If you wait too long to resume, the flow will fail. The logs will contatin one or more of the following messages:

   `2022-09-20 18:43:20.278 [Thread-94] ERROR net.corda.flow.pipeline.impl.FlowEventPipelineImpl - Flow execution timeout, Flow marked as failed, interrupt attempted`
   `java.util.concurrent.TimeoutException: null`
   `net.corda.flow.pipeline.exceptions.FlowEventException: Received a Wakeup for flow [f9a83184-2f83-4587-aca4-e622f4b1bfee] that does not exist`
   {{< /note >}}   
