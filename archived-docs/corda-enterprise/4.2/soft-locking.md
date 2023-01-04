---
aliases:
- /releases/4.2/soft-locking.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-soft-locking
    parent: corda-enterprise-4-2-key-concepts-vault
    weight: 1010
tags:
- locking
title: Soft Locking
---


# Soft Locking

Soft Locking is implemented in the vault to try and prevent a node constructing transactions that attempt to use the same input(s) simultaneously.
Such transactions would result in naturally wasted work when the notary rejects them as double spend attempts.

Soft locks are automatically applied to coin selection (eg. cash spending) to ensure that no two transactions attempt to
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

[VaultService.kt](https://github.com/corda/corda/blob/release/os/4.1/core/src/main/kotlin/net/corda/core/node/services/VaultService.kt)


## Query

By default vault queries will always include locked states in its result sets.
Custom filterable criteria can be specified using the `SoftLockingCondition` attribute of `VaultQueryCriteria`:

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

[QueryCriteria.kt](https://github.com/corda/corda/blob/release/os/4.1/core/src/main/kotlin/net/corda/core/node/services/vault/QueryCriteria.kt)


## Explicit Usage

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


## Use Cases

A prime example where *soft locking* is automatically enabled is within the process of issuance and transfer of fungible
state (eg. Cash). An issuer of some fungible asset (eg. Bank of Corda) may wish to transfer that new issue immediately
to the issuance requester (eg. Big Corporation). This issuance and transfer operation must be *atomic* such that another
flow (or instance of the same flow) does not step in and unintentionally spend the states issued by Bank of Corda
before they are transferred to the intended recipient. Soft locking will automatically prevent new issued states within
`IssuerFlow` from being spendable by any other flow until such time as the `IssuerFlow` itself terminates.

Other use cases for *soft locking* may involve competing flows attempting to match trades or any other concurrent
activities that may involve operating on an identical set of unconsumed states.
