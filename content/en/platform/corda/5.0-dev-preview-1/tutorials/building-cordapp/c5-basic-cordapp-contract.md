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
title: Write contracts
---

[Contracts](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-contracts.md) define the rules of how states can evolve. A CorDapp can have more than one contract, and each contract defines rules for one or more states. The contract includes [transactions](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-transactions.html) that update the ledger by marking zero or more existing ledger states as historic (the inputs), and producing zero or more new ledger states (the outputs). The contract(s) ensures that input and output states in transactions are valid and prevents invalid transactions from occurring. All parties that wish to transact in a network must run the same contract(s) for any transaction they’re a party to, verifying that the transaction is valid.

Contracts are classes that implement the Contract interface. They must override the `verify` method. The `verify` method takes transactions as input and evaluates them against rules defined as a `requireThat` element. Contract execution must be deterministic, and transaction acceptance is based on the transaction’s contents alone. Contract verification is the final step that governs the evolution of the ledger, thus it can only address on-ledger facts.

A transaction that is not contractually valid is not a valid proposal to update the ledger, and thus can never be committed to the ledger. In this way, contracts impose rules on the evolution of states over time that are independent of the willingness of the required signers to sign a given transaction.

Contract verification is not the only type of validation that you can apply in your CorDapp—you can use [workflows](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/flows/overview.html) to perform validation as well.

This tutorial guides you through writing the two contracts you need in your CorDapp: `MarsVoucherContract` and `BoardingTicketContract`. You will link these contracts to the states that you created in the [states](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-state.md) tutorials.

You will create these contracts in the `contracts/src/main/<kotlin>/net/corda/missionMars/contracts/` directory in this tutorial. Refer to the `TemplateContract.kt` file in this directory to see a template contract.

## Learning objectives

When you have completed this tutorial, you will know how to create and implement contracts in a Corda 5 Developer Preview CorDapp to restrict how your transaction flows are performed.

## Create the `MarsVoucherContract` contract

First, create the `MarsVoucherContract`. This contract verifies actions performed on the `MarsVoucher` state.

1. Right-click the **contracts** folder.

2. Select **New > Kotlin Class/File**.

3. In the **New Kotlin Class/File** window, select **Class** and name the file `MarsVoucherContract`.

{{< note >}}
When naming contracts, it’s best practice to match your contract and state names. In this case the contract is called `MarsVoucherContract`, and the state that links to it is called `MarsVoucher`. Follow this naming convention when you write an original CorDapp to avoid confusion.
{{< /note >}}

4. Open the file.

### Add the class name declaration

A Corda state typically has a corresponding contract class to document the rules/policy of that state when used in a transaction. To declare the contract class:

Add the class name `MarsVoucherContract` that implements the `Contract` class.

{{< note >}}
As you are writing the contract, you will notice that IntelliJ prompts you to add imports that correspond to elements you've added. Add the relevant imports to all suggested elements.
When adding imports, ignore `BoardingTicketContract` that is in red - you will add it in the *Create the `BoardingTicketContract`* section.
{{< /note >}}

This is what your code should look like now:

```kotlin
package net.corda.missionMars.contracts;

class MarsVoucherContract : Contract {

}
```

### Connect the `MarsVoucherContract` to the `MarsVoucher` state

After creating the contract class in a CorDapp, you must connect the contract to its correlating state. Add the `@BelongsToContract` annotation *in the state class* to establish the relationship between a state and a contract. Without this, your state does not know which contract is used to verify it.

1. Open your `MarsVoucher` class.
2. Insert the `@BelongsToContract` annotation with the `MarsVoucherContract` just before the definition of the `MarsVoucher` data class.

Transactions involving the `MarsVoucher` state are now verified using the `MarsVoucherContract`.

### Add commands

[Commands](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-transactions.html#commands) are built into a transaction to indicate the transaction's intent. They control the type of actions performed to the state that the contract can verify.

Each command is associated with a list of signers. The public keys listed in a contract's commands indicate the transaction's required signers.

In the `MarsVoucherContract`, you need a command that issues the `MarsVoucher`.

1. Add the `Commands : CommandData` interface declaration.

2. Inside the interface, add the `Issue` class that implements `Commands`.

   The `Issue` command is used to create the Mars voucher.

This is what your code should look like now:

```kotlin
package net.corda.missionMars.contracts;

class MarsVoucherContract : Contract {

  // Used to indicate the transaction's intent.
  interface Commands : CommandData {
      class Issue : Commands
  }

}
```

### Add the contract's ID

To identify your contract when building transactions, add its ID.

{{< note >}}
This ID is not used in the production environment, but it is used in testing scenarios. It's best practice to add it to the contract.
{{< /note >}}

This is what your code should look like now:

```kotlin
package net.corda.missionMars.contracts;

class MarsVoucherContract : Contract {

  // Used to indicate the transaction's intent.
  interface Commands : CommandData {
      class Issue : Commands
  }

companion object {
    // This is used to identify our contract when building a transaction.
    const val ID = "com.tutorial.contracts.MarsVoucherContract"
  }
}
```

### Add the `verify` method

The `verify` method is automatically triggered when your transaction is executed. It verifies that the transaction components are following the restrictions implemented inside the contract's `verify` method.

In this case, the `verify` method must confirm that there will only be one `MarsVoucher` state as an output of the transaction. It must also confirm that relevant trip information (the `voucherDesc`) is included in the state.

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

You have now finished writing the `MarsVoucherContract`. Your code should now look like this:

```kotlin
package net.corda.missionMars.contracts;

import net.corda.missionMars.states.MarsVoucher
import net.corda.v5.ledger.contracts.CommandData
import net.corda.v5.ledger.contracts.Contract
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.transactions.LedgerTransaction

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
        }
    }

    // Used to indicate the transaction's intent.
    interface Commands : CommandData {
        class Issue : Commands
    }

    companion object {
        // This is used to identify our contract when building a transaction.
        const val ID = "com.tutorial.contracts.MarsVoucherContract"
    }
}
```

## Create the `BoardingTicketContract`

Now that you've written your first contract, try writing the `BoardingTicketContract` using the following information.

The `BoardingTicketState` will be used on two occasions, which means that the `BoardingTicketContract` should have a `Commands` interface that carries two commands corresponding to the contract's two intentions:

* Mars Express creates the ticket to go to Mars. This intention is expressed by the `CreateTicket` command.
* Peter redeems the `BoardingTicket` state. This intention is expressed by the `RedeemTicket` command.

The rules inside the `requireThat` Corda DSL helper method are:

* For the `CreateTicket` command:

  * The transaction should only output one `BoardingTicket` state.
  * The output `BoardingTicket` state should have a clear description of the space trip.
  * The output `BoardingTicket` state should have a launch date later then the creation time.

* For the `RedeemTicket` command:

  * The transaction should consume two states.
  * The issuer of the `BoardingTicket` should be the space company that created the boarding ticket.
  * The output `BoardingTicket` state should have a launch date later than the creation time.


### Check your work

Once you've written the `BoardingTicketContract`, your code should look like this:

```kotlin
package net.corda.missionMars.contracts

import net.corda.missionMars.states.BoardingTicket
import net.corda.missionMars.states.MarsVoucher
import net.corda.v5.ledger.contracts.CommandData
import net.corda.v5.ledger.contracts.Contract
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.transactions.LedgerTransaction
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.*

class BoardingTicketContract : Contract {
    override fun verify(tx: LedgerTransaction) {
        //Extract the command from the transaction.
        val commandData = tx.commands[0].value
        val output = tx.outputsOfType(BoardingTicket::class.java)[0]

        when (commandData) {
            is Commands.CreateTicket -> requireThat {
                "This transaction should only output one BoardingTicket state".using(tx.outputs.size == 1)
                "The output BoardingTicket state should have clear description of space trip information".using(output.description != "")
                "The output BoardingTicket state should have a launching date later then the creation time".using(output.daysUntilLaunch > 0)
                null
            }
            is Commands.RedeemTicket -> requireThat {
                val input = tx.inputsOfType(MarsVoucher::class.java)[0]
                "This transaction should consume two states".using(tx.inputStates.size == 2)
                "The issuer of the BoardingTicket should be the space company which creates the boarding ticket".using(input.issuer == output.marsExpress)
                "The output BoardingTicket state should have a launching date later then the creation time".using(output.daysUntilLaunch > 0)
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

## Next steps

Follow the [Write flows](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-flows.md) tutorial to continue on this learning path.
