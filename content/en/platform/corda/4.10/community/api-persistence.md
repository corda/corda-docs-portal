---
aliases:
- /head/api-persistence.html
- /HEAD/api-persistence.html
- /api-persistence.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-api-persistence
    parent: corda-community-4-10-corda-api
    weight: 240
tags:
- api
- persistence
title: 'API: Persistence'
---

# API: Persistence


Corda offers developers the option to expose all or some parts of a contract state to an *Object Relational Mapping*
(ORM) tool to be persisted in a *Relational Database Management System* (RDBMS).

The purpose of this, is to assist [Vault]({{< relref "key-concepts-vault.md" >}})
development and allow for the persistence of state data to a custom database table. Persisted states held in the
vault are indexed for the purposes of executing queries. This also allows for relational joins between Corda tables
and the organization’s existing data.

The Object Relational Mapping is specified using [Java Persistence API](https://en.wikipedia.org/wiki/Java_Persistence_API)
(JPA) annotations. This mapping is persisted to the database as a table row (a single, implicitly structured data item) by the node
automatically every time a state is recorded in the node’s local vault as part of a transaction.

{{< note >}}
By default, nodes use an H2 database which is accessed using *Java Database Connectivity* JDBC. Any database
with a JDBC driver is a candidate and several integrations have been contributed to by the community.
Please see the info in [Node database]({{< relref "node-database-access-h2.md" >}}) for details.

{{< /note >}}

## Schemas

Every `ContractState` may implement the `QueryableState` interface if it wishes to be inserted into a custom table in the node’s
database and made accessible using SQL.

```kotlin
/**
 * A contract state that may be mapped to database schemas configured for this node to support querying for,
 * or filtering of, states.
 */
@KeepForDJVM
interface QueryableState : ContractState {
    /**
     * Enumerate the schemas this state can export representations of itself as.
     */
    fun supportedSchemas(): Iterable<MappedSchema>

    /**
     * Export a representation for the given schema.
     */
    fun generateMappedObject(schema: MappedSchema): PersistentState
}

```

[PersistentTypes.kt](https://github.com/corda/corda/blob/release/os/4.10/core/src/main/kotlin/net/corda/core/schemas/PersistentTypes.kt)

The `QueryableState` interface requires the state to enumerate the different relational schemas it supports, for
instance in situations where the schema has evolved. Each relational schema is represented as a `MappedSchema`
object returned by the state’s `supportedSchemas` method.

Nodes have an internal `SchemaService` which decides what data to persist by selecting the `MappedSchema` to use.
Once a `MappedSchema` is selected, the `SchemaService` will delegate to the `QueryableState` to generate a corresponding
representation (mapped object) via the `generateMappedObject` method, the output of which is then passed to the *ORM*.

```kotlin
/**
 * A configuration and customisation point for Object Relational Mapping of contract state objects.
 */
interface SchemaService {
    /**
     * All available schemas in this node
     */
    val schemas: Set<MappedSchema>

    /**
     * Given a state, select schemas to map it to that are supported by [generateMappedObject] and that are configured
     * for this node.
     */
    fun selectSchemas(state: ContractState): Iterable<MappedSchema>

    /**
     * Map a state to a [PersistentState] for the given schema, either via direct support from the state
     * or via custom logic in this service.
     */
    fun generateMappedObject(state: ContractState, schema: MappedSchema): PersistentState
}

```

[SchemaService.kt](https://github.com/corda/corda/blob/release/os/4.10/node/src/main/kotlin/net/corda/node/services/api/SchemaService.kt)

```kotlin
/**
 * A database schema that might be configured for this node.  As well as a name and version for identifying the schema,
 * also list the classes that may be used in the generated object graph in order to configure the ORM tool.
 *
 * @param schemaFamily A class to fully qualify the name of a schema family (i.e. excludes version)
 * @param version The version number of this instance within the family.
 * @param mappedTypes The JPA entity classes that the ORM layer needs to be configure with for this schema.
 */
@KeepForDJVM
open class MappedSchema(schemaFamily: Class<*>,
                        val version: Int,
                        val mappedTypes: Iterable<Class<*>>) {
    val name: String = schemaFamily.name

    /**
     * Optional classpath resource containing the database changes for the [mappedTypes]
     */
    open val migrationResource: String? = null

    override fun toString(): String = "${this.javaClass.simpleName}(name=$name, version=$version)"

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as MappedSchema

        if (version != other.version) return false
        if (mappedTypes != other.mappedTypes) return false
        if (name != other.name) return false

        return true
    }

    override fun hashCode(): Int {
        var result = version
        result = 31 * result + mappedTypes.hashCode()
        result = 31 * result + name.hashCode()
        return result
    }
}

```

[PersistentTypes.kt](https://github.com/corda/corda/blob/release/os/4.10/core/src/main/kotlin/net/corda/core/schemas/PersistentTypes.kt)

With this framework, the relational view of ledger states can evolve in a controlled fashion in lock-step with internal systems or other
integration points and is not dependant on changes to the contract code.

It is expected that multiple contract state implementations might provide mappings within a single schema.
For example an Interest Rate Swap contract and an Equity OTC Option contract might both provide a mapping to
a Derivative contract within the same schema. The schemas should typically not be part of the contract itself and should exist independently
to encourage re-use of a common set within a particular business area or CorDapp.

{{< note >}}
It’s advisable to avoid cross-references between different schemas as this may cause issues when evolving `MappedSchema`
or migrating its data. At startup, nodes log such violations as warnings stating that there’s a cross-reference between `MappedSchema`’s.
The detailed messages incorporate information about what schemas, entities and fields are involved.

{{< /note >}}
`MappedSchema` offer a family name that is disambiguated using Java package style name-spacing derived from the
class name of a *schema family* class that is constant across versions, allowing the `SchemaService` to select a
preferred version of a schema.

The `SchemaService` is also responsible for the `SchemaOptions` that can be configured for a particular
`MappedSchema`. These allow the configuration of database schemas or table name prefixes to avoid clashes with
other `MappedSchema`.

{{< note >}}
It is intended that there should be plugin support for the `SchemaService` to offer version upgrading, implementation
of additional schemas, and enable active schemas as being configurable.  The present implementation does not include these features
and simply results in all versions of all schemas supported by a `QueryableState` being persisted.
This will change in due course. Similarly, the service does not currently support
configuring `SchemaOptions` but will do so in the future.

{{< /note >}}

## Custom schema registration

Custom contract schemas are automatically registered at startup time for CorDapps. The node bootstrap process will scan for states that implement
the Queryable state interface. Tables are then created as specified by the `MappedSchema` identified by each state’s `supportedSchemas` method.

For testing purposes it is necessary to manually register the packages containing custom schemas as follows:


* Tests using `MockNetwork` and `MockNode` must explicitly register packages using the *cordappPackages* parameter of `MockNetwork`
* Tests using `MockServices` must explicitly register packages using the *cordappPackages* parameter of the `MockServices` *makeTestDatabaseAndMockServices()* helper method.

{{< note >}}
Tests using the *DriverDSL* will automatically register your custom schemas if they are in the same project structure as the driver call.

{{< /note >}}

## Object relational mapping

To facilitate the ORM, the persisted representation of a `QueryableState` should be an instance of a `PersistentState` subclass,
constructed either by the state itself or a plugin to the `SchemaService`. This allows the ORM layer to always
associate a `StateRef` with a persisted representation of a `ContractState` and allows joining with the set of
unconsumed states in the vault.

The `PersistentState` subclass should be marked up as a JPA 2.1 *Entity* with a defined table name and having
properties (in Kotlin, getters/setters in Java) annotated to map to the appropriate columns and SQL types. Additional
entities can be included to model these properties where they are more complex, for example collections (Persisting hierarchical data), so
the mapping does not have to be *flat*. The `MappedSchema` constructor accepts a list of all JPA entity classes for that schema in
the `MappedTypes` parameter. It must provide this list in order to initialise the ORM layer.

Several examples of entities and mappings are provided in the codebase, including `Cash.State` and
`CommercialPaper.State`. For example, here’s the first version of the cash schema.

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
package net.corda.finance.schemas

import net.corda.core.identity.AbstractParty
import net.corda.core.schemas.MappedSchema
import net.corda.core.schemas.PersistentState
import net.corda.core.serialization.CordaSerializable
import net.corda.core.utilities.MAX_HASH_HEX_SIZE
import net.corda.core.contracts.MAX_ISSUER_REF_SIZE
import org.hibernate.annotations.Type
import javax.persistence.*

/**
 * An object used to fully qualify the [CashSchema] family name (i.e. independent of version).
 */
object CashSchema

/**
 * First version of a cash contract ORM schema that maps all fields of the [Cash] contract state as it stood
 * at the time of writing.
 */
@Suppress("MagicNumber") // SQL column length
@CordaSerializable
object CashSchemaV1 : MappedSchema(schemaFamily = CashSchema.javaClass, version = 1, mappedTypes = listOf(PersistentCashState::class.java)) {

    override val migrationResource = "cash.changelog-master"

    @Entity
    @Table(name = "contract_cash_states", indexes = [Index(name = "ccy_code_idx", columnList = "ccy_code"), Index(name = "pennies_idx", columnList = "pennies")])
    class PersistentCashState(
            /** X500Name of owner party **/
            @Column(name = "owner_name", nullable = true)
            var owner: AbstractParty?,

            @Column(name = "pennies", nullable = false)
            var pennies: Long,

            @Column(name = "ccy_code", length = 3, nullable = false)
            var currency: String,

            @Column(name = "issuer_key_hash", length = MAX_HASH_HEX_SIZE, nullable = false)
            var issuerPartyHash: String,

            @Column(name = "issuer_ref", length = MAX_ISSUER_REF_SIZE, nullable = false)
            @Type(type = "corda-wrapper-binary")
            var issuerRef: ByteArray
    ) : PersistentState()
}

```
{{% /tab %}}




[CashSchemaV1.kt](https://github.com/corda/corda/blob/release/os/4.10/finance/contracts/src/main/kotlin/net/corda/finance/schemas/CashSchemaV1.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

{{< note >}}
If Cordapp needs to be portable between Corda OS (running against H2) and Corda Enterprise (running against a standalone database),
consider database vendors specific requirements.
Ensure that table and column names are compatible with the naming convention of the database vendors for which the Cordapp will be deployed,
e.g. for Oracle database, prior to version 12.2 the maximum length of table/column name is 30 bytes (the exact number of characters depends on the database encoding).

{{< /note >}}

## Persisting hierarchical data

You may want to persist hierarchical relationships within state data using multiple database tables.
To facilitate this, you must implement all queries making use of hierarchical relations as native SQL.

Example schemas implementing hierarchical relationships have been implemented below.

For one-to-one scenarios, use the following:

```kotlin
// Parent schema implemented as usual
class PersistentParent(
  @Column(name = "linear_id")
  var linearId: UUID
) : PersistentState() {
  constructor() : this( UUID.randomUUID() )
}

// Child has a reference to its parent
class PersistentChild(
  @Column(name = "linear_id")
  var linearId: UUID
  @Column=(name = "parent_linear_id")
  var parentLinearId: UUID
) : PersistentState() {
  constructor() : this( UUID.randomUUID(), UUID.randomUUID() )
}
```

For one-to-many scenarios, use the following:

```
// Parent schema implemented as usual
class PersistentParent(
  @Column(name = "linear_id")
  var linearId: UUID
) : PersistentState() {
  constructor() : this( UUID.randomUUID() )
}

// Child schema implemented as usual
class PersistentChild(
  @Column(name = "linear_id")
  var linearId: UUID
) : PersistentState() {
  constructor() : this( UUID.randomUUID())
}

// ParentChildThrough table schema
class PersistentThroughTable(
  @Column(name = "parent_linear_id")
  var parentLinearId: UUID
  @Column(name="child_linear_id")
  var childLinearId: UUID
) : PersistentState() {
  constructor() : this( UUID.randomUUID(), UUID.randomUUID() )
}
```

## Identity mapping

Schema entity attributes defined by identity types (`AbstractParty`, `Party`, `AnonymousParty`) are automatically
processed to ensure only the `X500Name` of the identity is persisted where an identity is well known, otherwise a null
value is stored in the associated column. To preserve privacy, identity keys are never persisted. Developers should use
the `IdentityService` to resolve keys from well know X500 identity names.

## JDBC session

{{< warning >}}
Using JDBC to interact with a node's database can have serious consequences if not carried out correctly. You must ensure you are able to test any changes in a safe environment and roll back if you encounter any errors. This method should be seen as a last resort if you cannot perform your tasks using any other method.
{{< /warning >}}

Apps may also interact directly with the underlying Node’s database by using a standard
JDBC connection (session) as described by the [Java SQL Connection API](https://docs.oracle.com/javase/8/docs/api/java/sql/Connection.html)

Use the `ServiceHub` `jdbcSession` function to obtain a JDBC connection as illustrated in the following example:

```kotlin
val nativeQuery = "SELECT v.transaction_id, v.output_index FROM vault_states v WHERE v.state_status = 0"

database.transaction {
    val jdbcSession = services.jdbcSession()
    val prepStatement = jdbcSession.prepareStatement(nativeQuery)
    val rs = prepStatement.executeQuery()
}
```

[HibernateConfigurationTest.kt](https://github.com/corda/corda/blob/release/os/4.10/node/src/test/kotlin/net/corda/node/services/persistence/HibernateConfigurationTest.kt)

JDBC sessions can be used in flows and services (see [Writing flows]({{< relref "api-flows.md" >}})).

The following example illustrates the creation of a custom Corda service using a `jdbcSession`:

```kotlin
object CustomVaultQuery {

    @CordaService
    class Service(val services: AppServiceHub) : SingletonSerializeAsToken() {
        private companion object {
            private val log = contextLogger()
        }

        fun rebalanceCurrencyReserves(): List<Amount<Currency>> {
            val nativeQuery = """
                select
                    cashschema.ccy_code,
                    sum(cashschema.pennies)
                from
                    vault_states vaultschema
                join
                    contract_cash_states cashschema
                where
                    vaultschema.output_index=cashschema.output_index
                    and vaultschema.transaction_id=cashschema.transaction_id
                    and vaultschema.state_status=0
                group by
                    cashschema.ccy_code
                order by
                    sum(cashschema.pennies) desc
            """
            log.info("SQL to execute: $nativeQuery")
            val session = services.jdbcSession()
            return session.prepareStatement(nativeQuery).use { prepStatement ->
                prepStatement.executeQuery().use { rs ->
                    val topUpLimits: MutableList<Amount<Currency>> = mutableListOf()
                    while (rs.next()) {
                        val currencyStr = rs.getString(1)
                        val amount = rs.getLong(2)
                        log.info("$currencyStr : $amount")
                        topUpLimits.add(Amount(amount, Currency.getInstance(currencyStr)))
                    }
                    topUpLimits
                }
            }
        }
    }
}

```

which is then referenced within a custom flow:

```kotlin
@Suspendable
@Throws(CashException::class)
override fun call(): List<SignedTransaction> {
    progressTracker.currentStep = AWAITING_REQUEST
    val topupRequest = otherPartySession.receive<TopupRequest>().unwrap {
        it
    }

    val customVaultQueryService = serviceHub.cordaService(CustomVaultQuery.Service::class.java)
    val reserveLimits = customVaultQueryService.rebalanceCurrencyReserves()

    val txns: List<SignedTransaction> = reserveLimits.map { amount ->
        // request asset issue
        logger.info("Requesting currency issue $amount")
        val txn = issueCashTo(amount, topupRequest.issueToParty, topupRequest.issuerPartyRef, topupRequest.notaryParty)
        progressTracker.currentStep = SENDING_TOP_UP_ISSUE_REQUEST
        return@map txn.stx
    }

    otherPartySession.send(txns)
    return txns
}
```

For examples on testing `@CordaService` implementations, see the oracle example [here]({{< relref "key-concepts-oracles.md" >}}).

### Restricted control of connections

Corda restricts the functions available by the `Connection` returned by `jdbcSession`. This is to prevent a flow's underlying database transaction from being tampered with, which would likely lead to errors within the flow.

Calling `jdbcSession` returns a `RestrictedConnection` which prevents calls to the following functions:

``` kotlin
abort(executor: Executor?)
clearWarnings()
close()
commit()
setSavepoint() methods
releaseSavepoint(savepoint: Savepoint?)
rollback() methods
setCatalog(catalog : String?)
setTransactionIsolation(level: Int)
setTypeMap(map: MutableMap<String, Class<*>>?)
setHoldability(holdability: Int)
setSchema(schema: String?)
setNetworkTimeout(executor: Executor?, milliseconds: Int)
setAutoCommit(autoCommit: Boolean)
setReadOnly(readOnly: Boolean)
```

## JPA support

In addition to `jdbcSession`, `ServiceHub` also exposes the Java Persistence API to flows via the `withEntityManager`
method. This method can be used to persist and query entities which inherit from `MappedSchema`. This is particularly
useful if off-ledger data must be maintained in conjunction with on-ledger state data.


{{< note >}}
Your entity must be included as a mappedType as part of a `MappedSchema` for it to be added to Hibernate
as a custom schema. If it’s not included as a mappedType, a corresponding table will not be created. See Samples below.

{{< /note >}}

The code snippet below defines a `PersistentFoo` type inside `FooSchemaV1`. Note that `PersistentFoo` is added to
a list of mapped types which is passed to `MappedSchema`. This is exactly how state schemas are defined, except that
the entity in this case should not subclass `PersistentState` (as it is not a state object). See examples:

{{< tabs name="tabs-3" >}}
{{% tab name="java" %}}
```java
public class FooSchema {}

public class FooSchemaV1 extends MappedSchema {
    FooSchemaV1() {
        super(FooSchema.class, 1, ImmutableList.of(PersistentFoo.class));
    }

    @Entity
    @Table(name = "foos")
    class PersistentFoo implements Serializable {
        @Id
        @Column(name = "foo_id")
        String fooId;

        @Column(name = "foo_data")
        String fooData;
    }
}
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
object FooSchema

object FooSchemaV1 : MappedSchema(
    schemaFamily = FooSchema.javaClass,
    version = 1,
    mappedTypes = listOf(PersistentFoo::class.java)
) {
    @Entity
    @Table(name = "foos")
    class PersistentFoo(
        @Id
        @Column(name = "foo_id")
        var fooId: String,
        @Column(name = "foo_data")
        var fooData: String
    ) : Serializable
}
```
{{% /tab %}}

{{< /tabs >}}

Instances of `PersistentFoo` can be manually persisted inside a flow as follows:

{{< tabs name="tabs-4" >}}
{{% tab name="java" %}}
```java
PersistentFoo foo = new PersistentFoo(new UniqueIdentifier().getId().toString(), "Bar");
serviceHub.withEntityManager(entityManager -> {
    entityManager.persist(foo);
    return null;
});
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
val foo = FooSchemaV1.PersistentFoo(UniqueIdentifier().id.toString(), "Bar")
serviceHub.withEntityManager {
    persist(foo)
}
```
{{% /tab %}}

{{< /tabs >}}

And retrieved via a query, as follows:

{{< tabs name="tabs-5" >}}
{{% tab name="java" %}}
```java
getServiceHub().withEntityManager((EntityManager entityManager) -> {
    CriteriaQuery<PersistentFoo> query = entityManager.getCriteriaBuilder().createQuery(PersistentFoo.class);
    Root<PersistentFoo> type = query.from(PersistentFoo.class);
    query.select(type);
    return entityManager.createQuery(query).getResultList();
});
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
serviceHub.withEntityManager {
    val query = criteriaBuilder.createQuery(FooSchemaV1.PersistentFoo::class.java)
    val type = query.from(FooSchemaV1.PersistentFoo::class.java)
    query.select(type)
    createQuery(query).resultList
}
```
{{% /tab %}}

{{< /tabs >}}

Please note that suspendable flow operations such as:


* `FlowSession.send`
* `FlowSession.receive`
* `FlowLogic.receiveAll`
* `FlowLogic.sendAll`
* `FlowLogic.sleep`
* `FlowLogic.subFlow`

Cannot be used within the lambda function passed to `withEntityManager`.

### Restricted control of entity managers

Corda restricts the functions available by the `EntityManager` returned by `withEntityManager`. This is to prevent a flow's underlying database transaction from being tampered with, which would likely lead to errors within the flow.

The `withEntityManager` function provides an object that adheres to the `EntityManager` interface but with two differences:

- `getTransaction` returns a `RestrictedEntityTransaction`.
- All other restricted functions will `UnsupportedOperationException` exceptions.

The full list of restricted functions are:

For `RestrictedEntityManager`:

``` kotlin
close()
unwrap()
getDelegate()
getMetamodel()
joinTransaction()
lock() methods
setProperty(propertyName: String?, value: Any?)
```

For `RestrictedEntityTransaction`:

```kotlin
rollback()
commit()
begin()
```

### Intermediate database sessions within flows

When you call `withEntityManager`, an intermediate database session is created that provides rollback capability without affecting the current transaction.

A `withEntityManager` block has 3 outcomes:

- __Completes successfully__: The intermediate session is automatically flushed to the underlying transaction.
- __Throws a database error__: The intermediate session is automatically rolled back.
- __Throws a non-database error__: The intermediate session is not flushed to the underlying transaction.

{{< note >}}
For the behaviour described above to occur, a flow does not need to manually flush or rollback an intermediate session.

{{< /note >}}

Changes are committed to the database when the transaction is committed.

{{< note >}}
A flow commits its current database transaction whenever it suspends.

{{< /note >}}

#### Handling database errors

This behaviour allows a flow to handle database exceptions that occur within a `withEntityManager` block without affecting the flow's underlying database transaction.

{{< warning >}}
Your flows should not handle database exceptions that occur outside a `withEntityManager` block. Doing so will lead to further errors as the flow's transaction needs to be rolled back.

{{< /warning >}}

You can handle database errors that occur within a `withEntityManager` by catching relevant exceptions. Below are two ways to handle these exceptions:

- Around the block:

  {{< tabs name="tabs-6" >}}
  {{% tab name="java" %}}
  ```java
  try {
      getServiceHub().withEntityManager(entityManager -> {
          entityManager.persist(entity);
      });
  } catch (PersistenceException e) {
      // Exception thrown due to constraint violation
      getLogger().info("Ok, let's not save this entity 2");
  }
  ```
  {{% /tab %}}

  {{% tab name="kotlin" %}}
  ```kotlin
  try {
      serviceHub.withEntityManager {
          persist(entity)
      }
  } catch (e: PersistenceException) {
      // Exception thrown due to constraint violation
      logger.info("Caught the exception!")
  }
  ```
  {{% /tab %}}
  {{< /tabs >}}

  There is no need for a `flush` when catching exceptions around the `withEntityManager` block. It will automatically trigger a `flush` when leaving the block.

  {{< note >}}
  R3 recommends that exceptions are handled around a `withEntityManager` block as it is less likely to lead to unexpected behaviour when interacting with JPA.

  {{< /note >}}

- Inside the block:

  {{< tabs name="tabs-7" >}}
  {{% tab name="java" %}}
  ```java
  getServiceHub().withEntityManager(entityManager -> {
      entityManager.persist(entity);
      try {
          // Manually trigger a flush on the intermediate session
          entityManager.flush();
      } catch (PersistenceException e) {
          // Exception thrown due to constraint violation
          getLogger().info("Ok, let's not save this entity");
      }
  });
  ```
  {{% /tab %}}

  {{% tab name="kotlin" %}}
  ```kotlin
  serviceHub.withEntityManager {
      persist(entity)
      try {
          // Manually trigger a flush on the intermediate session
          flush()
      } catch (e: PersistenceException) {
          // Exception thrown due to constraint violation
          logger.info("Ok, let's not save this entity")
      }
  }
  ```
  {{% /tab %}}
  {{< /tabs >}}

  A `flush` must be manually triggered if the exception is to be caught inside the entity manager. If the `flush` is not included, the code above would throw the `PersistenceException` instead of catching it.

  {{< warning >}}
  After a database error occurs inside a `withEntityManager` block, any executed updates will not be flushed to the underlying database transaction. All changes will be lost as the transaction will be rolled back to the state it had at the beginning of the block.

  {{< /warning >}}

#### Manually flushing intermediate database sessions

Manually flushing `withEntityManager` sessions was touched on in the example above. You will need to manually `flush` database changes to the underlying database transaction for two reasons:

- __Handling database errors__: Handle any possible database errors that occur from the `flush` within the `withEntityManager` block.
- __Survive non-database errors__: Keep your database changes even if a non-database error is thrown out of the `withEntityManager` block.

An example of flushing a session to survive a non-database error:

{{< tabs name="tabs-8" >}}
{{% tab name="java" %}}
```java
try {
    getServiceHub().withEntityManager(entityManager -> {
        entityManager.persist(entity);
        // Manually trigger a flush on the intermediate session
        entityManager.flush();
        throw new RuntimeException("Non-database error");
    });
} catch (Exception e) {
    getLogger().info("I still want to save that entity");
}
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
try {
    serviceHub.withEntityManager {
        persist(entity)
        // Manually trigger a flush on the intermediate session
        flush()
        throw RuntimeException("Non-database error")
    }
} catch (e: Exception) {
    logger.info("I still want to save that entity")
}
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
To avoid having to `flush` the sessions manually in order to survive non-database exceptions, R3 recommends that you keep any code that is likely to cause such errors out of `withEntityManager` blocks.

{{< /note >}}
