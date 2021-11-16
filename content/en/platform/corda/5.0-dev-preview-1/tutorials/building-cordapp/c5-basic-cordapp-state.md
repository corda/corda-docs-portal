---
date: '2021-09-15'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-state
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1030
tags:
- tutorial
- cordapp
title: "Write a simple state"
---

In Corda, states are immutable objects. One or more Corda nodes agree that these states exist at a specific point in time. These objects can represent any information - in this example, the states represent the voucher for a trip to Mars (`MarsVoucher`) and a ticket (`BoardingTicket`) given to the customer when they redeem their voucher. These states represent information that Mars Express and the customer share and have agreed upon.

States associated to a specific party's identity are stored in that entity's vault. They are also stored in the vaults of relevant parties, or other parties involved in transactions with that state. For a state to evolve, the current state must be marked as historic and a new, updated state must be created. The `MarsVoucher` state is issued by the company Mars Express to Peter, so it is stored in both parties' vaults. When Peter redeems his voucher, the `MarsVoucher` state is spent and this information is updated in both vaults. It's a similar process for the `BoardingTicket` state. The state is issued by Mars Express and spent when Peter takes his trip. Both the voucher and ticket are valid for single-use only - when the states are spent, it guarantees that they cannot be used again.

When you create a state, you include the relevant information about the fact you are storing. The `MarsVoucher` state includes a description of the voucher and the names of the issuer and holder. The `BoardingTicket` includes trip information, the issuer and owner of the ticket, and the days left until the rocket launch. You also include a reference to the contract that governs how the states should evolve over time. The state must implement <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#contractstate">`ContractState`</a> or one of its dependents.

This tutorial guides you through writing the `MarsVoucher` state. You will be creating this state in the `contracts/src/main/kotlin/net/corda/missionMars/states/` directory in this tutorial. Refer to the `TemplateState.kt` file in this directory to see a template state.

## Learning objectives

After you have completed this tutorial and the [Write an advanced state](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-state-2.md) tutorial, you will know how to create and implement states in a Corda 5 Developer Preview CorDapp.

## Before you start

Before you start building states, read [Key concepts: States](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/key-concepts/key-concepts-states.md).

## Clone the CorDapp template repo

The easiest way to write any CorDapp is to start from a template. This ensures that you have the correct files to begin building.

1. Clone the CorDapp template repo in the directory of your choice:

   ```kotlin
   git clone https://github.com/corda/corda5-cordapp-template-kotlin.git
   ```

2. Open `corda5-cordapp-template-kotlin` in [IntelliJ IDEA](https://www.jetbrains.com/idea/).

   If you don't know how to open a CorDapp in IntelliJ, see the documentation on [Running a sample CorDapp](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/run-demo-cordapp.html#open-the-sample-cordapp-in-intellij-idea).

3. If you want to customize the CorDapp template, [rename the package](https://www.jetbrains.com/help/idea/rename-refactorings.html#rename_package) to `missionMars`. This changes all instances of `template` in the project to `missionMars`.

## Create the `MarsVoucher` state

First create the `MarsVoucher` state. This state represents the voucher that Mars Express will issue to its customers and must include:
* A description of the voucher. This can include any relevant information, such as an expiration date.
* The name of the issuer. The customer can then verify which company the voucher was purchased from.
* The name of the current holder. The company can then verify the identity of the customer who redeems the voucher.

The `MarsVoucher` state must be transferable between entities. A customer redeems their voucher by returning it to the company that issued it. The value of this voucher does not change until it is redeemed, when the state is consumed and the voucher cannot be used again. You need a way to track the evolution of this state as it is transferred between parties.

Use a <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#linearstate">`LinearState`</a> to tie the `MarsVoucher` to a `linearId`. When the state is transferred to a new holder, the state evolves. This creates a sequence of `LinearStates` with each evolution. The `LinearState`s share a `linearId`, so you can track the lifecycle of the `MarsVoucher` state.

The `LinearState` makes sense for this use case, but there are several types of <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#contractstate">`ContractState`s</a> that you can use when writing your own CorDapp:

* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#linearstate">`LinearState`</a>
* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#ownablestate">`OwnableState`</a>
* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#fungiblestate">`FungibleState`</a>
* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#the-queryablestate-and-schedulablestate-interfaces">`QueryableState`</a>
* <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#the-queryablestate-and-schedulablestate-interfaces">`SchedulableState`</a>

### Set up the `MarsVoucher` class

1. Right-click the **states** folder, select **New > Kotlin Class/File**.

2. In the **New Kotlin Class/File** window, select **Class** and create a file called `MarsVoucher`.

3. Open the file.

### Define the `MarsVoucher` as a `LinearState`

Next, implement the `LinearState` interface in the `MarsVoucher`. This step ensures that Corda recognizes the `MarsVoucher` as a state.

You also need to add a `@ConstructorForDeserialization` and extend the `JsonRepresentable`. You will add the details to this `JsonRepresentable` [later](#add-the-json-representable-data-class).

1. Add the public class `MarsVoucher` implementing a `LinearState`.
2. Add the `@ConstructorForDeserialization`.
3. Extend the `JsonRepresentable`.

This is what your code should look like now:

```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.missionMars.contracts.MarsVoucherContract
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.UniqueIdentifier
import net.corda.v5.ledger.contracts.BelongsToContract
import net.corda.v5.ledger.contracts.LinearState

data class MarsVoucher @ConstructorForDeserialization constructor (
) : LinearState, JsonRepresentable{

}
```

#### Add content to the state

Next, you need to add the content of the state. Remember that the `MarsVoucher` state will be issued to the customer and it must include parameters for:

*  A description of the voucher - `voucherDesc`
*  The issuer of the voucher - `issuer`
*  The current owner of the voucher- `holder`

In the class, you need to implement a method to populate the `participants` of the state. `participants` is a list of the `AbstractParty` that are involved with the state. The `participants`:

* Store the state in their vault.
* Need to sign any notary-change and contract-upgrade transactions involving this state.
* Receive any finalized transactions involving this state as part of `FinalityFlow`.

After adding these features, your code should look like this:

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

data class MarsVoucher @ConstructorForDeserialization constructor (
        val voucherDesc : String,//For example: "One voucher can be exchanged for one ticket to Mars"
        val issuer: Party, //The party who issued the voucher
        val holder: Party, //The party who currently owns the voucher
        override val linearId: UniqueIdentifier,//LinearState required variable
) : LinearState, JsonRepresentable{

  override val participants: List<AbstractParty> get() = listOf<AbstractParty>(issuer,holder)

}
```

### Make the `MarsVoucher` class transmissible on the Corda RPC Client

The Corda RPC Client takes in JSON parameters. You must pass JSON parameters if you want the output to be returned over RPC. All of your CorDapp's external interactions are now performed via HTTP-RPC REST APIs. The node will return information in the same way.

Add a `JsonRepresentable` to `MarsVoucher` to ensure that it can be transmitted over RPC.

{{< note >}}
There are several ways to return your parameters in a JSON string. The tutorial shows you one method, but you are not restricted to using this specific method in Corda.
{{< /note >}}

#### Add a JSON representable data class

Place the private variables you just defined in a JSON representable data class outside of the `MarsVoucher` class. This sets up a template that the node uses to send this data class to the RPC Client.

After you've added this data class, your code should look like this:

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

### Extend the JSON representable

Add parameters in the form of a `JsonRepresentable` with these components:

* An overridden method from the `JsonRepresentable` interface: `@OverRide`. This is what the node will return each time the node is asked for a JSON representation of the state.
* A `Dto` class that will be used as the template of the returned JSON file. This class marks all variable types as `String`.
* A helper method that instantiates the data class and populates the template with the actual variables of the class.

1. Add the JSON representable with your variables. All of your variables must be strings.

2. Add the helper method that fills out the template for the node. The output contains all private variables in string format and their associated data.

After you've added these items, your code should look like this:

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

## Next steps

Now that you have written the first state for the Mission Mars CorDapp, [write the `BoardingTicket` state](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-state-2.md).
