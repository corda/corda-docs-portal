---
date: '2021-09-15'
section_menu: corda-5-dev-preview
menu:
  corda-5-dev-preview:
    identifier: corda-corda-5.0-dev-preview-1-tutorial-c5-basic-cordapp-state-2
    parent: corda-5-dev-preview-1-tutorials-building-cordapp
    weight: 1035
tags:
- tutorial
- cordapp
title: "Write a complex state"
---

Now that you have created a state to represent a voucher, you must create a `BoardingTicket` state to represent the ticket that the customer receives when they redeem their `MarsVoucher`. This state has some additional complexity—it uses a secondary constructor and helper method to change the owner of the `BoardingTicket`.

You will be creating this state in the same directory as `MarsVoucher` (`contracts/src/main/kotlin/net/corda/missionMars/states/`).

## Create the `BoardingTicket` state

The `BoardingTicket` state represents the ticket that Mars Express issues to a customer when they redeem their `MarsVoucher`. The state must include:

* Trip information.
* The company issuing the ticket.
* The current owner of the ticket.
* The number of days until the rocket launch.

The `BoardingTicket` state must be transferable between the issuer and the customer. A customer must redeem their boarding ticket when they get on the rocket to Mars. When the ticket is redeemed, the state is consumed and the ticket cannot be used again.

### Set up the `BoardingTicket` class

1. Right-click the **states** folder, select **New > Kotlin Class/File**.

2. In the **New Kotlin Class/File** window, select **Class** and create a file called `BoardingTicket`.

3. Open the file.

### Define the `BoardingTicket` data class

Include these variables in the `BoardingTicket` data class:

* `description`: Trip information. Use type `String`.
* `marsExpress`: The space travel company issuing the ticket. Use type `Party`.
* `owner`: The party exchanging the voucher for the ticket. Use type `Party`.
* `launchDate`: The date of the trip launch. Use type `LocalDate`.

This is what your code should look like now:

```kotlin
package net.corda.missionMars.states

import net.corda.v5.application.identity.Party

data class BoardingTicket(
        var description : String, //Trip information
        var marsExpress : Party, //Party selling the ticket
        var owner: Party, //The party who exchanges the ticket for the voucher
        var launchDate: LocalDate) {

    }
```

### Implement the `ContractState` interface

Use <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#contractstate">`ContractState`s</a> to create the `BoardingTicket` state. The state must use the `participants` field, but as it has no additional requirements you do not need to use any of `ContractState`'s sub-interfaces.

`ContractState` allows Corda to use the `BoardingTicket` class as a state. As in the `MarsVoucher` state, you need to implement a method to populate the `participants` of the state.

Your code should look like this now:

```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.ledger.contracts.ContractState

data class BoardingTicket(
        var description : String, //Trip information
        var marsExpress : Party, //Party selling the ticket
        var owner: Party, //The party who exchanges the ticket for the voucher
        var launchDate: LocalDate)
    : ContractState, JsonRepresentable {

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(marsExpress,owner)
  }
```

### Implement the `JsonRepresentable` interface to use the Corda RPC Client

`JsonRepresentable` ensures the object can be serialized to JSON and called over RPC. Implement this interface in `BoardingTicket` so that it can be used with the Corda RPC Client.

{{< note >}}
There are several ways to return your parameters in a JSON string. This tutorial shows you one method, but you are not restricted to using this specific method in Corda.
{{< /note >}}

1. Create a data transfer object that encapsulates the data of your `BoardingTicket` state—`BoardingTicketDto`. Include the same variables as the `BoardingTicket` class (`description`, `marsExpress`, `owner`, and `launchDate`) and define all variable types as `String`.
2. Create a function that instantiates the `BoardingTicketDto`.
3. Create an override function that converts the `BoardingTicketDto` variables to JSON using the `toJson` method.

Your code should now look like this:

```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.contracts.ContractState
import java.time.LocalDate
import java.util.*

data class BoardingTicket(
        var description : String, //Trip information
        var marsExpress : Party, //Party selling the ticket
        var owner: Party, //The party who exchanges the ticket for the voucher
        var launchDate: LocalDate)
    : ContractState, JsonRepresentable {

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(marsExpress,owner)

    fun toDto(): BoardingTicketDto {
        return BoardingTicketDto(
                description,
                marsExpress.name.toString(),
                owner.name.toString(),
                launchDate.toString()
        )
    }

    override fun toJsonString(): String {
        return Gson().toJson(this.toDto())
    }
}

data class BoardingTicketDto(
        var description : String, //Ticket information
        var marsExpress : String, //Origin of the ticket
        var owner: String, //The person who exchanges the ticket for the voucher
        var launchDate: String
)
```
### Define a secondary constructor and helper method to change the ticket owner

The `BoardingTicket` state is involved in two transactions. In the first transaction, Mars Express self-issues the `BoardingTicket`. The `marsExpress` party then fills both the `owner` and `marsExpress` fields of the transaction. In the second transaction, an ownership transfer occurs. Since you cannot change an immutable object, this creates a new instance of the `BoardingTicket` state on the ledger. While states are immutable, the ledger as a whole is mutable as states are created and consumed.

To implement this functionality:

1. Define a secondary constructor that creates the default `BoardingTicket` state. This constructor assigns `marsExpress` as the default `owner` of the ticket when no customer is specified.
2. Define a helper method that changes the owner of the `BoardingTicket` state—`changeOwner`. This function is used when Mars Express issues a `BoardingTicket` to a customer and returns the `BoardingTicket` with its updated variables.

You've finished writing the `BoardingTicket` state. Your code should look like this:

```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.contracts.ContractState
import java.time.LocalDate
import java.util.*

data class BoardingTicket(
        var description : String, //Trip information
        var marsExpress : Party, //Party selling the ticket
        var owner: Party, //The party who exchanges the ticket for the voucher
        var launchDate: LocalDate)
    : ContractState, JsonRepresentable {

    //Secondary Constructor
    constructor(description: String, marsExpress: Party, launchDate: LocalDate) : this(
            description = description,
            marsExpress = marsExpress,
            owner = marsExpress,
            launchDate = launchDate
    )

    fun changeOwner(buyer: Party): BoardingTicket {
        return BoardingTicket(description, marsExpress, buyer, launchDate)
    }

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(marsExpress,owner)

    fun toDto(): BoardingTicketDto {
        return BoardingTicketDto(
                description,
                marsExpress.name.toString(),
                owner.name.toString(),
                launchDate.toString()
        )
    }

    override fun toJsonString(): String {
        return Gson().toJson(this.toDto())
    }
}

data class BoardingTicketDto(
        var description : String, //Ticket information
        var marsExpress : String, //Origin of the ticket
        var owner: String, //The person who exchanges the ticket for the voucher
        var launchDate: String
)
```

## Next steps

Follow the tutorial on [writing contracts](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-contract.md) to continue on this learning path.
