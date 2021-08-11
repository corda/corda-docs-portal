---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-cordapps-flows
tags:
- api
- vault
- query
title: Writing vault queries
weight: 3
---



# Writing vault queries



## Overview

Corda has been designed from the ground up to encourage the use of industry standard, proven query frameworks and libraries for accessing RDBMS backed transactional stores (including the Vault).

Corda provides a number of flexible query mechanisms for accessing the Vault:


* Vault Query API
* Using a JDBC session (as described in [State Persistence](state-persistence.md))
* Custom [JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html)/[JPQL](http://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#hql) queries
* Custom 3rd party Data Access frameworks such as [Spring Data](http://projects.spring.io/spring-data)

The majority of query requirements can be satisfied by using the Vault Query API, which is exposed via the
`VaultService` for use directly by flows:

```kotlin
/**
 * Generic vault query function which takes a [QueryCriteria] object to define filters,
 * optional [PageSpecification] and optional [Sort] modification criteria (default unsorted),
 * and returns a [Vault.Page] object containing the following:
 *  1. states as a List of <StateAndRef> (page number and size defined by [PageSpecification])
 *  2. states metadata as a List of [Vault.StateMetadata] held in the Vault States table.
 *  3. total number of results available if [PageSpecification] supplied (otherwise returns -1).
 *  4. status types used in this query: [StateStatus.UNCONSUMED], [StateStatus.CONSUMED], [StateStatus.ALL].
 *  5. other results (aggregate functions with/without using value groups).
 *
 * @throws VaultQueryException if the query cannot be executed for any reason
 *        (missing criteria or parsing error, paging errors, unsupported query, underlying database error).
 *
 * Notes
 *   If no [PageSpecification] is provided, a maximum of [DEFAULT_PAGE_SIZE] results will be returned.
 *   API users must specify a [PageSpecification] if they are expecting more than [DEFAULT_PAGE_SIZE] results,
 *   otherwise a [VaultQueryException] will be thrown alerting to this condition.
 *   It is the responsibility of the API user to request further pages and/or specify a more suitable [PageSpecification].
 */
@Throws(VaultQueryException::class)
fun <T : ContractState> _queryBy(criteria: QueryCriteria,
                                 paging: PageSpecification,
                                 sorting: Sort,
                                 contractStateType: Class<out T>): Vault.Page<T>

/**
 * Generic vault query function which takes a [QueryCriteria] object to define filters,
 * optional [PageSpecification] and optional [Sort] modification criteria (default unsorted),
 * and returns a [DataFeed] object containing:
 * 1) a snapshot as a [Vault.Page] (described previously in [queryBy]).
 * 2) an [Observable] of [Vault.Update].
 *
 * @throws VaultQueryException if the query cannot be executed for any reason.
 *
 * Notes:
 *    - The snapshot part of the query adheres to the same behaviour as the [queryBy] function.
 *    - The update part of the query currently only supports query criteria filtering by contract
 *      type(s) and state status(es). CID-731 <https://r3-cev.atlassian.net/browse/CID-731> proposes
 *      adding the complete set of [QueryCriteria] filtering.
 */
@Throws(VaultQueryException::class)
fun <T : ContractState> _trackBy(criteria: QueryCriteria,
                                 paging: PageSpecification,
                                 sorting: Sort,
                                 contractStateType: Class<out T>): DataFeed<Vault.Page<T>, Vault.Update<T>>

```

[VaultService.kt](https://github.com/corda/corda/blob/release/os/4.6/core/src/main/kotlin/net/corda/core/node/services/VaultService.kt)

And via `CordaRPCOps` for use by RPC client applications:

```kotlin
@RPCReturnsObservables
fun <T : ContractState> vaultQueryBy(criteria: QueryCriteria,
                                     paging: PageSpecification,
                                     sorting: Sort,
                                     contractStateType: Class<out T>): Vault.Page<T>

```

[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/4.6/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)

```kotlin
@RPCReturnsObservables
fun <T : ContractState> vaultTrackBy(criteria: QueryCriteria,
                                     paging: PageSpecification,
                                     sorting: Sort,
                                     contractStateType: Class<out T>): DataFeed<Vault.Page<T>, Vault.Update<T>>

```

[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/4.6/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)

Helper methods are also provided with default values for arguments:

```kotlin
fun <T : ContractState> vaultQuery(contractStateType: Class<out T>): Vault.Page<T>

fun <T : ContractState> vaultQueryByCriteria(criteria: QueryCriteria, contractStateType: Class<out T>): Vault.Page<T>

fun <T : ContractState> vaultQueryByWithPagingSpec(contractStateType: Class<out T>, criteria: QueryCriteria, paging: PageSpecification): Vault.Page<T>

fun <T : ContractState> vaultQueryByWithSorting(contractStateType: Class<out T>, criteria: QueryCriteria, sorting: Sort): Vault.Page<T>

```

[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/4.6/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)

```kotlin
fun <T : ContractState> vaultTrack(contractStateType: Class<out T>): DataFeed<Vault.Page<T>, Vault.Update<T>>

fun <T : ContractState> vaultTrackByCriteria(contractStateType: Class<out T>, criteria: QueryCriteria): DataFeed<Vault.Page<T>, Vault.Update<T>>

fun <T : ContractState> vaultTrackByWithPagingSpec(contractStateType: Class<out T>, criteria: QueryCriteria, paging: PageSpecification): DataFeed<Vault.Page<T>, Vault.Update<T>>

fun <T : ContractState> vaultTrackByWithSorting(contractStateType: Class<out T>, criteria: QueryCriteria, sorting: Sort): DataFeed<Vault.Page<T>, Vault.Update<T>>

```

[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/4.6/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)

The API provides both static (snapshot) and dynamic (snapshot with streaming updates) methods for a defined set of
filter criteria:


* Use `queryBy` to obtain a current snapshot of data (for a given `QueryCriteria`)
* Use `trackBy` to obtain both a current snapshot and a future stream of updates (for a given `QueryCriteria`)

{{< note >}}
Streaming updates are only filtered based on contract type and state status (`UNCONSUMED`, `CONSUMED`, `ALL`).
They will not respect any other criteria that the initial query has been filtered by.

{{< /note >}}
Simple pagination (page number and size) and sorting (directional ordering using standard or custom property
attributes) is also specifiable. Defaults are defined for paging (`pageNumber` = 1, `pageSize` = 200) and sorting (`direction` = ASC).

## `QueryCriteria` interface

The `QueryCriteria` interface provides a flexible mechanism for specifying different filtering criteria, including
and/or composition and a rich set of operators to include:


* Binary logical (`AND`, `OR`)
* Comparison (`LESS_THAN`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`)
* Equality (`EQUAL`, `NOT_EQUAL`)
* Likeness (`LIKE`, `NOT_LIKE`)
* Nullability (`IS_NULL`, `NOT_NULL`)
* Collection based (`IN`, `NOT_IN`)
* Standard SQL-92 aggregate functions (`SUM`, `AVG`, `MIN`, `MAX`, `COUNT`)

There are four implementations of this interface which can be chained together to define advanced filters:


* `VaultQueryCriteria` provides filterable criteria on attributes within the **VAULT_STATES** table. Filterable attributes include one or more of the following: status (`UNCONSUMED`,
`CONSUMED`), state reference, contract state type, notary name, soft locked states, timestamps (`RECORDED`, `CONSUMED`), state constraints (see [Constraint Types](api-contract-constraints.md#implicit-constraint-types)), relevancy (`ALL`, `RELEVANT`, `NON_RELEVANT`), and participants (exact or any match).
{{< note >}}
Sensible defaults are defined for frequently used attributes (`status` = `UNCONSUMED`, always include soft
locked states).{{< /note >}}


* `FungibleAssetQueryCriteria` provides filterable criteria on attributes defined in the Corda Core
`FungibleAsset` contract state interface, used to represent assets that are fungible, countable and issued by a
specific party (for example, `Cash.State` and `CommodityContract.State` in the Corda finance module). Filterable attributes include one or more of the following: participants (exact or any match), owner, quantity, issuer name, and issuer reference.
{{< note >}}
All contract states that extend the `FungibleAsset` now automatically persist that interface's common
state attributes to the **VAULT_FUNGIBLE_STATES** table.{{< /note >}}


* `LinearStateQueryCriteria` provides filterable criteria on attributes defined in the Corda Core `LinearState`
and `DealState` contract state interfaces, used to represent entities that continuously supersede themselves, all
of which share the same `linearId` (for example, trade entity states such as the `IRSState` defined in the SIMM
valuation demo). Filterable attributes include one or more of the following: participants, linear ID, UUID, and external ID.
{{< note >}}
All contract states that extend `LinearState` or `DealState` now automatically persist those
interfaces' common state attributes to the **VAULT_LINEAR_STATES** table.{{< /note >}}


* `VaultCustomQueryCriteria` provides the means to specify one or many arbitrary expressions on attributes defined
by a custom contract state that implements its own schema as described in the [State Persistence](state-persistence.md)
documentation and associated examples. Custom criteria expressions are expressed using one of the following type-safe forms of
`CriteriaExpression`: `BinaryLogical`, `Not`, `ColumnPredicateExpression`, and `AggregateFunctionExpression`. The
`ColumnPredicateExpression` allows for the specification of arbitrary criteria using the previously enumerated operator
types. The `AggregateFunctionExpression` allows for the specification of an aggregate function type (`SUM`, `AVG`, `MAX`, `MIN`, `COUNT`) with optional grouping and sorting. Furthermore, a rich DSL is provided to enable simple
construction of custom criteria using any combination of `ColumnPredicate`. See the `Builder` object in
`QueryCriteriaUtils` for a complete specification of the DSL.
{{< note >}}
Custom contract schemas are automatically registered upon node startup for CorDapps. Please refer to
[State Persistence](state-persistence.md) for mechanisms of registering custom schemas for different testing
purposes.{{< /note >}}



All `QueryCriteria` implementations are composable using `AND` and `OR` operators.

All `QueryCriteria` implementations provide an explicitly specifiable set of common attributes:


* A state status attribute (`Vault.StateStatus`), which defaults to filtering on `UNCONSUMED` states.
When chaining several criteria using `AND` or `OR`, the last value of this attribute will override any previous value.
* Contract state types (`<Set<Class<out ContractState>>`), which will contain at minimum one type (by default,  this will be `ContractState` which resolves to all state types). When chaining several criteria using `AND` and `OR` operators, all specified contract state types are combined into a single set.

### Custom queries in Kotlin

An example of a custom query in Kotlin is provided below:

```kotlin
val generalCriteria = VaultQueryCriteria(Vault.StateStatus.ALL)

val results = builder {
    val currencyIndex = PersistentCashState::currency.equal(USD.currencyCode)
    val quantityIndex = PersistentCashState::pennies.greaterThanOrEqual(10L)

    val customCriteria1 = VaultCustomQueryCriteria(currencyIndex)
    val customCriteria2 = VaultCustomQueryCriteria(quantityIndex)

    val criteria = generalCriteria.and(customCriteria1.and(customCriteria2))
    vaultService.queryBy<Cash.State>(criteria)
}

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

{{< note >}}
Custom contract states that implement the `Queryable` interface may now extend the common schema types `FungiblePersistentState` or, `LinearPersistentState`.  Previously, all custom contracts extended the root `PersistentState` class and defined repeated mappings of `FungibleAsset` and `LinearState` attributes. See `SampleCashSchemaV2` and `DummyLinearStateSchemaV2` as examples.
{{< /note >}}

{{< note >}}
When specifying the `ContractType` as a parameterised type to the `QueryCriteria` in Kotlin, queries now include all concrete implementations of that type if this is an interface. Previously, it was only possible to query on concrete types (or the universe of all `ContractState`).
{{< /note >}}

The Vault Query API leverages the rich semantics of the underlying JPA [Hibernate](https://docs.jboss.org/hibernate/jpa/2.1/api/)-based [State Persistence](state-persistence.md) framework adopted by Corda.


{{< note >}}
Permissioning at the database level will be enforced at a later date to ensure authenticated, role-based, read-only access to underlying Corda tables.
{{< /note >}}

{{< note >}}
APIs now provide ease of use calling semantics from both Java and Kotlin. However, it should be noted that Java custom queries are significantly more verbose due to the use of reflection fields to reference schema attribute types.
{{< /note >}}

### Custom queries in Java

An example of a custom query in Java is provided below:

```java
QueryCriteria generalCriteria = new VaultQueryCriteria(Vault.StateStatus.ALL);

FieldInfo attributeCurrency = getField("currency", CashSchemaV1.PersistentCashState.class);
FieldInfo attributeQuantity = getField("pennies", CashSchemaV1.PersistentCashState.class);

CriteriaExpression currencyIndex = Builder.equal(attributeCurrency, "USD");
CriteriaExpression quantityIndex = Builder.greaterThanOrEqual(attributeQuantity, 10L);

QueryCriteria customCriteria2 = new VaultCustomQueryCriteria(quantityIndex);
QueryCriteria customCriteria1 = new VaultCustomQueryCriteria(currencyIndex);


QueryCriteria criteria = generalCriteria.and(customCriteria1).and(customCriteria2);
Vault.Page<ContractState> results = vaultService.queryBy(Cash.State.class, criteria);

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)


{{< note >}}
Queries by `Party` specify the `AbstractParty` which may be concrete or anonymous. Note, however, that if an anonymous party does not resolve to an X500 name via the `IdentityService`, no query results will ever be produced. For performance reasons, queries do not use `PublicKey` as search criteria.
{{< /note >}}

### Custom queries and case sensitivity

Custom queries can be either case sensitive or case insensitive. They are defined via a `Boolean` as one of the function parameters of each operator function. By default, each operator is case sensitive.

#### Case-sensitive custom query operators in Kotlin

An example of a case-sensitive custom query operator in Kotlin is provided below:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
val currencyIndex = PersistentCashState::currency.equal(USD.currencyCode, true)
```
{{% /tab %}}

{{< /tabs >}}

{{< note >}}
The `Boolean` input of `true` in this example could be removed since the function will default to `true` when not provided.
{{< /note >}}

#### Case-insensitive custom query operators in Kotlin

An example of a case-insensitive custom query operator in Kotlin is provided below:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
val currencyIndex = PersistentCashState::currency.equal(USD.currencyCode, false)
```
{{% /tab %}}

{{< /tabs >}}

#### Case-sensitive custom query operators in Java

An example of a case-sensitive custom query operator in Java is provided below:

{{< tabs name="tabs-3" >}}
{{% tab name="java" %}}
```java
FieldInfo attributeCurrency = getField("currency", CashSchemaV1.PersistentCashState.class);
CriteriaExpression currencyIndex = Builder.equal(attributeCurrency, "USD", true);
```
{{% /tab %}}

{{< /tabs >}}

#### Case-insensitive custom query operators in Java

An example of a case-insensitive custom query operator in Java is provided below:

{{< tabs name="tabs-4" >}}
{{% tab name="java" %}}
```java
FieldInfo attributeCurrency = getField("currency", CashSchemaV1.PersistentCashState.class);
CriteriaExpression currencyIndex = Builder.equal(attributeCurrency, "USD", false);
```
{{% /tab %}}

{{< /tabs >}}


## Pagination

The API provides support for paging where large numbers of results are expected (by default, a page size is set to 200
results). Defining a sensible default page size enables efficient checkpointing within flows, and frees the developer
from worrying about pagination where result sets are expected to be constrained to 200 or fewer entries. Where large
result sets are expected (such as using the RPC API for reporting and/or UI display), it is strongly recommended to
define a `PageSpecification` to correctly process results with efficient memory utilisation. A fail-fast mode is in
place to alert API users to the need for pagination where a single query returns more than 200 results and no
`PageSpecification` has been supplied.

Here’s a query that extracts every unconsumed `ContractState` from the vault in pages of size 200, starting from the
default page number (page one):

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
val vaultSnapshot = proxy.vaultQueryBy<ContractState>(
    QueryCriteria.VaultQueryCriteria(Vault.StateStatus.UNCONSUMED),
    PageSpecification(DEFAULT_PAGE_NUM, 200))
```
{{% /tab %}}

{{< /tabs >}}

{{< note >}}
A page's maximum size `MAX_PAGE_SIZE` is defined as `Int.MAX_VALUE` and should be used with extreme
caution as results returned may exceed your JVM’s memory footprint.

{{< /note >}}

{{< note >}}
To obtain reliable results when using paging, always specify the sort option. With no sort, RDBMS is free to return results in any order.

{{< /note >}}


## Example usage - Kotlin

Some examples of how to write vault queries in Kotlin are provided below.

### General snapshot queries using `VaultQueryCriteria`:

#### Query for all unconsumed states (simplest query possible):

```kotlin
val result = vaultService.queryBy<ContractState>()

/**
 * Query result returns a [Vault.Page] which contains:
 *  1) actual states as a list of [StateAndRef]
 *  2) state reference and associated vault metadata as a list of [Vault.StateMetadata]
 *  3) [PageSpecification] used to delimit the size of items returned in the result set (defaults to [DEFAULT_PAGE_SIZE])
 *  4) Total number of items available (to aid further pagination if required)
 */
val states = result.states
val metadata = result.statesMetadata


```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed states for some state references:

```kotlin
val sortAttribute = SortAttribute.Standard(Sort.CommonStateAttribute.STATE_REF_TXN_ID)
val criteria = VaultQueryCriteria(stateRefs = listOf(stateRefs.first(), stateRefs.last()))
val results = vaultService.queryBy<DummyLinearContract.State>(criteria, Sort(setOf(Sort.SortColumn(sortAttribute, Sort.Direction.ASC))))

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed states for several contract state types:

```kotlin
val criteria = VaultQueryCriteria(contractStateTypes = setOf(Cash.State::class.java, DealState::class.java))
val results = vaultService.queryBy<ContractState>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed states for specified contract state constraint types and sorted in ascending alphabetical order:

```kotlin
val constraintTypeCriteria = VaultQueryCriteria(constraintTypes = setOf(HASH, CZ_WHITELISTED))
val sortAttribute = SortAttribute.Standard(Sort.VaultStateAttribute.CONSTRAINT_TYPE)
val sorter = Sort(setOf(Sort.SortColumn(sortAttribute, Sort.Direction.ASC)))
val constraintResults = vaultService.queryBy<LinearState>(constraintTypeCriteria, sorter)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)


#### Query for unconsumed states for specified contract state constraints (type and data):

```kotlin
val constraintCriteria = VaultQueryCriteria(constraints = setOf(Vault.ConstraintInfo(constraintSignature),
        Vault.ConstraintInfo(constraintSignatureCompositeKey), Vault.ConstraintInfo(constraintHash)))
val constraintResults = vaultService.queryBy<LinearState>(constraintCriteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed states for a given notary:

```kotlin
val criteria = VaultQueryCriteria(notary = listOf(CASH_NOTARY))
val results = vaultService.queryBy<ContractState>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed states for a given set of participants (matches any state that contains at least one of the specified participants):

```kotlin
val criteria = LinearStateQueryCriteria(participants = listOf(BIG_CORP, MINI_CORP))
val results = vaultService.queryBy<ContractState>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed states for a given set of participants (exactly matches only states that contain all specified participants):

```kotlin
val strictCriteria = LinearStateQueryCriteria(exactParticipants = listOf(MEGA_CORP, BIG_CORP))
val strictResults = vaultService.queryBy<ContractState>(strictCriteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed states recorded between two time intervals:

```kotlin
val start = TODAY
val end = TODAY.plus(30, ChronoUnit.DAYS)
val recordedBetweenExpression = TimeCondition(
        QueryCriteria.TimeInstantType.RECORDED,
        ColumnPredicate.Between(start, end))
val criteria = VaultQueryCriteria(timeCondition = recordedBetweenExpression)
val results = vaultService.queryBy<ContractState>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

{{< note >}}
This example illustrates usage of a `Between` `ColumnPredicate`.
{{< /note >}}

#### Query for all states with pagination specification (10 results per page):

```kotlin
val pagingSpec = PageSpecification(DEFAULT_PAGE_NUM, 10)
val criteria = VaultQueryCriteria(status = Vault.StateStatus.ALL)
val results = vaultService.queryBy<ContractState>(criteria, paging = pagingSpec)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

{{< note >}}
The result set metadata field *totalStatesAvailable* allows you to further paginate accordingly as
demonstrated in the following example.
{{< /note >}}

#### Query for all states using a pagination specification and iterate using the *totalStatesAvailable* field until no further pages available:

```kotlin
var pageNumber = DEFAULT_PAGE_NUM
val states = mutableListOf<StateAndRef<ContractState>>()
do {
    val pageSpec = PageSpecification(pageNumber = pageNumber, pageSize = pageSize)
    val results = vaultService.queryBy<ContractState>(VaultQueryCriteria(), pageSpec)
    states.addAll(results.states)
    pageNumber++
} while ((pageSpec.pageSize * (pageNumber - 1)) <= results.totalStatesAvailable)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for only relevant states in the vault:

```kotlin
    val relevancyAllCriteria = VaultQueryCriteria(relevancyStatus = Vault.RelevancyStatus.RELEVANT)
    val allDealStateCount = vaultService.queryBy<DummyDealContract.State>(relevancyAllCriteria).states

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

### LinearState and DealState queries using `LinearStateQueryCriteria`:

#### Query for unconsumed linear states for given linear IDs:

```kotlin
val linearIds = issuedStates.states.map { it.state.data.linearId }.toList()
val criteria = LinearStateQueryCriteria(linearId = listOf(linearIds.first(), linearIds.last()))
val results = vaultService.queryBy<LinearState>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for all linear states associated with a linear ID:

```kotlin
val linearStateCriteria = LinearStateQueryCriteria(linearId = listOf(linearId), status = Vault.StateStatus.ALL)
val vaultCriteria = VaultQueryCriteria(status = Vault.StateStatus.ALL)
val results = vaultService.queryBy<LinearState>(linearStateCriteria and vaultCriteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed deal states with deal references:

```kotlin
val criteria = LinearStateQueryCriteria(externalId = listOf("456", "789"))
val results = vaultService.queryBy<DealState>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed deal states with deal parties (any match):

```kotlin
val criteria = LinearStateQueryCriteria(participants = parties)
val results = vaultService.queryBy<DealState>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for unconsumed deal states with deal parties (exact match):

```kotlin
val strictCriteria = LinearStateQueryCriteria().withExactParticipants(parties)
val strictResults = vaultService.queryBy<ContractState>(strictCriteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for only relevant linear states in the vault:

```kotlin
    val allLinearStateCriteria = LinearStateQueryCriteria(relevancyStatus = Vault.RelevancyStatus.RELEVANT)
    val allLinearStates = vaultService.queryBy<DummyLinearContract.State>(allLinearStateCriteria).states

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

### FungibleAsset and DealState queries using `FungibleAssetQueryCriteria`:

#### Query for fungible assets for a given currency:

```kotlin
val ccyIndex = builder { CashSchemaV1.PersistentCashState::currency.equal(USD.currencyCode) }
val criteria = VaultCustomQueryCriteria(ccyIndex)
val results = vaultService.queryBy<FungibleAsset<*>>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for fungible assets for a minimum quantity:

```kotlin
val fungibleAssetCriteria = FungibleAssetQueryCriteria(quantity = builder { greaterThan(2500L) })
val results = vaultService.queryBy<Cash.State>(fungibleAssetCriteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

{{< note >}}
This example uses the builder DSL.
{{< /note >}}

#### Query for fungible assets for a specific issuer party:

```kotlin
val criteria = FungibleAssetQueryCriteria(issuer = listOf(BOC))
val results = vaultService.queryBy<FungibleAsset<*>>(criteria)

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Query for only relevant fungible states in the vault:

```kotlin
val allCashCriteria = FungibleStateQueryCriteria(relevancyStatus = Vault.RelevancyStatus.RELEVANT)
val allCashStates = vaultService.queryBy<Cash.State>(allCashCriteria).states

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

### Aggregate Function queries using `VaultCustomQueryCriteria`:

{{< note >}}
Query results for aggregate functions are contained in the `otherResults` attribute of a results page.
{{< /note >}}

#### Aggregations on cash using various functions:

```kotlin
val sum = builder { CashSchemaV1.PersistentCashState::pennies.sum() }
val sumCriteria = VaultCustomQueryCriteria(sum)

val count = builder { CashSchemaV1.PersistentCashState::pennies.count() }
val countCriteria = VaultCustomQueryCriteria(count)

val max = builder { CashSchemaV1.PersistentCashState::pennies.max() }
val maxCriteria = VaultCustomQueryCriteria(max)

val min = builder { CashSchemaV1.PersistentCashState::pennies.min() }
val minCriteria = VaultCustomQueryCriteria(min)

val avg = builder { CashSchemaV1.PersistentCashState::pennies.avg() }
val avgCriteria = VaultCustomQueryCriteria(avg)

val results = vaultService.queryBy<FungibleAsset<*>>(sumCriteria
        .and(countCriteria)
        .and(maxCriteria)
        .and(minCriteria)
        .and(avgCriteria))

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

{{< note >}}
`otherResults` will contain 5 items, one per calculated aggregate function.
{{< /note >}}

#### Aggregations on cash grouped by currency for various functions:

```kotlin
val sum = builder { CashSchemaV1.PersistentCashState::pennies.sum(groupByColumns = listOf(CashSchemaV1.PersistentCashState::currency)) }
val sumCriteria = VaultCustomQueryCriteria(sum)

val max = builder { CashSchemaV1.PersistentCashState::pennies.max(groupByColumns = listOf(CashSchemaV1.PersistentCashState::currency)) }
val maxCriteria = VaultCustomQueryCriteria(max)

val min = builder { CashSchemaV1.PersistentCashState::pennies.min(groupByColumns = listOf(CashSchemaV1.PersistentCashState::currency)) }
val minCriteria = VaultCustomQueryCriteria(min)

val avg = builder { CashSchemaV1.PersistentCashState::pennies.avg(groupByColumns = listOf(CashSchemaV1.PersistentCashState::currency)) }
val avgCriteria = VaultCustomQueryCriteria(avg)

val results = vaultService.queryBy<FungibleAsset<*>>(sumCriteria
        .and(maxCriteria)
        .and(minCriteria)
        .and(avgCriteria))

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

{{< note >}}
`otherResults` will contain 24 items, one result per calculated aggregate function per currency (the grouping attribute - currency in this case - is returned per aggregate result).
{{< /note >}}

#### Sum aggregation on cash grouped by issuer party and currency and sorted by sum:

```kotlin
val sum = builder {
    CashSchemaV1.PersistentCashState::pennies.sum(groupByColumns = listOf(CashSchemaV1.PersistentCashState::issuerPartyHash,
            CashSchemaV1.PersistentCashState::currency),
            orderBy = Sort.Direction.DESC)
}

val results = vaultService.queryBy<FungibleAsset<*>>(VaultCustomQueryCriteria(sum))

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

{{< note >}}
`otherResults` will contain 12 items sorted from largest summed cash amount to smallest, one result per calculated aggregate function per issuer party and currency (grouping attributes are returned per aggregate result).
{{< /note >}}

Dynamic queries (also using `VaultQueryCriteria`) are an extension to the snapshot queries by returning an additional `QueryResults` return type in the form of an `Observable<Vault.Update>`. Refer to
[ReactiveX Observable](http://reactivex.io/documentation/observable.html) for a detailed understanding and usage of this type.

#### Track unconsumed cash states:

```kotlin
        vaultService.trackBy<Cash.State>().updates     // UNCONSUMED default

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

#### Track unconsumed linear states:

```kotlin
val (snapshot, updates) = vaultService.trackBy<LinearState>()

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)

{{< note >}}
This will return both `DealState` and `LinearState` states.
{{< /note >}}

#### Track unconsumed deal states:

```kotlin
val (snapshot, updates) = vaultService.trackBy<DealState>()

```

[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)


{{< note >}}
This will return only `DealState` states.
{{< /note >}}

## Example usage - Java

Some examples of how to write vault queries in Java are provided below.

#### Query for all unconsumed linear states:

```java
Vault.Page<LinearState> results = vaultService.queryBy(LinearState.class);

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

#### Query for all consumed cash states:

```java
VaultQueryCriteria criteria = new VaultQueryCriteria(Vault.StateStatus.CONSUMED);
Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, criteria);

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

#### Query for consumed deal states or linear IDs, specify a paging specification and sort by unique identifier:

```java
Vault.StateStatus status = Vault.StateStatus.CONSUMED;
@SuppressWarnings("unchecked")
Set<Class<LinearState>> contractStateTypes = new HashSet(singletonList(LinearState.class));

QueryCriteria vaultCriteria = new VaultQueryCriteria(status, contractStateTypes);

List<UniqueIdentifier> linearIds = singletonList(ids.getSecond());
QueryCriteria linearCriteriaAll = new LinearStateQueryCriteria(null, linearIds, Vault.StateStatus.UNCONSUMED, null);
QueryCriteria dealCriteriaAll = new LinearStateQueryCriteria(null, null, dealIds);

QueryCriteria compositeCriteria1 = dealCriteriaAll.or(linearCriteriaAll);
QueryCriteria compositeCriteria2 = compositeCriteria1.and(vaultCriteria);

PageSpecification pageSpec = new PageSpecification(DEFAULT_PAGE_NUM, MAX_PAGE_SIZE);
Sort.SortColumn sortByUid = new Sort.SortColumn(new SortAttribute.Standard(Sort.LinearStateAttribute.UUID), Sort.Direction.DESC);
Sort sorting = new Sort(ImmutableSet.of(sortByUid));
Vault.Page<LinearState> results = vaultService.queryBy(LinearState.class, compositeCriteria2, pageSpec, sorting);

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

#### Query for all states using a pagination specification and iterate using the *totalStatesAvailable* field until no further pages available:

```java
int pageNumber = DEFAULT_PAGE_NUM;
List<StateAndRef<Cash.State>> states = new ArrayList<>();
long totalResults;
do {
    PageSpecification pageSpec = new PageSpecification(pageNumber, pageSize);
    Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, new VaultQueryCriteria(), pageSpec);
    totalResults = results.getTotalStatesAvailable();
    List<StateAndRef<Cash.State>> newStates = results.getStates();
    System.out.println(newStates.size());
    states.addAll(results.getStates());
    pageNumber++;
} while ((pageSize * (pageNumber - 1) <= totalResults));

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

### Aggregate Function queries using `VaultCustomQueryCriteria`:

#### Aggregations on cash using various functions:

```java
FieldInfo pennies = getField("pennies", CashSchemaV1.PersistentCashState.class);

QueryCriteria sumCriteria = new VaultCustomQueryCriteria(sum(pennies));
QueryCriteria countCriteria = new VaultCustomQueryCriteria(Builder.count(pennies));
QueryCriteria maxCriteria = new VaultCustomQueryCriteria(Builder.max(pennies));
QueryCriteria minCriteria = new VaultCustomQueryCriteria(Builder.min(pennies));
QueryCriteria avgCriteria = new VaultCustomQueryCriteria(Builder.avg(pennies));

QueryCriteria criteria = sumCriteria.and(countCriteria).and(maxCriteria).and(minCriteria).and(avgCriteria);
Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, criteria);

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

#### Aggregations on cash grouped by currency for various functions:

```java
FieldInfo pennies = getField("pennies", CashSchemaV1.PersistentCashState.class);
FieldInfo currency = getField("currency", CashSchemaV1.PersistentCashState.class);

QueryCriteria sumCriteria = new VaultCustomQueryCriteria(sum(pennies, singletonList(currency)));
QueryCriteria countCriteria = new VaultCustomQueryCriteria(Builder.count(pennies));
QueryCriteria maxCriteria = new VaultCustomQueryCriteria(Builder.max(pennies, singletonList(currency)));
QueryCriteria minCriteria = new VaultCustomQueryCriteria(Builder.min(pennies, singletonList(currency)));
QueryCriteria avgCriteria = new VaultCustomQueryCriteria(Builder.avg(pennies, singletonList(currency)));

QueryCriteria criteria = sumCriteria.and(countCriteria).and(maxCriteria).and(minCriteria).and(avgCriteria);
Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, criteria);

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

#### Sum aggregation on cash grouped by issuer party and currency and sorted by sum:

```java
FieldInfo pennies = getField("pennies", CashSchemaV1.PersistentCashState.class);
FieldInfo currency = getField("currency", CashSchemaV1.PersistentCashState.class);
FieldInfo issuerPartyHash = getField("issuerPartyHash", CashSchemaV1.PersistentCashState.class);
QueryCriteria sumCriteria = new VaultCustomQueryCriteria(sum(pennies, asList(issuerPartyHash, currency), Sort.Direction.DESC));
Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, sumCriteria);

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

#### Track unconsumed cash states:

```java
@SuppressWarnings("unchecked")
Set<Class<ContractState>> contractStateTypes = new HashSet(singletonList(Cash.State.class));

VaultQueryCriteria criteria = new VaultQueryCriteria(Vault.StateStatus.UNCONSUMED, contractStateTypes);
DataFeed<Vault.Page<ContractState>, Vault.Update<ContractState>> results = vaultService.trackBy(ContractState.class, criteria);

Vault.Page<ContractState> snapshot = results.getSnapshot();


```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

#### Track unconsumed deal states or linear states (with snapshot including specification of paging and sorting by unique identifier):

```java
@SuppressWarnings("unchecked")
Set<Class<ContractState>> contractStateTypes = new HashSet(asList(DealState.class, LinearState.class));
QueryCriteria vaultCriteria = new VaultQueryCriteria(Vault.StateStatus.UNCONSUMED, contractStateTypes);

List<UniqueIdentifier> linearIds = singletonList(uid);
List<AbstractParty> dealParty = singletonList(MEGA_CORP.getParty());
QueryCriteria dealCriteria = new LinearStateQueryCriteria(dealParty, null, dealIds);
QueryCriteria linearCriteria = new LinearStateQueryCriteria(dealParty, linearIds, Vault.StateStatus.UNCONSUMED, null);
QueryCriteria dealOrLinearIdCriteria = dealCriteria.or(linearCriteria);
QueryCriteria compositeCriteria = dealOrLinearIdCriteria.and(vaultCriteria);

PageSpecification pageSpec = new PageSpecification(DEFAULT_PAGE_NUM, MAX_PAGE_SIZE);
Sort.SortColumn sortByUid = new Sort.SortColumn(new SortAttribute.Standard(Sort.LinearStateAttribute.UUID), Sort.Direction.DESC);
Sort sorting = new Sort(ImmutableSet.of(sortByUid));
DataFeed<Vault.Page<ContractState>, Vault.Update<ContractState>> results = vaultService.trackBy(ContractState.class, compositeCriteria, pageSpec, sorting);

Vault.Page<ContractState> snapshot = results.getSnapshot();

```

[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/4.6/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)


## Troubleshooting

If the results you were expecting do not match actual returned query results, we recommend you add an entry to your `log4j2.xml` configuration file to enable display of executed SQL statements:

```kotlin
<Logger name="org.hibernate.SQL" level="debug" additivity="false">

    <AppenderRef ref="Console-Appender"/>

</Logger>
```


## Behavioural notes


* `TrackBy` updates do not take into account the full criteria specification due to different and more restrictive syntax in [observables](https://github.com/ReactiveX/RxJava/wiki) filtering (vs full SQL-92 JDBC filtering as used in snapshot views). Specifically, dynamic updates are filtered by `contractStateType` and `stateType` (`UNCONSUMED`, `CONSUMED`, `ALL`) only.
* `QueryBy` and `TrackBy` snapshot views using pagination may return different result sets, as each paging request is a separate SQL query on the underlying database, and it is entirely conceivable that state modifications are taking place in between and/or in parallel to paging requests. When using pagination, always check the value of the `totalStatesAvailable` (from the `Vault.Page` result) and adjust further paging requests appropriately.


## Other use-case scenarios

For advanced use cases that require sophisticated pagination, sorting, grouping, and aggregation functions, it is recommended that the CorDapp developer utilise one of the many proven frameworks that ship with this capability out of the box, namely, implementations of JPQL (JPA Query Language) such as Hibernate for advanced SQL access, and Spring Data for advanced pagination and ordering constructs.

## Mapping owning keys to external IDs

When creating new public keys via the `KeyManagementService`, it is possible to create an association between the newly created public key and an external ID. This, in effect, allows CorDapp developers to group state ownership/participation keys by an account ID.

{{< note >}}
This only works with freshly generated public keys and *not* the node’s legal identity key. If you require that the freshly generated keys be for the node’s identity, then use `PersistentKeyManagementService.freshKeyAndCert` instead of `freshKey`.
Currently, the generation of keys for other identities is not supported.

{{< /note >}}
The code snippet below show how keys can be associated with an external ID by using the exposed JPA functionality:

{{< tabs name="tabs-6" >}}
{{% tab name="java" %}}
```java
public AnonymousParty freshKeyForExternalId(UUID externalId, ServiceHub services) {
    // Create a fresh key pair and return the public key.
    AnonymousParty anonymousParty = freshKey();
    // Associate the fresh key to an external ID.
    services.withEntityManager(entityManager -> {
        PersistentKeyManagementService.PublicKeyHashToExternalId mapping = PersistentKeyManagementService.PublicKeyHashToExternalId(externalId, anonymousParty.owningKey);
        entityManager.persist(mapping);
        return null;
    });
    return anonymousParty;
}
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
fun freshKeyForExternalId(externalId: UUID, services: ServiceHub): AnonymousParty {
    // Create a fresh key pair and return the public key.
    val anonymousParty = freshKey()
    // Associate the fresh key to an external ID.
    services.withEntityManager {
        val mapping = PersistentKeyManagementService.PublicKeyHashToExternalId(externalId, anonymousParty.owningKey)
        persist(mapping)
    }
    return anonymousParty
}
```
{{% /tab %}}

{{< /tabs >}}

As can be seen in the code snippet above, the `PublicKeyHashToExternalId` entity has been added to `PersistentKeyManagementService`, which allows you to associate your public keys with external IDs.

{{< note >}}
Here, it is worth noting that we must map **owning keys** to external IDs, as opposed to **state objects**. This is because it might be the case that a `LinearState` is owned by two public keys generated by the same node.
{{< /note >}}

The logic here is that when these public keys are used to own or participate in a state object, it is trivial to then associate those states with a particular external ID. Behind the scenes, when states are persisted to the vault, the owning keys for each state are persisted to a `PersistentParty` table. The `PersistentParty` table can be joined with the `PublicKeyHashToExternalId` table to create a view which maps each state to one or more external IDs. The [entity relationship diagram](/en/images/state-to-external-id.png "state to external id") illustrates how this works.

When performing a vault query, it is now possible to query for states by external ID using the `externalIds` parameter in `VaultQueryCriteria`.
