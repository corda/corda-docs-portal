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
* The name of the company issuing the ticket. The customer can then verify which company the voucher was purchased from.
* The current owner of the ticket. The company can then verify the identity of the customer who redeems the voucher.
* The number of days until the rocket launch. Both parties are aware of the trip date.

Private variables:
* `description` - Trip information. Use type `String`.
* `marsExpress` - The space travel company issuing the ticket. Use type `Party`.
* `owner` - The party exchanging the ticket for the voucher. Use type `Party`.
* `daysUntilLaunch` - The number of days until the launch date. Use type `int`.

The `BoardingTicket` state is involved in two transactions. In the first transaction, Mars Express self-issues the `BoardingTicket`. The `marsExpress` party then fills both the `owner` and `marsExpress` fields of the transaction.

In the second transaction, an ownership transfer occurs. This means you must implement a helper method to perform the change of ownership.

### Check your work

After you have written the `BoardingTicket` state, your code should look like this:

```kotlin
package net.corda.missionMars.states

import com.google.gson.Gson
import net.corda.missionMars.contracts.BoardingTicketContract
import net.corda.v5.application.identity.AbstractParty
import net.corda.v5.application.identity.Party
import net.corda.v5.application.utilities.JsonRepresentable
import net.corda.v5.ledger.contracts.BelongsToContract
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
