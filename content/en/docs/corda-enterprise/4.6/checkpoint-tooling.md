---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- checkpoint
- tooling
title: Checkpoint Tooling
weight: 110
---


# Checkpoint Tooling

This page contains information about checkpoint tooling. These tools can be used to debug the causes of stuck flows.

Before reading this page, please ensure you understand the mechanics and principles of Corda Flows by reading key-concepts-flows and [Writing flows](flow-state-machines.md).
It is also recommended that you understand the purpose and behaviour of the node-flow-hospital in relation to *checkpoints* and flow recovery.
An advanced explanation of *checkpoints* within the flow state machine can be found here: contributing-flow-internals.

{{< note >}}
As a recap,

A flow *checkpoint* is a serialised snapshot of the flow’s stack frames and any objects reachable from the stack. Checkpoints are saved to
the database automatically when a flow suspends or resumes, which typically happens when sending or receiving messages. A flow may be replayed
from the last checkpoint if the node restarts. Automatic checkpointing is an unusual feature of Corda and significantly helps developers write
reliable code that can survive node restarts and crashes. It also assists with scaling up, as flows that are waiting for a response can be flushed
from memory.

{{< /note >}}
The checkpoint tools available are:


* [Checkpoint dumper](#checkpoint-dumper)
* [Checkpoint agent](#checkpoint-agent)



## Checkpoint dumper

The checkpoint dumper outputs information about flows running on a node. This is useful for diagnosing the causes of stuck flows. Using the generated output,
corrective actions can be taken to resolve the issues flows are facing. One possible solution, is ending a flow using the `flow kill` command.


{{< warning >}}
Deleting checkpoints manually or via `flow kill`/`killFlow` can lead to an inconsistent ledger among transacting parties. Great care
and coordination with a flow’s counterparties must be taken to ensure that a initiating flow and flows responding to it are correctly
removed. This experience will be improved in the future. Making it easier to kill flows while notifying their counterparties.

{{< /warning >}}


To retrieve this information, execute `checkpoints dump` in the node’s shell. The command creates a zip and generates a JSON file for each flow.


* Each file follows the naming format `<flow name>-<flow id>.json` (for example, `CashIssueAndPaymentFlow-90613d6f-be78-41bd-98e1-33a756c28808.json`).
* The zip is placed into the `logs` directory of the node and is named `checkpoints_dump-<date and time>.zip` (for example, `checkpoints_dump-20190812-153847`).

Below are some of the more important fields included in the output:


* `flowId`: The id of the flow.
* `topLevelFlowClass`: The name of the original flow that was invoked (by RPC or a service).
* `topLevelFlowLogic`: Detailed view of the top level flow.
* `flowCallStackSummary`: A summarised list of the current stack of sub flows along with any progress tracker information.
* `suspendedOn`: The command that the flow is suspended on (for example, `SendAndReceive`), which includes the `suspendedTimestamp`.
* `flowCallStack` A detailed view of the of the current stack of sub flows.



### Sample output

Below is an example of the JSON output:

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



## Checkpoint Agent

The Checkpoint Agent is a very low level diagnostics tool that can be used to output the type, size and content of flow *checkpoints* at node runtime.
It is primarily targeted at users developing and testing code that may exhibit flow mis-behaviour (preferably before going into production).

For a given flow *checkpoint*, the agent outputs:



* Information about the checkpoint such as its `id` (also called a `flow id`) that can be used to correlate with that flows lifecycle details in the main Corda logs.
* A nested hierarchical view of its reachable objects (indented and tagged with depth and size) and their associated sizes, including the state
of any flows held within the checkpoint.


Diagnostics information is written to standard log files (eg. log4j2 configured logger).

This tool is particularly useful when used in conjunction with the `checkpoints dump` CRaSH shell command to troubleshoot and identify potential
problems associated with checkpoints for flows that appear to not be completing.

The checkpoint agent can be downloaded from [here](https://software.r3.com/artifactory/corda-releases/net/corda/corda-tools-checkpoint-agent/).

To run simply pass in the following jar to the JVM used to start a Corda node: `-Dcapsule.jvm.args=-javaagent:<PATH>/checkpoint-agent.jar[=arg=value,...]`

{{< note >}}
As above also ensure to use the jar when using corda gradle plugin configuration tasks: e.g. `cordformation deployNodes` task.
See [https://docs.corda.net/head/generating-a-node.html#the-cordform-task](https://docs.corda.net/head/generating-a-node.html#the-cordform-task)

{{< /note >}}

{{< warning >}}
This tool requires additional memory footprint and we recommended a minimal heap size of at least 1Gb.

{{< /warning >}}


The agent can be customised with a number of optional parameters described below.


### Configuration

The checkpoint agent can be started with the following optional parameters:

```shell
checkpoint-agent.jar=[instrumentType=<read|write>],[instrumentClassname=<CLASSNAME>],[minimumSize=<MIN_SIZE>],[maximumSize=<MAX_SIZE>, [graphDepth=<DEPTH>], [printOnce=<true|false>]
```


* `instrumentType`: whether to output checkpoints on read or write. Possible values: [read, write]. Default: read.
* `instrumentClassname`: specify the base type of objects to log. The default setting is to process all *Flow* object types. Default: net.corda.node.services.statemachine.FlowStateMachineImpl.
* `minimumSize`: specifies the minimum size (in bytes) of objects to log. Default: 8192 bytes (8K)
* `maximumSize`: specifies the maximum size (in bytes) of objects to log. Default: 20000000 bytes (20Mb)
* `graphDepth`: specifies how many levels deep to display the graph output. Default: unlimited
* `printOnce`: if true, will display a full object reference (and its sub-graph) only once. Otherwise an object will be displayed repeatedly as referenced. Default: true

These arguments are passed to the JVM along with the agent specification. For example:

```shell
-javaagent:<PATH>/checkpoint-agent.jar=instrumentClassname=net.corda.vega.flows.SimmFlow,instrumentType=read,minimumSize=10240,maximumSize=512000,graphDepth=6,printOnce=false
```

{{< note >}}
Arguments may be passed into the agent in any order and should **not** contain spaces between them.

{{< /note >}}

### Checkpoint Dump support

When used in combination with the `checkpoints dump` shell command (see [Checkpoint Dumper](#checkpoint-dumper)),
the checkpoint agent will automatically output additional diagnostic information for all checkpoints dumped by the aforementioned tool.

You should therefore see two different output files upon invoking the checkpoint dumper command:


* `<NODE_BASE>\logs\checkpoints_dump-<date>.zip` contains zipped JSON representation of checkpoints (from `checkpoints dump` shell command)
* `<NODE_BASE>\logs\checkpoints_agent-<date>.log` contains output from this agent tool (types and sizes of a checkpoint stack)

{{< note >}}
A checkpoint agent log is created by default even when no specific configuration is provided for checkpoint  agent. Every time a node starts up, an empty checkpoint agent log is created.
{{< /note >}}

If you **only** wish to log checkpoint data for failing flows, start the checkpoint agent with the following arguments:

```shell
checkpoint-agent.jar=instrumentType=read,instrumentClassname=NONE
```

and use the `checkpoints dump` shell command to trigger diagnostics collection.

{{< warning >}}
The checkpoint agent JAR file must be called “checkpoint-agent.jar” as the checkpoint dump support code uses Java reflection to
determine whether the VM has been instrumented or not at runtime.
{{< /warning >}}



### Logging configuration

The agent will log output to a log4j2 configured logger.

It is recommended to configure a separate log file to capture this information by configuring an appender as follows:

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

If an error does occur when deserializing the flow's checkpoint, a `ReloadFlowFromCheckpointException` is thrown, which causes the flow to be kept in for overnight observation (`HOSPITALIZED` status in the database). This only occurs when the configuration option is turned on as this is not standard behaviour. The exception that caused the failure is logged, which will hopefully provides enough information to figure out what object could not be deserialized correctly. From this point, you can either change your flow or apply custom serialization for objects that failed deserialization.

When a failure occurs in this way, an error similar to the following would be seen in the nodes logs:

```javastacktrace
Caused by: java.lang.IllegalStateException: Broken on purpose
	at net.corda.node.flows.BrokenMap.put(FlowRetryTest.kt:449) ~[integrationTest/:?]
	at com.esotericsoftware.kryo.serializers.MapSerializer.read(MapSerializer.java:162) ~[kryo-4.0.2.jar:?]
	at com.esotericsoftware.kryo.serializers.MapSerializer.read(MapSerializer.java:39) ~[kryo-4.0.2.jar:?]
	at com.esotericsoftware.kryo.Kryo.readObject(Kryo.java:731) ~[kryo-4.0.2.jar:?]
	at co.paralleluniverse.io.serialization.kryo.ReplaceableObjectKryo.readObject(ReplaceableObjectKryo.java:92) ~[quasar-core-0.7.12_r3-jdk8.jar:0.7.12_r3]
	at com.esotericsoftware.kryo.serializers.DefaultArraySerializers$ObjectArraySerializer.read(DefaultArraySerializers.java:391) ~[kryo-4.0.2.jar:?]
	at com.esotericsoftware.kryo.serializers.DefaultArraySerializers$ObjectArraySerializer.read(DefaultArraySerializers.java:302) ~[kryo-4.0.2.jar:?]
	at com.esotericsoftware.kryo.Kryo.readObject(Kryo.java:731) ~[kryo-4.0.2.jar:?]
	at co.paralleluniverse.io.serialization.kryo.ReplaceableObjectKryo.readObject(ReplaceableObjectKryo.java:92) ~[quasar-core-0.7.12_r3-jdk8.jar:0.7.12_r3]
	at com.esotericsoftware.kryo.serializers.ObjectField.read(ObjectField.java:125) ~[kryo-4.0.2.jar:?]
	at com.esotericsoftware.kryo.serializers.CompatibleFieldSerializer.read(CompatibleFieldSerializer.java:145) ~[kryo-4.0.2.jar:?]
	at com.esotericsoftware.kryo.Kryo.readObjectOrNull(Kryo.java:782) ~[kryo-4.0.2.jar:?]
	at co.paralleluniverse.io.serialization.kryo.ReplaceableObjectKryo.readObjectOrNull(ReplaceableObjectKryo.java:107) ~[quasar-core-0.7.12_r3-jdk8.jar:0.7.12_r3]
	at com.esotericsoftware.kryo.serializers.ObjectField.read(ObjectField.java:132) ~[kryo-4.0.2.jar:?]
	at com.esotericsoftware.kryo.serializers.FieldSerializer.read(FieldSerializer.java:543) ~[kryo-4.0.2.jar:?]
	at co.paralleluniverse.fibers.Fiber$FiberSerializer.read(Fiber.java:2156) ~[quasar-core-0.7.12_r3-jdk8.jar:0.7.12_r3]
	at co.paralleluniverse.fibers.Fiber$FiberSerializer.read(Fiber.java:2086) ~[quasar-core-0.7.12_r3-jdk8.jar:0.7.12_r3]
	at com.esotericsoftware.kryo.Kryo.readClassAndObject(Kryo.java:813) ~[kryo-4.0.2.jar:?]
	at co.paralleluniverse.io.serialization.kryo.ReplaceableObjectKryo.readClassAndObject(ReplaceableObjectKryo.java:112) ~[quasar-core-0.7.12_r3-jdk8.jar:0.7.12_r3]
	at net.corda.nodeapi.internal.serialization.kryo.KryoCheckpointSerializer$deserialize$1$1.invoke(KryoCheckpointSerializer.kt:142) ~[corda-node-api-4.6-SNAPSHOT.jar:?]
	at net.corda.nodeapi.internal.serialization.kryo.KryoCheckpointSerializer$deserialize$1$1.invoke(KryoCheckpointSerializer.kt:44) ~[corda-node-api-4.6-SNAPSHOT.jar:?]
	at net.corda.nodeapi.internal.serialization.kryo.KryoStreams.kryoInput(KryoStreams.kt:20) ~[corda-node-api-4.6-SNAPSHOT.jar:?]
	at net.corda.nodeapi.internal.serialization.kryo.KryoCheckpointSerializer$deserialize$1.invoke(KryoCheckpointSerializer.kt:131) ~[corda-node-api-4.6-SNAPSHOT.jar:?]
	at net.corda.nodeapi.internal.serialization.kryo.KryoCheckpointSerializer$deserialize$1.invoke(KryoCheckpointSerializer.kt:44) ~[corda-node-api-4.6-SNAPSHOT.jar:?]
	at net.corda.nodeapi.internal.serialization.kryo.KryoCheckpointSerializer$kryo$1.execute(KryoCheckpointSerializer.kt:120) ~[corda-node-api-4.6-SNAPSHOT.jar:?]
	at com.esotericsoftware.kryo.pool.KryoPoolQueueImpl.run(KryoPoolQueueImpl.java:58) ~[kryo-4.0.2.jar:?]
	at net.corda.nodeapi.internal.serialization.kryo.KryoCheckpointSerializer.kryo(KryoCheckpointSerializer.kt:116) ~[corda-node-api-4.6-SNAPSHOT.jar:?]
	at net.corda.nodeapi.internal.serialization.kryo.KryoCheckpointSerializer.deserialize(KryoCheckpointSerializer.kt:130) ~[corda-node-api-4.6-SNAPSHOT.jar:?]
	at net.corda.node.services.statemachine.FlowCreator.getFiberFromCheckpoint(FlowCreator.kt:243) ~[corda-node-4.6-SNAPSHOT.jar:?]
	at net.corda.node.services.statemachine.FlowCreator.createFlowFromCheckpoint(FlowCreator.kt:80) ~[corda-node-4.6-SNAPSHOT.jar:?]
	at net.corda.node.services.statemachine.SingleThreadedStateMachineManager.retryFlowFromSafePoint(MultiThreadedStateMachineManager.kt:464) ~[corda-node-4.6-SNAPSHOT.jar:?]
	at net.corda.node.services.statemachine.ActionExecutorImpl.executeRetryFlowFromSafePoint(ActionExecutorImpl.kt:245) ~[corda-node-4.6-SNAPSHOT.jar:?]
	at net.corda.node.services.statemachine.ActionExecutorImpl.executeAction(ActionExecutorImpl.kt:70) ~[corda-node-4.6-SNAPSHOT.jar:?]
	at net.corda.node.services.statemachine.interceptors.MetricActionInterceptor.executeAction(MetricInterceptor.kt:33) ~[corda-node-4.6-SNAPSHOT.jar:?]
	at net.corda.node.services.statemachine.TransitionExecutorImpl.executeTransition(TransitionExecutorImpl.kt:47) ~[corda-node-4.6-SNAPSHOT.jar:?]
```

Most of this stack trace is not useful to you as a developer, but it does indicate what object it was trying to serialize at the time. In this scenario, it was trying to serialize a `Map` (as denoted by the `MapSerializer`). This information should allow you to determine what is going wrong.

#### Skipping checkpoints

A flow can decide to skip persisting a checkpoint when calling a suspending function. Even if this is done, the flow will still be reloaded. However, in this scenario the checkpoint that the flow loads from is an earlier checkpoint instead of the current checkpoint (since it was not saved). This is not useful for detecting deserialization errors but it checks that the flow generally handles retries correctly.

#### Idempotent/timed flows

Idempotent/timed flows always retry from their initial checkpoint when a retry is needed. Therefore, when one of these flows is reloaded when reaching a suspending function, it will load the initial checkpoint and st
