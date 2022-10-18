---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-9-monitoring-logging
tags:
- checkpoint
- tooling
title: Checkpoint tooling
weight: 110
---

This page contains information about the checkpoint dumper and the checkpoint agent tools. Use these tools to debug stuck flows.

Ensure that you understand the mechanics of [flows](../../../../../../../../en/platform/corda/4.9/enterprise/cordapps/api-flows.md) and [Node flow hospital](../../../../../../../../en/platform/corda/4.9/enterprise/node/node-flow-hospital.md).

A checkpoint is a serialised snapshot of the stack frames associated with the flow and any objects reachable from the stack. Checkpoints are saved to the Corda node database automatically whenever a flow suspends or resumes, which typically happens when sending or receiving messages. A flow may be replayed from the last checkpoint if the node restarts, increasing flow durability.


## Use the checkpoint dumper

The checkpoint dumper outputs information about flows running on a node. You can use this information to diagnose the causes of stuck flows. Using the generated output, corrective actions can be taken to resolve the issues flows are facing.

To use the checkpoint dumper:

1. Open the node shell.
2. Run the `checkpoints dump` command.
3. Open the `logs` directory of the node. There will be a `.zip` file named `checkpoint_dump-<date-and-time.zip`.

Inside the `.zip` checkpoint dump file there will be a `.json` file for each flow that was running when the checkpoint dump happened. Each `.json`  file follows the naming format `<flow name>-<flow id>.json`.

The most important fields in the output are:

* The id of the flow, `flowId`.
* The name of the original flow that was invoked (by RPC or a service), `topLevelFlowClass`.
* A detailed view of the top level flow, `topLevelFlowLogic`.
* A summarised list of the current stack of sub flows along with any progress tracker information, `flowCallStackSummary`.
* The command that the flow is suspended on (for example, `SendAndReceive`), which includes the `suspendedTimestamp`, `suspendedOn`.
* A detailed view of the of the current stack of sub flows, `flowCallStack`.

### Sample output

Below is an example of the `.json` output:

```json
{
  "flowId" : "90613d6f-be78-41bd-98e1-33a756c28808",
  "topLevelFlowClass" : "net.corda.finance.flows.CashIssueAndPaymentFlow",
  "topLevelFlowLogic" : {
    "amount" : "10.00 USD",
    "issueRef" : "MTIzNA==",
    "recipient" : "O=BigCorporation, L=New York, C=US",
    "anonymous" : true,
    "notary" : "O=Notary, L=London, C=GB"
  },
  "flowCallStackSummary" : [
    {
      "flowClass" : "net.corda.finance.flows.CashIssueAndPaymentFlow",
      "progressStep" : "Paying recipient"
    },
    {
      "flowClass" : "net.corda.finance.flows.CashPaymentFlow",
      "progressStep" : "Generating anonymous identities"
    },
    {
      "flowClass" : "net.corda.confidential.SwapIdentitiesFlow",
      "progressStep" : "Awaiting counterparty's anonymous identity"
    }
  ],
  "suspendedOn" : {
    "sendAndReceive" : [
      {
        "session" : {
          "peer" : "O=BigCorporation, L=New York, C=US",
          "ourSessionId" : -5024519991106064492
        },
        "sentPayloadType" : "net.corda.confidential.SwapIdentitiesFlow$IdentityWithSignature",
        "sentPayload" : {
          "identity" : {
            "class" : "net.corda.core.identity.PartyAndCertificate",
            "deserialized" : "O=BankOfCorda, L=London, C=GB"
          },
          "signature" : "M5DN180OeE4M8jJ3mFohjgeqNYOWXzR6a2PIclJaWyit2uLnmJcZatySoSC12b6e4rQYKIICNFUXRzJnoQTQCg=="
        }
      }
    ],
    "suspendedTimestamp" : "2019-08-12T15:38:39Z",
    "secondsSpentWaiting" : 7
  },
  "flowCallStack" : [
    {
      "flowClass" : "net.corda.finance.flows.CashIssueAndPaymentFlow",
      "progressStep" : "Paying recipient",
      "flowLogic" : {
        "amount" : "10.00 USD",
        "issueRef" : "MTIzNA==",
        "recipient" : "O=BigCorporation, L=New York, C=US",
        "anonymous" : true,
        "notary" : "O=Notary, L=London, C=GB"
      }
    },
    {
      "flowClass" : "net.corda.finance.flows.CashPaymentFlow",
      "progressStep" : "Generating anonymous identities",
      "flowLogic" : {
        "amount" : "10.00 USD",
        "recipient" : "O=BigCorporation, L=New York, C=US",
        "anonymous" : true,
        "issuerConstraint" : [ ],
        "notary" : "O=Notary, L=London, C=GB"
      }
    },
    {
      "flowClass" : "net.corda.confidential.SwapIdentitiesFlow",
      "progressStep" : "Awaiting counterparty's anonymous identity",
      "flowLogic" : {
        "otherSideSession" : {
          "peer" : "O=BigCorporation, L=New York, C=US",
          "ourSessionId" : -5024519991106064492
        },
        "otherParty" : null
      }
    }
  ],
  "origin" : {
    "rpc" : "bankUser"
  },
  "ourIdentity" : "O=BankOfCorda, L=London, C=GB",
  "activeSessions" : [ ],
  "errored" : null
}
```

## Use the checkpoint agent

The checkpoint agent is a diagnostics tool that outputs the type, size, and content of flow checkpoints at node runtime. You should use the checkpoint agent when developing and testing flows. A checkpoint agent log is created by default even when no specific configuration is provided for checkpoint agent. Every time a node starts, an empty checkpoint agent log is created.

For a given flow checkpoint, the agent reports:
* Information about the checkpoint such as its `flowId`.
* A nested hierarchical view of its reachable objects and their associated sizes, including the state of any flows held within the checkpoint.

The checkpoint agent writes information to standard Log4j2 log files in the node's `log` directory. This tool is particularly useful when used in conjunction with the `checkpoints dump` [CRaSH shell command](../../../../../../../../en/platform/corda/4.9/enterprise/node/operating/shell.html#output-information-about-the-flows-running-on-the-node) to identify and troubleshoot problems associated with flows not completing. When a checkpoint is serialized to disk the checkpoint agent has access to all checkpoint data, including the fiber it was running on and the checkpoint ID. When a checkpoint is deserialized from disk the checkpoint agent only has access to the stack class hierarchy.

To use the checkpoint agent:

1. Download the checkpoint agent from [Artifactory](https://software.r3.com/artifactory/corda-releases/net/corda/corda-tools-checkpoint-agent/).
2. Add the `-Dcapsule.jvm.args=-javaagent:<PATH>/checkpoint-agent.jar[=arg=value,...]` option when starting the node. To log checkpoint data only for failing flows, start the checkpoint agent with the `checkpoint-agent.jar=instrumentType=read,instrumentClassname=NONE` arguments.
3. If you are using the Corda gradle plugin configuration tasks, alter the task to include the checkpoint agent. See [the cordform task](../../../../../../../../en/platform/corda/4.9/enterprise/node/deploy/generating-a-node.md) for information on updating the `cordform` task.

{{< note >}}
The checkpoint agent increases the memory requirement of the node. You should set a minimum memory heap size of 1 GB for nodes running the checkpoint agent.
{{< /note >}}

### Configure the checkpoint agent and checkpoint agent logger

The checkpoint agent logs output to a Log4j2-configured logger. This logger must be defined in the logging configuration file.

To configure the checkpoint agent logger:

1. Open the `sql.xml` logging configuration file. For information on general logging configuration, see [Monitoring and logging](../../../../../../../../en/platform/corda/4.9/enterprise/node/operating/monitoring-and-logging/overview.md).
2. Add the following logger entry:

    ```xml
    <Logger name="CheckpointAgent" level="info" additivity="false">
        <AppenderRef ref="Checkpoint-Agent-RollingFile-Appender"/>
    </Logger>
    ```

    You must specify `CheckpointAgent` as the logger name.
3. Add the logger configuration. See this configuration example:

    ```xml
    <RollingFile name="Checkpoint-Agent-RollingFile-Appender"
                 fileName="${log-path}/checkpoints_agent-${date:yyyyMMdd-HHmmss}.log"
                 filePattern="${archive}/checkpoints_agent.%date{yyyy-MM-dd}-%i.log.gz">

        <PatternLayout pattern="[%-5level] %date{ISO8601}{UTC}Z [%t] %c{2}.%method - %msg%n"/>

        <Policies>
            <TimeBasedTriggeringPolicy/>
            <SizeBasedTriggeringPolicy size="100MB"/>
        </Policies>

        <DefaultRolloverStrategy min="1" max="100">
            <Delete basePath="${archive}" maxDepth="1">
                <IfFileName glob="${log-name}*.log.gz"/>
                <IfLastModified age="60d">
                    <IfAny>
                        <IfAccumulatedFileSize exceeds="10 GB"/>
                    </IfAny>
                </IfLastModified>
            </Delete>
        </DefaultRolloverStrategy>

    </RollingFile>
    ```
4. Save and close the `sql.xml` file.
5. When you start your node, pass the `sql.xml` file to the node JVM by adding the `-Dlog4j.configurationFile=sql.xml` option.

You can add the following optional parameters when starting the checkpoint agent:

```shell
checkpoint-agent.jar=[instrumentType=<read|write>],[instrumentClassname=<CLASSNAME>],[minimumSize=<MIN_SIZE>],[maximumSize=<MAX_SIZE>, [graphDepth=<DEPTH>], [printOnce=<true|false>]
```

| Option | Description |
|--------|-------------|
| `instrumentType` | String. Specifies whether `read` or `write` checkpoints are logged. Default: read |
| `instrumentClassname` | String. Specifies the base type of objects to log, as a class name. Defaults to all flow objects. Default: net.corda.node.services.statemachine.FlowStateMachineImpl |
| `minimumSize` | Integer. Specifies the minimum size of objects to log, in bytes. Default: 8192 bytes (8 KB) |
| `maximumSize` | Integer. Specifies the maximum size of objects to log, in bytes. Default: 20000000 bytes (20 MB) |
| `graphDepth` | Integer. Specifies the depth of the graph output, 0 is unlimited. Default: unlimited |
| `printOnce` | Boolean. If true, displays each full object reference and sub-graph only once. Default: true |

These arguments are passed to the JVM along with the agent specification. For example:

```shell
-javaagent:<PATH>/checkpoint-agent.jar=instrumentClassname=net.corda.vega.flows.SimmFlow,instrumentType=read,minimumSize=10240,maximumSize=512000,graphDepth=6,printOnce=false
```

#### Sample output

Using the Log4j2 configuration described above, the following output is generated to a file called `checkpoints_agent-<DATE>.log` under
the node `logs` directory:

```none
[INFO ] 2019-07-11T18:25:15,723Z [Node thread-1] CheckpointAgent. - [WRITE] Fiber@10000004:[43c7d5c8-aa66-4a98-beed-dc91354d0353][task: co.paralleluniverse.fibers.RunnableFiberTask@4dc8eaf(Fiber@10000004), target: null, scheduler: co.paralleluniverse.fibers.FiberExecutorScheduler@4e468018]
000:net.corda.node.services.statemachine.FlowStateMachineImpl 21,149

[INFO ] 2019-07-11T18:19:51,115Z [FiberDeserializationChecker] CheckpointAgent. - [READ] class net.corda.node.services.statemachine.FlowStateMachineImpl
000:net.corda.node.services.statemachine.FlowStateMachineImpl 21,151
001:  net.corda.node.services.statemachine.FlowStateMachineImpl 21,149
002:    java.lang.String 107
003:      [C 77
002:    co.paralleluniverse.fibers.Stack 20,932
003:      [J 278
003:      [Ljava.lang.Object; 20,054
004:        net.corda.finance.flows.CashIssueAndPaymentFlow 7,229
005:          net.corda.core.utilities.ProgressTracker 5,664
etc ...

[INFO ] 2019-07-11T18:35:03,198Z [rpc-server-handler-pool-2] CheckpointAgent. - [READ] class net.corda.node.services.statemachine.ErrorState$Clean
Checkpoint id: 15f16740-4ea2-4e48-bcb3-fd9051d5ba59
000:net.corda.node.services.statemachine.FlowStateMachineImpl 21,151
001:  [C 77
001:  [J 278
001:  [Ljava.lang.Object; 20,054
002:    java.util.ArrayList 1,658
003:      net.corda.core.utilities.ProgressTracker$STARTING 0
etc ...
```

### Combining the checkpoint agent and the checkpoint dumper

If you are using the checkpoint agent, the `checkpoints dump` shell command will output an additional diagnostic log file.

The checkpoint dumper will create a log file called `<NODE_BASE>\logs\checkpoints_dump-<date>.zip`, and an additional `<NODE_BASE>\logs\checkpoints_agent-<date>.log` file will be created. The additional log file contains the types and sizes of the checkpoint stack.

{{< warning >}}
The checkpoint agent JAR file must be called `checkpoint-agent.jar` as the checkpoint dump support code uses Java reflection to determine whether or not the VM has been instrumented at runtime.
{{< /warning >}}


## Automatic detection of unrestorable checkpoints

You can detect flows with unrestorable checkpoints during development and testing by enabling the `reloadCheckpointAfterSuspend` configuration option. When enabled, this configuration option causes any calls to a suspending function to execute the following steps:

1. Save a new checkpoint.
2. Reload the checkpoint from the database and recreate the flow from it.
3. If no errors occurred, continue executing the called suspending function.

An example (with comments to highlight where the reloads occur) follows below:

```kotlin
@StartableByRPC
@InitiatingFlow
class MyFlow(private val party: Party) : FlowLogic<Unit>() {

    @Suspendable
    override fun call() {
        val session = initiateFlow(party)
        // checkpoints when calling [send], reloads and continues with the [send]
        session.send("an important message")
        // checkpoints when calling [receive], reloads and continues with the [receive]
        session.receive(String::class.java).unwrap { it }
        // checkpoints when calling [sleep], reloads and continues with the [sleep]
        sleep(10.seconds)
    }
}
```

This causes the execution of a flow to test that each checkpoint can be used to restore the flow successfully. By using this feature you can address the following common problems:

* Flows containing objects or leveraging data structures that cannot be serialized/deserialized correctly by Kryo (the checkpoint serialization library Corda uses).
* Flows that are not idempotent or do not deduplicate behavior (such as calls to an external system).

If a failure occurs, you can find the stack trace in the node's log files. The stack trace indicates the object that was being serialized when the error occurred. Flows can be written to deliberately avoid checkpointing when calling a suspending function. In this case, the flow will reload from an earlier checkpoint.

Idempotent and timed flows always retry from their initial checkpoint. When an idempotent or timed flow is reloaded after reaching a suspending function, it will load the initial checkpoint and start from the beginning.

### Enable automatic detection of unrestorable checkpoints

The detection of unrestorable checkpoints can be enabled either by a node configuration option or as an inclusion in driver tests.

To enable this feature in the node configuration:

1. Open the `node.conf` node configuration file.
2. Add the `reloadCheckpointAfterSuspend` [option](../../../../../../../../en/platform/corda/4.9/enterprise/node/setup/corda-configuration-fields.html#reloadCheckpointAfterSuspend) to your node configuration, set to true:
    ```
    reloadCheckpointAfterSuspend = true
    ```
3. Save and close the node configuration file.
4. Start or restart your node.

To use this feature from a driver test, add the following code to your driver test:

```kotlin
driver {
    startNode(
        providedName = ALICE_NAME,
        customOverrides = mapOf(NodeConfiguration::reloadCheckpointAfterSuspend.name to true)
    ).getOrThrow()
}
```

The feature can also be enabled by setting the system property `reloadCheckpointAfterSuspend` to `true`, which enables it for all driver tests as long as the property value remains as `true`.

## Related content

* [Troubleshooting stuck flows](../../../../../../../../en/platform/corda/4.9/enterprise/node/operating/monitoring-and-logging/diagnosing-stuck-flows.md)
