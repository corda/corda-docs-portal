---
date: '2021-09-15'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-contract-2
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1045
tags:
- tutorial
- cordapp
title: Write a complex contract
expiryDate: '2022-09-28'
---

Before you try writing a complex contract, make sure you try [a simple one first](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-contract.md). Then, you're ready to write this `BoardingTicketContract`.

The `BoardingTicketState` is used when the Mars Express creates the ticket and when the customer redeems the ticket. This means that the `BoardingTicketContract` needs a `Commands` interface with commands for both uses.

The `requireThat` Corda DSL helper method has two sets of rules.

* For the `CreateTicket` command:

  * The transaction should only output one `BoardingTicket` state.
  * The output `BoardingTicket` state should have a clear description of the space trip.
  * The output `BoardingTicket` state should have a launch date later then the creation time.

* For the `RedeemTicket` command:

  * The transaction should consume two states. This ensures that the `MarsVoucher` and `BoardingTicket` states cannot be used for more than one trip.
  * The issuer of the `BoardingTicket` should be the space company that created the boarding ticket.
  * The output `BoardingTicket` state should have a launch date later than the creation time.

### Set up the `BoardingTicketContract` class

First, create the `BoardingTicketContract`. This contract verifies actions performed on the `BoardingTicket` state.

1. Right-click the **contracts** folder.

2. Select **New > Kotlin Class/File**.

3. In the **New Kotlin Class/File** window, select **Class** and name the file `BoardingTicketContract`.

4. Open the file.

### Create the contract class

Corda states typically have a corresponding contract class to document the rules/policy of that state when used in a transaction. To declare the contract class:

Add the class name `BoardingTicketContract`, which implements the `Contract` class.

This is what your code should look like now:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.contracts;

class BoardingTicketContract : Contract {

}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.contracts;

public class BoardingTicketContract implements Contract {

}
```
{{% /tab %}}

{{< /tabs >}}

### Connect the `BoardingTicketContract` to the `BoardingTicket` state

After creating the contract class in a CorDapp, you must connect the contract to its correlating state. Add the `@BelongsToContract` annotation *in the state class* to establish the relationship between a state and a contract. Without this, your state does not hold a relationship to the contract that is used to verify it.

1. Open your `BoardingTicket` class.
2. Insert the `@BelongsToContract` annotation with the `BoardingTicketContract` just before the definition of the `BoardingTicket` data class.

Transactions involving the `BoardingTicket` state are now verified using the `BoardingTicketContract`.

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.contracts.ContractState
import java.time.LocalDate
import java.util.*

@BelongsToContract(BoardingTicketContract::class)
data class BoardingTicket(
        var description : String, //Trip information
        var marsExpress : Party, //Party selling the ticket
        var owner: Party, //The party who exchanges the ticket for the voucher
        var launchDate: LocalDate)
...
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.states;

import net.corda.missionMars.contracts.BoardingTicketContract;
import net.corda.v5.application.identity.AbstractParty;
import net.corda.v5.application.identity.Party;
import net.corda.v5.ledger.contracts.BelongsToContract;
import net.corda.v5.ledger.contracts.ContractState;
import org.jetbrains.annotations.NotNull;
import java.time.LocalDate;

@BelongsToContract(BoardingTicketContract.class)
public class BoardingTicket implements ContractState {

    //Private Variables
    private String description;
    private Party marsExpress;
    private Party owner;
    private LocalDate launchDate;

    ......
}
```
{{% /tab %}}

{{< /tabs >}}

### Define commands

The `BoardingTicketContract` requires two commands:

* `CreateTicket` - Define this command to express the intention of Mars Express creating the ticket to go to Mars.
* `RedeemTicket` - Define this command to express the intention of Peter redeeming the `BoardingTicket` state.

1. Extend the `CommandData` interface into a new interface called `Commands`.

2. Within the `Commands` interface, create two classes named `CreateTicket` and `RedeemTicket`, implementing their parent interface.


Your code should now look like this:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.contracts;

class BoardingTicketContract : Contract {

  // Used to indicate the transaction's intent.
  interface Commands : CommandData {
        class CreateTicket : Commands
        class RedeemTicket : Commands
  }

}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
public class BoardingTicketContract implements Contract {

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will only have one command.
        class CreateTicket implements BoardingTicketContract.Commands {}
        class RedeemTicket implements BoardingTicketContract.Commands {}
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

class BoardingTicketContract : Contract {

  // Used to indicate the transaction's intent.
  interface Commands : CommandData {
        class CreateTicket : Commands
        class RedeemTicket : Commands
  }
companion object {
    // This is used to identify the contract when building a transaction.
    const val ID = "net.corda.missionMars.contracts.BoardingTicketContract"
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
public class BoardingTicketContract implements Contract {

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will only have one command.
        class CreateTicket implements BoardingTicketContract.Commands {}
        class RedeemTicket implements BoardingTicketContract.Commands {}
    }

    // This is used to identify our contract when building a transaction.
    public static final String ID = "net.corda.missionMars.contracts.BoardingTicketContract";
}
```
{{% /tab %}}

{{< /tabs >}}

### Add `verify` methods

You must add a `verify` method that triggers automatically when a transaction executes. Use the `verify` method to confirm that the transaction components are following the restrictions that you want to implement with the contract.

In the `BoardingTicketContract`, the `verify` method must confirm that when creating the ticket:

* The transaction only outputs one `BoardingTicket` state.
* The output `BoardingTicket` state must have a clear description of trip information.
* The output `BoardingTicket` state must have a launch date later than today's date.

The contract must also verify transaction components for when the ticket is redeemed:

* The transaction must consume two states (`MarsVoucher` and `BoardingTicket`).
* The issuer of the `BoardingTicket` must be the space company that creates the `BoardingTicket`.
* The output `BoardingTicket` state must have a launch date later than the time the ticket is created.

{{< note >}}
These are simplified verifications for the purpose of this example. When writing your own CorDapp, components of the `verify` method should be strong representations of your CorDapp's business logic. The contract controls how states evolve on the ledger, so the components of your verification ensure that the conditions of your business rules are met.
{{< /note >}}

Once you've added the verify methods to your `BoardingTicketContract`, your code should look like this:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.missionMars.contracts

import net.corda.missionMars.states.BoardingTicket
import net.corda.missionMars.states.MarsVoucher
import net.corda.v5.ledger.contracts.CommandData
import net.corda.v5.ledger.contracts.Contract
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.transactions.LedgerTransaction
import java.time.LocalDate
import java.time.LocalDateTime

class BoardingTicketContract : Contract {
    override fun verify(tx: LedgerTransaction) {
        //Extract the command from the transaction.
        val commandData = tx.commands[0].value
        val output = tx.outputsOfType(BoardingTicket::class.java)[0]

        when (commandData) {
            is Commands.CreateTicket -> requireThat {
                "This transaction should only output one BoardingTicket state".using(tx.outputs.size == 1)
                "The output BoardingTicket state should have clear description of space trip information".using(output.description != "")
                val current = LocalDateTime.now()
                val today = LocalDate.of(current.year, current.month, current.dayOfMonth)
                val launchDay = output.launchDate
                "The output BoardingTicket state should have a launching date later than today".using(launchDay.isAfter(today))
                null
            }
            is Commands.RedeemTicket -> requireThat {
                val input = tx.inputsOfType(MarsVoucher::class.java)[0]
                "This transaction should consume two states".using(tx.inputStates.size == 2)
                "The issuer of the BoardingTicket should be the space company which creates the boarding ticket".using(input.issuer == output.marsExpress)
                val current = LocalDateTime.now()
                val today = LocalDate.of(current.year, current.month, current.dayOfMonth)
                val launchDay = output.launchDate
                "The output BoardingTicket state should have a launching date later than today".using(launchDay.isAfter(today))
                null
            }
        }
    }

    // Used to indicate the transaction's intent.
    interface Commands : CommandData {
        class CreateTicket : Commands
        class RedeemTicket : Commands
    }

    companion object {
        // This is used to identify our contract when building a transaction.
        const val ID = "net.corda.missionMars.contracts.BoardingTicketContract"
    }
}
```
{{% /tab %}}

{{% tab name="Java" %}}
```java
package net.corda.missionMars.contracts;

import net.corda.missionMars.states.BoardingTicket;
import net.corda.missionMars.states.MarsVoucher;
import net.corda.v5.ledger.contracts.CommandData;
import net.corda.v5.ledger.contracts.Contract;
import net.corda.v5.ledger.transactions.LedgerTransaction;
import org.jetbrains.annotations.NotNull;

import java.time.LocalDate;
import java.time.LocalDateTime;

import static net.corda.v5.ledger.contracts.ContractsDSL.requireThat;

public class BoardingTicketContract implements Contract {

    // This is used to identify our contract when building a transaction.
    public static final String ID = "net.corda.missionMars.contracts.BoardingTicketContract";

    @Override
    public void verify(@NotNull LedgerTransaction tx) {
        final CommandData commandData = tx.getCommands().get(0).getValue();
        BoardingTicket output = tx.outputsOfType(BoardingTicket.class).get(0);

        if (commandData instanceof BoardingTicketContract.Commands.CreateTicket) {
            //Using Corda DSL function requireThat to replicate conditions-checks
            requireThat(require -> {
                require.using("This transaction should only output one BoardingTicket state", tx.getOutputs().size() == 1);
                require.using("The output BoardingTicket state should have clear description of space trip information", !(output.getDescription().equals("")));
                LocalDateTime current = LocalDateTime.now();
                LocalDate today = LocalDate.of(current.getYear(),current.getMonth(),current.getDayOfMonth());
                LocalDate launchDay = output.getlaunchDate();
                require.using("The output BoardingTicket state should have a launching date later then the creation time", launchDay.isAfter(today));
                return null;
            });
        }else if(commandData instanceof BoardingTicketContract.Commands.RedeemTicket) {
            MarsVoucher input = tx.inputsOfType(MarsVoucher.class).get(0);
            requireThat(require -> {
                require.using("This transaction should consume two states", tx.getInputStates().size() == 2);
                require.using("The issuer of the BoardingTicket should be the space company which creates the boarding ticket", input.getIssuer().equals(output.getMarsExpress()));
                LocalDateTime current = LocalDateTime.now();
                LocalDate today = LocalDate.of(current.getYear(),current.getMonth(),current.getDayOfMonth());
                LocalDate launchDay = output.getlaunchDate();
                require.using("The output BoardingTicket state should have a launching date later then the creation time", launchDay.isAfter(today));
                return null;
            });
        }

    }

    // Used to indicate the transaction's intent.
    public interface Commands extends CommandData {
        //In our hello-world app, We will only have one command.
        class CreateTicket implements BoardingTicketContract.Commands {}
        class RedeemTicket implements BoardingTicketContract.Commands {}
    }
}


```
{{% /tab %}}

{{< /tabs >}}


## Next steps

Follow the [Write flows](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-flows.md) tutorial to continue on this learning path.
