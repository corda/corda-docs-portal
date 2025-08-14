---
date: '2021-07-15'
menu:
  corda-enterprise-4-13:
    identifier: corda-enterprise-4-13-cordapps-flows-system
    name: System flows
    parent: corda-enterprise-4-13-cordapps-flows
tags:
- api
- flows
title: System flows
weight: 70
---


# System flows

*System flows* are [flows]({{< relref "api-flows.md" >}}) that run at node startup, before any services flows or user flows. The only currently supported system flow is [automatic ledger recovery]({{< relref "../node/ledger-recovery/automatic-ledger-recovery.md" >}}). 

To configure a node to run system flows, including the automatic ledger recovery flow, the Boolean parameter `runSystemFlowsAtStartup` in the *[enterpriseConfiguration]({{< relref "../node/setup/corda-configuration-fields.md#enterpriseconfiguration" >}})* section of the [node configuration]({{< relref "../node/setup/corda-configuration-fields.md" >}}) must be set to `true`. The node will now have a system flow phase after startup, during which system flows are run. 

A second parameter, `systemFlowsStuckSkipThreshold`, must also be configured. This integer parameter specifies the number of seconds that a system flow can be stuck on a suspension point during a system flow phase before it is skipped. Such a flow will skip up to two times: once in checkpoint system flows phase, then again in startup system flows phase.

System flow annotation has the property `supersedes`. This is used with the fully qualified name of another system flow to run that in its place at startup.  For example, the following example shows how an existing system flow A could be superseded by flow B:

```
@SystemFlow(supersedes = "com.r3.mypackage.FlowA")
@StartableByRPC
@InitiatingFlow
class FlowB : FlowLogic<Unit>() {
  @Suspendable
  override fun call() {
   //my code
  }
}
```

Once a node is configured to run system flows at startup, the following sequence of actions occurs during the system flow phase:

1. If there are system flows that were previously checkpointed, these checkpointed system flows will run before the startup system flows.  
2. Once any checkpointed system flows have either completed or resulted in an exception, normal system flows then run. 
3. If there are paused flows, unpausing flows during the system flow phase will only unpause system flows. 
4. If a system flow gets stuck on a suspension point during the system flow phase for longer than the value (in seconds) of the `systemFlowsStuckSkipThreshold` configured in the [node configuration]({{< relref "../node/setup/corda-configuration-fields.md#enterpriseconfiguration" >}}), it will skip up to two times: once for checkpoint system flows and then again for startup system flows (each system flow is checked for being stuck every one minute).
4. If the node is configured with the "[pause all flows]({{< relref "../flow-pause-and-resume.md#starting-the-node-and-pausing-all-flows" >}})" option (`smmStartMode="Safe"`) or flow draining mode is on, then system flows will not run at startup.
5. While system flows at startup are running, if an RPC flow is started, it will be blocked until the system flows have finished.
6. Flows annotated with `@SystemFlow` should be able to start from RPC as normal during the the system flow phase.
7. After the startup system flows finish, then user and non-system checkpointed flows will run, after the `SystemFlowsPhaseCompleted` event is distributed.
9. Once system flows have finished, a `SystemFlowsPhaseCompleted` event is produced, and the metric `SystemFlows.Phase` is recorded, with values CHECKPOINT, STARTUP and USER in this order (only the latest metric is recorded).
8. Unpausing after the system flow phase is complete will unpause only user and non-system flows.