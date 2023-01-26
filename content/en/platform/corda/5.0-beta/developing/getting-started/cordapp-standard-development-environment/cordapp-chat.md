---
date: '2023-01-23'
title: "Chat CorDapp"
menu:
  corda-5-beta:
    parent: corda-5-beta-start
    identifier: corda-5-beta-chatcordapp
    weight: 3000
section_menu: corda-5-beta
---

## ChatState

The foundation for the Chat app is the ChatState which is the data model for facts recorded to the ledger. It can be represented in the CDL as follows:

{{< figure src="chat-state.png" figcaption="Data model for facts recorded to the ledger" alt="Data model for facts recorded to the ledger" >}}

Where:

* `id` is a unique identifier for the chat. It is the equivalent of a `linearId` in Corda 4 and is the common identifier for all the states in the backchain for a particular chat between two participants. (`LinearStates` and `LinearId` are not implemented yet in Corda 5, as of Beta 1).
* `chatName` is a human readable name for the chat. It does not guarantee uniqueness.

* `messageFrom` is the `MemberX500Name` for the virtual node which created this `ChatState`.
* message is the message in the Chat.
* participants is the list of PublicKeys belonging to the Vnodes of the participants of the chat.

The history of a chat will be recorded in the backchain of the chat.

### Chat Smart Contract

The Smart Contract (combination of the ChatState and ChatContract) can be represented by a simple Smart Contract View diagram:

{{< figure src="chat-smart-contract-view.png" figcaption="Smart Contract View diagram" alt="Smart Contract View diagram" >}}

Points to note:

* In CDL the arrows represent transactions with the indicated command type. The state at the beginning of the arrow represents the input state, the state at the end of the arrow represents the output state for the transaction.
* There is no ChatState status in this simple design.

* The multiplicities (numbers on the arrows) indicate that for the create command there should be no input state and one output ChatState.

* The multiplicities for the update command indicates there should be one input ChatState and one output ChatState.

* SC: indicates the signing constraint, that is who needs to sign the transaction. In this case both participants for both the create and update commands.

* The universal constraint applies to all transactions, in this case that there should always be only two  participants in the ChatState.

### Chat State Evolution

The evolution of the ledger when stepping through the walkthrough steps can be shown using the CDL State evolution view:

{{< figure src="chat-state-evolution-view.png" figcaption="CDL state evolution view" alt="CDL state evolution view" >}}

* The Create transaction has no input and starts a new chat with a unique id. The id operates similarly to the Corda 4  `LinearStateId`, which has not been implemented yet in Corda 5.
* Each Update transaction creates the new ChatState as an output and consumes the previous ChatState as an input.
* To recreate the historic conversation the back chain is traversed from newest (unconsummed) state to oldest.

### Chat Flows

There are six flows in the Chat Application:

<table>
<col style="width:30%">
<col style="width:20%">
<col style="width:20%">
<col style="width:50%">
<thead>
<tr>
<th>Flow</th>
<th>Flow type</th>
<th>Inputs</th>
<th>Action</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>CreateNewChatFlow </code></td>
<td><code>RPCStartableFlow </code></td>
<td><code>chatName,otherMember,message</code></td>
<td> Forms a draft transaction using the transaction builder, which creates a new ChatState with the details provided. Signs the draft transaction with the VNodes first Ledger Key. Calls <code>FinalizeChatSubFlow</code> which finalizes the transaction.</td>
</tr>
<tr>
<td><code>UpdateChatFlow </code></td>
<td><code>RPCStartableFlow </code></td>
<td><code> id, message </code></td>
<td> Locates the last message in the backchain for the given id.Creates a draft transaction which consumes the last message in the chain and creates a new chatState with the latest message. Signs the draft transaction with the VNodes first Ledger Key.  Calls <code>FinalizeChatSubFlow</code> which finalises the transaction. </td>
</tr>
<tr>
<td><code>ListChatsFlow </code></a></td>
<td><code>RPCStartableFlow </code></td>
<td><code>none</code></td>
<td>Calls <code>FinalizeChatSubFlow</code> which finalises the transaction.</td>
</tr>
<tr>
<td><code>GetChatsFlow </code></td>
<td><code>RPCStartableFlow </code></td>
<td><code>id, numberofRecords </code></td>
<td>Reads the backchain to a depth of `numberOfRecords` for a given id. Returns the list of messages together with who sent them.</td>
</tr>
<tr>
<td><code>FinalizeChatFlow </code></td>
<td><code>SubFlow </code></td>
<td><code>signedTransaction (to finalize),otherMember </code></td>
<td>The common subflow used by both by both <code>CreateNewChatFlow</code> and <code>UpdateChatFlow</code>. This removes the need to duplicate the responder code. Sets up a session with the <code>FinalizeChatResponderFlow</code> and calls the finality() function. finality()/ receiveFinality() functions, collects required signatures, notarises the transaction and stores the finalized transaction to the respective vaults.</td>
</tr>
<tr>
<td><code>FinalizeChatResponderFlow</code></td>
<td><code>ResponderFlow </code></td>
<td><code>FlowSession  </code></td>
<td>Runs the <code>receiveFinality()</code> function which performs the responder side of the finality() function.<code>ReceiveFinality()<code> takes a Lambda verifier which runs validations on the transactions.The validator checks for banned words and checks that the message comes from the same party as the messageFrom field.</td>
</tr>
</tbody>
</table>

## Configuring the Application Network (Virtual Nodes)

The CSDE is configured to create a four party application network required to run the Chat Cordapp, including virtual nodes for Alice, Bob, Charlie and a Notary. If you want to change the network configuration please see section [Configuring the Network Participants](../../getting-started/configure-the-network-participants/network-participants.md)

{{< note >}}
You will need to keep the notary party otherwise the application will not be able to finalise transactions.
{{< /note >}}

## Deploying the CorDapp

To deploy and run the CorDapp you will follow the same steps as outlined in the [Running Your First CorDapp](../../getting-started/running-your-first-cordapp/run-first-cordapp.md) section of this getting started guide.
However, when you come to trigger the flows you will need to trigger the appropriate `ChatFlow` rather than `MyFirstFlow`.
Remember to start your docker engine before you attempt to start Corda and make sure Corda is responding to requests before deploying the CorDapp.

## Using Swagger

For this walkthrough we will assume you are using the `Swagger GUI` to trigger flows. For each flow we will be using the Flow Management section of the API.
You will need to know the `holdingidentityshorthash` for both Alice and Bob’s nodes, you can get this by running the `listVNodes` Gradle helper in the csde-queries section of the gradle helper tasks.

{{< figure src="listvnodes.png" figcaption="listVnodes Gradler helper" alt="listVnodes Gradler helper" >}}

Which will return something similar to this:

{{< figure src="listvnodes-result.png" figcaption="listVnodes result" alt="listVnodes result" >}}

The Vnode `holdingidentityshorthashes` (short hashes) are the 12 digit hex numbers. In the above Alice’s short hash is "17F49B05B2B5" and Bob’s is “8C73E39AF476”. Whenever the API requires the short hash substitute the appropriate number depending on which Vnode you want to run the flow on.

For running the flows we will use the POST: /flow/{holdingidentityshorthash}/ end point. This requires a request body to be provided which includes:

* clientRequestId to uniquely identify the request

* flowClassName which provides the fully qualified name of the flow to be triggered

* requestData which provides the input arguments for the flow

For example:

```java
   {
    "clientRequestId": "create-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.CreateNewChatFlow",
    "requestData": {
        "chatName":"Chat with Bob",
        "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB",
        "message": "Hello Bob"
        }
}
 ```

Swagger will also give you the curl command which can be used to run the request directly from the command line, for example:

  ```java
curl -X 'POST' \
  'https://localhost:8888/api/v1/flow/17F49B05B2B5' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "clientRequestId": "create-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.CreateNewChatFlow",
    "requestData": {
        "chatName":"Chat with Bob",
        "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB",
        "message": "Hello Bob"
        }
}'
```

If the flow has been successfully started Swagger will show a “START REQEUSTED” response, for example:

  ```java
{
  "holdingIdentityShortHash": "17F49B05B2B5",
  "clientRequestId": "create-1",
  "flowId": null,
  "flowStatus": "START_REQUESTED",
  "flowResult": null,
  "flowError": null,
  "timestamp": "2023-01-18T09:45:25.911889Z"
}
```

If something has gone wrong you will get an error response.
For polling for the result of a flow we will use the GET: /flow/{holdingidentityshorthash}/{clientrequestid} endpoint. This requires the short hash of the node the flow was run against and the clientRequestId specified when the flow was run.

The curl version is:
curl -X 'GET' \
  'https://localhost:8888/api/v1/flow/17F49B05B2B5/create-1' \
  -H 'accept: application/json'
If the flow has run successfully this will return a “COMPLETED” Status together with the flowResult.

  ```java
{
  "holdingIdentityShortHash": "17F49B05B2B5",
  "clientRequestId": "create-1",
  "flowId": "fa0dec91-4a94-476c-8b1b-82dc95a55134",
  "flowStatus": "COMPLETED",
  "flowResult": "SHA-256D:FACC6487F3478D69A543CE7061611C8792C0FBC1FCC4903742ABF82E0D8F1D14",
  "flowError": null,
  "timestamp": "2023-01-18T10:36:16.889777Z"
}
```

{{< note >}}
It can take up to a minute for Corda to Process the flow, this is likely a function of using the local Combined Worker version of Corda which runs all the cluster processes in one JVM with limited resources. If this were to be run in a more typical cloud deployment you would expect it to be much faster. Whilst corda is still processing the request you would get a “RUNNING” status returned. Keep polling the end point every 10 seconds or so until you get a result.
{{< /note >}}

## Typical Set of Flows

A typical set of flows for a conversation between Alice and Bob would be as follows:

1. Alice Creates an new Chat using the CreateNewChatFlow

POST: /flow/{holdingidentityshorthash}

  ```java
{
    "clientRequestId": "create-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.CreateNewChatFlow",
    "requestData": {
        "chatName":"Chat with Bob",
        "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB",
        "message": "Hello Bob"
        }
}
```

Followed by polling for status with `GET: /flow/{holdingidentityshorthash}/{clientrequestid}`
It should return “COMPLETED” after a short delay.

2. Bob lists his Chats that he is a participant in using the `ListChatFlow`.
POST: /flow/{holdingidentityshorthash}  

  ```java
{
    "clientRequestId": "list-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.ListChatsFlow",
    "requestData": {}
}
```

Followed by polling for status with: `GET: /flow/{holdingidentityshorthash}/{clientrequestid}`
It should return “COMPLETED” after a short delay. The output shows the flowResult with the single chat that Bob is a participant in. From this he can get the id number `674276c9-f311-43a6-90b8-73439bc7e28b` which he needs to update the chat.

  ```java
{
  "holdingIdentityShortHash": "8C73E39AF476",
  "clientRequestId": "list-1",
  "flowId": "fee5d450-4796-49ec-9347-247a9dfd4c5b",
  "flowStatus": "COMPLETED",
  "flowResult": "[{\"id\":\"674276c9-f311-43a6-90b8-73439bc7e28b\",\"chatName\":\"Chat with Bob\",\"messageFromName\":\"CN=Alice, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"Hello Bob\"}]",
  "flowError": null,
  "timestamp": "2023-01-18T10:47:13.104870Z"
}
 ```

3. Bob updates the chat twice using UpdateChatFlow.
POST: /flow/{holdingidentityshorthash}

  ```java
{
    "clientRequestId": "update-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.UpdateChatFlow",
    "requestData": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "message": "Hi Alice"
        }
}
 ```

{{< note >}}
Remember to update the id otherwise you will get an error or update the wrong chat.
{{< /note >}}

Polling for status with GET: /flow/{holdingidentityshorthash}/{clientrequestid}, wait for “COMPLETED” status.
POST: /flow/{holdingidentityshorthash}

  ```java
{
    "clientRequestId": "update-2",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.UpdateChatFlow",
    "requestData": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "message": "How are you today?"
        }
}
```

Polling for status with GET: /flow/{holdingidentityshorthash}/{clientrequestid}, wait for “COMPLETED” statuses.

4. Alice uses ListCHatsFlow to get the id of the chat with Bob.
POST: /flow/{holdingidentityshorthash}

  ```java
{
    "clientRequestId": "list-2",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.ListChatsFlow",
    "requestData": {}
}
```

Polling for status with GET: /flow/{holdingidentityshorthash}/{clientrequestid}, wait for “COMPLETED” status.

5. Alice checks the history on the chat with Bob using GetChatFlow.
POST: /flow/{holdingidentityshorthash}

  ```java
{
    "clientRequestId": "get-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.GetChatFlow",
    "requestData": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "numberOfRecords":"4"
    }
}
```

Polling for status with GET: /flow/{holdingidentityshorthash}/{clientrequestid}, wait for “COMPLETED” status. The flowResult will show the previous messages for the chat in reverse order:

  ```java
{
  "holdingIdentityShortHash": "17F49B05B2B5",
  "clientRequestId": "get-1",
  "flowId": "25932ec9-ff81-4b58-bf7c-c21e67487cf9",
  "flowStatus": "COMPLETED",
  "flowResult": "[{\"messageFrom\":\"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"How are you today?\"},{\"messageFrom\":\"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"Hi Alice\"},{\"messageFrom\":\"CN=Alice, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"Hello Bob\"}]",
  "flowError": null,
  "timestamp": "2023-01-18T11:02:58.526047Z"
}
```

6. Alice replies to Bob using the UpdateChatFlow.
POST: /flow/{holdingidentityshorthash}

  ```java
{
    "clientRequestId": "update-4",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.UpdateChatFlow",
    "requestData": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "message": "I am very well thank you"
        }
}
```

Polling for status with GET: /flow/{holdingidentityshorthash}/{clientrequestid}, wait for “COMPLETED” status.

7. Bob get the chat history using GetChatFlow, but limits it to the last 2 entries.
POST: /flow/{holdingidentityshorthash}

  ```java

{
    "clientRequestId": "get-2",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.GetChatFlow",
    "requestData": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "numberOfRecords":"2"
    }
}
```

Polling for status with GET: /flow/{holdingidentityshorthash}/{clientrequestid}, wait for “COMPLETED” status. The resultData should show the last two messages in the chat:

  ```java
{
  "holdingIdentityShortHash": "8C73E39AF476",
  "clientRequestId": "get-2",
  "flowId": "7dd326dc-31b5-42b7-b20b-ca8512b076db",
  "flowStatus": "COMPLETED",
  "flowResult": "[{\"messageFrom\":\"CN=Alice, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"I am very well thank you\"},{\"messageFrom\":\"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"How are you today?\"}]",
  "flowError": null,
  "timestamp": "2023-01-18T11:09:13.282302Z"
}
```
