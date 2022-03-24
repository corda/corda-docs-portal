---
date: '2021-09-23'
section_menu: tutorials
menu:
  tutorials:
    identifier: corda-community-4-9-tutorial-basic-cordapp-int-test
    parent: corda-community-4-9-tutorial-basic-cordapp-intro
    weight: 1070
tags:
- tutorial
- cordapp
title: Write integration tests
---

This tutorial guides you through writing integration tests for your CorDapp. Integration tests allow you to test all features of your CorDapp together.

You will be creating your integration tests in this directory: `workflows/src/test/java/com/tutorial/`

## Learning objectives

After you've completed this tutorial, you will be able to write integration tests for your CorDapp.

## Before you start

Before you start writing your own unit tests:

* Read the [API: Testing](../../../../../platform/corda/4.8/open-source/api-testing.md) documentation.
* Download `TemplateInitiator.java` and `TemplateContract.java` from the [CorDapp tutorial repository](https://github.com/corda/samples-java/tree/master/Basic/tutorial-applestamp).
* Move `TemplateState.java` into your `com.tutorial` package.

## Write the `CreateAndIssueAppleStamp` integration test

When writing flow unit tests, you rely on both states and contracts to test the functionality of the flow. You also must create a `MockNetwork` with `StartedMockNode`s. `StartedMockNode`s behave like normal Corda nodes, but their services are mocked out.

Flow tests are generally more complicated, so we recommend having a file for each flow you wish to test.

Follow these steps to write a flow unit test for the `CreateAndIssueAppleStampTest`:

### Add the `MockNetwork` and `StartedMockNode`s

1. Create a file called `CreateAndIssueAppleStampTest`.
2. Add the `CreateAndIssueAppleStampTest` public class.
3. Add the private `MockNetwork` and a network name.
4. Add two private `StartedMockNode`s named `a` and `b`.

So far, your code should look like this:

```java
package com.tutorial;

import net.corda.testing.node.MockNetwork;
import net.corda.testing.node.StartedMockNode;

public class CreateAndIssueAppleStampTest {
    private MockNetwork network;
    private StartedMockNode a;
    private StartedMockNode b;
```

### Add the CorDapp details

Next you must indicate where your CorDapp is so that the test engine can run:

1. Add a `@Before` annotation to indicate that this is what must happen before the test is run.
2. Add a `public void setup` including the `new MockNetwork` and `new MockNetworkParameters`. Use `withCordappsForAllNodes` to reference the CorDapp.
3. Add  the function `TestCorDapp.findCordapp` to find the contracts and flows `.jar`s (`com.tutorial.contracts` and `com.tutorial.flows`, respectively).
4. Create an `a` and `b` node using `createPartyNode`. Use `null` for the `legalName` of the node to use the default.
5. Add the `runNetwork` command to start the `MockNetwork`.

So far, your code should look like this:

```java
package com.tutorial;

import com.google.common.collect.ImmutableList;
import net.corda.testing.node.MockNetwork;
import net.corda.testing.node.MockNetworkParameters;
import net.corda.testing.node.StartedMockNode;
import net.corda.testing.node.TestCordapp;
import org.junit.Before;

public class CreateAndIssueAppleStampTest {
    private MockNetwork network;
    private StartedMockNode a;
    private StartedMockNode b;

    @Before
    public void setup() {
        network = new MockNetwork(new MockNetworkParameters().withCordappsForAllNodes(ImmutableList.of(
                TestCordapp.findCordapp("com.tutorial.contracts"),
                TestCordapp.findCordapp("com.tutorial.flows"))));
        a = network.createPartyNode(null);
        b = network.createPartyNode(null);
        network.runNetwork();
    }
```

### Add an `@After` annotation and steps to tear down the network

After your test has run, you will want the network to be torn down to free up resources on your machine.

1. Add an `@After` annotation.
2. Add a `tearDown` method.
3. Inside the method, add `stopNodes` command to stop the nodes on the `network`.

### Add the test content

Now that you've added steps for before and after, you can finally add the content that will test your `CreateAndIssueAppleStamp` flow.

1. Add the `@Test` annotation.
2. Add a `public void` with the `CreateAndIssueAppleStampTest`.
3. Reference the flow that is being tested to create the test flow. Here you should reference both the parent class of the flow (`CreateAndIssueAppleStamp`) and the initiating subflow (`CreateAndIssueAppleStampInitiator`). Call this `flow1` in your test.
4. Add the `stampDescription` from your initiating flow with sample content - for example, `stampDescription: "Honey Crisp 4072"`.
5. Reference the `b` node that you added in your `MockNetwork` using `getInfo`, `getLegalIdentities`, and `get(0)` methods. This will return a party, completing the constructor.
6. You need a node to run the test flow you just created. Use node `a` and the `startFlow` command to start `flow1`.
7. Add a `runNetwork` command to start the network and test the flow.

### Add `QueryCriteria`

To verify that the flow test has run and the flow works, you must query the database of one of the `StartedMockNode`s to see if the transaction was successfully stored. Since `a` initiated the flow, you must check the database of node `b` to ensure that the state was successfully issued to them.

1. Create a query with `VaultQueryCriteria`.
2. In the `VaultQueryCriteria`, look for a status of `UNCONSUMED` using the `withStatus` method.
3. Add your query for the `AppleStamp` state. Use the `getServices` and `getVaultService` methods to query node `b`'s vault.
4. Return a list of states with `getStates`, then return the reference of the first of these states with `get(0)`. Return `getState` to get the state, then `getData` to extract the data from the state. This gives you an `AppleStamp` object.
5. `assert` this `AppleStamp` object to verify that the `stampDesc` matches the example content you entered (`Honey Crisp 4072`).

After you have finished writing the query, your flow test is finished and your code should look like this:

```java
package com.tutorial;

import com.google.common.collect.ImmutableList;
import com.tutorial.flows.CreateAndIssueAppleStamp;
import com.tutorial.flows.TemplateInitiator;
import com.tutorial.states.AppleStamp;
import com.tutorial.states.TemplateState;
import net.corda.core.node.services.Vault;
import net.corda.core.node.services.vault.QueryCriteria;
import net.corda.core.transactions.SignedTransaction;
import net.corda.testing.node.MockNetwork;
import net.corda.testing.node.MockNetworkParameters;
import net.corda.testing.node.StartedMockNode;
import net.corda.testing.node.TestCordapp;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.util.concurrent.Future;

public class CreateAndIssueAppleStampTest {
    private MockNetwork network;
    private StartedMockNode a;
    private StartedMockNode b;

    @Before
    public void setup() {
        network = new MockNetwork(new MockNetworkParameters().withCordappsForAllNodes(ImmutableList.of(
                TestCordapp.findCordapp("com.tutorial.contracts"),
                TestCordapp.findCordapp("com.tutorial.flows"))));
        a = network.createPartyNode(null);
        b = network.createPartyNode(null);
        network.runNetwork();
    }

    @After
    public void tearDown() {
        network.stopNodes();
    }

    @Test
    public void dummyTest() {
        TemplateInitiator flow = new TemplateInitiator(b.getInfo().getLegalIdentities().get(0));
        Future<SignedTransaction> future = a.startFlow(flow);
        network.runNetwork();

        //successful query means the state is stored at node b's vault. Flow went through.
        QueryCriteria inputCriteria = new QueryCriteria.VaultQueryCriteria().withStatus(Vault.StateStatus.UNCONSUMED);
        TemplateState state = b.getServices().getVaultService()
                .queryBy(TemplateState.class,inputCriteria).getStates().get(0).getState().getData();
    }

    @Test
    public void CreateAndIssueAppleStampTest(){
        CreateAndIssueAppleStamp.CreateAndIssueAppleStampInitiator flow1 =
                new CreateAndIssueAppleStamp.CreateAndIssueAppleStampInitiator(
                        "HoneyCrispy 4072",this.b.getInfo().getLegalIdentities().get(0));
        Future<SignedTransaction> future1 = a.startFlow(flow1);
        network.runNetwork();

        //successful query means the state is stored at node b's vault. Flow went through.
        QueryCriteria inputCriteria = new QueryCriteria.VaultQueryCriteria()
                .withStatus(Vault.StateStatus.UNCONSUMED);
        AppleStamp state = b.getServices().getVaultService()
                .queryBy(AppleStamp.class,inputCriteria).getStates().get(0).getState().getData();
        assert(state.getStampDesc().equals("HoneyCrispy 4072"));
    }




}
```

Take a look at the [Apple Stamp CorDapp solution](https://github.com/corda/samples-java/tree/master/Basic/tutorial-applestamp) to see the implementation of integration tests for the `RedeemApples` flow and the `PackageApples` flow.
