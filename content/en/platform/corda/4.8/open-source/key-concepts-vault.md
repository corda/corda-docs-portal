---
aliases:
- /head/key-concepts-vault.html
- /HEAD/key-concepts-vault.html
- /key-concepts-vault.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-vault
    parent: corda-os-4-8-key-concepts
    weight: 1090
tags:
- concepts
- vault
title: Vault
---


# Vault


A Corda vault is a database containing all data from the ledger relevant to a node. The database keeps track of both spent and unspent (consumed and unconsumed) states. From a business perspective, this means a record of all the transaction states that can be spent by you as the node owner, as well as a record of all spent states from transactions relevant to you. It can be compared to a wallet in crypto currency - a record of what you have spent, and how much you have available to spend. You can also attach descriptive textual notes against any transaction stored in the vault.

### Spent and unspent states

**Unspent** or unconsumed states represent:  
    * Fungible states available for spending.
    * States available to transfer to another party.
    * Linear states available for evolution. For example, in response to a lifecycle event on a deal.

**Spent** or consumed states represent a ledger immutable state. These are kept for the purpose of:
    * Transaction reporting.
    * Audit and archives, including the ability to perform joins with app-private data, like customer notes.

Data in your Corda vault can be used to create transactions that send value to another party by combining [fungible states](key-concepts-states.md), and possibly adding a change output that makes the values balance. This process is referred to as ‘coin selection’.

Spending from the vault in this way ensures that transactions respect fungibility rules. The issuer and reference data is preserved as the assets pass from hand to hand.

## Data management on and off ledger

The vault supports the management of data in both authoritative **on-ledger** form and, where appropriate, shadow **off-ledger** form:

* On-ledger data refers to distributed ledger state (cash, deals, trades) to which a party is participant.
* Off-ledger data refers to a party's internal reference, static, and systems data.

This diagram illustrates the breakdown of the vault into sub-system components:

{{< figure alt="vault" width=80% zoom="/en/images/vault.png" >}}

You can see:

* The vault's on-ledger store tracks unconsumed state and is updated internally by the node upon recording of a transaction on the ledger
(following successful smart contract verification and signature by all participants).
* The vault “Off Ledger” store refers to additional data added by the node owner subsequent to transaction recording.
* The vault performs fungible state spending (and in future, fungible state optimisation management including merging, splitting and re-issuance).
* Vault extensions represent additional custom plugin code a developer may write to query specific custom contract state attributes.
* Customer “Off Ledger” (private store) represents internal organisational data that may be joined with the vault data to perform additional reporting or processing.
* A [Vault Query API](api-vault-query.md) is exposed to developers using standard Corda RPC and CorDapp plugin mechanisms.
* A vault update API is internally used by transaction recording flows.
* The vault database schemas are directly accessible via JDBC for customer joins and queries.

## The Archive

To prevent a node database from becoming too large, you can use the Archive service to remove all but the minimum required data relating to consumed transactions. If you plan your CorDapp design accordingly, you can ensure that your spent states are moved to the archive regularly. By using the archive, your vault does not get weighed down by the full backchain data, but retains the essential information to maintain ledger integrity.

Find out more about the [Archive Service](archive-service.md).

## Soft locking to prevent double spend attempts

**Soft locking**  automatically or explicitly reserves states to prevent
multiple transactions within the same node from trying to use the same output simultaneously. Whilst any double spend attempts would
ultimately be detected by a notary, soft locking provides a mechanism of early detection for such unwarranted and
invalid scenarios.

Soft locks are automatically applied to coin selection, like cash spending, to ensure that no two transactions attempt to
spend the same fungible states. The outcome of such an eventuality will result in an `InsufficientBalanceException` for one
of the requesters if there are insufficient number of fungible states available to satisfy both requests.

{{< note >}}

The Cash Contract schema table is now automatically generated upon node startup as Coin Selection now uses
this table to ensure correct locking and selection of states to satisfy minimum requested spending amounts.

{{< /note >}}

Soft locks are also automatically applied within flows that issue or receive new states.
These states are effectively soft locked until flow termination (exit or error) or by explicit release.

In addition, the `VaultService` exposes a number of functions a developer may use to explicitly reserve, release and
query soft locks associated with states as required by their CorDapp application logic:

```kotlin

    /**
     * Reserve a set of [StateRef] for a given [UUID] unique identifier.
     * Typically, the unique identifier will refer to a [FlowLogic.runId]'s [UUID] associated with an in-flight flow.
     * In this case if the flow terminates the locks will automatically be freed, even if there is an error.
     * However, the user can specify their own [UUID] and manage this manually, possibly across the lifetime of multiple
     * flows, or from other thread contexts e.g. [CordaService] instances.
     * In the case of coin selection, soft locks are automatically taken upon gathering relevant unconsumed input refs.
     *
     * @throws [StatesNotAvailableException] when not possible to soft-lock all of requested [StateRef].
     */
    @Throws(StatesNotAvailableException::class)
    fun softLockReserve(lockId: UUID, stateRefs: NonEmptySet<StateRef>)

    /**
     * Release all or an explicitly specified set of [StateRef] for a given [UUID] unique identifier.
     * A [Vault] soft-lock manager is automatically notified from flows that are terminated, such that any soft locked
     * states may be released.
     * In the case of coin selection, soft-locks are automatically released once previously gathered unconsumed
     * input refs are consumed as part of cash spending.
     */
    fun softLockRelease(lockId: UUID, stateRefs: NonEmptySet<StateRef>? = null)

```

[VaultService.kt](https://github.com/corda/corda/blob/release/os/4.8/core/src/main/kotlin/net/corda/core/node/services/VaultService.kt)


### Querying the vault with `SoftLockingCondition`

By default, vault queries always include locked states in its result sets. Custom filterable criteria can be specified using the `SoftLockingCondition` attribute of `VaultQueryCriteria`:

```kotlin
    @CordaSerializable
    data class SoftLockingCondition(val type: SoftLockingType, val lockIds: List<UUID> = emptyList())

    @CordaSerializable
    enum class SoftLockingType {
        UNLOCKED_ONLY,  // only unlocked states
        LOCKED_ONLY,    // only soft locked states
        SPECIFIED,      // only those soft locked states specified by lock id(s)
        UNLOCKED_AND_SPECIFIED   // all unlocked states plus those soft locked states specified by lock id(s)
    }

```

[QueryCriteria.kt](https://github.com/corda/corda/blob/release/os/4.8/core/src/main/kotlin/net/corda/core/node/services/vault/QueryCriteria.kt)


### Explicit Usage

Soft locks are associated with transactions, and typically within the lifecycle of a flow. Specifically, every time a
flow is started a soft lock identifier is associated with that flow for its duration (and released upon it’s natural
termination or in the event of an exception). The `VaultSoftLockManager` is responsible within the Node for
automatically managing this soft lock registration and release process for flows. The `TransactionBuilder` class has a
new `lockId` field for the purpose of tracking lockable states. By default, it is automatically set to a random
`UUID` (outside of a flow) or to a flow’s unique ID (within a flow).

Upon building a new transaction to perform some action for a set of states on a contract, a developer must explicitly
register any states they may wish to hold until that transaction is committed to the ledger. These states will be effectively ‘soft
locked’ (not usable by any other transaction) until the developer explicitly releases these or the flow terminates or errors
(at which point they are automatically released).


## An example of soft locking in action

A prime example where *soft locking* is automatically enabled is within the process of issuance and transfer of fungible
state, like cash.

For example, Bank of Corda - an issuer of fungible assets - wants to transfer newly issued assets immediately
to Big Corp, the issuance requester. This issuance and transfer operation must be *atomic*, such that another
flow, or instance of the same flow, does not step in and unintentionally spend the states issued by Bank of Corda
before they are transferred to the intended recipient. Soft locking automatically prevents the new issued states within
`IssuerFlow` from being spendable by any other flow until such time as the `IssuerFlow` itself terminates.

Other use cases for *soft locking* may involve competing flows attempting to match trades or any other concurrent
activities that may involve operating on an identical set of unconsumed states.
