---
date: '2021-09-23'
title: Query API
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-persistence
    identifier: corda-5-dev-preview-1-cordapps-persistence-query
    weight: 1200
section_menu: corda-5-dev-preview
---

This guide explains how to use the `query` functions.

For instructions on how to call named-query APIs from HTTP-RPC, see the [HTTP-RPC Named Query API](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/http-named-query-api.md) guide.

Named queries:
* Are static `Strings` defined on JPA entities using the `@NamedQuery` annotation.
* Are given a name and can be executed by the `PersistenceService` query APIs.
* Are like stored procedures, they are written in JPQL and are similar to SQL, but they query for entities rather than tables.
* Require fully qualified class names of entity classes.
* Support named parameters allowing users to input data into `WHERE` clauses.

Named parameters are prefixed with a colon in the query string.

## Create a named-query cursor

The `PersistenceService` provides several query APIs which take (at a minimum) the name of a named-query and a map of named parameters.

Use these to create a named-query `Cursor` object which can then be polled for results:

```kotlin
fun <R> query(
    queryName: String,
    namedParameters: Map<String, Any>
): Cursor<R>

fun <R> query(
    queryName: String,
    namedParameters: Map<String, Any>,
    postFilter: NamedQueryFilter
): Cursor<R>

fun <R> query(
    queryName: String,
    namedParameters: Map<String, Any>,
    postProcessorName: String
): Cursor<R>

fun <R> query(
    queryName: String,
    namedParameters: Map<String, Any>,
    postFilter: NamedQueryFilter,
    postProcessorName: String
): Cursor<R>

fun <R> query(persistenceQueryRequest: PersistenceQueryRequest): Cursor<R>
```

In this object:
* `queryName` is the name of the named-query that has already been defined. For example, `"VaultState.findByStateStatus"`.
* `namedParameters` is the map of named parameters to be set into the query. For example, "stateStatus": `"... WHERE stateStatus = :stateStatus`.
* `postProcessorName` is optional and defines the name of a post-processor to transform named-query results.
* `postFilter` is optional and applies a post-filtering step after named-query execution.
* `persistenceQueryRequest` is a data class with a builder, handy for Java users.
* Results are cast to generic type `R`.

## Polling the cursor

The query APIs return a `Cursor` object and this can be used to page through results:

1. Call the `poll` function with the max poll size and timeout duration.
  - `poll` is `@Suspendable`
2. Utilize `Cursor.PollResult.isLastResult` to loop over all results until reaching the end.
3. Use `Cursor.PollResult.values` to get the values from a batch of data.

The `Cursor` interface is defined as follows:

```kotlin
interface Cursor<T> {
    fun asyncPoll(maxCount: Int, awaitForResultTimeout: Duration): CompletableFuture<PollResult<T>> {
        return CompletableFuture.supplyAsync { poll(maxCount, awaitForResultTimeout) }
    }

    @Suspendable
    fun poll(maxCount: Int, awaitForResultTimeout: Duration): PollResult<T>

    @CordaSerializable
    @DoNotImplement
    interface PollResult<T> {
        val positionedValues: List<PositionedValue<T>>
        val values: List<T> get() = positionedValues.map { it.value }
        val firstPosition: Long get() = positionedValues.first().position
        val lastPosition: Long get() = positionedValues.last().position
        val remainingElementsCountEstimate: Long?
        val isEmpty: Boolean get() = positionedValues.isEmpty()
        val isLastResult: Boolean

        @CordaSerializable
        @DoNotImplement
        interface PositionedValue<T> {
            val value: T
            val position: Long
        }
    }
}
```

This example creates the cursor (typed to `SomeEntity`) and polls once for a list of up to 100 `MyEntity`.

```kotlin
val cursor: Cursor<SomeEntity> = persistenceService.query<SomeEntity>(
    "SomeEntity.findAllBySomeNamedParam",
    mapOf("someNamedParam" to someValue)
)
val someEntities: List<SomeEntity> = cursor.poll(100, 10.seconds)
    .values
```

This example creates the cursor and pages through all the results while `poll.isLastResult` is false.

```kotlin
val cursor: Cursor<SomeEntity> = persistenceService.query<SomeEntity>(
    "SomeEntity.findBySomeNamedParam",
    mapOf("someNamedParam" to someValue)
)
val accumulator = mutableListOf<SomeEntity>()
var poll = cursor.poll(25, 10.seconds)
while(!poll.isLastResult) {
    accumulator.addAll(poll.values)
    poll = cursor.poll(25, 10.seconds)
}
return accumulator
```

## Create your own named queries

Named queries are written in JPQL. They can include features like `JOIN`, `WHERE`, sub-queries, constructor expressions, and aggregate functions.

You can annotate entities with `@NamedQuery` or `@NamedQueries` for multiple definitions, for example:

```kotlin
@Entity
    @NamedQueries(
        NamedQuery(name = "RecordedItem.findByItemName", query = "from net.corda.sample.datapersistence.schema.RecordedItemSchemaV1\$RecordedItem where itemName = :itemName"),
        NamedQuery(name = "RecordedItem.findByItemIdIn", query = "from net.corda.sample.datapersistence.schema.RecordedItemSchemaV1\$RecordedItem where itemId IN :itemIds")
    )
    @Table(name = "recorded_item")
    @CordaSerializable
    data class RecordedItem(
            @Id
            @Column(name = "item_id")
            var itemId: String,
            @Column(name = "item_name")
            var itemName: String,
            @Column(name = "item_time")
            var itemTimestamp: java.time.Instant
    ) : Serializable
```
To use these named queries in the query API, provide either the name `"RecordedItem.findByItemName"` or `"RecordedItem.findByItemIdIn"`.

Named queries can also join with ledger tables, for example:

```kotlin
    @Entity
    @Table(name = "pet_states")
    @NamedQuery(name = "PersistentPet.findUnconsumedByName",
        query = "SELECT pet" +
                " FROM net.corda.linearstatesample.schema.PetSchemaV1\$PersistentPet pet," +
                " net.corda.v5.ledger.schemas.vault.VaultSchemaV1\$VaultState state" +
                " WHERE pet.name = :name" +
                " AND state.stateStatus = 0" +
                " AND state.stateRef.txId = pet.stateRef.txId" +
                " AND state.stateRef.index = pet.stateRef.index"
    )
    class PersistentPet(
            @Column(name = "pet_name")
            var name: String,

            @Column(name = "pet_owner")
            var ownerName: String,

            @Column(name = "pet_linear_id")
            @Convert(converter = UUIDConverter::class)
            var linearId: UUID
    ) : PersistentState()
```
This named-query joins `VaultSchemaV1.VaultState` on `txId` and `index`.

## Post-processing

Post-processing is an optional in-memory transformation step applied to named-query results on remote database worker processes before they are returned to the user.

Persistence operations are performed on a separate database worker process, therefore, results from the Query API must be serialized and transmitted from this process to the user via a messaging bus.

A post-processor gives you the opportunity to transform entities into custom objects before the results are sent over the wire to the user.

For example, a post-processor can:
* Transform entities into custom objects.
* Pick desirable fields from entities to return lighter-weight objects.
* Convert entities to JSON or JSON serializable objects.
* Return `ContractStates` or `StateAndRefs`.

### Using post-processors

All post-processors have a name and this name is provided to the `query` API as a simple `String`.

Corda provides two built-in post-processors. These can be used when entities returned from named-queries extend `PersistentState` (therefore have a `StateRef`) and can be transformed into `StateAndRef` or `ContractState`:
* `"Corda.IdentityContractStatePostProcessor"`
* `"Corda.IdentityStateAndRefPostProcessor"`

This example uses the named-query "PersistentPet.findUnconsumedByName" to find `PersistentPet` entities, and `"IdentityContractStatePostProcessor"` to convert `PersistentPet` entities into `PetStates`.

```kotlin
val cursor = persistenceService.query<PetState>(
    queryName = "PersistentPet.findUnconsumedByName",
    namedParameters = mapOf("name" to "Roger the rabbit"),
    postProcessorName = "Corda.IdentityContractStatePostProcessor"
)
val contractStates: List<PetState> = cursor.poll(100, 10.seconds)
    .values
```

### Implementing your own post-processor

The Corda 5 Developer Preview provides two interfaces for you to implement your own custom post-processors:

* `StateAndRefPostProcessor`
* `CustomQueryPostProcessor`

Both interfaces have a `name` property which must be overridden. This is the `postProcessorName` which is used in the APIs.

Optionally, `availableForRpc` can be overridden to `true` to make post-processors available via HTTP Named Query APIs. See [HTTP Named Query API](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/http-named-query-api.md) for more info.

### Implementing `StateAndRefPostProcessor`

* `StateAndRefPostProcessor` can only be used with named-queries that return entities that extend `PersistentState`.
* Each entity has a `StateRef` because it extends `PersistentState`.
* The framework automatically fetches `StateAndRefs` for each `StateRef`.
* The implementation of `postProcess` gets a `Stream<StateAndRef<ContractState>>` as inputs.
* You can select fields, create new objects, and define what is returned.

For example, this post-processor transforms `CustomState` into `PostProcessedObject`:

```kotlin
class CustomStatePostProcessor : StateAndRefPostProcessor<PostProcessedObject> {
    companion object{
        const val POST_PROCESSOR_NAME = "data-persistence.CustomStatePostProcessor"
    }
    override fun postProcess(inputs: Stream<StateAndRef<ContractState>>): Stream<PostProcessedObject> {
        return inputs
                .filter { it.state.data is CustomState }
                .map {
                    val customState = it.state.data as CustomState
                    PostProcessedObject(
                            customState.linearId.id,
                            customState.name,
                            customState.initiatorId,
                            it.state.contract,
                            it.ref.txhash.toString(),
                            it.ref.index,
                            it.state.notary.toString()
                    )
                }
    }

    override val name = POST_PROCESSOR_NAME
    override val availableForRPC = true
}

@CordaSerializable
data class PostProcessedObject(
        val linearId: UUID,
        val name: String,
        val initiatorId: String,
        val contractStateClassName: String,
        val txId: String,
        val index: Int,
        val notaryName: String
)
```

In this example:
* `"data-persistence.CustomStatePostProcessor"` is the `postProcessorName` used in the Query APIs.
* `availableForRPC` is `false` by default. Override this to `true` to allow the post-processor to be called over HTTP-RPC APIs.

### Implementing `CustomQueryPostProcessor`

* `CustomQueryPostProcessor` can be used to transform results from custom named queries that return any custom entities.
* The framework passes raw named-query results to this post-processor.
* No additional fetching of `StateRef` or any other data.
* You should ensure type safety and perform any casting.

For example, this post-processor capitalizes results from a named-query and implements `CustomQueryPostProcessor`:

```kotlin
class StringCapitalizationPostProcessor : CustomQueryPostProcessor<String?> {
    companion object {
        const val POST_PROCESSOR_NAME = "data-persistence.StringCapitalizationPostProcessor"
    }

    override val name = POST_PROCESSOR_NAME

    override fun postProcess(inputs: Stream<Any?>): Stream<String?> {
        return inputs.map {
            if (it is String) {
                it.toUpperCase()
            } else {
                null
            }
        }
    }
}
```

To use this post-processor, pass `"data-persistence.StringCapitalizationPostProcessor"` as the `postProcessorName` field.

### Use a post-processor to return states

You need to take a different approach for `ContractStates` as they aren't entities (named queries only query for entities).

For example, the named-query `"VaultState.findByStateStatus"` quite literally queries for `VaultState` entities.

To obtain actual `ContractState`s, you must provide the name of a `StateAndRefPostProcessor`. Then use a named-query
that returns entities that extend `PersistentState`. This could be either:
* A `QueryableState`'s mapped entity.
* A VaultSchema entity (for example, `VaultState` or `VaultLinearState`).

The framework loads state data for each entity's state reference.

Alternatively, you can implement your own version of `StateAndRefPostProcessor` to process and transform results how you wish.

If you want to post-process `VaultState` entities directly, you can implement `CustomQueryPostProcessor` and the inputs will be the raw named-query `VaultState` entities.

## Query for states when your state does not have a mapped schema

Creating your own query using the `@NamedQuery` annotation is relevant when you have defined an entity. For example, a state that implements `QueryableState` which has a mapped schema entity defined.

But what should you do when your state doesn't implement `QueryableState`?

Corda defines a suite of built-in named queries which you can use along with an identity post-processor to return `ContractStates` or `StateAndRef`s.

These built-in named queries return ledger state entities such as `VaultState` or `LinearState`. The table below details the names of these queries and their named parameter names.


{{<table>}}

| Query name                                                              | Named Parameters                     |
|-------------------------------------------------------------------------|--------------------------------------|
| `VaultState.findByStateStatus`                                            | `stateStatus`                          |
| `VaultState.findByStateStatusAndContractStateClassName`                   | `stateStatus`, `contractStateClassName`  |
| `VaultState.findByStateStatusAndContractStateClassNameIn`                 | `stateStatus`, `contractStateClassNames` |
| `VaultState.findByTxIdIn`                                                 | `txIds`                                |
| `LinearState.findByUuid`                                                  | `uuid`                                 |
| `LinearState.findByUuidAndStateStatus`                                    | `uuid`, `stateStatus`                    |

{{</table>}}

The query names illustrate the name of the entity followed by the operation (find) followed by the `"WHERE"` clauses. For example:
- `"LinearState.findByUuidAndStateStatus"` queries for `VaultLinearState` entities with `"WHERE"` clauses on:
  - `VaultLinearState.uuid` (`java.util.UUID`) where the field equals the named parameter `uuid`.
  - `VaultState.stateStatus` (`StateStatus`) where the field equals the named parameter `stateStatus`.
- `"VaultState.findByStateStatusAndContractStateClassNameIn"` queries for the `VaultState` entity with `"WHERE"` clauses on:
  - `VaultState.stateStatus` (`StateStatus`) where the field equals the named parameter `stateStatus`.
  - `VaultState.contractStateClassName` (`String`) where the field is in a list provided as a named parameter `contractStateClassNames`.

{{< note >}}
If the built-in named-queries are not suitable for your needs, you will need to change your state to implement `QueryableState` and define your own named-query. If this is not possible, you might be able to achieve your goal using [post-filtering](#post-filtering).
{{< /note >}}

## Post-filtering

Post-filtering is an additional in-memory step which can be applied to named-query results after named-query execution.

It is applied on the remote database worker process, before any post-processing or fetching of state data is performed. So it can cut down on the number of state references to be fetched. It can assist in querying when the named-query itself cannot be added or changed.

It is recommended to filter using `"WHERE"` clauses in the named query itself. Post-filtering serves to supplement the Query API and improve performance.

The only filtering implementation is `SetBasedVaultQueryFilter`. Use the `SetBasedVaultQueryFilter.Builder()` to create the filter.

Since filtering happens before additional state data is loaded, it can only apply to the fields present on the entity returned from the query. For example, if your query returns a:
- `VaultState` - `txId`, `contractStateClassNames`, `relevancyStatus`, `stateStatus` filters will apply.
- `LinearState` - only `txId` filter will apply.
- `PersistentState` - only `txId` filter will apply.
- Other custom entity - no filter fields apply.

This example filters the named-query results for all relevant states:

```kotlin
val cursor = persistenceService.query<ContractState>(
    queryName = "VaultState.findByStateStatus",
    namedParameters = mapOf("stateStatus" to StateStatus.UNCONSUMED),
    postFilter = SetBasedVaultQueryFilter.Builder()
        .withRelevancyStatuses(NonEmptySet.of(RelevancyStatus.RELEVANT))
        .build(),
    postProcessorName = IdentityContractStatePostProcessor.POST_PROCESSOR_NAME
)
val contractStates = cursor.poll(100, 10.seconds)
    .values
```

This example filters the named-query results for `CustomStates`:

```kotlin
val cursor = persistenceService.query<CustomState>(
    queryName = "VaultState.findByStateStatus",
    namedParameters = mapOf("stateStatus" to StateStatus.UNCONSUMED),
    postFilter = SetBasedVaultQueryFilter.Builder()
        .withContractStateClassNames(NonEmptySet.of(CustomState::class.java.name))
        .build(),
    postProcessorName = IdentityContractStatePostProcessor.POST_PROCESSOR_NAME
)
val customStates = cursor.poll(100, 10.seconds)
    .values
```

This example filters the named-query results for states in a specific transaction:
```kotlin
val cursor = persistenceService.query<CustomState>(
    queryName = "VaultState.findByStateStatus",
    namedParameters = mapOf("stateStatus" to StateStatus.UNCONSUMED),
    postFilter = SetBasedVaultQueryFilter.Builder()
        .withTxIds(NonEmptySet.of(myTx.id.toString()))
        .build(),
    postProcessorName = IdentityContractStatePostProcessor.POST_PROCESSOR_NAME
)
val customStates = cursor.poll(100, 10.seconds)
    .values
```

## Examples using the query API

The examples in this guide use this [schema definition](#schema-definition).

Query for 100 `UNCONSUMED` `StateAndRefs`, with a timeout of 10 seconds:

```kotlin
val cursor = persistenceService.query<StateAndRef<ContractState>>(
    "VaultState.findByStateStatus",
    mapOf("stateStatus" to StateStatus.UNCONSUMED),
    IdentityStateAndRefPostProcessor.POST_PROCESSOR_NAME,
)
val stateAndRefs = cursor.poll(100, 10.seconds)
    .values
```

Query for one state with the given `uuid`, returning a `ContractState`, with a timeout of 10 seconds:

```kotlin
@StartableByRPC
class QueryForMyLinearStateFlow(private val uuid: String) : Flow<MyLinearState> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): MyLinearState {
        val cursor = persistenceService.query<MyLinearState>(
            "LinearState.findByUuid",
            mapOf("uuid" to UUID.fromString(uuid)),
            IdentityContractStatePostProcessor.POST_PROCESSOR_NAME,
        )
        return cursor.poll(1, 10.seconds)
            .values
    }
}
```

Find shopping items costing more than a specific amount:

```kotlin
@StartableByRPC
class FindItemsCostingMoreThan(private val cost: Int) : Flow<List<String>> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): List<String> {
        return persistenceService.query<ShoppingSchemaV1.ShoppingItem>(
            "ShoppingItem.findByCostGreaterThan",
            mapOf("cost" to cost)
        )
            .poll(100, 10.seconds)
            .values
            .map { it.name }
    }
}
```

Sum totals of items in shopping cart with specified ID:

```kotlin
@StartableByRPC
class SumItemsCostInCart(private val cartId: String) : Flow<Long> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): Long {
        return persistenceService.query<Long>(
            "ShoppingCart.sumTotalItemsCostByCartId",
            mapOf("cartId" to cartId)
        )
            .poll(1, 10.seconds)
            .values
            .first()
    }
}
```

## Schema definition

Shopping schema:

```kotlin
object ShoppingSchema

object ShoppingSchemaV1 : MappedSchema(
    schemaFamily = ShoppingSchema.javaClass,
    version = 1,
    mappedTypes = listOf(ShoppingItem::class.java, ShoppingCart::class.java)
) {

    @Entity
    @Table(name = "shopping_item")
    @NamedQueries(
        NamedQuery(
            name = "ShoppingItem.findByCostGreaterThan",
            query = "from net.corda.sample.datapersistence.schema.ShoppingSchemaV1\$ShoppingItem item where item.cost > :cost"
        )
    )
    @CordaSerializable
    data class ShoppingItem(
        @Id
        val id: String,

        @Column(name = "item_name", nullable = false)
        val name: String,

        @Column(name = "cost", nullable = false)
        var cost: Int
    )

    @Entity
    @Table(name = "shopping_cart")
    @NamedQueries(
        NamedQuery(
            name = "ShoppingCart.sumTotalItemsCostByCartId",
            query = "SELECT sum(items.cost)" +
                    " FROM net.corda.sample.datapersistence.schema.ShoppingSchemaV1\$ShoppingCart cart" +
                    " JOIN cart.shoppingItems items" +
                    " WHERE cart.id = :cartId"
        )
    )
    @CordaSerializable
    data class ShoppingCart(
        @Id
        val id: String,

        @Column(name = "cart_name", nullable = true)
        val name: String,

        @OneToMany(fetch = FetchType.EAGER, targetEntity = ShoppingItem::class, cascade = [CascadeType.ALL])
        @JoinTable(
            name="shopping_items_in_cart",
            joinColumns = [JoinColumn(name = "cart_id", referencedColumnName = "id")],
            inverseJoinColumns = [JoinColumn(name = "item_id", referencedColumnName = "id")]
        )
        var shoppingItems: MutableList<ShoppingItem>,

        @Column(name = "created_time", nullable = false)
        val createdTime: Instant
    ) {
        @ConstructorForDeserialization
        constructor(id: String, name: String, shoppingItems: Collection<ShoppingItem>, createdTime: Instant)
                : this(id, name, shoppingItems.toMutableList(), createdTime)
    }
}
```

`PetState` definition:

```kotlin
@BelongsToContract(PetContract::class)
data class PetState(
    val name: String = "Rex",
    val initiatorId: String,
    override val owner: AbstractParty,
    override val linearId: UniqueIdentifier = UniqueIdentifier(name),
): OwnableState, LinearState, QueryableState, JsonRepresentable {
    override val participants: List<AbstractParty> get() = listOf(owner)
    override fun toString() = "$name<${linearId.id}>: is owned by $owner"

    override fun supportedSchemas(): Iterable<MappedSchema> = listOf(PetSchemaV1)
    override fun generateMappedObject(schema: MappedSchema): PersistentState {
        return when (schema) {
            is PetSchemaV1 -> PetSchemaV1.PersistentPet(
                    this.name,
                    this.owner.toString(),
                    this.linearId.id
            )
            else -> throw IllegalArgumentException("Unrecognised schema $schema")
        }
    }

    override fun withNewOwner(newOwner: AbstractParty): CommandAndState {
        return CommandAndState(PetContract.Commands.Transfer(), this.copy(owner = newOwner))
    }
    override fun toJsonString(): String {
        return """{ "name": "$name", "initiatorId": "$initiatorId", "owner": "${owner.nameOrNull()}", "linearId": "$linearId" }"""
    }
}

/**
 * Simple Pojo that can be easily serialized.
 */
@CordaSerializable
data class PetStatePojo(
    val name: String,
    val initiatorId: String,
    val owner: String,
    val linearId: String
)
```

`PetState` mapped schema:

```kotlin
object PetSchema

object PetSchemaV1 : MappedSchema(
    schemaFamily = PetSchema.javaClass,
    version = 1,
    mappedTypes = listOf(PersistentPet::class.java)) {

    override val migrationResource: String
        get() = "pet.changelog-master";

    @Entity
    @Table(name = "pet_states")
    @NamedQuery(name = "PersistentPet.findUnconsumedByName",
        query = "SELECT pet" +
                " FROM net.corda.linearstatesample.schema.PetSchemaV1\$PersistentPet pet," +
                " net.corda.v5.ledger.schemas.vault.VaultSchemaV1\$VaultState state" +
                " WHERE pet.name = :name" +
                " AND state.stateStatus = 0" +
                " AND state.stateRef.txId = pet.stateRef.txId" +
                " AND state.stateRef.index = pet.stateRef.index"
    )
    class PersistentPet(
        @Column(name = "pet_name")
        var name: String,

        @Column(name = "pet_owner")
        var ownerName: String,

        @Column(name = "pet_linear_id")
        @Convert(converter = UUIDConverter::class)
        var linearId: UUID
    ) : PersistentState() {
        // Default constructor required by hibernate.
        constructor(): this("", "Rex", UniqueIdentifier("Rex").id)
    }
}
```
