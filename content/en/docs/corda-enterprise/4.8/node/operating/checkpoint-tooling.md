---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-monitoring-logging
tags:
- checkpoint
- tooling
title: Checkpoint Tooling
weight: 110
---

This page contains information about the checkpoint dumper and the checkpoint agent tools. Use these tools to debut stuck flows.

Ensure that you understand the mechanics of [flows](../../cordapps/api-flows.md/) and [Node flow hospital](../node-flow-hospital.md/).

A checkpoint is a serialised snapshot of the stack frames associated with the flow and any objects reachable from the stack. Checkpoints are saved to the node database automatically whenever a flow suspends or resumes, which typically happens when sending or receiving messages. A flow may be replayed from the last checkpoint if the node restarts, increasing flow durability.

Use these tools to debug stuck flows.


## Use the checkpoint dumper

The checkpoint dumper outputs information about flows running on a node. You can use this information to diagnose the causes of stuck flows. Using the generated output, corrective actions can be taken to resolve the issues flows are facing. <!--One possible solution, is ending a flow using the `flow kill` command.-->

To use the checkpoint dumper:

1. Open the node shell.
2. Run the `checkpoints dump` command.
3. Open the `logs` directory of the node. There will be a `.zip` file named `checkpoint_dump-<date-and-time.zip`.

Inside the `.zip` checkpoint dump file there will be a `.json` file for each flow that was running when the checkpoint dump happened. Each `.json`  file follows the naming format `<flow name>-<flow id>.json`. Each `.json` flow file contains the checkpoints of

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

The checkpoint agent is a diagnostics tool that outputs the type, size, and content of flow checkpoints at node runtime. You should use the checkpoint agent when developing and testing flows.

For a given flow checkpoint, the agent outputs:

* Information about the checkpoint such as its `flowId`.
* A nested hierarchical view of its reachable objects and their associated sizes, including the state of any flows held within the checkpoint.

The checkpoint agent writes information to standard Log4j2 log files in the node's `log` directory.

This tool is particularly useful when used in conjunction with the `checkpoints dump` CRaSH shell command to identify and troubleshoot problems associated with flows not completing.

The checkpoint agent can be downloaded from [here](https://software.r3.com/artifactory/corda-releases/net/corda/corda-tools-checkpoint-agent/).

To run the checkpoint agent add `-Dcapsule.jvm.args=-javaagent:<PATH>/checkpoint-agent.jar[=arg=value,...]` to the command starting the Corda node.

The checkpoint agent increases the memory requirement of the node. You should set a minimum memory heap size of 1 GB for nodes running the checkpoint agent.

{{< note >}}
A checkpoint agent log is created by default even when no specific configuration is provided for checkpoint agent. Every time a node starts, an empty checkpoint agent log is created.
{{< /note >}}

If you **only** wish to log checkpoint data for failing flows, start the checkpoint agent with the following arguments:

```shell
checkpoint-agent.jar=instrumentType=read,instrumentClassname=NONE
```

{{< note >}}
If you are using the Corda gradle plugin configuration tasks, ensure that you alter the task to include the checkpoint agent. See [the cordform task](../deploy/generating-a-node.md/) for information on updating the cordform task.
{{< /note >}}


### Configure the checkpoint agent

The checkpoint agent can be started with the following optional parameters:

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

### Combining the checkpoint agent and the checkpoint dumper

If you are using the checkpoint agent, the `checkpoints dump` shell command will output an additional diagnostic log file.

The checkpoint dumper will create a log file called `<NODE_BASE>\logs\checkpoints_dump-<date>.zip`, and an additional `<NODE_BASE>\logs\checkpoints_agent-<date>.log` file will be created. The additional log file contains the types and sizes of the checkpoint stack.

{{< warning >}}
The checkpoint agent JAR file must be called “checkpoint-agent.jar” as the checkpoint dump support code uses Java reflection to
determine whether the VM has been instrumented or not at runtime.
{{< /warning >}}


### Logging configuration

The agent will log output to a Log4j2 configured logger.

Configure a separate log file to capture this information by configuring an appender as follows:

```xml
<Logger name="CheckpointAgent" level="info" additivity="false">
    <AppenderRef ref="Checkpoint-Agent-RollingFile-Appender"/>
</Logger>
```


{{< warning >}}
You must specify “CheckpointAgent” as the logger name.

{{< /warning >}}


In this instance we are specifying a Rolling File appender with archival rotation as follows:

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

The *log4j2.xml* containing the above configuration must now be be passed to the Corda node JVM along with the agent specification:

```shell
-Dlog4j.configurationFile=<PATH>/log4j2.xml
```


### Sample output

Using the *log4j2* configuration described above, the following output is generated to a file called `checkpoints_agent-<DATE>.log` under
the Corda node `logs` directory for a single flow execution (in this case):

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

Note,


* on WRITE (eg. a checkpoint is being serialized to disk), we have complete information of the checkpoint object including the Fiber it is
running on and its checkpoint id (43c7d5c8-aa66-4a98-beed-dc91354d0353)
* on READ (eg. a checkpoint is being deserialized from disk), we only have information about the stack class hierarchy.
Additionally, if we are using the CRaSH shell `checkpoints dump` command, we also see a flows checkpoint id.


## Flow diagnostic process

Lets assume a scenario where we have triggered a flow in a node (eg. node acting as a flow initiator) but the flow does not appear to complete.

For example, you may see the following using the CRaSH shell `flow watch` command:

```none
Id                                Flow name                                                           Initiator                        Status
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
15f16740-4ea2-4e48-bcb3-fd9051d5b Cash Issue And Payment                                              bankUser                         In progress
1c6c3e59-26aa-4b93-8435-4e34e265e Cash Issue And Payment                                              bankUser                         In progress
90613d6f-be78-41bd-98e1-33a756c28 Cash Issue And Payment                                              bankUser                         In progress
43c7d5c8-aa66-4a98-beed-dc91354d0 Cash Issue And Payment                                              bankUser                         In progress
Waiting for completion or Ctrl-C ...
```

Note that “In progress” indicates the flows above have not completed (and will have been checkpointed).


* Check the main corda node log file for *hospitalisation* and/or *flow retry* messages: `<NODE_BASE>\logs\node-<hostname>.log`

```none
[INFO ] 2019-07-11T17:56:43,227Z [pool-12-thread-1] statemachine.FlowMonitor. - Flow with id 90613d6f-be78-41bd-98e1-33a756c28808 has been waiting for 97904 seconds to receive messages from parties [O=BigCorporation, L=New York, C=US].
```

{{< note >}}
Always search for the flow id, in this case **90613d6f-be78-41bd-98e1-33a756c28808**

{{< /note >}}

* From the CRaSH shell run the `checkpoints dump` command to trigger diagnostics information.

```none
Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

Thu Jul 11 18:56:48 BST 2019>>> checkpoints dump
```

You will now see an addition line in the main corda node log file as follows:

```none
[INFO ] 2019-07-11T18:02:47,610Z [rpc-server-handler-pool-0] rpc.CheckpointDumper. - Checkpoint agent processing checkpointId: [90613d6f-be78-41bd-98e1-33a756c28808]
```

And two additional files will appear in the nodes logs directory:


* `<NODE_BASE>\logs\checkpoints_dump-20190711-180247.zip`
* `<NODE_BASE>\logs\checkpoints_agent-20190711-185424.log`


* Unzip the `<NODE_BASE>\logs\checkpoints_dump-<date>.zip` file, and you should see a file with a matching flow id as above:
**CashIssueAndPaymentFlow-90613d6f-be78-41bd-98e1-33a756c28808.json**Its contents will contain the following diagnostics information:

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


* View the contents of the node agent diagnostics file:

```none
[INFO ] 2019-07-11T18:02:47,615Z [rpc-server-handler-pool-0] CheckpointAgent. - [READ] class net.corda.node.services.statemachine.Checkpoint
Checkpoint id: 90613d6f-be78-41bd-98e1-33a756c28808
000:net.corda.node.services.statemachine.Checkpoint 29,200
001:  net.corda.node.services.statemachine.ErrorState$Clean 0
001:  net.corda.node.services.statemachine.FlowState$Started 26,061
002:    net.corda.core.internal.FlowIORequest$SendAndReceive 4,666
003:      java.util.Collections$SingletonMap 4,536
004:        net.corda.node.services.statemachine.FlowSessionImpl 500
005:          net.corda.core.identity.Party 360
005:          net.corda.node.services.statemachine.SessionId 28
004:        net.corda.core.serialization.SerializedBytes 3,979
002:    net.corda.core.serialization.SerializedBytes 21,222
001:  net.corda.core.context.InvocationContext 905
002:    net.corda.core.context.Actor 259
002:    net.corda.core.context.InvocationOrigin$RPC 13
002:    net.corda.core.context.Trace 398
001:  net.corda.core.identity.Party 156
002:    net.i2p.crypto.eddsa.EdDSAPublicKey 45
002:    net.corda.core.identity.CordaX500Name 92
001:  java.util.LinkedHashMap 327
002:    net.corda.node.services.statemachine.SessionState$Initiating 214
001:  java.util.ArrayList 1,214
002:    net.corda.node.services.statemachine.SubFlow$Inlined 525
003:      java.lang.Class 47
003:      net.corda.node.services.statemachine.SubFlowVersion$CorDappFlow 328
004:        net.corda.core.crypto.SecureHash$SHA256 118
005:          [B 33
002:    net.corda.node.services.statemachine.SubFlow$Initiating 322
003:      java.lang.Class 39
003:      net.corda.core.flows.FlowInfo 124
003:      net.corda.node.services.statemachine.SubFlowVersion$CorDappFlow 11
002:    net.corda.node.services.statemachine.SubFlow$Initiating 250
003:      java.lang.Class 41
003:      net.corda.core.flows.FlowInfo 99
004:        java.lang.String 91
005:          [C 85
003:      net.corda.node.services.statemachine.SubFlowVersion$CoreFlow 28
```


* Take relevant recovery action, which may include:


* killing and retrying the flow:

```none
Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

Thu Jul 11 20:24:11 BST 2019>>> flow kill 90613d6f-be78-41bd-98e1-33a756c28808
[ERROR] 20:24:18+0100 [Node thread-1] corda.flow. - Flow interrupted while waiting for events, aborting immediately {actor_id=bankUser, actor_owning_identity=O=BankOfCorda, L=London, C=GB, actor_store_id=NODE_CONFIG, fiber-id=10000003, flow-id=15f16740-4ea2-4e48-bcb3-fd9051d5ba59, invocation_id=45622dc7-c4cf-4d11-85ad-1c45e0943455, invocation_timestamp=2019-07-11T18:19:40.519Z, origin=bankUser, session_id=02010e15-8e7a-46f7-976b-5e0626451c54, session_timestamp=2019-07-11T18:19:32.285Z, thread-id=176}
Killed flow [90613d6f-be78-41bd-98e1-33a756c28808]

Thu Jul 11 20:26:45 BST 2019>>> flow start CashIssueAndPaymentFlow amount: $1000, issueRef: 0x01, recipient: "Bank B", anonymous: false, notary: "Notary Service"
```


* attempting to perform a graceful shutdown (draining all outstanding flows and preventing others from starting) and re-start of the node:

```none
Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

Thu Jul 11 19:52:56 BST 2019>>> gracefulShutdown
```

Upon re-start ensure you disable flow draining mode to allow the node to continue to receive requests:

```none
Welcome to the Corda interactive shell.
Useful commands include 'help' to see what is available, and 'bye' to shut down the node.

Thu Jul 11 19:52:56 BST 2019>>> run setFlowsDrainingModeEnabled enabled: false
```

See also Flow draining mode.


* contacting other participants in the network where their nodes are not responding to an initiated flow.
The checkpoint dump gives good diagnostics on the reason a flow may be suspended (including the destination peer participant node that is not responding):

```json
{
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
  }
}
```

## Automatic detection of unrestorable checkpoints

This is a new functionality introduced in Corda 4.6, which enables you to detect unrestorable checkpoints when developing CorDapps and thus reduces the risk of writing flows that cannot be retried gracefully.

It allows you to address the following common problems:

* Create objects or leveraging data structures that cannot be serialized/deserialized correctly by Kryo (the checkpoint serialization library Corda uses).
* Write flows that are not idempotent or do not deduplicate behaviour (such as calls to an external system).

The feature provides a way for flows to reload from checkpoints, even if no errors occur. As a result, as a developer you can be more confident your flows will work correctly, without needing a way to inject recoverable errors throughout the flows.

### How to use this feature

Add the `reloadCheckpointAfterSuspend` [node configuration option](node/setup/corda-configuration-fields.md#reloadCheckpointAfterSuspend) and set it to `true`, as shown below:

```
reloadCheckpointAfterSuspend = true
```

{{< note >}}
This option is disabled by default and is independent from `devMode`.
{{< /note >}}

There are no further steps that you need to take either as a node operator or as a developer testing your application.

#### How to use from a driver test

To use this feature from a driver test:

```kotlin
driver {
    startNode(
        providedName = ALICE_NAME,
        customOverrides = mapOf(NodeConfiguration::reloadCheckpointAfterSuspend.name to true)
    ).getOrThrow()
}
```

The feature can also be enabled by setting the system property `reloadCheckpointAfterSuspend` to `true`, which enables it for all driver tests as long as the property value remains as `true`.

### How it works

Enabling the configuration option will cause all flows to reload their current checkpoint whenever they suspend.

More precisely, any calls to a suspending function execute the following steps:

1. Save a new checkpoint.
2. Reload the checkpoint from the database and recreate the flow from it.
3. Continue executing the called suspending function.

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

If no errors occur from reloading the flow from the newly created checkpoint, then the flow will continue as normal.

#### Deserialization errors

When a failure occurs, you can see an error in the node's logs. The stack trace indicates what object it attempted to serialize, which allows you to determine the source of the error.

#### Skipping checkpoints

A flow can decide to skip persisting a checkpoint when calling a suspending function. Even if this is done, the flow will still be reloaded. However, in this scenario the checkpoint that the flow loads from is an earlier checkpoint instead of the current checkpoint (since it was not saved). This is not useful for detecting deserialization errors but it checks that the flow generally handles retries correctly.

#### Idempotent/timed flows

Idempotent/timed flows always retry from their initial checkpoint when a retry is needed. Therefore, when one of these flows is reloaded when reaching a suspending function, it will load the initial checkpoint and start from the beginning. This is not useful for detecting deserialization errors but checks that the flow generally handles retries correctly.
