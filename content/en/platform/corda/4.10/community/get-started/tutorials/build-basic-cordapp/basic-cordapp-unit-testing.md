---
date: '2023-01-12'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-tutorial-basic-cordapp-unit-test
    parent: corda-community-4-10-tutorial-basic-cordapp-intro
    weight: 100
tags:
- tutorial
- cordapp
title: Write unit tests
---

This tutorial guides you through writing unit tests for the states and contracts in your CorDapp. Unit tests allow you to test the individual features of your CorDapp.

You will be creating your unit tests in these directories:

* State tests - `contracts/src/test/java/com/tutorial/contracts`.
* Contract tests - `contracts/src/test/java/com/tutorial/contracts`.

{{< note >}}
You cannot create unit tests with flows because they depend on states and contracts to run. Use integration tests to test the functionality of your flows and entire CorDapp. Learn how to create an integration test in the [Write integration tests](basic-cordapp-int-testing.md) tutorial.
{{< /note >}}

## Learning objectives

After you've completed this tutorial, you will be able to write state and contract unit tests for your CorDapp.

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

* `stampDesc` - `String`.
* `issuer` - `Party`.
* `holder` - `Party`.

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

In the contract test, you will use a feature called `MockServices` to fake a transaction in order to test the contract code. You must include the contract `.jar` with the `MockServices` you create. This ensures that everything from the contract folder is available for testing. To run the contract test, you must have both the contracts and states created.

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

## Next steps

Now that you know how to write unit tests, learn how to [run your CorDapp](basic-cordapp-running.md) then write [Integration tests](basic-cordapp-int-testing.md).
