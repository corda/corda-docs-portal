---
date: '2023-05-03'
title: "Write Contracts"
menu:
  corda5:
    identifier: corda5-develop-first-cordapp-contract
    parent: corda5-develop-first-cordapp
    weight: 3000
---

This tutorial guides you through writing the two contracts you need in your CorDapp: `AppleStampContract` and `BasketOfApplesContract`. You will link these contracts to the states that you created in the [Write States]({{< relref"./state.md" >}}) tutorial.

You will create these contracts in the `ledger-utxo-example-apples-contract/src/main/kotlin/net/cordapp/utxo/apples/contracts` directory in this tutorial.


## Learning Objectives

Once you have completed this tutorial, you will know how to create and implement contracts in a CorDapp to restrict how your transaction flows are performed.


## Create the `AppleStampContract` Contract

First, create the `AppleStampContract`. This contract verifies actions performed by the `AppleStamp` state.

1. Right-click the **contracts** folder.
2. Select **New > Kotlin Class**.
3. Create a file called `AppleStampContract`.

   {{< note >}}
   When naming contracts, it’s best practice to match your contract and state names. In this case the contract is called `AppleStampContract`, and the state that links to it is called `AppleStamp`. Follow this naming convention when you write your own original CorDapp to avoid confusion.
   {{< /note >}}

4. Open the file.

### Declare the Contract Class

A Corda state typically has a corresponding contract class to document the rules/policy of that state when used in a transaction.
To declare the contract class, add the public class `AppleStampContract` that implements the `Contract` class. Your code should look as follows:

```kotlin
package net.cordapp.utxo.apples.contracts

class AppleStampContract : Contract
```

### Add Commands

Commands indicate the transaction's intent — what type of actions performed by the state the contract can verify. In this step, you will define a command for issuing the bushel of apples.

1. Add the `Commands` public interface declaration.
2. Inside the interface, add the `Issue` class that implements `AppleStampContract.Commands`.

   This is what your code should look like now:

   ```kotlin
   package net.cordapp.utxo.apples.contracts

   class AppleStampContract : Contract {

    // Used to indicate the transaction's intent
    interface Commands : Command {
        // In our hello-world app, we will have two commands
        class Issue : Commands
        }
    }
    ```

### Add the `verify` Method

The `verify` method is automatically triggered when your transaction is executed. It verifies that the transaction components are following the restrictions implemented inside the contract's `verify` method.

1. If you're using IntelliJ, you will see an error indicator under the class name and implementation. This indicates that the class is missing the required method. Hover over the class definition, then:
   * On macOS: press **Option** + **Enter**.
   * On Windows: press **Alt** + **Enter**.
2. Select **Implement methods > verify** from the dropdown menu.
   The `verify` method preceded by the `override` keyword appears.
3. Extract the command from the transaction.
4. Verify the intention of the transaction (Issue or Redeem) using an `if/else` or `when` block.
5. Use Kotlin’s `requires` method to include the contract’s verification rules for issuing:
   ```kotlin
   val output = transaction.getOutputStates<AppleStamp>().first()
   require(transaction.outputContractStates.size == 1) {
     "This transaction should only have one AppleStamp state as output"
   }
   require(output.stampDesc.isNotBlank()) {
    "The output AppleStamp state should have clear description of the type of redeemable goods"
   }
   ```
6. When the intention of the transaction is not recognized by the `verify` method, use `else` to throw an error.

This is what your code should look like now:

```kotlin
package net.cordapp.utxo.apples.contracts

class AppleStampContract : Contract {

    // Used to indicate the transaction's intent
    interface Commands : Command {
        // In our hello-world app, we will have two commands
        class Issue : Commands
    }

    override fun verify(transaction: UtxoLedgerTransaction) {
        // Extract the command from the transaction
        // Verify the transaction according to the intention of the transaction
        when (val command = transaction.commands.first()) {
            is Commands.Issue -> {
                val output = transaction.getOutputStates<AppleStamp>().first()
                require(transaction.outputContractStates.size == 1) {
                    "This transaction should only have one AppleStamp state as output"
                }
                require(output.stampDesc.isNotBlank()) {
                    "The output AppleStamp state should have clear description of the type of redeemable goods"
                }
            }
            is BasketOfApplesContract.Commands.Redeem -> {
                // Transaction verification will happen in BasketOfApplesContract
            }
            else -> {
                // Unrecognised Command type
                throw IllegalArgumentException("Incorrect type of AppleStamp commands: ${command::class.java.name}")
            }
        }
    }
}
```

### Add Imports

If you are using IntelliJ or another IDE, the IDE will automatically add the imports you need. IntelliJ indicates that an import is missing with red text.

When you have added all the missing imports, you have finished writing the `AppleStampContract`. Your code should now look like this:

```kotlin
package net.cordapp.utxo.apples.contracts

import net.corda.v5.ledger.utxo.Command
import net.corda.v5.ledger.utxo.Contract
import net.corda.v5.ledger.utxo.transaction.UtxoLedgerTransaction
import net.corda.v5.ledger.utxo.transaction.getOutputStates
import net.cordapp.utxo.apples.states.AppleStamp

class AppleStampContract : Contract {

    // Used to indicate the transaction's intent
    interface Commands : Command {
        // In our hello-world app, we will have two commands
        class Issue : Commands
    }

    override fun verify(transaction: UtxoLedgerTransaction) {
        // Extract the command from the transaction
        // Verify the transaction according to the intention of the transaction
        when (val command = transaction.commands.first()) {
            is Commands.Issue -> {
                val output = transaction.getOutputStates<AppleStamp>().first()
                require(transaction.outputContractStates.size == 1) {
                    "This transaction should only have one AppleStamp state as output"
                }
                require(output.stampDesc.isNotBlank()) {
                    "The output AppleStamp state should have clear description of the type of redeemable goods"
                }
            }
            is BasketOfApplesContract.Commands.Redeem -> {
                // Transaction verification will happen in BasketOfApplesContract
            }
            else -> {
                // Unrecognised Command type
                throw IllegalArgumentException("Incorrect type of AppleStamp commands: ${command::class.java.name}")
            }
        }
    }
}
```

## Create the `BasketOfApplesContract`

The `BasketOfApplesContract` has two intentions:

* Farmer Bob creates the basket of apples. This intention is expressed by the `PackBasket` command.
* Peter redeems the `BasketOfApples` state. This intention is expressed by the `Redeem` command.

The rules inside the `verify` method in the `requireThat` Corda DSL helper method are:

* For the `PackBasket` command:
  * This transaction should only output one `BasketOfApples` state.
  * The output of the `BasketOfApples` state should have a clear description of the apple product.
  * The output of the `BasketOfApples` state should have a non-zero weight.
* For the `Redeem` command:
  * The transaction should consume two states.
  * The issuer of the `AppleStamp` should be the producing farm of this basket of apples.
  * The weight of the basket of apples must be greater than zero.


### Check Your Work

Once you have written the `BasketOfApplesContract`, check your code against the sample below. Your code should look like this:

```kotlin
package net.cordapp.utxo.apples.contracts

import net.corda.v5.ledger.utxo.Command
import net.corda.v5.ledger.utxo.Contract
import net.corda.v5.ledger.utxo.transaction.UtxoLedgerTransaction
import net.corda.v5.ledger.utxo.transaction.getInputStates
import net.corda.v5.ledger.utxo.transaction.getOutputStates
import net.cordapp.utxo.apples.states.AppleStamp
import net.cordapp.utxo.apples.states.BasketOfApples

class BasketOfApplesContract : Contract{

    interface Commands : Command {
        class PackBasket : Commands
        class Redeem : Commands
    }

    override fun verify(transaction: UtxoLedgerTransaction) {
        // Extract the command from the transaction
        when (val command = transaction.commands.first()) {
            is Commands.PackBasket -> {
                // Retrieve the output state of the transaction
                val output = transaction.getOutputStates<BasketOfApples>().first()
                require(transaction.outputContractStates.size == 1) {
                    "This transaction should only output one BasketOfApples state"
                }
                require(output.description.isNotBlank()) {
                    "The output BasketOfApples state should have clear description of Apple product"
                }
                require(output.weight > 0) {
                    "The output BasketOfApples state should have non zero weight"
                }
            }
            is Commands.Redeem -> {
                // Retrieve the input and output state of the transaction
                val input = transaction.getInputStates<AppleStamp>().first()
                val output = transaction.getOutputStates<BasketOfApples>().first()
                require(transaction.inputContractStates.size == 2) {
                    "This transaction should consume two states"
                }
                require(input.issuer == output.farm) {
                    "The issuer of the Apple stamp should be the producing farm of this basket of apple"
                }

                require(output.weight > 0) {
                    "The basket of apple has to weight more than 0"
                }
            }
            else -> {
                throw IllegalArgumentException("Incorrect type of BasketOfApples commands: ${command::class.java.name}")
            }
        }
    }
}
```

## Next Steps

Follow the [Write flows]({{< relref "./flows.md" >}}) tutorial to continue on this learning path.