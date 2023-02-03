---
date: '2023-01-13'
menu:
  corda-enterprise-4-7:
    identifier: corda-enterprise-4-7-tutorial-basic-cordapp-running
    parent: corda-enterprise-4-7-tutorial-basic-cordapp-intro
    weight: 110
tags:
- tutorial
- cordapp
title: Run your CorDapp
---

## Learning objectives

After you have completed this tutorial, you will know how to deploy, launch, and interact with the CorDapp that you built by following the previous tutorials.

The Corda network needed for this CorDapp includes one notary and two nodes, each representing a party in the network - Farmer Bob and Peter. A Corda node is an individual instance of Corda representing one party in a network.

Deploy and run your CorDapp on the test nodes:

* `Notary`, which runs a notary service.
* `PartyA`.
* `PartyB`.

## Before you start

Before you run your CorDapp, check your work against the [Apple Stamp CorDapp Java solution](https://github.com/corda/samples-java/tree/master/Basic/tutorial-applestamp).

## Deploy the CorDapp locally

1. Open the command line from the root of your project.

2. Compile your code into a Java application by running the `deployNodes` Gradle task:

* Unix/macOS: `./gradlew clean deployNodes`.
* Windows: `gradlew.bat clean deployNodes`.

This builds three nodes with the CorDapp installed on them.

3. When the build finishes, go to the `build/nodes` folder.

You will see:

* A folder for each generated node
* A `runnodes` shell script for running all the nodes simultaneously on macOS.
* A `runnodes.bat` batch file for running all the nodes simultaneously on Windows.

{{< note >}}

`deployNodes` is a utility task that can be used in a development environment to create a new set of nodes for testing a CorDapp. In a production environment, you would create a single node instead, and build your CorDapp `.jar`s.

{{< /note >}}


## Launch the sample CorDapp

To start the nodes and the sample CorDapp, run the command that corresponds to your operating system:

* Unix/macOS: `./build/nodes/runnodes`.
* Windows: `.\build\nodes\runnodes.bat`.


{{< note >}}

On Unix/macOS, do not click/change focus until all seven additional terminal windows have opened, or some nodes may fail to start. You can run `/build/nodes/runnodes --headless` to prevent each server from opening in a new terminal window.

{{< /note >}}

The `runnodes` script creates a node tab/window for each node. It usually takes about 60 seconds for all the nodes to start. Each node displays `Welcome to the Corda interactive shell` along with a prompt.


## Interact with your CorDapp

Follow the instructions in this section to interact with your CorDapp as Farmer Bob (`PartyA` node) and Peter (`PartyB` node).

### Create and issue the `AppleStamp` voucher

In this first part of the process, Farmer Bob creates and issues a voucher to Peter for the apples he wishes to buy. He includes a description of the apples Peter requested (`Fuji4072`) and indicates that Peter is the holder of this new `AppleStamp`.

1. Go to the `PartyA` node window and run the command:

`flow start CreateAndIssueAppleStampInitiator stampDescription: Fuji4072, holder: PartyB`

This issues the `AppleStamp` to Peter. Farmer Bob and Peter both will have a copy of the `AppleStamp` voucher in their vaults.

2. Pull the data from the vault to verify if your transaction is performed correctly. Run the following command on both `PartyA` and `PartyB` nodes:

`run vaultQuery contractStateType: com.tutorial.states.AppleStamp`

You should see the same information in both vaults.

### Package apples

Next, Farmer Bob prepares the amount of apples Peter requested by self-issuing a `BasketofApples` state.

1. Go to the `PartyA` node window and run the command:

`flow start PackApplesInitiator appleDescription: Fuji10472, weight: 10`

2. Pull the data from the vault to verify if your transaction was performed correctly. This is a self-issuance transaction so run this command on the `PartyA` node only:

`run vaultQuery contractStateType: com.tutorial.states.BasketOfApple`

If you run the same query on the `PartyB` node, you won't get any data because they were not involved in this transaction.

### Redeem the `AppleStamp` voucher

Finally, Peter goes to the orchard to pick up his apples and redeems his voucher. The voucher is marked as spent and Farmer Bob gives Peter his apples.

1. Go to the `PartyA` node window and run this command:

`flow start RedeemApplesInitiator buyer: PartyB, stampId: <voucher ID of the voucher that you created in step 1>`

2. Now you can query `PartyB` again to verify if they redeemed their `AppleStamp` voucher correctly:

`run vaultQuery contractStateType: com.tutorial.states.BasketOfApples`

## Next steps

Follow the [Write integration tests](basic-cordapp-int-testing.md) tutorial to finish this learning path.
