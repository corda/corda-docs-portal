---
title: "Starting flows"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing-exposing-rpc
    identifier: corda-5-dev-preview-1-nodes-developing-exposing-rpc-start-flow
    weight: 2200
section_menu: corda-5-dev-preview
description: >
  How to allow flows to be invoked using HTTP-RPC.
expiryDate: '2022-09-28'
---

Use this guide to allow flows to be invoked using HTTP-RPC.

As part of the Corda 5 Developer Preview, you can start flows using the `FlowStarterRPCOps` interface and add annotation
to expose them via the HTTP server.

{{< note >}}

To invoke a flow via HTTP-RPC:
* The flow must be annotated with `StartableByRPC`.
* The flow must have a constructor annotated with `@JsonConstructor` taking a single parameter of type `RpcStartFlowRequestParameters`.

{{< /note >}}

## Use the `startFlow` method

The `startFlow` method uses the endpoint: `https://[baseUrl]/startflow` and
requires `RpcStartFlowRequest` as a body parameter. Here's an example:

```kotlin
@HttpRpcResource(
        name = "FlowStarterRPCOps",
        description = "FlowStarterRPCOps",
        path = "flowstarter"
)
interface FlowStarterRPCOps :  RPCOps {
    @HttpRpcPOST
    fun startFlow(
            @HttpRpcRequestBodyParameter(
                    description = "httpRpcFlowRequest",
                    required = true
            )
            rpcStartFlowRequest: RpcStartFlowRequest): RpcStartFlowResponse
}
```

When implemented, the `startFlow` method:
1. Looks up the specified flow.
2. Checks if the user has permission to start the flow.
3. Instantiates the flow via the constructor that takes an `RpcStartFlowRequestParameters` parameter and executes it.
4. Returns an `RpcStartFlowResponse`.

### Add `RpcStartFlowRequest` as an input to `startFlow`

To allow flows to be invoked using HTTP-RPC, you need to add `RpcStartFlowRequest` to the `startFlow` method with this
structure:
```kotlin
data class RpcStartFlowRequest(
        val flowName: String,
        val clientId: String,
        val parameters: RpcStartFlowRequestParameters
)
```

Once the flow is discovered by its full name (package name and class name), it is instantiated with the
`RpcStartFlowRequestParameters` parameter.
The flow's developer needs to deserialize this parameter and initialize the flow class.

```kotlin
data class RpcStartFlowRequestParameters(val parametersInJson: String)
```

### Expected output from `RpcStartFlowResponse`

`startFlow` extracts and returns relevant information from `FlowStateMachineHandle` (once it's available). You should
see a response that contains a unique identifier for a single state machine run and the client id.

```kotlin
data class RpcStartFlowResponse (
        val stateMachineRunId: StateMachineRunId,
        val clientId: String?)
```

## Manage user permissions

To start a flow via HTTP-RPC, a user needs:
1. Permission to invoke the `startFlow` method `InvokeRpc:net.corda.client.rpc.flow.FlowStarterRPCOps#startFlow`.
2. Permission to execute the flow(s) that the user wants to start. For example `startflow.net.corda.finance.flows.ExampleFlowClass`.

Here is an example of a `node.conf` section that allows the user `demouser` to execute the flow `MessageStateIssue` via HTTP-RPC:

 ```shell
security {
    authService {
        dataSource {
            type=INMEMORY
            users=[
                  {
                      password=test
                      permissions=["InvokeRpc:net.corda.client.rpc.flow.FlowStarterRPCOps#startFlow",
"startflow.net.corda.httprpcdemo.workflows.MessageStateIssue"
                      ]
                      user=demouser
                  }
            ]
        }
    }
}
```

## `startFlow` example in the HTTP-RPC demo

The `README.md` file of the HTTP-RPC demo sample contains instructions on how to build and run the HTTP-RPC demo.
Once it is up and running, you can execute `MessageStateIssue` via HTTP-RPC by passing in this body parameter to the
`startflow` endpoint:

```json
{
  "rpcStartFlowRequest": {
    "clientId": "id",
    "flowName": "net.corda.httprpcdemo.workflows.MessageStateIssue",
    "parameters": {
      "parametersInJson": "{\"message\":\"hello\"}"
    }
  }
}
```
