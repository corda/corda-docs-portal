---
date: '2021-09-15'
section_menu: tutorials
menu:
  tutorials:
    identifier: corda-corda-5.0-dev-preview-1-os-tutorial-c5-basic-cordapp-contract
    parent: corda-5.0-dev-preview-1-os-tutorial-c5-basic-cordapp-intro
    weight: 1040
tags:
- tutorial
- cordapp
title: Write contracts
---

In Corda, contracts govern how states should evolve over time by restricting how transaction flows are performed. They are the Java or Kotlin interfaces used to mark the defined class where a transaction `verify` method is implemented.

This tutorial guides you through writing the two contracts you need in your CorDapp: `MarsVoucherContract` and `BoardingTicketContract`. You will link these contracts to the states that you created in the [Write the states](c5-basic-cordapp-state.md) tutorial.

You will create these contracts in the `contracts/src/main/<kotlin or java>/net/corda/missionMars/contracts/` directory in this tutorial. Refer to the `TemplateContract.kt` or `TemplateContract.java` file in this directory to see a template contract.


## Learning objectives

Once you have completed this tutorial, you will know how to create and implement contracts in a CorDapp to restrict how your transaction flows are performed.


## Create the `MarsVoucherContract` contract

First, create the `MarsVoucherContract`. This contract verifies actions performed by the `MarsVoucher` state.

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

This is what your code should look like now:

```kotlin
package net.corda.missionMars.contracts;

//Domain Specific Language
class MarsVoucherContract : Contract {

}
```

### Add commands

Commands indicate the transaction's intent — what type of actions performed by the state the contract can verify. Follow the steps below to add the command for issuing the Mars voucher.

1. Add the `Commands : CommandData` interface declaration.

2. Inside the interface, add the `Issue` class that implements `Commands`.

This is what your code should look like now:

```kotlin
package net.corda.missionMars.contracts;

//Domain Specific Language
class MarsVoucherContract : Contract {

}

// Used to indicate the transaction's intent.
interface Commands : CommandData {
    //In our hello-world app, We will have two commands.
    class Issue : Commands
}
```

### Add the `verify` method

The `verify` method is automatically triggered when your transaction is executed. It verifies:

* The intention of the transaction - the commands that you are using for that specific transaction.
* That the transaction components are following the restrictions implemented inside the contract's `verify` method.

1. If you're using IntelliJ, you will see an error indicator under the class name and implementation. This indicates that the class is missing the required method. Hover over the class definition, then:

   * On MacOS: press **Option** + **Enter**.

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


This is what your code should look like now:

```kotlin
package net.corda.missionMars.contracts;

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
        }
    }

    // Used to indicate the transaction's intent.
    interface Commands : CommandData {
        //In our hello-world app, We will have two commands.
        class Issue : Commands
    }
}
```

### Add the contract's ID

To identify your contract when building transactions, add its ID.

{{< note >}}
This ID is not used in the production environment, but it is used in the testing scenarios. It's best practice to add it to the contract.
{{< /note >}}

This is what your code should look like now:

```kotlin
package net.corda.missionMars.contracts;

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
        }
    }

    // Used to indicate the transaction's intent.
    interface Commands : CommandData {
        //In our hello-world app, We will have two commands.
        class Issue : Commands
    }

    companion object {
        // This is used to identify our contract when building a transaction.
        const val ID = "com.tutorial.contracts.MarsVoucherContract"
    }
}
```

### Add imports

If you're using IntelliJ or another IDE, the IDE will automatically add the imports you need.

IntelliJ indicates that an import is missing with red text. To add the import:

1. Click the red text.

2. Automatically import the missing variable:

   * On MacOS: press **Option** + **Enter**.
   * On Windows: press **Alt** + **Enter**.

3. Repeat this process for all missing imports.

{{< note >}}

When adding imports, ignore `BoardingTicketContract` that is also in red - you will add it in the *Create the `BoardingTicketContract`* section.

{{< /note >}}

After adding all the missing imports, you have finished writing the `MarsVoucherContract`. Your code should now look like this:


```kotlin
package net.corda.missionMars.contracts;

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
        }
    }

    // Used to indicate the transaction's intent.
    interface Commands : CommandData {
        //In our hello-world app, We will have two commands.
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

The `BoardingTicketContract` has two intentions:

* Mars Express creates the ticket to go to Mars. This intention is expressed by the `CreateTicket` command.
* Peter redeems the `BoardingTicket` state. This intention is expressed by the `RedeemTicket` command.

The rules inside the `requireThat` Corda DSL helper method are:

* For the `CreateTicket` command:

  * The transaction should only output one BoardingTicket state.
  * The output BoardingTicket state should have clear description of the space trip.
  * The output BoardingTicket state should have a launching date later then the creation time.

* For the `RedeemTicket` command:

  * The transaction should consume two states.
  * The issuer of the BoardingTicket should be the space company which created the boarding ticket.
  * The output BoardingTicket state should have a launching date later then the creation time.


### Check your work

Once you've written the `BoardingTicketContract`, check your code against the sample below. Your code should look like this:

```kotlin
package net.corda.missionMars.contracts

import net.corda.missionMars.states.BoardingTicket
import net.corda.missionMars.states.MarsVoucher
import net.corda.v5.ledger.contracts.CommandData
import net.corda.v5.ledger.contracts.Contract
import net.corda.v5.ledger.contracts.requireThat
import net.corda.v5.ledger.transactions.LedgerTransaction
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
                "The output BoardingTicket state should have a launching date later then the creation time".using(output.date > Calendar.getInstance().time)
                null
            }
            is Commands.RedeemTicket -> requireThat {
                val input = tx.inputsOfType(MarsVoucher::class.java)[0]
                "This transaction should consume two states".using(tx.inputStates.size == 2)
                "The issuer of the BoardingTicket should be the space company which creates the boarding ticket".using(input.issuer == output.spaceCompany)
                "The output BoardingTicket state should have a launching date later then the creation time".using(output.date > Calendar.getInstance().time)
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
        const val ID = "com.tutorial.contracts.BoardingTicketContract"
    }
}
```

## Next steps

Follow the [Write flows](c5-basic-cordapp-flows.md) tutorial to continue on this learning path.
