---
aliases:
- /releases/3.2/api-states.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-api-states
    parent: corda-enterprise-3-2-corda-api
    weight: 1010
tags:
- api
- states
title: 'API: States'
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# API: States

{{< note >}}
Before reading this page, you should be familiar with the key concepts of [States](key-concepts-states.md).

{{< /note >}}


## ContractState

In Corda, states are instances of classes that implement `ContractState`. The `ContractState` interface is defined
as follows:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
/**
 * A contract state (or just "state") contains opaque data used by a contract program. It can be thought of as a disk
 * file that the program can use to persist data across transactions. States are immutable: once created they are never
 * updated, instead, any changes must generate a new successor state. States can be updated (consumed) only once: the
 * notary is responsible for ensuring there is no "double spending" by only signing a transaction if the input states
 * are all free.
 */
@CordaSerializable
interface ContractState {
    /**
     * A _participant_ is any party that is able to consume this state in a valid transaction.
     *
     * The list of participants is required for certain types of transactions. For example, when changing the notary
     * for this state, every participant has to be involved and approve the transaction
     * so that they receive the updated state, and don't end up in a situation where they can no longer use a state
     * they possess, since someone consumed that state during the notary change process.
     *
     * The participants list should normally be derived from the contents of the state.
     */
    val participants: List<AbstractParty>
}

```
{{% /tab %}}



{{< /tabs >}}

`ContractState` has a single field, `participants`. `participants` is a `List` of the `AbstractParty` that
are considered to have a stake in the state. Among other things, the `participants` will:


* Usually store the state in their vault (see below)
* Need to sign any notary-change and contract-upgrade transactions involving this state
* Receive any finalised transactions involving this state as part of `FinalityFlow`


## ContractState sub-interfaces

The behaviour of the state can be further customised by implementing sub-interfaces of `ContractState`. The two most
common sub-interfaces are:


* `LinearState`
* `OwnableState`

`LinearState` models shared facts for which there is only one current version at any point in time. `LinearState`
states evolve in a straight line by superseding themselves. On the other hand, `OwnableState` is meant to represent
assets that can be freely split and merged over time. Cash is a good example of an `OwnableState` - two existing $5
cash states can be combined into a single $10 cash state, or split into five $1 cash states. With `OwnableState`, its
the total amount held that is important, rather than the actual units held.

We can picture the hierarchy as follows:

![state hierarchy](/en/images/state-hierarchy.png "state hierarchy")

### LinearState

The `LinearState` interface is defined as follows:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
/**
 * A state that evolves by superseding itself, all of which share the common "linearId".
 *
 * This simplifies the job of tracking the current version of certain types of state in e.g. a vault.
 */
interface LinearState : ContractState {
    /**
     * Unique id shared by all LinearState states throughout history within the vaults of all parties.
     * Verify methods should check that one input and one output share the id in a transaction,
     * except at issuance/termination.
     */
    val linearId: UniqueIdentifier
}

```
{{% /tab %}}



{{< /tabs >}}

Remember that in Corda, states are immutable and can’t be updated directly. Instead, we represent an evolving fact as a
sequence of `LinearState` states that share the same `linearId` and represent an audit trail for the lifecycle of
the fact over time.

When we want to extend a `LinearState` chain (i.e. a sequence of states sharing a `linearId`), we:


* Use the `linearId` to extract the latest state in the chain from the vault
* Create a new state that has the same `linearId`
* Create a transaction with:
    * The current latest state in the chain as an input
    * The newly-created state as an output



The new state will now become the latest state in the chain, representing the new current state of the agreement.

`linearId` is of type `UniqueIdentifier`, which is a combination of:


* A Java `UUID` representing a globally unique 128 bit random number
* An optional external-reference string for referencing the state in external systems


### OwnableState

The `OwnableState` interface is defined as follows:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin

/**
 * Return structure for [OwnableState.withNewOwner]
 */
data class CommandAndState(val command: CommandData, val ownableState: OwnableState)

/**
 * A contract state that can have a single owner.
 */
interface OwnableState : ContractState {
    /** There must be a MoveCommand signed by this key to claim the amount. */
    val owner: AbstractParty

    /** Copies the underlying data structure, replacing the owner field with this new value and leaving the rest alone. */
    fun withNewOwner(newOwner: AbstractParty): CommandAndState
}

```
{{% /tab %}}



{{< /tabs >}}

Where:


* `owner` is the `PublicKey` of the asset’s owner
* `withNewOwner(newOwner: AbstractParty)` creates an copy of the state with a new owner

Because `OwnableState` models fungible assets that can be merged and split over time, `OwnableState` instances do
not have a `linearId`. $5 of cash created by one transaction is considered to be identical to $5 of cash produced by
another transaction.


### Other interfaces

You can also customize your state by implementing the following interfaces:


* `QueryableState`, which allows the state to be queried in the node’s database using custom attributes (see
[API: Persistence](api-persistence.md))
* `SchedulableState`, which allows us to schedule future actions for the state (e.g. a coupon payment on a bond) (see
[Event scheduling](event-scheduling.md))


## User-defined fields

Beyond implementing `ContractState` or a sub-interface, a state is allowed to have any number of additional fields
and methods. For example, here is the relatively complex definition for a state representing cash:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
    /** A state representing a cash claim against some party. */
    data class State(
            override val amount: Amount<Issued<Currency>>,

            /** There must be a MoveCommand signed by this key to claim the amount. */
            override val owner: AbstractParty
    ) : FungibleAsset<Currency>, QueryableState {
        constructor(deposit: PartyAndReference, amount: Amount<Currency>, owner: AbstractParty)
                : this(Amount(amount.quantity, Issued(deposit, amount.token)), owner)

        override val exitKeys = setOf(owner.owningKey, amount.token.issuer.party.owningKey)
        override val participants = listOf(owner)

        override fun withNewOwnerAndAmount(newAmount: Amount<Issued<Currency>>, newOwner: AbstractParty): FungibleAsset<Currency>
                = copy(amount = amount.copy(newAmount.quantity), owner = newOwner)

        override fun toString() = "${Emoji.bagOfCash}Cash($amount at ${amount.token.issuer} owned by $owner)"

        override fun withNewOwner(newOwner: AbstractParty) = CommandAndState(Commands.Move(), copy(owner = newOwner))
        infix fun ownedBy(owner: AbstractParty) = copy(owner = owner)
        infix fun issuedBy(party: AbstractParty) = copy(amount = Amount(amount.quantity, amount.token.copy(issuer = amount.token.issuer.copy(party = party))))
        infix fun issuedBy(deposit: PartyAndReference) = copy(amount = Amount(amount.quantity, amount.token.copy(issuer = deposit)))
        infix fun withDeposit(deposit: PartyAndReference): Cash.State = copy(amount = amount.copy(token = amount.token.copy(issuer = deposit)))

        /** Object Relational Mapping support. */
        override fun generateMappedObject(schema: MappedSchema): PersistentState {
            return when (schema) {
                is CashSchemaV1 -> CashSchemaV1.PersistentCashState(
                        owner = this.owner,
                        pennies = this.amount.quantity,
                        currency = this.amount.token.product.currencyCode,
                        issuerPartyHash = this.amount.token.issuer.party.owningKey.toStringShort(),
                        issuerRef = this.amount.token.issuer.reference.bytes
                )
            /** Additional schema mappings would be added here (eg. CashSchemaV2, CashSchemaV3, ...) */
                else -> throw IllegalArgumentException("Unrecognised schema $schema")
            }
        }

        /** Object Relational Mapping support. */
        override fun supportedSchemas(): Iterable<MappedSchema> = listOf(CashSchemaV1)
        /** Additional used schemas would be added here (eg. CashSchemaV2, CashSchemaV3, ...) */
    }

```
{{% /tab %}}



{{< /tabs >}}


## The vault

Whenever a node records a new transaction, it also decides whether it should store each of the transaction’s output
states in its vault. The default vault implementation makes the decision based on the following rules:



* If the state is an `OwnableState`, the vault will store the state if the node is the state’s `owner`
* Otherwise, the vault will store the state if it is one of the `participants`


States that are not considered relevant are not stored in the node’s vault. However, the node will still store the
transactions that created the states in its transaction storage.


## TransactionState

When a `ContractState` is added to a `TransactionBuilder`, it is wrapped in a `TransactionState`:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
typealias ContractClassName = String

/**
 * A wrapper for [ContractState] containing additional platform-level state information and contract information.
 * This is the definitive state that is stored on the ledger and used in transaction outputs.
 */
@CordaSerializable
data class TransactionState<out T : ContractState> @JvmOverloads constructor(
        /** The custom contract state */
        val data: T,
        /**
         * The contract class name that will verify this state that will be created via reflection.
         * The attachment containing this class will be automatically added to the transaction at transaction creation
         * time.
         *
         * Currently these are loaded from the classpath of the node which includes the cordapp directory - at some
         * point these will also be loaded and run from the attachment store directly, allowing contracts to be
         * sent across, and run, from the network from within a sandbox environment.
         */
        // TODO: Implement the contract sandbox loading of the contract attachments
        val contract: ContractClassName,
        /** Identity of the notary that ensures the state is not used as an input to a transaction more than once */
        val notary: Party,
        /**
         * All contract states may be _encumbered_ by up to one other state.
         *
         * The encumbrance state, if present, forces additional controls over the encumbered state, since the platform checks
         * that the encumbrance state is present as an input in the same transaction that consumes the encumbered state, and
         * the contract code and rules of the encumbrance state will also be verified during the execution of the transaction.
         * For example, a cash contract state could be encumbered with a time-lock contract state; the cash state is then only
         * processable in a transaction that verifies that the time specified in the encumbrance time-lock has passed.
         *
         * The encumbered state refers to another by index, and the referred encumbrance state
         * is an output state in a particular position on the same transaction that created the encumbered state. An alternative
         * implementation would be encumbering by reference to a [StateRef], which would allow the specification of encumbrance
         * by a state created in a prior transaction.
         *
         * Note that an encumbered state that is being consumed must have its encumbrance consumed in the same transaction,
         * otherwise the transaction is not valid.
         */
        val encumbrance: Int? = null,
        /**
         * A validator for the contract attachments on the transaction.
         */
        val constraint: AttachmentConstraint = AutomaticHashConstraint)

```
{{% /tab %}}



{{< /tabs >}}

Where:


* `data` is the state to be stored on-ledger
* `contract` is the contract governing evolutions of this state
* `notary` is the notary service for this state
* `encumbrance` points to another state that must also appear as an input to any transaction consuming this
state
* `constraint` is a constraint on which contract-code attachments can be used with this state
