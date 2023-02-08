---
date: '2023-01-12'
menu:
  corda-enterprise-4-10:
    identifier: corda-enterprise-4-10-tutorial-basic-cordapp-contract
    parent: corda-enterprise-4-10-tutorial-basic-cordapp-intro
    weight: 80
tags:
- tutorial
- cordapp
title: Write contracts
---

This tutorial guides you through writing the two contracts you need in your CorDapp: `AppleStampContract` and `BasketOfApplesContract`. You will link these contracts to the states that you created in the [Write the states](basic-cordapp-state.md) tutorial.

You will create these contracts in the `contracts/src/main/java/com/template/contracts/` directory in this tutorial. Refer to the `TemplateContract.java` file in this directory to see a template contract.


## Learning objectives

Once you have completed this tutorial, you will know how to create and implement contracts in a CorDapp to restrict how your transaction flows are performed.


## Create the `AppleStampContract` contract

First, create the `AppleStampContract`. This contract verifies actions performed by the `AppleStamp` state.

1. Right-click the **contracts** folder.
2. Select **New > Java Class**.
3. Create a file called `AppleStampContract`.

   {{< note >}}
   When naming contracts, it’s best practice to match your contract and state names. In this case the contract is called `AppleStampContract`, and the state that links to it is called `AppleStamp`. Follow this naming convention when you write an original CorDapp to avoid confusion.
   {{< /note >}}

4. Open the file.


### Declare the public class

A Corda state typically has a corresponding contract class to document the rules/policy of that state when used in a transaction. To declare the contract class:

1. Add the public class `AppleStampContract` that implements the `Contract` class.

2. Identify your contract by adding its ID.

   {{< note >}}
   This ID is not used in the production environment, but it is used in the testing scenarios. It's best practice to add it to the contract.
   {{< /note >}}

This is what your code should look like now:

```java
package com.tutorial.contracts;

public class AppleStampContract implements Contract {

    // This is used to identify our contract when building a transaction.
    public static final String ID = "com.tutorial.contracts.AppleStampContract";
}
```

### Add commands

Commands indicate the transaction's intent — what type of actions performed by the state the contract can verify. In this tutorial, you will add two commands: one for issuing the bushel of apples, and one for redeeming it.

1. Add the `Commands` public interface declaration.

2. Inside the interface, add the `Issue` and `Redeem` classes that implement `AppleStampContract.Commands`.


This is what your code should look like now:

```java
package com.tutorial.contracts;

public class AppleStampContract implements Contract {


    // This is used to identify our contract when building a transaction.
    public static final String ID = "com.tutorial.contracts.AppleStampContract";


    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will have two commands.
        class Issue implements AppleStampContract.Commands {}
    }
}
```

### Add the `verify` method

The `verify` method is automatically triggered when your transaction is executed. It verifies that the transaction components are following the restrictions implemented inside the contract's `verify` method.

1. If you're using IntelliJ, you will see an error indicator under the class name and implementation. This indicates that the class is missing the required method. Hover over the class definition, then:

   * On macOS: press **Option** + **Enter**.

   * On Windows: press **Alt** + **Enter**.

2. Select **Implement methods > verify** from the dropdown menu.

   The `verify` method preceded by the `@Override` annotation appears.

3. Extract the command from the transaction.

4. Verify the intention of the transaction (Issue or Redeem) using the `if-then-else` loop.

5. Add this domain-specific language (DSL) `requireThat` helper method to the issue verification code:

   ```java
   requireThat(require -> {
       require.using("This transaction should only output one AppleStamp state", tx.getOutputs().size() == 1);
       require.using("The output AppleStamp state should have clear description of the type of redeemable goods", !output.getStampDesc().equals(""));
       return null;
   });
   ```

   {{< note >}}

   This is a Corda-specific helper method used for writing contracts only.

   {{< /note >}}

6. When the intention of the transaction is not recognized by the `verify` method, use `else` to throw an error.

This is what your code should look like now:

```java
package com.tutorial.contracts;

public class AppleStampContract implements Contract {


    // This is used to identify our contract when building a transaction.
    public static final String ID = "com.tutorial.contracts.AppleStampContract";

    @Override
    public void verify(@NotNull LedgerTransaction tx) throws IllegalArgumentException {

        //Extract the command from the transaction.
        final CommandData commandData = tx.getCommands().get(0).getValue();

        //Verify the transaction according to the intention of the transaction
        if (commandData instanceof AppleStampContract.Commands.Issue){
            AppleStamp output = tx.outputsOfType(AppleStamp.class).get(0);
            requireThat(require -> {
                require.using("This transaction should only have one AppleStamp state as output", tx.getOutputs().size() == 1);
                require.using("The output AppleStamp state should have clear description of the type of redeemable goods", !output.getStampDesc().equals(""));
                return null;
            });
        }else if(commandData instanceof BasketOfApplesContract.Commands.Redeem){
            //Transaction verification will happen in BasketOfApples Contract
        }
        else{
            //Unrecognized Command type
            throw new IllegalArgumentException("Incorrect type of AppleStamp Commands");
        }
    }

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will have two commands.
        class Issue implements AppleStampContract.Commands {}
    }
}
```

### Add imports

If you're using IntelliJ or another IDE, the IDE will automatically add the imports you need.

IntelliJ indicates that an import is missing with red text. To add the import:

1. Click the red text.

   A pop-up that says "Unresolvable reference: {name of the missing input}" appears.

2. Automatically import the missing variable:

   * On macOS: press **Option** + **Enter**.
   * On Windows: press **Alt** + **Enter**.

3. Repeat this process for all missing imports.

When you have added all the missing imports, you have finished writing the `AppleStampContract`. Your code should now look like this:

```java
package com.tutorial.contracts;

import com.tutorial.states.AppleStamp;
import com.tutorial.states.BasketOfApples;
import net.corda.core.contracts.CommandData;
import net.corda.core.contracts.Contract;
import net.corda.core.transactions.LedgerTransaction;
import org.jetbrains.annotations.NotNull;

import static net.corda.core.contracts.ContractsDSL.requireThat; //Domain Specific Language


public class AppleStampContract implements Contract {

    // This is used to identify our contract when building a transaction.
    public static final String ID = "com.tutorial.contracts.AppleStampContract";

    @Override
    public void verify(@NotNull LedgerTransaction tx) throws IllegalArgumentException {

        //Extract the command from the transaction.
        final CommandData commandData = tx.getCommands().get(0).getValue();

        //Verify the transaction according to the intention of the transaction
        if (commandData instanceof AppleStampContract.Commands.Issue){
            AppleStamp output = tx.outputsOfType(AppleStamp.class).get(0);
            requireThat(require -> {
                require.using("This transaction should only have one AppleStamp state as output", tx.getOutputs().size() == 1);
                require.using("The output AppleStamp state should have clear description of the type of redeemable goods", !output.getStampDesc().equals(""));
                return null;
            });
        }else if(commandData instanceof BasketOfApplesContract.Commands.Redeem){
            //Transaction verification will happen in BasketOfApple Contract
        }
        else{
            //Unrecognized Command type
            throw new IllegalArgumentException("Incorrect type of AppleStamp Commands");
        }
    }

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will have two commands.
        class Issue implements AppleStampContract.Commands {}
    }
}
```

## Create the `BasketOfApplesContract`

The `BasketOfApplesContract` has two intentions:

* Farmer Bob creates the basket of apples. This intention is expressed by the `packBasket` command.
* Peter redeems the `BasketOfApples` state. This intention is expressed by the `Redeem` command.

The rules inside the `verify` method in the `requireThat` Corda DSL helper method are:

* For the `packBasket` command:

  * This transaction should only output one `BasketOfApples` state.
  * The output of the `BasketOfApples` state should have a clear description of the apple product.
  * The output of the `BasketOfApples` state should have a non-zero weight.

* For the `Redeem` command:

  * The transaction should consume two states.
  * The issuer of the `AppleStamp` should be the producing farm of this basket of apples.
  * The weight of the basket of apples must be greater than zero.


### Check your work

Once you've written the `BasketOfApplesContract`, check your code against the sample below. Your code should look like this:

```java
package com.tutorial.contracts;

import com.tutorial.states.AppleStamp;
import com.tutorial.states.BasketOfApples;
import net.corda.core.contracts.CommandData;
import net.corda.core.contracts.Contract;
import net.corda.core.transactions.LedgerTransaction;
import org.jetbrains.annotations.NotNull;

import static net.corda.core.contracts.ContractsDSL.requireThat;

public class BasketOfApplesContract implements Contract {

    // This is used to identify our contract when building a transaction.
    public static final String ID = "com.tutorial.contracts.BasketOfApplesContract";


    @Override
    public void verify(@NotNull LedgerTransaction tx) throws IllegalArgumentException {
        //Extract the command from the transaction.
        final CommandData commandData = tx.getCommands().get(0).getValue();

        if (commandData instanceof BasketOfApplesContract.Commands.packBasket){
            BasketOfApples output = tx.outputsOfType(BasketOfApples.class).get(0);
            requireThat(require -> {
                require.using("This transaction should only output one BasketOfApples state", tx.getOutputs().size() == 1);
                require.using("The output BasketOfApples state should have clear description of Apple product", !output.getDescription().equals(""));
                require.using("The output BasketOfApples state should have non zero weight", output.getWeight() > 0);
                return null;
            });
        }
        else if (commandData instanceof BasketOfApplesContract.Commands.Redeem) {
            //Retrieve the output state of the transaction
            AppleStamp input = tx.inputsOfType(AppleStamp.class).get(0);
            BasketOfApples output = tx.outputsOfType(BasketOfApples.class).get(0);

            //Using Corda DSL function requireThat to replicate conditions-checks
            requireThat(require -> {
                require.using("This transaction should consume two states", tx.getInputStates().size() == 2);
                require.using("The issuer of the Apple stamp should be the producing farm of this basket of apple", input.getIssuer().equals(output.getFarm()));
                require.using("The basket of apple has to weight more than 0", output.getWeight() > 0);
                return null;
            });
        }
        else{
            //Unrecognized Command type
            throw new IllegalArgumentException("Incorrect type of BasketOfApples Commands");
        }
    }

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        class packBasket implements BasketOfApplesContract.Commands {}
        class Redeem implements BasketOfApplesContract.Commands {}

    }
}
```

## Next steps

Follow the [Write flows](basic-cordapp-flows.md) tutorial to continue on this learning path.
