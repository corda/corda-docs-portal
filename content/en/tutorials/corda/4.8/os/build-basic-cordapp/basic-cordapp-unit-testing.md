---
aliases:
- /docs/corda-os/4.8/tutorial-test-dsl.html
- /docs/platform/corda/4.8/os/tutorial-test-dsl.html
- /docs/corda-os/4.8/flow-testing.html
- /docs/platform/corda/4.8/os/flow-testing.html
date: '2021-09-23'
section_menu: tutorials
menu:
  tutorials:
    identifier: corda-os-4-8-tutorial-basic-cordapp-unit-test
    parent: corda-os-4-8-tutorial-basic-cordapp-intro
    weight: 1070
tags:
- tutorial
- cordapp
title: Write unit tests
---

This tutorial guides you through writing unit tests for the states, contracts, and flows in your CorDapp. Unit tests allow you to test the individual features of your CorDapp.

You will be creating your unit tests in these directories:

* State tests - `contracts/src/test/java/com/tutorial/contracts`
* Contract tests - `contracts/src/test/java/com/tutorial/contracts`
* Flow tests - `workflows/src/test/java/com/tutorial/`

## Learning objectives

After you've completed this tutorial, you will be able to write state, contract, and flow unit tests for your CorDapp.

## Before you start

Before you start writing your own unit tests, read the [API: Testing](../../../../../platform/corda/4.8/open-source/api-testing.md) documentation.

## Write state tests

This tutorial shows you how to write simple tests that check if the states have the correct parameter types. State tests can be more complex, but this example demonstrates a basic test you can implement.

You do not need to have the contract or flows created to run these state tests.

You can write all of your state tests in the same file, as shown in this tutorial, or you can create a file for each state test.

Follow these steps to write state tests:

1. Create a file called `StateTests`.
2. Add the `StateTests` public class.
3. Add the `@Test` annotation.
4. Add a class definition for `hasFieldOfCorrectType` and throw an exception called `NoSuchFieldException`.
5. Fill the class with the `TemplateState` version of the test:
```java
TemplateState.class.getDeclaredField("msg");
        assert (TemplateState.class.getDeclaredField("msg").getType().equals(String.class));
```
Your code should now look like this:
```java
package com.tutorial.contracts;

import com.tutorial.states.TemplateState;
import org.junit.Test;

public class StateTests {

    //Mock State test check for if the state has correct parameters type
    @Test
    public void hasFieldOfCorrectType() throws NoSuchFieldException {
        TemplateState.class.getDeclaredField("msg");
        assert (TemplateState.class.getDeclaredField("msg").getType().equals(String.class));
    }
```

Use the template test above to create another class with tests for the parameters from the `AppleStamp` state:

* `stampDesc` - `String`
* `issuer` - `Party`
* `holder` - `Party`

### Check your work

After you have finished, your state test is complete and your code should look like this:

```java
package com.tutorial.contracts;

import com.tutorial.states.AppleStamp;
import com.tutorial.states.TemplateState;
import net.corda.core.identity.Party;
import org.junit.Test;

public class StateTests {

    //Mock State test check for if the state has correct parameters type
    @Test
    public void hasFieldOfCorrectType() throws NoSuchFieldException {
        TemplateState.class.getDeclaredField("msg");
        assert (TemplateState.class.getDeclaredField("msg").getType().equals(String.class));
    }

    @Test
    public void AppleStampStateHasFieldOfCorrectType() throws NoSuchFieldException {
        AppleStamp.class.getDeclaredField("stampDesc");
        assert (AppleStamp.class.getDeclaredField("stampDesc").getType().equals(String.class));

        AppleStamp.class.getDeclaredField("issuer");
        assert (AppleStamp.class.getDeclaredField("issuer").getType().equals(Party.class));

        AppleStamp.class.getDeclaredField("holder");
        assert (AppleStamp.class.getDeclaredField("issuer").getType().equals(Party.class));
    }

}
```

## Write a contract test

In the contract test, you will use a feature called `MockServices` to fake a transaction in order to test the contract code. You include the contract `.jar` with the `MockServices` you create to include everything from the contract folder and perform this test. This means that for the contract test, you need both the state and contract to be created.

### Add `MockServices` and `TestIdentity`

Follow these steps to create the `MockServices` and mock identities to use when running the test:

1. Create a file called `ContractTests`.
2. Add the `ContractTests` public class.
3. Add the private function `MockServices` and reference the `com.tutorial.contracts` `.jar` file.
4. Add two `TestIdentity`s, giving them both X500 names.

After adding the `MockServices` and `TestIdentity`s, your code should look like this:

```java
package com.tutorial.contracts;

import net.corda.core.identity.CordaX500Name;
import net.corda.testing.core.TestIdentity;
import net.corda.testing.node.MockServices;
import org.junit.Test;

import java.util.Arrays;

import static net.corda.testing.node.NodeTestUtils.ledger;


public class ContractTests {
    private final MockServices ledgerServices = new MockServices(Arrays.asList("com.tutorial.contracts"));
    TestIdentity alice = new TestIdentity(new CordaX500Name("Alice",  "TestLand",  "US"));
    TestIdentity bob = new TestIdentity(new CordaX500Name("Alice",  "TestLand",  "US"));
```

### Use the template contract test to add Apple Stamp contract tests

The template CorDapp includes the following template contract test:

```java
@Test
public void issuerAndRecipientCannotHaveSameEmail() {
    TemplateState state = new TemplateState("Hello-World",alice.getParty(),bob.getParty());
    ledger(ledgerServices, l -> {
        l.transaction(tx -> {
            tx.input(TemplateContract.ID, state);
            tx.output(TemplateContract.ID, state);
            tx.command(alice.getPublicKey(), new TemplateContract.Commands.Send());
            return tx.fails(); //fails because of having inputs
        });
        l.transaction(tx -> {
            tx.output(TemplateContract.ID, state);
            tx.command(alice.getPublicKey(), new TemplateContract.Commands.Send());
            return tx.verifies();
        });
        return null;
    });
}
```
Follow this example to write two tests that check:

* That the stamp issuance can only have one output. Call this test `StampIssuanceCanOnlyHaveOneOutput`.
* That the stamp has a description. Call this test `StampMustHaveDescription`.

### Check your work

After you have completed both the `StampIssuanceCanOnlyHaveOneOutput` and `StampMustHaveDescription` tests, your contract tests are complete and your code should look like this:

```java
package com.tutorial.contracts;

import com.tutorial.states.AppleStamp;
import com.tutorial.states.TemplateState;
import net.corda.core.contracts.UniqueIdentifier;
import net.corda.core.identity.CordaX500Name;
import net.corda.testing.core.TestIdentity;
import net.corda.testing.node.MockServices;
import org.junit.Test;

import java.util.Arrays;

import static net.corda.testing.node.NodeTestUtils.ledger;


public class ContractTests {
    private final MockServices ledgerServices = new MockServices(Arrays.asList("com.tutorial.contracts"));
    TestIdentity alice = new TestIdentity(new CordaX500Name("Alice",  "TestLand",  "US"));
    TestIdentity bob = new TestIdentity(new CordaX500Name("Alice",  "TestLand",  "US"));

    //Template Tester
    @Test
    public void issuerAndRecipientCannotHaveSameEmail() {
        TemplateState state = new TemplateState("Hello-World",alice.getParty(),bob.getParty());
        ledger(ledgerServices, l -> {
            l.transaction(tx -> {
                tx.input(TemplateContract.ID, state);
                tx.output(TemplateContract.ID, state);
                tx.command(alice.getPublicKey(), new TemplateContract.Commands.Send());
                return tx.fails(); //fails because of having inputs
            });
            l.transaction(tx -> {
                tx.output(TemplateContract.ID, state);
                tx.command(alice.getPublicKey(), new TemplateContract.Commands.Send());
                return tx.verifies();
            });
            return null;
        });
    }

    //Basket of Apple cordapp testers
    @Test
    public void StampIssuanceCanOnlyHaveOneOutput(){
        AppleStamp stamp = new AppleStamp("FUji4072", alice.getParty(),bob.getParty(),new UniqueIdentifier());
        AppleStamp stamp2 = new AppleStamp("HoneyCrispy7864", alice.getParty(),bob.getParty(),new UniqueIdentifier());

        ledger(ledgerServices, l -> {
            l.transaction(tx -> {
                tx.output(AppleStampContract.ID, stamp);
                tx.output(AppleStampContract.ID, stamp2);
                tx.command(alice.getPublicKey(), new AppleStampContract.Commands.Issue());
                return tx.fails(); //fails because of having inputs
            });
            l.transaction(tx -> {
                tx.output(AppleStampContract.ID, stamp);
                tx.command(alice.getPublicKey(), new AppleStampContract.Commands.Issue());
                return tx.verifies();
            });
            return null;
        });
    }

    @Test
    public void StampMustHaveDescription(){
        AppleStamp stamp = new AppleStamp("", alice.getParty(),bob.getParty(),new UniqueIdentifier());
        AppleStamp stamp2 = new AppleStamp("FUji4072", alice.getParty(),bob.getParty(),new UniqueIdentifier());

        ledger(ledgerServices, l -> {
            l.transaction(tx -> {
                tx.output(AppleStampContract.ID, stamp);
                tx.command(Arrays.asList(alice.getPublicKey(),bob.getPublicKey()), new AppleStampContract.Commands.Issue());
                return tx.fails(); //fails because of having inputs
            });
            l.transaction(tx -> {
                tx.output(AppleStampContract.ID, stamp2);
                tx.command(Arrays.asList(alice.getPublicKey(),bob.getPublicKey()), new AppleStampContract.Commands.Issue());
                return tx.verifies();
            });
            return null;
        });
    }


}
```

## Write a flow test

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
4. Return a list of states with `getStates` then return the reference of the first of these states with `get(0)`. Return `getState` to get the state then `getData` to extract the data from the state. This gives you an `AppleStamp` object.
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

Take a look at the [`AppleStamp` CorDapp solution](XXX) to see the implementation of flow tests for the `RedeemApples` flow and the `PackageApples` flow.

## Next steps

Now that you know how to write unit tests, learn how to [run your CorDapp](XXX) then write [Integration tests](../supplmentary-tutorials/tutorial-integration-testing.md).
