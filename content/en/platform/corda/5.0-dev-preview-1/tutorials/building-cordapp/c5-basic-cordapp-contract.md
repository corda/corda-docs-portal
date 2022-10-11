---
date: '2021-09-15'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-contract
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1040
tags:
- tutorial
- cordapp
title: Write a simple contract
---

[Contracts](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-contracts.md) define the rules of how states can evolve. A CorDapp can have more than one contract, and each contract defines rules for one or more states. The contract governs the execution of [transactions](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-transactions.html) that update the ledger by marking zero or more existing ledger states as historic (the inputs), and producing zero or more new ledger states (the outputs). The contract(s) ensures that input and output states in transactions are valid and prevents invalid transactions from occurring. All parties that wish to transact in a network must run the same contract(s) for any transaction they’re a party to, verifying that the transaction is valid.

Contracts are classes that implement the `Contract` interface. They must override the `verify` method. The `verify` method takes transactions as input and evaluates them against rules defined as a `requireThat` element. Contract execution must be deterministic, and transaction acceptance is based on the transaction’s contents alone. Contract verification is the final step that governs the evolution of the ledger, thus it can only address on-ledger facts.

A transaction that is not contractually valid is not a valid proposal to update the ledger, therefore it can never be committed to the ledger. In this way, contracts impose rules on the evolution of states over time that are independent of the willingness of the required signers to sign a given transaction.

Contract verification is not the only type of validation that you can apply in your CorDapp—you can use [workflows](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/flows/overview.html) to perform validation as well.

This tutorial guides you through writing the two contracts you need in your CorDapp: `MarsVoucherContract` and `BoardingTicketContract`. You will link these contracts to the states that you created in the [states](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-state.md) tutorials.

You will create these contracts in the `contracts/src/main/<kotlin>/net/corda/missionMars/contracts/` directory. Refer to the `TemplateContract.kt` file in this directory to see a template contract.

## Learning objectives

When you have completed this tutorial, you will know how to create and implement contracts in a Corda 5 Developer Preview CorDapp to restrict how your transaction flows are performed.

## Create the `MarsVoucherContract` contract

The `MarsVoucherContract` contract verifies actions performed on the `MarsVoucher` state.

1. Right-click the **contracts** folder.

2. Select **New > Kotlin Class/File**.

3. In the **New Kotlin Class/File** window, select **Class** and name the file `MarsVoucherContract`.

  {{< note >}}
  When naming contracts, it’s best practice to match your contract and state names. In this case the contract is called `MarsVoucherContract`, and the state that links to it is called `MarsVoucher`. Follow this naming convention when you write an original CorDapp to avoid confusion.
  {{< /note >}}

4. Open the file.

### Create the contract class

A Corda state typically has a corresponding contract class to document the rules/policy of that state when used in a transaction.

To declare the contract class, add the class name `MarsVoucherContract` that implements the `Contract` class.

{{< note >}}
As you are writing the contract, you will notice that IntelliJ prompts you to add imports that correspond to elements you've added. Add the relevant imports to all suggested elements.
When adding imports, ignore `BoardingTicketContract` that is in red—you will add it in the [Create the `BoardingTicketContract`](#create-the-boardingticketcontract) section.
{{< /note >}}

This is what your code should look like now:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.contracts;

class MarsVoucherContract : Contract {

}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.contracts;

public class MarsVoucherContract implements Contract {

}
```
{{% /tab %}}

{{< /tabs >}}

### Connect the `MarsVoucherContract` to the `MarsVoucher` state

After creating the contract class in a CorDapp, you must connect the contract to its correlating state. Add the `@BelongsToContract` annotation *in the state class* to establish the relationship between a state and a contract. Without this, your state does not hold a relationship to the contract that is used to verify it.

1. Open your `MarsVoucher` class.

2. Annotate the `MarsVoucher` data class with the `@BelongsToContract` annotation.

Transactions involving the `MarsVoucher` state are now verified using the `MarsVoucherContract`.

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.LinearState

@BelongsToContract(MarsVoucherContract::class)
data class MarsVoucher (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: Party, //The party who issued the voucher
        val holder: Party, //The party who currently owns the voucher
        override val linearId: UniqueIdentifier,//LinearState required variable
) ...
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.states;

import net.corda.missionMars.contracts.MarsVoucherContract;
import net.corda.v5.application.identity.AbstractParty;
import net.corda.v5.application.identity.Party;
import net.corda.v5.application.utilities.JsonRepresentable;
import net.corda.v5.ledger.UniqueIdentifier;
import net.corda.v5.ledger.contracts.BelongsToContract;
import net.corda.v5.ledger.contracts.LinearState;

@BelongsToContract(MarsVoucherContract.class)
public class MarsVoucher implements LinearState, JsonRepresentable {

    private String voucherDesc;
    private Party issuer;
    private Party holder;
    private UniqueIdentifier linearId;

    ......
}
```
{{% /tab %}}

{{< /tabs >}}

### Define commands

[Commands](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-transactions.html#commands) are built into a transaction to indicate its intent. They control the type of actions performed to the state that the contract can verify.

Each command is associated with a list of signers. The public keys listed in a contract's commands indicate the transaction's required signers.

In the `MarsVoucherContract`, you need a command that issues an instance of the `MarsVoucher`, which creates a new state on the ledger. You also need a command that transfers the `MarsVoucher` state to a new holder.

1. Extend the `CommandData` interface into a new interface called `Commands`.

2. Within the `Commands` interface, create a class named `Issue`, implementing its parent interface.

3. Within the `Commands` interface, create a class named `Transfer`, implementing its parent interface.

This is what your code should look like now:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.contracts;

class MarsVoucherContract : Contract {

  // Used to indicate the transaction's intent.
  interface Commands : CommandData {
      class Issue : Commands
      class Transfer: Commands
  }

}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
public class MarsVoucherContract implements Contract {

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will only have one command.
        class Issue implements MarsVoucherContract.Commands {}
        class Transfer implements MarsVoucherContract.Commands {}
    }
}
```
{{% /tab %}}

{{< /tabs >}}

### Add the contract's ID

To identify your contract when building transactions, add its ID.

{{< note >}}
This ID is not used in the production environment, but it is used in testing scenarios. It's best practice to add it to the contract.
{{< /note >}}

This is what your code should look like now:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.contracts;

class MarsVoucherContract : Contract {

  // Used to indicate the transaction's intent.
  interface Commands : CommandData {
      class Issue : Commands
      class Transfer: Commands
  }

companion object {
    // This is used to identify our contract when building a transaction.
    const val ID = "com.tutorial.contracts.MarsVoucherContract"
  }
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
public class MarsVoucherContract implements Contract {

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will only have one command.
        class Issue implements MarsVoucherContract.Commands {}
        class Transfer implements MarsVoucherContract.Commands {}
    }

    // This is used to identify our contract when building a transaction.
    public static final String ID = "net.corda.missionMars.contracts.MarsVoucherContract";
}
```
{{% /tab %}}

{{< /tabs >}}

### Add the `verify` method

The `verify` method is automatically triggered when your transaction is executed. It verifies that the transaction components are following the restrictions implemented inside the contract's `verify` method.

In this case, the `verify` method must confirm:
* That there will only be one `MarsVoucher` state as an output of the transaction.
* That relevant trip information (the `voucherDesc`) is included in the state.
* That when the `MarsVoucher` state is transferred, the transaction consumes one `MarsVoucher` state.
* That the holder cannot issue the `MarsVoucher` to themselves.

1. If you're using IntelliJ, you will see an error indicator under the class name and implementation. This indicates that the class is missing the required method. Hover over the class definition, then:

   * On macOS: press **Option** + **Enter**.

   * On Windows: press **Alt** + **Enter**.

2. Click **Implement members**.

   The **Implement Members** window appears.

3. In the **Implement Members** window, select **verify(tx: LedgerTransaction): Unit**. Click **OK**.

4. Extract the command from the transaction.

5. Verify the transaction according to its intention using the Lambda `when-is` expression.

6. Implement domain-specific language (DSL) `requireThat` helper method to the `Issue` verification code.

{{< note >}}

This is a Corda-specific helper method used for writing contracts only.

{{< /note >}}

You have now finished writing the `MarsVoucherContract`. Your code should look like this:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.contracts

import net.corda.missionMars.states.MarsVoucher
import net.corda.v5.ledger.contracts.CommandData
import net.corda.v5.ledger.contracts.Contract
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.transactions.LedgerTransaction


//Domain Specific Language
class MarsVoucherContract : Contract {

    override fun verify(tx: LedgerTransaction) {

        //Extract the command from the transaction.
        val commandData = tx.commands[0].value

        //Verify the transaction according to the intention of the transaction
        when (commandData) {
            is Commands.Issue -> requireThat {
                val output = tx.outputsOfType(MarsVoucher::class.java)[0]
                "This transaction should only have one MarsVoucher state as output".using(tx.outputs.size == 1)
                "The output MarsVoucher state should have clear description of the type of Space trip information".using(output.voucherDesc != "")
                null
            }
            is BoardingTicketContract.Commands.RedeemTicket-> requireThat {
                //Transaction verification will happen in BoardingTicket Contract
            }
            is Commands.Transfer -> requireThat {
                "This transaction should consume one Marsvoucher states".using(tx.inputStates.size == 1)
                val input = tx.inputsOfType(MarsVoucher::class.java)[0]
                val output = tx.outputsOfType(MarsVoucher::class.java)[0]
                "You cannot gift the voucher to yourself".using(input.holder != output.holder)
                null
            }
        }
    }





    // Used to indicate the transaction's intent.
    interface Commands : CommandData {
        //In our Mission Mars app, we have two commands.
        class Issue : Commands
        class Transfer: Commands
    }

    companion object {
        // This is used to identify our contract when building a transaction.
        @JvmStatic
        val ID = "net.corda.missionMars.contracts.MarsVoucherContract"
    }
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
```java
package net.corda.missionMars.contracts;

import net.corda.missionMars.states.MarsVoucher;
import net.corda.v5.ledger.contracts.CommandData;
import net.corda.v5.ledger.contracts.Contract;
import net.corda.v5.ledger.transactions.LedgerTransaction;
import org.jetbrains.annotations.NotNull;

import static net.corda.v5.ledger.contracts.ContractsDSL.requireThat;

public class MarsVoucherContract implements Contract {
    // This is used to identify our contract when building a transaction.
    public static final String ID = "net.corda.missionMars.contracts.MarsVoucherContract";

    @Override
    public void verify(@NotNull LedgerTransaction tx) {
        final CommandData commandData = tx.getCommands().get(0).getValue();
        if (commandData instanceof MarsVoucherContract.Commands.Issue) {
            //Retrieve the output state of the transaction
            MarsVoucher output = tx.outputsOfType(MarsVoucher.class).get(0);

            //Using Corda DSL function requireThat to replicate conditions-checks
            requireThat(require -> {
                require.using("This transaction should only have one MarsVoucher state as output", tx.getOutputs().size() == 1);
                require.using("The output MarsVoucher state should have clear description of the type of Space trip information", !(output.getVoucherDesc().equals("")));
                return null;
            });
        }else if(commandData instanceof MarsVoucherContract.Commands.Transfer){
            //Retrieve the output state of the transaction
            MarsVoucher output = tx.outputsOfType(MarsVoucher.class).get(0);
            MarsVoucher input = tx.inputsOfType(MarsVoucher.class).get(0);
            requireThat(require -> {
                require.using("You cannot gift the voucher to yourself", !(input.getHolder().equals(output.getHolder())));
                return null;
            });

        }else if(commandData instanceof BoardingTicketContract.Commands.RedeemTicket){
            //Transaction verification will happen in BoardingTicket Contract
        }
    }

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will only have one command.
        class Issue implements MarsVoucherContract.Commands {}
        class Transfer implements MarsVoucherContract.Commands {}

    }
}

```
{{% /tab %}}

{{< /tabs >}}

## Next steps

Now that you have written the first contract for the Mission Mars CorDapp, <a href="../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-contract-2.md">write the `BoardingTicket` contract</a>.  
