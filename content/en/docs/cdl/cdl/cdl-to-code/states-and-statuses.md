---
title: States and statuses
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-states-and-statuses"
    weight: 20

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---


# States and Statuses

A core element of the CDL Smart Contract view is that Corda states can have different statuses. When a state has a particular status, there are different restrictions on the form of the state and the transitions that state can make.

`ContractStates` which require a status property should implement the `StatusState` interface. This requires a `val status: Status?` property to be implemented by the state.

In `ContractUtils`, the interfaces for `StatusState` and `Status` are defined as follows:

{{< tabs name="status interface" >}}
{{% tab name="kotlin" %}}
```kotlin
/**
 * The StatusState interface should be implemented for all [ContractState]s that require a status field.
 *
 * [status] is nullable so that when there is no input or output state in a transaction, the status can be represented as [null]
 *
 */
interface StatusState: ContractState {
    val status: Status?
}

/**
 * Statuses are defined as enum classes in the StatusState which should implement this Status interface.
 */
@CordaSerializable
interface Status

```
{{% /tab %}}
{{< /tabs >}}

You can see that `status` is nullable because the intention is to represent no state as a status `null`. For example, when defining Paths allowed in transactions which have no input state, you define the input status as `null` so you can map  `null` -> allowed Paths when there is no input state.

These interfaces are used to define the `AgreementState` and the enum set of statuses based on the CDL status states:

{{< figure zoom="./resources/cdl-agreement-smart-contract-statuses.png" width="1000" title="Click to zoom image in new tab/window" >}}

AgreementState.kt:

{{< tabs name="implement the state" >}}
{{% tab name="kotlin" %}}
```kotlin
@BelongsToContract(AgreementContract::class)
data class AgreementState(override val status: AgreementStatus?,
                          val buyer: Party,
                          val seller: Party,
                          val goods: String,
                          val price: Amount<Currency>,
                          val proposer: Party,
                          val consenter: Party,
                          val rejectionReason: String? = null,
                          val rejectedBy: Party?= null,
                          override val participants: List<AbstractParty> = listOf(buyer, seller),
                          override val linearId: UniqueIdentifier = UniqueIdentifier()) : LinearState, StatusState

enum class AgreementStatus: Status {
    PROPOSED,
    REJECTED,
    AGREED
}

```
{{% /tab %}}
{{< /tabs >}}
