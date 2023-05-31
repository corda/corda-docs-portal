---
date: '2023-05-03'
title: "Write States"
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-first-cordapp-state
    parent: corda5-develop-first-cordapp
    weight: 2000
---

# Write States

This tutorial guides you through writing the two states you need in your CorDapp: `AppleStamp` and `BasketofApples`.
You will create these states in the `contracts/src/main/kotlin/com/r3/developers/apples/states` directory.

## Learning Objectives

After you have completed this tutorial, you will know how to create and implement states in a CorDapp.

## Before You Start

Before you start building states, read more about [states]({{< relref "../components/ledger/states.md" >}}).


## Create the `AppleStamp` State

First, create the `AppleStamp` state. This state is the voucher issued to customers.

1. Go to the `contracts/src/main/kotlin/com/r3/developers/apples` folder.
2. Right-click the **states** folder, select **New > Kotlin Class** and create a file called `AppleStamp`.
3. Open the file.

### Add Annotations

The first thing you should do when writing a state is add the `@BelongsToContract` annotation. This annotation
establishes the relationship between a state and a contract. Without this, your state does not know which contract is used to verify it.

Add the annotation `@BelongsToContract(AppleStampContract::class)` to your state. The contract will be defined later.

This what your code should look like so far:

```kotlin
@BelongsToContract(AppleStampContract.class)
```

{{< note >}}
Adding this annotation triggers an error in IntelliJ because you have not created the `AppleStampContract` yet. Ignore this error for now - you will add the contract class in the [Write Contracts]({{< relref "./contract.md" >}}) tutorial.
{{< /note >}}

When naming your CorDapp files, it's best practice to match your contract and state names. In this case the state is called `AppleStamp`, so the contract is called `AppleStampContract`. Follow this naming convention when you write your own original CorDapp to avoid confusion.

### Implement the State

The next line of code you add defines the type of `ContractState` you implement with the `AppleStamp` class. Add this line to ensure that Corda recognizes the `AppleStamp` as a state.

Add the public class `AppleStamp` implementing a `ContractState`.

Your code should now look as follows:

```kotlin
@BelongsToContract(AppleStampContract::class)
class AppleStamp : ContractState
```

### Add the Required Properties

1. Add the properties for the following parameters:
   * The stamp identifier (`id`)
   * The stamp description (`stampDesc`)
   * The issuer of the stamp (`issuer`)
   * The current owner of the stamp (`holder`)

2. All `ContractStates` must include a parameter to indicate the participants that store the states. As `ContractState`
is a Java API, you must store the participants as private members.
Add this property to the `AppleStamp`:

   ```kotlin
   private val participants: List<PublicKey>
   ```

3. To expose the `participants` value, override the `getParticipants()` method in the `AppleStamp`:

   ```kotlin
   override fun getParticipants(): List<PublicKey> = participants
   ```

After following these steps, your code should look as follows:

```kotlin
@BelongsToContract(AppleStampContract::class)
class AppleStamp(
    val id: UUID,
    val stampDesc: String,
    val issuer: PublicKey,
    val holder: PublicKey,
    private val participants: List<PublicKey>
) : ContractState {

    override fun getParticipants(): List<PublicKey> = participants
}
```

{{< note >}}
The `PublicKey`s referred to in the `participants` property are the `ledgerKey`s of the participants expected to store the states.
{{< /note >}}

### Add Imports

If you are using IntelliJ or another IDE, the IDE automatically adds the imports you need. IntelliJ indicates that an import is missing with red text.

Once you have added all imports, your code should look like this:

```kotlin
package com.r3.developers.apples.states

import com.r3.developers.apples.contracts.AppleStampContract
import net.corda.v5.ledger.utxo.BelongsToContract
import net.corda.v5.ledger.utxo.ContractState
import java.security.PublicKey
import java.util.*

@BelongsToContract(AppleStampContract::class)
class AppleStamp(
    val id: UUID,
    val stampDesc: String,
    val issuer: PublicKey,
    val holder: PublicKey,
    private val participants: List<PublicKey>
) : ContractState {

    override fun getParticipants(): List<PublicKey> = participants
}

```

### Create the `BasketOfApples` State

The `BasketOfApples` state is the basket of apples that Farmer Bob self-issues to prepare the apples for Dave. Now that you have written your first state, try writing the `BasketOfApples` state using the following properties:

* `description` - The brand or type of apple. Use type `String`.
* `farm` - The origin of the apples. Use type `PublicKey`.
* `owner` - The current owner of the basket. Use type `PublicKey`.
* `weight` - The weight of the basket of apples. Use type `int`.

You will also need to define a `participants` property and override the getter method, as you did when creating the `AppleStamp` contract.

The `BasketOfApples` state is involved in two transactions. In the first transaction, Farmer Bob self-issues the `BasketOfApples`.
At this point, Farmer Bob is both the `owner` and `farm` of the transaction. The second transaction occurs when Dave
wishes to redeem his `AppleStamp` for the `BasketOfApples`. At this point, the owner changes from Bob to Dave.

To enable this, implement a `changeOwner` function within the state. It allows an updated state to be returned with a new owner.
Add the following code to your `BasketOfApples` state class:

```kotlin
fun changeOwner(buyer: PublicKey): BasketOfApples {
    val participants = listOf(farm, buyer)
    return BasketOfApples(description, farm, buyer, weight, participants)
}
```

#### Check Your Work

Once you’ve written the `BasketOfApples` state, check your code against the sample below. Your code should look something like this:

```kotlin
package com.r3.developers.apples.states

import com.r3.developers.apples.contracts.BasketOfApplesContract
import net.corda.v5.ledger.utxo.BelongsToContract
import net.corda.v5.ledger.utxo.ContractState
import java.security.PublicKey

@BelongsToContract(BasketOfApplesContract::class)
class BasketOfApples(
    val description: String,
    val farm: PublicKey,
    val owner: PublicKey,
    val weight: Int,
    private val participants: List<PublicKey>
) : ContractState {

    override fun getParticipants(): List<PublicKey> = participants

    fun changeOwner(buyer: PublicKey): BasketOfApples {
        val participants = listOf(farm, buyer)
        return BasketOfApples(description, farm, buyer, weight, participants)
    }
}

```

## Next Steps

Follow the [Write Contracts]({{< relref"./contract.md" >}}) tutorial to continue on this learning path.
