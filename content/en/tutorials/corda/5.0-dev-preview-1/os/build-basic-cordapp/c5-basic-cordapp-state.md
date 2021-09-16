---
date: '2021-09-15'
section_menu: tutorials
menu:
  tutorials:
    identifier: corda-corda-5.0-dev-preview-1-os-tutorial-c5-basic-cordapp-state
    parent: corda-5.0-dev-preview-1-os-tutorial-c5-basic-cordapp-intro
    weight: 1030
tags:
- tutorial
- cordapp
title: Write states
---

In Corda, states are immutable objects on the ledger that represent a fact known by one or more Corda nodes at a specific point in time. They can represent facts of any kind - for example, stocks, bonds, loans, and so on. States relevant to a specific node are stored in that node's vault. For a state to evolve, the current state must be marked as historic and a new, updated state must be created.

When you create a state, you include the relevant information about the fact you are storing. You also include a reference to the contract that governs how the states should evolve over time.

States in the Corda 5 Developer Preview are largely the same as states in Corda 4. A state still must implement `ContractState` or one of its dependents. The main difference when writing states with the Developer Preview is that you must add a <a href="#add-the-json-representable">`JsonRepresentable`</a>. This ensures that the output can be returned over RPC.

This tutorial guides you through writing the two states you need in your CorDapp: `MarsVoucher` and `BoardingTicket`. You will be creating these states in the `contracts/src/main/kotlin/com/marsvoucher/states/` directory in this tutorial. Refer to the `TemplateState.kt` file in this directory to see a template state.

## Learning objectives

After you have completed this tutorial, you will know how to create and implement states in a CorDapp.

## Before you start

Before you start building states, read [Key concepts: States](../../../../../platform/corda/4.8/open-source/key-concepts.md).

## Clone the CorDapp template repo

The easiest way to write any CorDapp is to start from a template. This ensures that you have the correct files to begin building.

1. Navigate to the Kotlin template repository.
  * https://github.com/corda/cordapp-template-kotlin
<!--Update with correct link for dev preview. XXX -->

2. Open a terminal window in the directory where you want to download the CorDapp template.

3. Run the following command:

   ```kotlin
   git clone https://github.com/corda/cordapp-template-kotlin.git
   ```
<!--Update with correct link for dev preview. XXX -->

4. After you have cloned the repository you wish to use, navigate to the correct subdirectory:

   ```kotlin
   cd cordapp-template-kotlin
   ```

5. After you clone the CorDapp template, open the `cordapp-template-kotlin` in [IntelliJ IDEA](https://www.jetbrains.com/idea/).

   If you don't know how to open a CorDapp in IntelliJ, see the documentation on [Running a sample CorDapp](run-demo-cordapp.html#open-the-sample-cordapp-in-intellij-idea).

6. [Rename the package](https://www.jetbrains.com/help/idea/rename-refactorings.html#rename_package) to `missionmars`. This changes all instances of `template` in the project to `missionmars`

## Create the `MarsVoucher` state

First create the `MarsVoucher` state. This state is the voucher issued to customers.

1. Right-click the **states** folder, select **New > Java Class** and create a file called `MarsVoucher`.

2. Open the file.

### Add annotations

The first thing you should do when writing a state is add the `@BelongsToContract` annotation. This annotation establishes the relationship between a state and a contract. Without this, your state does not know which contract is used to verify it.

1. If you've copied in the template state, change the `TemplateContract.class` to `MarsVoucherContract.class`.

2. Add the annotation `@BelongsToContract(MarsVoucherContract.class)` to your state.

This what your code should look like so far:

```java
@BelongsToContract(MarsVoucherContract.class)
```

{{< note >}}
Adding this annotation triggers an error in IntelliJ because you haven't created the `MarsVoucherContract` yet. Ignore this error for now - you will add the contract class in the [Write contracts](XXX) tutorial.
{{< /note >}}

When naming your CorDapp files, it's best practice to match your contract and state names. In this case the state is called `MarsVoucher`, so the contract is called `MarsVoucherContract`. Follow this naming convention when you write an original CorDapp to avoid confusion.

{{< note >}}
You've probably noticed that the state template includes imports at the top of the file. Don't worry, we'll get back to these in a little while.
{{< /note >}}

### Implement the state

The next line of code you add defines the type of <a href="../../../../../platform/corda/4.8/open-source/api-states.html#contractstate">`ContractState`</a> you implement with the `MarsVoucher` data class. Add this line to ensure that Corda recognizes the `MarsVoucher` as a state.

In this case, use a `LinearState` to tie the `MarsVoucher` to a `LinearID`. You will also need to add a `@ConstructorForDeserialization` and a `JsonRepresentable`. You will add the details to this `JsonRepresentable` [later](#add-the-json-representable-data-class).

1. Add the public class `MarsVoucher` implementing a `LinearState`.
2. Add the `@ConstructorForDeserialization`.
3. Add the empty `JsonRepresentable`.

This is what your code should look like now:

```kotlin
@BelongsToContract(MarsVoucherContract::class)
data class MarsVoucher @ConstructorForDeserialization constructor (
) : LinearState, JsonRepresentable{

}
```

### Add private variables

Next, add these private variables:

* `voucherDesc` - voucher description
* `issuer` - the issuer of the voucher
* `holder` - the current owner of the voucher

After adding these variables, your code should look like this:

```kotlin
@BelongsToContract(MarsVoucherContract::class)
data class MarsVoucher @ConstructorForDeserialization constructor (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: Party, //The party who issued the voucher
        val holder: Party, //The party who currently owns the voucher
        override val linearId: UniqueIdentifier,//LinearState required variable
) : LinearState, JsonRepresentable{

}
```

### Add the JSON representable data class

Place the private variables you just defined in a JSON representable data class outside of the `MarsVoucher` class. This sets up a template that the node uses to send this data class to external parties.

After you've added this data class, your code should look like this:

```kotlin
@BelongsToContract(MarsVoucherContract::class)
data class MarsVoucher @ConstructorForDeserialization constructor (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: Party, //The party who issued the voucher
        val holder: Party, //The party who currently owns the voucher
        override val linearId: UniqueIdentifier,//LinearState required variable
) : LinearState, JsonRepresentable{

}

data class MarsVoucherDto(
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: String, //The party who issued the voucher
        val holder: String, //The party who currently owns the voucher
        val linearId: String,//LinearState required variable
)
```

### Add the JSON representable

As noted in the [introduction](c5-basic-cordapp-intro.md), you must pass JSON parameters if you want the output to be returned over RPC. All of your CorDapp's external interactions are now performed via HTTP-RPC REST APIs, so you can no longer pass objects to the RPC, you must parse a JSON-formatted object. You must pass information to the node using a `JsonRepresentable`. The node will return information in the same way.

You must also add `participants` here. In Corda 4, you could add `participants` to the class directly. In the Corda 5 Developer Preview, however, you must add the `participants` separately.

1. Add a JSON representable with your variables. All of your variables must be strings.

2. Add `participants` inside the JSON representable.

3. Add a helper method that fills out the template for the node. The output contains all private variables in string format and their associated data.

After you've added these items, your code should look like this:

```kotlin
@BelongsToContract(MarsVoucherContract::class)
data class MarsVoucher @ConstructorForDeserialization constructor (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: Party, //The party who issued the voucher
        val holder: Party, //The party who currently owns the voucher
        override val linearId: UniqueIdentifier,//LinearState required variable
) : LinearState, JsonRepresentable{

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(issuer,holder)

    fun toDto(): MarsVoucherDto {
        return MarsVoucherDto(
                voucherDesc,
                issuer.name.toString(),
                holder.name.toString(),
                linearId.toString()
        )
    }

    override fun toJsonString(): String {
        return Gson().toJson(this.toDto())
    }
}

data class MarsVoucherDto(
      val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
      val issuer: String, //The party who issued the voucher
      val holder: String, //The party who currently owns the voucher
      val linearId: String,//LinearState required variable
)
```

### Add imports

If you're using IntelliJ or another IDE, the IDE automatically adds the imports you need.

IntelliJ indicates that an import is missing with red text. To add the import:

1. Click the red text. A message appears: "Unresolvable reference: {name of the missing input}".

2. On MacOS: press **Option** + **Enter** to automatically import that variable.

    On Windows: press **Alt** + **Enter** to automatically import that variable.

3. Repeat this process with all missing imports.

Once you have added all imports, your code should look like this:

```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.missionMars.contracts.MarsVoucherContract
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.BelongsToContract
import net.corda.v5.ledger.contracts.LinearState

@BelongsToContract(MarsVoucherContract::class)
data class MarsVoucher @ConstructorForDeserialization constructor (
  val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
  val issuer: Party, //The party who issued the voucher
  val holder: Party, //The party who currently owns the voucher
  override val linearId: UniqueIdentifier,//LinearState required variable
) : LinearState, JsonRepresentable{

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(issuer,holder)

    fun toDto(): MarsVoucherDto {
        return MarsVoucherDto(
                voucherDesc,
                issuer.name.toString(),
                holder.name.toString(),
                linearId.toString()
        )
    }

    override fun toJsonString(): String {
        return Gson().toJson(this.toDto())
    }
}

data class MarsVoucherDto(
      val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
      val issuer: String, //The party who issued the voucher
      val holder: String, //The party who currently owns the voucher
      val linearId: String,//LinearState required variable
)

```

## Create the `BoardingTicket` state

The `BoardingTicket` state is the ticket that Mars Express self-issues to later give to Peter. Now that you've written your first state, try writing the `BoardingTicket` state using the following information.

Private variables:
* `description` - Trip information. Use type `String`.
* `marsExpress` - The space travel company issuing the ticket. Use type `Party`.
* `owner` - The party exchanging the ticket for the voucher. Use type `Party`.
* `date` - The launch date of the trip. Use type `Date`.

The `BoardingTicket` state is involved in two transactions. In the first transaction, Mars Express self-issues the `BoardingTicket`. The `marsExpress` party then fills both the `owner` and `marsExpress` fields of the transaction. You could compact the transaction to carry only these parameters: `public BoardingTicket(String description, Party marsExpress, Date date) {}`

<!---
If you are writing in Java, when you have multiple constructors in one state class, you must annotate which constructor is the base for serialization. This constructor will most likely carry all relevant information for the state. For example, the constructor `public BasketOfApple(String description, Party farm, int weight) {}`), does not have an `owner` field. You must create another constructor that has all fields, and annotate this constructor with `@ConstructorForDeserialization`.
Commenting this out as we don't yet have the Java version.--->

### Check your work

Once you've written the `BoardingTicket` state, check your code against the sample below. Your code should look like this:

```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.missionMars.contracts.BoardingTicketContract
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.contracts.BelongsToContract
import net.corda.v5.ledger.contracts.ContractState
import java.util.*

@BelongsToContract(BoardingTicketContract::class)
data class BoardingTicket(
        var description : String, //Trip information
        var marsExpress : Party, //Party selling the ticket
        var owner: Party, //The party who exchanges the ticket for the voucher
        var date: Date)
    : ContractState, JsonRepresentable {

    //Secondary Constructor
    constructor(description: String, spaceCompany: Party, date: Date) : this(
            description = description,
            spaceCompany = spaceCompany,
            owner = spaceCompany,
            date = date
    )

    fun changeOwner(buyer: Party): BoardingTicket {
        return BoardingTicket(description, spaceCompany, buyer, date)
    }

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(spaceCompany,owner)

    fun toDto(): BoardingTicketDto {
        return BoardingTicketDto(
                description,
                spaceCompany.name.toString(),
                owner.name.toString(),
                date.toString()
        )
    }

    override fun toJsonString(): String {
        return Gson().toJson(this.toDto())
    }
}

data class BoardingTicketDto(
        var description : String, //Brand or type
        var spaceshipCompany : String, //Origin of the apple
        var owner: String, //The person who exchange the basket of apple with the stamp.
        var date: String
)
```

## Next steps

Follow the [Write contracts](c5-basic-cordapp-contract.md) tutorial to continue on this learning path.

## Related content

* [API: States](../../../../../platform/corda/4.8/open-source/api-states.md#api-states)
* [Reissuing states](../../../../../platform/corda/4.8/open-source/reissuing-states.md)
