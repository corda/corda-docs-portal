---
date: '2021-07-15'
menu:
  corda-enterprise-4-10:
    identifier: corda-enterprise-4-10-cordapps-states
    name: "Writing CorDapp states"
    parent: corda-enterprise-4-10-cordapps
tags:
- api
- states
title: CorDapp states
weight: 60
---

# CorDapp states

Before you read this article, make sure you understand the [state key concepts]({{< relref "../key-concepts-states.md" >}}).

In Corda, a contract state (or just ‘state’) stores data that the CorDapp needs to move from one transaction to another.

States are:
* Immutable. That means they can never be updated - any change to a state generates a new successor state. This is called **consuming** the state.
* Single-use. You can only consume a state once - this prevents double-spending. The notary only signs transactions if the input states are all free.

States are instances of classes that implement `ContractState`:

```kotlin
@KeepForDJVM
@CordaSerializable
interface ContractState {
    val participants: List<AbstractParty>
}
```

`ContractState` has a single field, `participants`. `participants` is a `List` of the `AbstractParty` that
has a stake in the state. A `participant` is any party that should be notified if the state is
created or consumed.

Certain types of transactions require a list of participants. For example, when changing the notary of a
state, every participant must approve the transaction. They then receive the updated, post-notary-change state. This prevents a situation where participants in a transaction end up holding a spent state, because another participant consumed that state while performing a notary change.

Derive the participants list from the contents of the state.

The `participants` in a state:

* Store the state in their vault (in most instances).
* Sign any notary change and contract upgrade transactions.
* Receive any finalized transactions as part of `FinalityFlow` / `ReceiveFinalityFlow`.

{{< note >}}
See [Reissuing states](reissuing-states.md) for information about reissuing states with a guaranteed state replacement, which allows you to break transaction backchains.
{{< /note >}}

## ContractState sub-interfaces

You can customize the behavior of the state by implementing sub-interfaces of `ContractState`. The two most
common sub-interfaces are `LinearState` and `OwnableState`.

* `LinearState`: If there is only one version of facts for any point in time, use a `LinearState`. `LinearState`
states evolve in a straight line by superseding themselves.
* `OwnableState`: If you are representing assets that can be freely split and merged over time, use `OwnableState`. Cash is a good example of an `OwnableState` - two existing $5 cash states can be combined into a single $10 cash state, or split into five $1 cash states. With `OwnableState`, it is the total amount held that is important, rather than the individual units.

You can visualize the hierarchy like this:

{{< figure alt="state hierarchy" width=80% zoom="/en/images/state-hierarchy.png" >}}

### LinearState

The `LinearState` interface is defined as follows:

```kotlin
/**
 * A state that evolves by superseding itself, all of which share the common "linearId".
 *
 * This simplifies the job of tracking the current version of certain types of state in e.g. a vault.
 */
@KeepForDJVM
interface LinearState : ContractState {
    /**
     * Unique id shared by all LinearState states throughout history within the vaults of all parties.
     * Verify methods should check that one input and one output share the id in a transaction,
     * except at issuance/termination.
     */
    val linearId: UniqueIdentifier
}
```

States are immutable and can’t be updated directly. Instead, an evolving fact is represented by a sequence of `LinearState` states that share the same `linearId`, and create an audit trail for the lifecycle of
the fact over time.

To extend a `LinearState` chain (a sequence of states sharing a `linearId`):

* Use the `linearId` to extract the latest state in the chain from the vault.
* Create a new state that has the same `linearId`.
* Create a transaction with:
    * The current latest state in the chain as an input.
    * The newly-created state as an output.

The new state is now the latest state in the chain, representing the current state of the agreement.

`linearId` is of type `UniqueIdentifier`, which is a combination of:

* A Java `UUID` representing a globally unique 128 bit random number.
* An optional external-reference string for referencing the state in external systems.


### OwnableState

The `OwnableState` interface is:

```kotlin
/**
 * Return structure for [OwnableState.withNewOwner]
 */
@KeepForDJVM
data class CommandAndState(val command: CommandData, val ownableState: OwnableState)

/**
 * A contract state that can have a single owner.
 */
@KeepForDJVM
interface OwnableState : ContractState {
    /** There must be a MoveCommand signed by this key to claim the amount. */
    val owner: AbstractParty

    /** Copies the underlying data structure, replacing the owner field with this new value and leaving the rest alone. */
    fun withNewOwner(newOwner: AbstractParty): CommandAndState
}
```

Where:

* `owner` is the `PublicKey` of the asset’s owner.
* `withNewOwner(newOwner: AbstractParty)` creates a copy of the state with a new owner.

Because `OwnableState` models fungible assets that can be merged and split over time, `OwnableState` instances do
not have a `linearId`. $5 of cash created by one transaction is considered identical to $5 of cash produced by
another transaction.


### FungibleState

`FungibleState<T>` is an interface that represents fungible items - items that can be split and merged. That’s the only assumption made by this interface. Implement this interface if you want to represent fractional ownership of one item, or if you have many items.

For example:

* There is only one Mona Lisa. You represent it by issuing 100 tokens, each representing a 1% interest in the Mona Lisa.
* A company issues 1000 shares with a nominal value of 1, in one batch of 1000. This means the single batch of 1000
shares could be split up into 1000 units of 1 share.

The interface is defined as follows:

```kotlin
@KeepForDJVM
interface FungibleState<T : Any> : ContractState {
    /**
     * Amount represents a positive quantity of some token which can be cash, tokens, stock, agreements, or generally
     * anything else that's quantifiable with integer quantities. See [Amount] for more details.
     */
    val amount: Amount<T>
}
```

The interface takes a type parameter `T`, which represents the fungible item. This should describe
the basic type of the asset e.g. GBP, USD, oil, shares in company <X>, etc. and any additional metadata (issuer, grade,
class, etc.). An upper-bound is not specified for `T` to ensure flexibility. Typically, a class would be provided that
implements *TokenizableAssetInfo* so the item can be easily added and subtracted using the `Amount` class.

This interface has been added in addition to `FungibleAsset` to provide some additional flexibility which
`FungibleAsset` lacks, in particular:


* `FungibleAsset` defines an amount property of type `Amount<Issued<T>>`, therefore there is an assumption that all
fungible items are issued by a single well known party but this is not always the case.
* `FungibleAsset` implements `OwnableState`, as such there is an assumption that all fungible items are ownable.


### The `QueryableState` and `SchedulableState` interfaces

You can customize your state by implementing the following interfaces:

* `QueryableState`, which allows the state to be queried in the node’s database using custom attributes (see
api-persistence).
* `SchedulableState`, which allows us to schedule future actions for the state (e.g. a coupon payment on a bond) (see
[Event Scheduling]({{< relref "../event-scheduling.md" >}}).


## User-defined fields

Beyond implementing `ContractState` or a sub-interface, a state is allowed to have any number of additional fields
and methods. For example, here is the relatively complex definition for a state representing cash:

```kotlin
/** A state representing a cash claim against some party. */
@BelongsToContract(Cash::class)
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


## The vault

Whenever a node records a new transaction, it also decides whether it should store each of the transaction’s output
states in its vault. The default vault implementation makes the decision based on whether the state is an `OwnableState`:

* If it is, the vault stores the state if the node is the state’s `owner`.
* If it is not, the vault stores the state if it is one of the `participants`.
* If the node is neither an `owner` or a `participant` in a transaction, it will not store the state in the vault. Instead, the node stores the transaction that created the states in its transaction storage.



## TransactionState

When a `ContractState` is added to a `TransactionBuilder`, it is wrapped in a `TransactionState`:

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
        val contract: ContractClassName = requireNotNull(data.requiredContractClassName) {
            //TODO: add link to docsite page, when there is one.
            """
    Unable to infer Contract class name because state class ${data::class.java.name} is not annotated with
    @BelongsToContract, and does not have an enclosing class which implements Contract. Either annotate ${data::class.java.name}
    with @BelongsToContract, or supply an explicit contract parameter to TransactionState().
    """.trimIndent().replace('\n', ' ')
        },
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
        val constraint: AttachmentConstraint = AutomaticPlaceholderConstraint) {

    private companion object {
        val logger = loggerFor<TransactionState<*>>()
    }

    init {
        when {
            data.requiredContractClassName == null -> logger.warn(
                    """
        State class ${data::class.java.name} is not annotated with @BelongsToContract,
        and does not have an enclosing class which implements Contract. Annotate ${data::class.java.simpleName}
        with @BelongsToContract(${contract.split("\\.\\$").last()}.class) to remove this warning.
        """.trimIndent().replace('\n', ' ')
            )
            data.requiredContractClassName != contract -> logger.warn(
                    """
        State class ${data::class.java.name} belongs to contract ${data.requiredContractClassName},
        but is bundled with contract $contract in TransactionState. Annotate ${data::class.java.simpleName}
        with @BelongsToContract(${contract.split("\\.\\$").last()}.class) to remove this warning.
        """.trimIndent().replace('\n', ' ')
            )
        }
    }
}
```

Where:


* `data` is the state to be stored on-ledger.
* `contract` is the contract governing evolutions of this state.
* `notary` is the notary service for this state.
* `encumbrance` points to another state that must also appear as an input to any transaction consuming this state.
* `constraint` is a constraint on which contract-code attachments can be used with this state.



## Reference states

If you need to use reference data across multiple transactions, you can use a reference state. Reference states are `ContractState`s with unique properties:

* Input and output state contracts can refer to them, but their contracts are not executed during the transaction verification process.
* They are not consumed when the transaction is committed to the ledger. Instead, they are checked to make sure they are up-to-date.  The contract logic doesn't run for the referencing transaction.
* They behave as standard states when they are in an input or output position.

This enables multiple parties to reuse a state, and the state owner to update the state. For example, parties holding related financial instruments could create a reference state for the financial instrument reference data.

The node resolves the chain of provenance for reference states and verifies all dependency transactions the same way it would for a standard state. This ensures the data is valid according to
the contract governing it, and that all previous participants in the state approved prior updates.

**Known limitations:**

*Notary change:* Reference state users usually do not have permission to change the notary assigned to a reference state. If you add a reference state to a transaction that is assigned to a different notary than the input and output states, you must move the inputs and outputs to the notary used by the reference state.

You cannot commit a transaction to a ledger if you add two or more reference states that are assigned to different notaries. If you add reference states assigned to multiple notaries to a transaction builder,
then the check below will fail.


{{< warning >}}
Do not use encumberances with reference states. The data in the encumbered state is likely to take on a different meaning once the encumbrance state is taken into account. If a state is encumbered by an encumbrance state, reference the encumbrance state in the same transaction.

{{< /warning >}}




## State pointers

A `StatePointer` contains a pointer to a `ContractState`. You can include a `StatePointer` in a `ContractState` as a property, or include it in an off-ledger data structure. Perform a lookup to resolve a `StatePointer` to a `StateAndRef`. `StatePointers` do not enable a feature in Corda which was previously unavailable - they use reference states to formalize development patterns that were already possible.

There are two types of pointers:

* **`StaticPointer`s**: You can use `StaticPointer`s with any type of `ContractState`. `StaticPointer`s always point to the same `ContractState`. Use `StaticPointer`s to refer to a specific state from another transaction.
* **`LinearPointer`s**: You can use `LinearPointer`s with `LinearStates`. `LinearPointer`s automatically point you to the latest version of a `LinearState` that the node performing `resolve`.
is aware of. In effect, the pointer “moves” as the `LinearState` is updated. Use `LinearState` to refer to a particular lineage of states.

If the node calling `resolve` has not seen any transactions containing a `ContractState` which the `StatePointer`
points to, then `resolve` will throw an exception. In this case, the node calling `resolve` might be missing some crucial data.

The node calling `resolve` for a `LinearPointer` may have seen and stored transactions containing a `LinearState` with
the specified `linearId`. However, there is no guarantee the `StateAndRef<T>` returned by `resolve` is the most recent
version of the `LinearState`. The node only returns the most recent version that it is aware of.

You can choose to use the `resolveStatePointers` method to resolve any `StatePointer`s contained within inputs or outputs added to a `TransactionBuilder` to reference states. Any data you point to is carried along with the transaction.
