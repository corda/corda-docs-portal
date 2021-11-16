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
title: "Write an advanced state"
---

Now that you have created a state to represent a voucher, you must create a `BoardingTicket` state to represent the ticket that the customer receives when they redeem their `MarsVoucher`. This state has some additional complexity. You will be creating this state in the same directory as the `MarsVoucher` (`contracts/src/main/kotlin/net/corda/missionMars/states/`).

## Create the `BoardingTicket` state

The `BoardingTicket` state represents the ticket that Mars Express issues to a customer when they redeem their `MarsVoucher`. The state must include:

* Trip information.
* The company issuing the ticket. The customer can then verify which company the voucher was purchased from.
* The current owner of the ticket. The company can then verify the identity of the customer who redeems the voucher.
* The number of days until the rocket launch. Both parties are aware of the trip date.

The `BoardingTicket` state must be transferable between the issuer and the customer. A customer must redeem their boarding ticket when they get on the rocket to Mars. The value of the ticket does not change until it is redeemed, when the state is consumed and the ticket cannot be used again.

Use <a href="../../../../../../en/platform/corda/4.8/open-source/api-states.html#contractstate">`ContractState`s</a> to create the `BoardingTicket` state. The state must use the `participants` field, but has no additional requirements so you do not need to use any of `ContractState`'s sub-interfaces.

### Set up the `BoardingTicket` class

1. Right-click the **states** folder, select **New > Kotlin Class/File**.

2. In the **New Kotlin Class/File** window, select **Class** and create a file called `BoardingTicket`.

3. Open the file.

### Define the `BoardingTicket` as a `ContractState`

Next, define the `BoardingTicket` data class, implementing the `ContractState` and `JsonRepresentable` interfaces. `ContractState` allows Corda to use this class as a state, while `JsonRepresentable` ensures the object can be serialized to JSON and called over RPC. Include these variables:

* `description` - Trip information. Use type `String`.
* `marsExpress` - The space travel company issuing the ticket. Use type `Party`.
* `owner` - The party exchanging the voucher for the ticket. Use type `Party`.
* `daysUntilLaunch` - The number of days until the launch date. Use type `int`.

This is what your code should look like now:

```kotlin
package net.corda.missionMars.states

import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.contracts.ContractState

data class BoardingTicket(
        var description : String, //Trip information
        var marsExpress : Party, //Party selling the ticket
        var owner: Party, //The party who exchanges the ticket for the voucher
        var daysUntilLaunch: Int)
    : ContractState, JsonRepresentable {

    }
```

#### Implement the interfaces

override val participants: List<AbstractParty> get() = listOf<AbstractParty>(marsExpress,owner)

fun toDto(): BoardingTicketDto {
    return BoardingTicketDto(
            description,
            marsExpress.name.toString(),
            owner.name.toString(),
            daysUntilLaunch.toString()
    )
}

override fun toJsonString(): String {
    return Gson().toJson(this.toDto())
}



#### Add content to the state

Next, you need to add the content of the state. Define a secondary constructor that

Define a function that changes the owner of the `BoardingTicket` state. `changeOwner` is used when Mars Expresses issues a `BoardingTicket` to the customer.

The `BoardingTicket` state is involved in two transactions. In the first transaction, Mars Express self-issues the `BoardingTicket`. The `marsExpress` party then fills both the `owner` and `marsExpress` fields of the transaction.

In the second transaction, an ownership transfer occurs. This means you must implement a helper method to perform the change of ownership.

#### Add a JSON representable data class

### Check your work

After you have written the `BoardingTicket` state, your code should look like this:

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
        var daysUntilLaunch: Int)
    : ContractState, JsonRepresentable {

    //Secondary Constructor
    constructor(description: String, marsExpress: Party, daysUntilLaunch: Int) : this(
            description = description,
            marsExpress = marsExpress,
            owner = marsExpress,
            daysUntilLaunch = daysUntilLaunch
    )

    fun changeOwner(buyer: Party): BoardingTicket {
        return BoardingTicket(description, marsExpress, buyer, daysUntilLaunch)
    }

    override val participants: List<AbstractParty> get() = listOf<AbstractParty>(marsExpress,owner)

    fun toDto(): BoardingTicketDto {
        return BoardingTicketDto(
                description,
                marsExpress.name.toString(),
                owner.name.toString(),
                daysUntilLaunch.toString()
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
        var daysUntilLaunch: String
)
```

## Next steps

Follow the [Write contracts](../../../../../../en/platform/corda/5.0-dev-preview-1/tutorials/building-cordapp/c5-basic-cordapp-contract.md) tutorial to continue on this learning path.
