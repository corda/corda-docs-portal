---
date: '2023-05-03'
title: "Write Contracts"
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-first-cordapp-contract
    parent: corda5-develop-first-cordapp
    weight: 3000
---

# Write Contracts

This tutorial guides you through writing the two contracts you need in your CorDapp: `AppleStampContract` and `BasketOfApplesContract`. You will link these contracts to the states that you created in the [Write States]({{< relref"./state.md" >}}) tutorial.

You will create these contracts in the `contracts/src/main/kotlin/com/r3/developers/apples/contracts` directory in this tutorial.


## Learning Objectives

Once you have completed this tutorial, you will know how to create and implement contracts in a CorDapp to restrict how your transaction flows are performed.


## Create the `AppleStampContract` Contract

First, create the `AppleStampContract`. This contract verifies actions performed by the `AppleStamp` state.

1. Go to `contracts/src/main/kotlin/com/r3/developers/apples` and right-click the **contracts** folder.
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

Commands indicate the transaction's intent — what type of actions performed by the state the contract can verify.
In this step, you will define a command for issuing the bushel of apples.
You will do this in a separate file as commands can be used by different contracts within the CorDapp.

1.	Go to `contracts/src/main/kotlin/com/r3/developers/apples` and right-click the `contracts` folder.
2.	Select **New > Kotlin Class**.
3.	Create a file called `AppleCommands`.
4.	Open that file.
5.	Add an `AppleCommands` public interface declaration which inherits from `Command`.
6.	Inside the interface, add `Issue` and `Redeem` classes that implement `AppleCommands`.

This is what your code should look like now:

```kotlin
package com.r3.developers.apples.contracts

import net.corda.v5.ledger.utxo.Command

// Used to indicate the transaction's intent
interface AppleCommands : Command {
    class Issue : AppleCommands
    class Redeem : AppleCommands
}
  ```

### Add the `verify` Method

Returning to `AppleStampContract`, the `verify` method is automatically triggered when your transaction is executed.
It verifies that the transaction components are following the restrictions implemented inside the contract's `verify` method.

1. If you're using IntelliJ, you will see an error indicator under the class name and implementation. This indicates that the class is missing the required method. Hover over the class definition, then:
   * On macOS: press **Option** + **Enter**.
   * On Windows: press **Alt** + **Enter**.
2. Select **Implement methods > verify** from the dropdown menu.
   The `verify` method preceded by the `override` keyword appears.
3. Extract the command from the transaction.
4. Verify the intention of the transaction (Issue or Redeem) using an `if/else` or `when` block.
5. Use Kotlin’s `require` method to include the contract’s verification rules for issuing:
   ```kotlin
   val output = transaction.getOutputStates(AppleStamp::class.java).first()
   require(transaction.outputContractStates.size == 1) {
       "This transaction should only have one AppleStamp state as output"
   }
   require(output.stampDesc.isNotBlank()) {
       "The output AppleStamp state should have clear description of the type of redeemable goods"
   }
   ```
6. Similarly, add verification rules for redeeming:

{{< note >}}
When the intention of the transaction is not recognized by the `verify` method, use `else` to throw an error.
{{< /note >}}

   ```kotlin
    val inputs = transaction.getInputStates(AppleStamp::class.java)
      require(inputs.size == 1) {
          "This transaction should only have one AppleStamp state as input"
      }
      require(transaction.signatories.contains(inputs.first().holder)) {
          "The holder of the input AppleStamp state must be a signatory to the transaction"
      }
   ```

This is what your code should look like now:

```kotlin
package com.r3.developers.apples.contracts

class AppleStampContract : Contract {

    override fun verify(transaction: UtxoLedgerTransaction) {
        // Extract the command from the transaction
        // Verify the transaction according to the intention of the transaction
        when (val command = transaction.commands.first()) {
            is AppleCommands.Issue -> {
                val output = transaction.getOutputStates(AppleStamp::class.java).first()
                require(transaction.outputContractStates.size == 1) {
                    "This transaction should only have one AppleStamp state as output"
                }
                require(output.stampDesc.isNotBlank()) {
                    "The output AppleStamp state should have clear description of the type of redeemable goods"
                }
            }
            is AppleCommands.Redeem -> {
                val inputs = transaction.getInputStates(AppleStamp::class.java)
                require(inputs.size == 1) {
                    "This transaction should only have one AppleStamp state as input"
                }
                require(transaction.signatories.contains(inputs.first().holder)) {
                    "The holder of the input AppleStamp state must be a signatory to the transaction"
                }
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
package com.r3.developers.apples.contracts

import com.r3.developers.apples.states.AppleStamp
import net.corda.v5.ledger.utxo.Contract
import net.corda.v5.ledger.utxo.transaction.UtxoLedgerTransaction

class AppleStampContract : Contract {

    override fun verify(transaction: UtxoLedgerTransaction) {
        // Extract the command from the transaction
        // Verify the transaction according to the intention of the transaction
        when (val command = transaction.commands.first()) {
            is AppleCommands.Issue -> {
                val output = transaction.getOutputStates(AppleStamp::class.java).first()
                require(transaction.outputContractStates.size == 1) {
                    "This transaction should only have one AppleStamp state as output"
                }
                require(output.stampDesc.isNotBlank()) {
                    "The output AppleStamp state should have clear description of the type of redeemable goods"
                }
            }
            is AppleCommands.Redeem -> {
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
* Dave redeems the `BasketOfApples` state. This intention is expressed by the `Redeem` command, which you defined when creating `AppleStampContract`.

The rules inside the `verify` method in the `require` Corda DSL helper method are:

* For the `PackBasket` command:
  * This transaction should only output one `BasketOfApples` state.
  * The output of the `BasketOfApples` state should have a clear description of the apple product.
  * The output of the `BasketOfApples` state should have a non-zero weight.
* For the `Redeem` command:
  * The transaction should consume exactly two states: one `AppleStamp` and one `BasketOfApples`.
  * The issuer of the `AppleStamp` should be the producing farm of this basket of apples.
  * The weight of the basket of apples must be greater than zero.
* The `Issue` command does not need to be handled by this contract, because this is only relevant when dealing with an `AppleStamp`, not a `BasketOfApples`

Using what you learned when writing `AppleStampContract`, implement the above in a new class. You will also need to
update the `AppleCommands` interface defined earlier to account for the new `PackBasket` command.

### Check Your Work

Once you have written the `BasketOfApplesContract`, check your code against the samples below.

Your `AppleCommands` file should look like this:

```kotlin
package com.r3.developers.apples.contracts

import net.corda.v5.ledger.utxo.Command

// Used to indicate the transaction's intent
interface AppleCommands : Command {
    class Issue : AppleCommands
    class Redeem : AppleCommands
    class PackBasket : AppleCommands
}
```

Your `BasketOfApplesContract` file should look like this:

```kotlin
package com.r3.developers.apples.contracts

import com.r3.developers.apples.states.AppleStamp
import com.r3.developers.apples.states.BasketOfApples
import net.corda.v5.ledger.utxo.Contract
import net.corda.v5.ledger.utxo.transaction.UtxoLedgerTransaction


class BasketOfApplesContract : Contract {

    override fun verify(transaction: UtxoLedgerTransaction) {
        // Extract the command from the transaction
        when (val command = transaction.commands.first()) {
            is AppleCommands.PackBasket -> {
                // Retrieve the output state of the transaction
                val output = transaction.getOutputStates(BasketOfApples::class.java).first()
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
            is AppleCommands.Redeem -> {
                require(transaction.inputContractStates.size == 2) {
                    "This transaction should consume two states"
                }

                // Retrieve the inputs to this transaction, which should be exactly one AppleStamp
                // and one BasketOfApples
                val stampInputs = transaction.getInputStates(AppleStamp::class.java)
                val basketInputs = transaction.getInputStates(BasketOfApples::class.java)

                require(stampInputs.isNotEmpty() && basketInputs.isNotEmpty()) {
                    "This transaction should have exactly one AppleStamp and one BasketOfApples input state"
                }
                require(stampInputs.single().issuer == basketInputs.single().farm) {
                    "The issuer of the Apple stamp should be the producing farm of this basket of apple"
                }
                require(basketInputs.single().weight > 0) {
                    "The basket of apple has to weigh more than 0"
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
