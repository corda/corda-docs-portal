---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-monitoring-logging
tags:
- checkpoint
- tooling
title: Troubleshooting stuck flows
weight: 120
---

When flows become

Use the checkpoint tools to diagnose the causes of stuck flows.

1. Use the `flow watch` command to see the flows in progress on your node. The output should look like this:

    ```none
    Id                                Flow name                                                           Initiator                        Status
    -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    15f16740-4ea2-4e48-bcb3-fd9051d5b Cash Issue And Payment                                              bankUser                         In progress
    1c6c3e59-26aa-4b93-8435-4e34e265e Cash Issue And Payment                                              bankUser                         In progress
    90613d6f-be78-41bd-98e1-33a756c28 Cash Issue And Payment                                              bankUser                         In progress
    43c7d5c8-aa66-4a98-beed-dc91354d0 Cash Issue And Payment                                              bankUser                         In progress
    Waiting for completion or Ctrl-C ...
    ```
2.

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

Note that "In progress" indicates the flows above have not completed (and will have been checkpointed).


* Check the main node log file for *hospitalisation* and/or *flow retry* messages: `<NODE_BASE>\logs\node-<hostname>.log`

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

You will now see an addition line in the main node log file as follows:

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
