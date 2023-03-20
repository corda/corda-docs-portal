---
date: '2023-01-23'
title: "Running the Chat CorDapp"
menu:
  corda-5-beta:
    parent: corda-5-beta-utxo-example
    identifier: corda-5-beta-runchat
    weight: 2000
section_menu: corda-5-beta
---


## Configuring the Application Network (Virtual Nodes)

The CSDE is configured to create a five party application network required to run the Chat CorDapp, including virtual nodes for Alice, Bob, Charlie, Dave and a Notary. To change the network configuration, see [Configuring the Network Participants]({{< relref "../../getting-started/configure-the-network-participants/network-participants.md" >}}).

{{< note >}}
You must keep the notary node to enable the CorDapp to finalise transactions.
{{< /note >}}

## Deploying the CorDapp

To deploy and run the CorDapp, follow the same steps as outlined in the [Running Your First CorDapp]({{< relref "../../getting-started/running-your-first-cordapp/run-first-cordapp.md" >}}) section of this [Getting Started guide]({{< relref "../../getting-started/get-started.md" >}}).
However, when you come to trigger the flows, you must trigger the appropriate `ChatFlow` rather than `MyFirstFlow`.

{{< note >}}
Remember to start your docker engine before you attempt to start Corda and make sure Corda is responding to requests before deploying the CorDapp.
{{< /note >}}

## Using Swagger

For this walkthrough, we assume you are using the `Swagger GUI` to trigger flows. For each flow we use the Flow Management section of the API.
You must know the `holdingidentityshorthash` for both Alice and Bob’s nodes. You can retrieve this by running the `listVNodes` Gradle helper in the `csde-queries` section of the [gradle helper]({{< relref "../../../../5.0-beta/developing/getting-started/cordapp-standard-development-environment/csde.md" >}}) tasks.

{{< figure src="listvnodes.png" figcaption="listVnodes Gradler helper" alt="listVnodes Gradler helper" >}}

The task returns something similar to this:

{{< figure src="listvnodes-result.png" figcaption="listVnodes result" alt="listVnodes result" >}}

The vnode `holdingidentityshorthashes` (short hashes) are the 12 digit hex numbers. In the above example,  Alice’s short hash is "253501665E9D" and Bob’s is “86BC1B1A18AA”. Whenever the API requires the short hash, substitute the appropriate number depending on which vnode you want to run the flow on.

For running the flows use the `POST: /flow/{holdingidentityshorthash}/` endpoint. This requires a request body to be provided which includes:

* `clientRequestId` to uniquely identify the request

* `flowClassName` which provides the fully qualified name of the flow to be triggered

* `requestBody` which provides the input arguments for the flow

For example:

```java
   {
    "clientRequestId": "create-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.CreateNewChatFlow",
    "requestBody": {
        "chatName":"Chat with Bob",
        "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB",
        "message": "Hello Bob"
        }
}
 ```

Swagger also gives the curl command which you can use to run the request directly from the command line, for example:

  ```java
curl -X 'POST' \
  'https://localhost:8888/api/v1/flow/253501665E9D' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46YWRtaW4=' \
  -H 'Content-Type: application/json' \
  -d '{
  "clientRequestId": "create-1",
  "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.CreateNewChatFlow",
  "requestBody": {
  "chatName":"Chat with Bob",
  "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB",
  "message": "Hello Bob"
  }
  }'
```

If the flow has been successfully started, Swagger shows “START REQUESTED” response, for example:

  ```java
{
  "holdingIdentityShortHash": "253501665E9D",
  "clientRequestId": "create-1",
  "flowId": null,
  "flowStatus": "START_REQUESTED",
  "flowResult": null,
  "flowError": null,
  "timestamp": "2023-03-20T17:23:18.998Z"
  }
```

If something has gone wrong, Swagger shows an error response.
For polling for the result of a flow, use the `GET: /flow/{holdingidentityshorthash}/{clientrequestid}` endpoint. This requires the short hash of the node the flow was run against and the `clientRequestId` specified when the flow was run.

The curl version is:
  ```java
curl -X 'GET' \
  'https://localhost:8888/api/v1/flow/253501665E9D/create-1' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic YWRtaW46YWRtaW4='
  ```
If the flow has run successfully, this returns a “COMPLETED” status together with the `flowResult`.

  ```java
{
  "holdingIdentityShortHash": "253501665E9D",
  "clientRequestId": "create-1",
  "flowId": "a1109c50-b455-48e0-adf2-f1811e420bb6",
  "flowStatus": "COMPLETED",
  "flowResult": "SHA-256D:AA9C38E9EE5EA62595AD68F19DD2BA360CC665D8086045E7FFB4E7FCD3CDC24E",
  "flowError": null,
  "timestamp": "2023-03-20T17:28:49.213Z"
  }
  ```

{{< note >}}
It can take up to a minute for Corda to process the flow, this is likely a function of using the local Combined Worker version of Corda which runs all the cluster processes in one JVM with limited resources. If this were to be run in a more typical cloud deployment, you would expect it to be much faster. Whilst Corda is still processing the request, Swagger returns a “RUNNING” status. Keep polling the end point every 10 seconds or so until you get a result.
{{< /note >}}

## Typical Set of Flows

The following is a typical set of flows for a conversation between Alice and Bob:

1. Alice creates a new chat using the `POST: /flow/{holdingidentityshorthash}` endpoint and the following code:

   ```java
   {
    "clientRequestId": "create-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.CreateNewChatFlow",
    "requestBody": {
        "chatName":"Chat with Bob",
        "otherMember":"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB",
        "message": "Hello Bob"
        }
   }
   ```

   Followed by polling for status with `GET: /flow/{holdingidentityshorthash}/{clientrequestid}`. This should return “COMPLETED” after a short delay.

2. Bob lists his chats that he is a participant in using the `POST: /flow/{holdingidentityshorthash}` endpoint and the following code:

   ```java
   {
    "clientRequestId": "list-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.ListChatsFlow",
    "requestBody": {}
   }
   ```

   Followed by polling for the status with `GET: /flow/{holdingidentityshorthash}/{clientrequestid}`. This should return “COMPLETED” after a short delay. The output shows the `flowResult` with the single chat that Bob is a participant in. From this he can get the `id` number 674276c9-f311-43a6-90b8-73439bc7e28b and update the chat.

     ```java
    {
     "holdingIdentityShortHash": "86BC1B1A18AA",
     "clientRequestId": "list-1",
     "flowId": "fee5d450-4796-49ec-9347-247a9dfd4c5b",
     "flowStatus": "COMPLETED",
     "flowResult": "[{\"id\":\"674276c9-f311-43a6-90b8-73439bc7e28b\",\"chatName\":\"Chat with Bob\",\"messageFromName\":\"CN=Alice, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"Hello Bob\"}]",
     "flowError": null,
     "timestamp": "2023-01-18T10:47:13.104870Z"
     }
     ```

3. Bob updates the chat twice using the `POST: /flow/{holdingidentityshorthash}` endpoint and the following code:

   ```java
   {
    "clientRequestId": "update-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.UpdateChatFlow",
    "requestBody": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "message": "Hi Alice"
        }
   }
   ```

   {{< note >}}
   Remember to update the `id` or you will get an error or update the wrong chat.
   {{< /note >}}

   Poll for status with `GET: /flow/{holdingidentityshorthash}/{clientrequestid}` and the following code:

   ```java
   {
    "clientRequestId": "update-2",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.UpdateChatFlow",
    "requestBody": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "message": "How are you today?"
        }
   }
   ```
   Wait for “COMPLETED” status.

4. Alice uses the `POST: /flow/{holdingidentityshorthash}` endpoint and the following code to get the `id` of the chat with Bob:

   ```java
   {
    "clientRequestId": "list-2",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.ListChatsFlow",
    "requestBody": {}
   }
   ```

   Poll for status with `GET: /flow/{holdingidentityshorthash}/{clientrequestid}` and wait for “COMPLETED” status.

5. Alice checks the history on the chat with Bob using the `POST: /flow/{holdingidentityshorthash}` endpoint and the following code:

   ```java
   {
    "clientRequestId": "get-1",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.GetChatFlow",
    "requestBody": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "numberOfRecords":"4"
    }
   }
   ```

   Poll for status with `GET: /flow/{holdingidentityshorthash}/{clientrequestid}` and wait for “COMPLETED” status. The `flowResult` shows the previous messages for the chat in reverse order:

   ```java
   {
     "holdingIdentityShortHash": "253501665E9D",
     "clientRequestId": "get-1",
     "flowId": "25932ec9-ff81-4b58-bf7c-c21e67487cf9",
     "flowStatus": "COMPLETED",
     "flowResult": "[{\"messageFrom\":\"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"How are you today?\"},{\"messageFrom\":\"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"Hi Alice\"},{\"messageFrom\":\"CN=Alice, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"Hello Bob\"}]",
     "flowError": null,
     "timestamp": "2023-01-18T11:02:58.526047Z"
   }
   ```

6. Alice replies to Bob using the `POST: /flow/{holdingidentityshorthash}` endpoint and the following code:

   ```java
   {
    "clientRequestId": "update-4",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.UpdateChatFlow",
    "requestBody": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "message": "I am very well thank you"
        }
   }
   ```

   Poll for status with `GET: /flow/{holdingidentityshorthash}/{clientrequestid}` and wait for “COMPLETED” status.

7. Bob gets the chat history limited it to the last 2 entries using the `POST: /flow/{holdingidentityshorthash}` endpoint and the following code:

   ```java
   {
    "clientRequestId": "get-2",
    "flowClassName": "com.r3.developers.csdetemplate.utxoexample.workflows.GetChatFlow",
    "requestBody": {
        "id":"674276c9-f311-43a6-90b8-73439bc7e28b",
        "numberOfRecords":"2"
    }
   }
   ```

   Poll for status with `GET: /flow/{holdingidentityshorthash}/{clientrequestid}` and wait for “COMPLETED” status. The `resultData` should show the last two messages in the chat:

   ```java
   {
     "holdingIdentityShortHash": "86BC1B1A18AA",
     "clientRequestId": "get-2",
     "flowId": "7dd326dc-31b5-42b7-b20b-ca8512b076db",
     "flowStatus": "COMPLETED",
     "flowResult": "[{\"messageFrom\":\"CN=Alice, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"I am very well thank you\"},{\"messageFrom\":\"CN=Bob, OU=Test Dept, O=R3, L=London, C=GB\",\"message\":\"How are you today?\"}]",
     "flowError": null,
     "timestamp": "2023-01-18T11:09:13.282302Z"
   }
   ```
