---
date: '2021-09-23'
title: PersistenceService API
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    identifier: corda-5-dev-preview-1-cordapps-persistence
    weight: 1500
section_menu: corda-5-dev-preview
---

In the Corda 5 Developer Preview, the `PersistenceService` API provides operations to persist, find, merge, remove, and
query data.

This guide explains how to use the new `PersistenceService` API for persistence operations from flows and services, and
provides examples.

`PersistenceService` reflects a subset of operations on the `EntityManager` interface. It also provides a `query`
mechanism for executing pre-defined named queries with optional in-memory post filtering and post-processing to
transform results.

For more information on querying, read the [Named Query API](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.md) guide.

## Inject the `PersistenceService` API

`PersistenceService` is injectable into flows and services using the `@CordaInject` mechanism.

```kotlin
@CordaInject
lateinit var persistenceService: PersistenceService
```

## Using the `PersistenceService` API

The examples in this guide use this [schema definition](#shoppingschema).

## Persist new entities

There are two functions on the API for persisting entities to the database.

This function persists a single entity to the database:

```kotlin
@Suspendable
fun persist(entity: Any)
```
`CordaPersistenceException` is thrown and the transaction rolled back when, for example, the given instance is not an entity (not annotated with `@Entity`).

This function persists multiple entities in a single transaction to the database:

```kotlin
@Suspendable
fun persist(entities: List<Any>)
```

`CordaPersistenceException` is thrown and the transaction rolled back when, for example, one of the given instances is not an entity (not annotated with `@Entity`).

### Examples

Persists a single cart:
```kotlin
@StartableByRPC
class PersistShoppingCartFlow(private val name: String) : Flow<String> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): String {
        val id = UUID.randomUUID().toString()
        persistenceService.persist(ShoppingSchemaV1.ShoppingCart(id, name, mutableListOf(), Instant.now()))
        return id
    }
}
```

Persists multiple shopping items in one transaction:
```kotlin
@StartableByRPC
class PersistMultipleShoppingItemsFlow(private val names: List<String>, private val costs: List<Int>) : Flow<List<String>> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): List<String> {
        val items = names.zip(costs)
            .map { (name, cost) ->
                ShoppingSchemaV1.ShoppingItem(UUID.randomUUID().toString(), name, cost)
            }
        persistenceService.persist(items)
        return items.map { it.id }
    }
}
```

## Find entities

There are two functions on the API for finding entities in the database.

This function finds a single entity matching the given type and primary key:

```kotlin
@Suspendable
fun <T : Any> find(entityClass: Class<T>, primaryKey: Any): T?
```

`CordaPersistenceException` is thrown and the transaction rolled back when, for example:
* The entity class is not an entity (not annotated with `@Entity`).
* The primary key is not a valid type for that entity's primary key.
* The primary key is `null`.

`null` is returned if the entity cannot be found.

This function finds multiple entities of a given a type matching the given primary keys within a single transaction.

```kotlin
@Suspendable
fun <T : Any> find(entityClass: Class<T>, primaryKeys: List<Any>): List<T>
```

`CordaPersistenceException` is thrown and the transaction rolled back when, for example:
* The entity class is not an entity (not annotated with `@Entity`).
* A primary key is not a valid type for that entity's primary key.
* The primary key is `null`.

Primary keys that cannot be found are skipped. Therefore, if no entities match, the result is an empty list.

If you are a Kotlin developer, there are two extension functions that allow you to drop the `entityClass` parameter:

```kotlin
inline fun <reified T : Any> PersistenceService.find(primaryKey: Any): T?
inline fun <reified T : Any> PersistenceService.find(primaryKeys: List<Any>): List<T>
```

### Examples

Find a single cart or throw if not found:
```kotlin
@StartableByRPC
class FindShoppingCartFlow(private val id: Any) : Flow<ShoppingSchemaV1.ShoppingCart> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): ShoppingSchemaV1.ShoppingCart {
        return persistenceService.find(ShoppingSchemaV1.ShoppingCart::class.java, id) ?: throw RuntimeException("Cart was not found.")
    }
}
```

Find all shopping items with `id` matching one in `itemIds`:
```kotlin
@StartableByRPC
class FindShoppingItemsFlow(private val itemIds: List<Any>) : Flow<List<ShoppingSchemaV1.ShoppingItem>> {
    private companion object {
        val logger = contextLogger()
    }

    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): List<ShoppingSchemaV1.ShoppingItem> {
        val items = persistenceService.find(ShoppingSchemaV1.ShoppingItem::class.java, itemIds)
        if (items.size != itemIds.size) {
            logger.warn("Some items were not found")
        }
        return items
    }
}
```

## Merge entities

There are two functions on the API for merging entities to the database.

This function:
* Merges the state of the given entity into the persistence context in a single transaction.
* If the entity exists in the persistence context, it merges the given entity with the stored one.
* If the entity does not exist in the persistence context, it adds the given entity to the persistence context and stores it in the database.
* Returns the merged instance.

```kotlin
@Suspendable
fun <T : Any> merge(entity: T): T?
```

`CordaPersistenceException` is thrown and the transaction rolled back when, for example:
* The given instance is not an entity (not annotated with `@Entity`) or is a removed entity.
* An exception occurs during the transaction.

This function:
* Merges the state of multiple entities into the persistence context in a single transaction.
* for each entity, if it exists in the persistence context, it merges it with the stored one.
* for each entity, if it does not exist in the persistence context, it adds the given entity to the persistence context and stores it in the database.
* Returns a list of the entity instances that the given entities were merged to.

```kotlin
@Suspendable
fun <T : Any> merge(entities: List<T>): List<T>
```

`CordaPersistenceException` is thrown and the transaction rolled back when, for example:
* The given instance is not an entity (not annotated with `@Entity`) or is a removed entity.
* An exception occurs during the transaction.

### Examples

Add an item to a cart:
```kotlin
@StartableByRPC
class AddSingleShoppingItemToCartFlow(private val cartId: String, private val itemId: String) : Flow<ShoppingSchemaV1.ShoppingCart?> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): ShoppingSchemaV1.ShoppingCart? {
        val cart = persistenceService.find<ShoppingSchemaV1.ShoppingCart>(cartId) ?: throw RuntimeException("Cart $cartId was not found")
        val item = persistenceService.find<ShoppingSchemaV1.ShoppingItem>(itemId) ?: throw RuntimeException("Item $itemId was not found")
        cart.shoppingItems.add(item)
        return persistenceService.merge(cart)
    }
}
```

Add shopping items with the given IDs to a shopping cart:
```kotlin
@StartableByRPC
class AddItemToShoppingCartFlow(private val cartId: String, private val itemIds: List<String>) : Flow<ShoppingSchemaV1.ShoppingCart?> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): ShoppingSchemaV1.ShoppingCart? {
        val cart = persistenceService.find<ShoppingSchemaV1.ShoppingCart>(cartId) ?: throw RuntimeException("Cart $cartId was not found")
        val items = persistenceService.find<ShoppingSchemaV1.ShoppingItem>(itemIds)
        cart.shoppingItems.addAll(items)
        return persistenceService.merge(cart)
    }
}
```

Update the cost of multiple items:
```kotlin
@StartableByRPC
class ChangeShoppingItemCostsFlow(private val itemIds: List<String>, private val newCost: List<Int>) :
    Flow<List<ShoppingSchemaV1.ShoppingItem>> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call(): List<ShoppingSchemaV1.ShoppingItem> {
        val item = persistenceService.find<ShoppingSchemaV1.ShoppingItem>(itemIds)
        if (item.isEmpty()) {
            return emptyList()
        }
        val updatedItems = item.zip(newCost).map {
            it.first.copy(cost = it.second)
        }
        return persistenceService.merge(updatedItems)
    }
}
```

## Remove entities

There are two functions on the API for removing entities from the database.

This function removes a single entity from the persistence context and writes to the database:

```kotlin
@Suspendable
fun remove(entity: Any)
```

`CordaPersistenceException` is thrown and the transaction rolled back when, for example:
* The given instance is not an entity (not annotated with `@Entity`).
* An exception occurs during the transaction.

This function removes multiple entities from the persistence context and writes this change to the database:

```kotlin
@Suspendable
fun remove(entities: List<Any>)
```

`CordaPersistenceException` is thrown and the transaction rolled back when, for example:
* The given instance is not an entity (not annotated with `@Entity`).
* An exception occurs during the transaction.

### Examples

Given a list of `items`, remove them in a single transaction:

```kotlin
@StartableByRPC
class RemoveShoppingItemsFlow(private val items: List<ShoppingSchemaV1.ShoppingItem>) : Flow<Unit> {
    @CordaInject
    lateinit var persistenceService: PersistenceService

    @Suspendable
    override fun call() {
        persistenceService.remove(items)
    }
}
```

## Execute named queries

The `PersistenceService` has APIs for executing pre-defined named queries from flows and services. See the [Query API](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.md) guide for further information.

You can also call the Query API over HTTP-RPC. See the [HTTP-RPC Named Query API](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/http-named-query-api.md)
guide for further information.

## Notes

* Entities must be marked with `@CordaSerializable`.
* Entities cannot be final.
* Entities must be defined with an `EAGER` fetch type in the entity definition, such as, `OneToMany(fetch = FetchType.EAGER)`.
* Entities must avoid cyclic, bi-directional dependencies.
* Entities must have constructors that take all properties, and one that takes no args (requirement for hibernate/JPA).
* For `CordaSerialization` to reconstitute the object with a mutable collection during deserialization, entities with mutable collections need to:
  * Provide another constructor annotated with `@ConstructorForDeserialization` taking `Collection`.
  * Call the original constructor using the `toMutableList()`/`toMutableSet()` functions provided by Kotlin stdlib.
  For example:

```kotlin
@ConstructorForDeserialization
constructor(id: String, name: String, shoppingItems: Collection<ShoppingItem>, createdTime: Instant)
        : this(id, name, shoppingItems.toMutableList(), createdTime)
```

## `ShoppingSchema`

The examples in this guide use the following schema:

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
