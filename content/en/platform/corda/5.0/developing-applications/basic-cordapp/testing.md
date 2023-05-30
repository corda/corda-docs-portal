---
date: '2023-05-03'
title: "Test Your CorDapp"
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-first-cordapp-testing
    parent: corda5-develop-first-cordapp
    weight: 5000
---

# Test Your CorDapp

This tutorial guides you through the steps required to execute the flows you have previously created,
to confirm the CorDapp works as expected.

## Learning Objectives

Once you have completed this tutorial, you will know how to execute flows and analyse the results of these
flows to confirm correct behaviour of your CorDapp.

## Before You Start

Before you run your flows, you must install the CSDE environment.
The CSDE environment will automatically provision a notary virtual node, in addition to virtual nodes for four participants
– Alice, Bob, Charlie, and Dave. You will use the Bob and Dave virtual nodes for your flows. They represent the farmer
and the customer referenced in the earlier tutorials.

1. Follow the [CSDE environment instructions]({{< relref "../getting-started/cordapp-standard-development-environment/csde.md" >}})
to start the Corda combined worker and to deploy the static network.
2. Once done, confirm that the nodes are available by running the `listVNodes` gradle task. It should return something like the following:
```shell
CPI Name		 Holding identity short hash 		X500 Name
MyCorDapp		E18496F580F4 		CN=Bob, OU=Test Dept, O=R3, L=London, C=GB
MyCorDapp		19F285FA7192 		CN=Alice, OU=Test Dept, O=R3, L=London, C=GB
MyCorDapp		943300F6BD04 		CN=Charlie, OU=Test Dept, O=R3, L=London, C=GB
NotaryServer		82E04CE54296 		CN=NotaryRep1, OU=Test Dept, O=R3, L=London, C=GB
MyCorDapp		715E366736B2 		CN=Dave, OU=Test Dept, O=R3, L=London, C=GB
```
3. **Optional:** You may need to run this a few times following network setup, to give the system chance to update
the data being broadcast following registration.
4. Take note of the holding ID short hash for both Bob and Dave. You will need these when running flows.

## Running Flows

Now that you have created virtual nodes and your CorDapp has been installed on these, you can test the code that
you have written in the previous tutorials.

### Verify the Flow Installation

To ensure that your flows are available on the virtual nodes you will be using, perform a sanity check:

1. Following the [CSDE documentation]({{< relref "../getting-started/cordapp-standard-development-environment/csde.md" >}})
steps, open the Swagger UI and log in.
2. Use the `GET flowclass/{holdingidentityshorthash}` endpoint to list the flows available.
You should do this specifying the holding identities that you noted down earlier for both Bob and Dave.
The returned classes should contain the flow classes that you wrote in earlier tutorials.

### Issue an `AppleStamp`

First, Bob the farmer will issue Dave the customer an `AppleStamp` which Dave can exchange for a basket of applies
at a future time.

1. use the `POST /flow/{holdingidentityshorthash}` endpoint, specifying Bob’s holding ID
and the following request body with Dave’s name as the holder:

```kotlin
{
  "clientRequestId": "create-stamp-1",
  "flowClassName": "com.r3.developers.apples.workflows.CreateAndIssueAppleStampFlow",
  "requestBody": {
    "stampDescription": "Can be exchanged for a single basket of apples",
    "holder": "CN=Dave, OU=Test Dept, O=R3, L=London, C=GB"
  }
}
```

2. To confirm successful issuance of the stamp, run the `GET /flow/{holdingidentityshorthash}/{clientrequestid}` endpoint,
specifying Bob’s holding ID again, and the client request ID used in the previous step.

You should observe that the `flowStatus` in the response is completed, and `flowResult` contains a UUID.

3. Make a note of the UUID, as this is the ID of the newly issued stamp, which you will use again later.

### Create `BasketOfApples`

Farmer Bob now has a `BasketOfApples` which he wishes to put on the ledger so that it can be redeemed for an `AppleStamp`.

1. Repeat the instructions from the previous section, but use the following request body, which invokes a different flow:

```kotlin
{
  "clientRequestId": "package-apples-1",
  "flowClassName": "com.r3.developers.apples.workflows.PackageApplesFlow",
  "requestBody": {
    "appleDescription": "Golden delicious apples, picked on 11th May 2023",
    "weight": 214
  }
}
```

2. Check the result of this flow.

The `flowStatus` in the response should be completed. In this case, we do not care about the
flow result as this is not required to redeem the `AppleStamp`.

### Redeem the `AppleStamp` for a `BasketOfApples`

Finally, Dave can redeem his `AppleStamp`.

1. Start a new flow against Bob’s virtual node. The request body in this case should be:

```kotlin
{
  "clientRequestId": "redeem-apples-1",
  "flowClassName": "com.r3.developers.apples.workflows.RedeemApplesFlow",
  "requestBody": {
    "buyer": "CN=Dave, OU=Test Dept, O=R3, L=London, C=GB",
    "stampId": "<The stamp id noted earlier>"
  }
}
```

The `flowStatus` in the response should also be completed. Following this step, the `AppleStamp` has been spent,

## Error Scenarios

The above steps show the “happy path”. However, you may wish to execute some further flows to ensure that your contract
validation works as expected. Some additional scenarios to try are:

* Try redeeming the original `AppleStamp` again. You can do this by entering a new flow as you did when following the steps
for redeeming the `AppleStamp`, but with a new client request ID. The transaction should fail with an error indicating
that an `AppleStamp` with the specified ID could not be found.
* Repeat all the steps for issuing an `AppleStamp`, but get another virtual node (for example, Charlie) to
issue an `AppleStamp` to Dave, rather than Bob doing this. On redemption, the transaction should fail because Bob
does not recognise the `AppleStamp` ID provided.
* Repeat all the steps for redeeming the `AppleStamp`, but on redemption, Bob tries to redeem Dave’s
`AppleStamp` by specifying himself as the buyer. This should be rejected. Similarly, attempting to specify a different
entity altogether (for example, Charlie) should also be rejected.
