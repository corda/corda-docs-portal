---
date: '2023-01-11'
title: "Write States"
menu:
  corda-5-beta:
    parent: corda-5-beta-tutorial-develop-building-your-first-basic-cordapp
    identifier: corda-5-beta-tutorial-develop-write-states
    weight: 1200
section_menu: corda-5-beta
---

This tutorial guides you through writing the two states you need in your CorDapp: `AppleStamp` and `BasketofApples`. You will be creating these states in the `ledger-utxo-example-apples-contract/src/main/kotlin/net/cordapp/utxo/apples/states` directory in this tutorial.

## Learning Objectives

After you have completed this tutorial, you will know how to create and implement states in a CorDapp.

## Before You Start

Before you start building states, read more about [states](../../ledger/states.md).


## Create the `AppleStamp` State

First create the `AppleStamp` state. This state is the voucher issued to customers.

1. Right-click the **states** folder, select **New > Kotlin Class** and create a file called `AppleStamp`.

2. Open the file.

### Add Annotations

The first thing you should do when writing a state is add the `@BelongsToContract` annotation. This annotation establishes the relationship between a state and a contract. Without this, your state does not know which contract is used to verify it.

Add the annotation `@BelongsToContract(ApplesStampContract::class)` to your state. The contract will be defined later.

This what your code should look like so far:

```kotlin
@BelongsToContract(AppleStampContract.class)
```

{{< note >}}
Adding this annotation triggers an error in IntelliJ because you haven't created the `AppleStampContract` yet. Ignore this error for now - you will add the contract class in the [Write Contracts](basic-cordapp-contract.md) tutorial.
{{< /note >}}

When naming your CorDapp files, it's best practice to match your contract and state names. In this case the state is called `AppleStamp`, so the contract is called `AppleStampContract`. Follow this naming convention when you write an original CorDapp to avoid confusion.


### Implement the State

The next line of code you add defines the type of `ContractState` you implement with the `AppleStamp` class. Add this line to ensure that Corda recognizes the `AppleStamp` as a state.

Add the public class `AppleStamp` implementing a `ContractState`.

This is what your code should look like now:

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

2. All `ContractStates` must include a parameter to indicate the participants that store the states. Add this property to the `AppleStamp`:

```kotlin
override val participants: List<PublicKey>
```

After adding these properties, your code should look like this:

```kotlin
@BelongsToContract(AppleStampContract::class)
class AppleStamp(
    val id: UUID,
    val stampDesc: String,
    val issuer: Party,
    val holder: Party,
    override val participants: List<PublicKey>
) : ContractState
```

{{< note >}}
The `PublicKey`s referred to in the `participants` property are the `ledgerKey`s of the participants expected to store the states.
{{< /note >}}

### Add Imports

If you’re using IntelliJ or another IDE, the IDE automatically adds the imports you need. IntelliJ indicates that an import is missing with red text.

Once you have added all imports, your code should look like this:

```kotlin
package net.cordapp.utxo.apples.states

import net.corda.v5.ledger.common.Party
import net.corda.v5.ledger.utxo.BelongsToContract
import net.corda.v5.ledger.utxo.ContractState
import net.cordapp.utxo.apples.contracts.AppleStampContract
import java.security.PublicKey
import java.util.UUID

@BelongsToContract(AppleStampContract::class)
class AppleStamp(
    val id: UUID,
    val stampDesc: String,
    val issuer: Party,
    val holder: Party,
    override val participants: List<PublicKey>
) : ContractState
```

### Create the `BasketOfApples` State

The `BasketOfApples` state is the basket of apples that Farmer Bob self-issues to prepare the apples for Peter. Now that you’ve written your first state, try writing the `BasketOfApples` state using the following information.

Properties:

* `description` - The brand or type of apple. Use type `String`.

* `farm` - The origin of the apples. Use type `Party`.

* `owner` - The person exchanging the basket of apples for the voucher (Farmer Bob). Use type `Party`.

* `weight` - The weight of the basket of apples. Use type `int`.

The `BasketOfApples` state is involved in two transactions. In the first transaction, Farmer Bob self-issues the `BasketOfApples`. The `Farm` party then fills both the `owner` and `farm` fields of the transaction.

#### Check Your Work

Once you’ve written the `BasketOfApples` state, check your code against the sample below. Your code should look something like this:

```kotlin
package net.cordapp.utxo.apples.states

import net.corda.v5.ledger.common.Party
import net.corda.v5.ledger.utxo.BelongsToContract
import net.corda.v5.ledger.utxo.ContractState
import net.cordapp.utxo.apples.contracts.BasketOfApplesContract
import java.security.PublicKey

@BelongsToContract(BasketOfApplesContract::class)
class BasketOfApples(
    val description: String,
    val farm: Party,
    val owner: Party,
    val weight: Int,
    override val participants: List<PublicKey>
) : ContractState {

    fun changeOwner(buyer: Party): BasketOfApples {
        val participants = listOf(farm.owningKey, buyer.owningKey)
        return BasketOfApples(description, farm, buyer, weight, participants)
    }
}
```

## Next Steps

Follow the [Write Contracts](basic-cordapp-contract.md) tutorial to continue on this learning path.
