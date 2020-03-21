---
aliases:
- /releases/release-V1.0/api-vault-query.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-1-0:
    identifier: corda-os-1-0-api-vault-query
    parent: corda-os-1-0-api-index
    weight: 1040
tags:
- api
- vault
- query
title: 'API: Vault Query'
---


# API: Vault Query

Corda has been architected from the ground up to encourage usage of industry standard, proven query frameworks and libraries for accessing RDBMS backed transactional stores (including the Vault).

Corda provides a number of flexible query mechanisms for accessing the Vault:


* Vault Query API
* using a JDBC session (as described in [Persistence](api-persistence.md#jdbc-session-ref))
* custom [JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html)/[JPQL](http://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#hql) queries
* custom 3rd party Data Access frameworks such as [Spring Data](http://projects.spring.io/spring-data)

The majority of query requirements can be satisfied by using the Vault Query API, which is exposed via the `VaultService` for use directly by flows:

```kotlin
    /**
     * Generic vault query function which takes a [QueryCriteria] object to define filters,
     * optional [PageSpecification] and optional [Sort] modification criteria (default unsorted),
     * and returns a [Vault.Page] object containing the following:
     *  1. states as a List of <StateAndRef> (page number and size defined by [PageSpecification])
     *  2. states metadata as a List of [Vault.StateMetadata] held in the Vault States table.
     *  3. total number of results available if [PageSpecification] supplied (otherwise returns -1)
     *  4. status types used in this query: UNCONSUMED, CONSUMED, ALL
     *  5. other results (aggregate functions with/without using value groups)
     *
     * @throws VaultQueryException if the query cannot be executed for any reason
     *        (missing criteria or parsing error, paging errors, unsupported query, underlying database error)
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
     * and returns a [Vault.PageAndUpdates] object containing
     * 1) a snapshot as a [Vault.Page] (described previously in [queryBy])
     * 2) an [Observable] of [Vault.Update]
     *
     * @throws VaultQueryException if the query cannot be executed for any reason
     *
     * Notes: the snapshot part of the query adheres to the same behaviour as the [queryBy] function.
     *        the [QueryCriteria] applies to both snapshot and deltas (streaming updates).
     */
    @Throws(VaultQueryException::class)
    fun <T : ContractState> _trackBy(criteria: QueryCriteria,
                                     paging: PageSpecification,
                                     sorting: Sort,
                                     contractStateType: Class<out T>): DataFeed<Vault.Page<T>, Vault.Update<T>>

```
{{/* github src='core/src/main/kotlin/net/corda/core/node/services/VaultService.kt' url='https://github.com/corda/corda/blob/1.0/core/src/main/kotlin/net/corda/core/node/services/VaultService.kt#L243-L284' raw='https://raw.githubusercontent.com/corda/corda/1.0/core/src/main/kotlin/net/corda/core/node/services/VaultService.kt' start='DOCSTART VaultQueryAPI' end='DOCEND VaultQueryAPI' */}}[VaultService.kt](https://github.com/corda/corda/blob/release/os/1.0/core/src/main/kotlin/net/corda/core/node/services/VaultService.kt)
and via `CordaRPCOps` for use by RPC client applications:

```kotlin
    @RPCReturnsObservables
    fun <T : ContractState> vaultQueryBy(criteria: QueryCriteria,
                                         paging: PageSpecification,
                                         sorting: Sort,
                                         contractStateType: Class<out T>): Vault.Page<T>

```
{{/* github src='core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' url='https://github.com/corda/corda/blob/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt#L93-L97' raw='https://raw.githubusercontent.com/corda/corda/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' start='DOCSTART VaultQueryByAPI' end='DOCEND VaultQueryByAPI' */}}[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)
```kotlin
    @RPCReturnsObservables
    fun <T : ContractState> vaultTrackBy(criteria: QueryCriteria,
                                         paging: PageSpecification,
                                         sorting: Sort,
                                         contractStateType: Class<out T>): DataFeed<Vault.Page<T>, Vault.Update<T>>

```
{{/* github src='core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' url='https://github.com/corda/corda/blob/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt#L131-L135' raw='https://raw.githubusercontent.com/corda/corda/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' start='DOCSTART VaultTrackByAPI' end='DOCEND VaultTrackByAPI' */}}[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)
Helper methods are also provided with default values for arguments:

```kotlin
    fun <T : ContractState> vaultQuery(contractStateType: Class<out T>): Vault.Page<T> {
        return vaultQueryBy(QueryCriteria.VaultQueryCriteria(), PageSpecification(), Sort(emptySet()), contractStateType)
    }
    fun <T : ContractState> vaultQueryByCriteria(criteria: QueryCriteria, contractStateType: Class<out T>): Vault.Page<T> {
        return vaultQueryBy(criteria, PageSpecification(), Sort(emptySet()), contractStateType)
    }
    fun <T : ContractState> vaultQueryByWithPagingSpec(contractStateType: Class<out T>, criteria: QueryCriteria, paging: PageSpecification): Vault.Page<T> {
        return vaultQueryBy(criteria, paging, Sort(emptySet()), contractStateType)
    }
    fun <T : ContractState> vaultQueryByWithSorting(contractStateType: Class<out T>, criteria: QueryCriteria, sorting: Sort): Vault.Page<T> {
        return vaultQueryBy(criteria, PageSpecification(), sorting, contractStateType)
    }

```
{{/* github src='core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' url='https://github.com/corda/corda/blob/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt#L104-L115' raw='https://raw.githubusercontent.com/corda/corda/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' start='DOCSTART VaultQueryAPIHelpers' end='DOCEND VaultQueryAPIHelpers' */}}[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)
```kotlin
    fun <T : ContractState> vaultTrack(contractStateType: Class<out T>): DataFeed<Vault.Page<T>, Vault.Update<T>> {
        return vaultTrackBy(QueryCriteria.VaultQueryCriteria(), PageSpecification(), Sort(emptySet()), contractStateType)
    }
    fun <T : ContractState> vaultTrackByCriteria(contractStateType: Class<out T>, criteria: QueryCriteria): DataFeed<Vault.Page<T>, Vault.Update<T>> {
        return vaultTrackBy(criteria, PageSpecification(), Sort(emptySet()), contractStateType)
    }
    fun <T : ContractState> vaultTrackByWithPagingSpec(contractStateType: Class<out T>, criteria: QueryCriteria, paging: PageSpecification): DataFeed<Vault.Page<T>, Vault.Update<T>> {
        return vaultTrackBy(criteria, paging, Sort(emptySet()), contractStateType)
    }
    fun <T : ContractState> vaultTrackByWithSorting(contractStateType: Class<out T>, criteria: QueryCriteria, sorting: Sort): DataFeed<Vault.Page<T>, Vault.Update<T>> {
        return vaultTrackBy(criteria, PageSpecification(), sorting, contractStateType)
    }

```
{{/* github src='core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' url='https://github.com/corda/corda/blob/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt#L142-L153' raw='https://raw.githubusercontent.com/corda/corda/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt' start='DOCSTART VaultTrackAPIHelpers' end='DOCEND VaultTrackAPIHelpers' */}}[CordaRPCOps.kt](https://github.com/corda/corda/blob/release/os/1.0/core/src/main/kotlin/net/corda/core/messaging/CordaRPCOps.kt)
The API provides both static (snapshot) and dynamic (snapshot with streaming updates) methods for a defined set of filter criteria.


* Use `queryBy` to obtain a only current snapshot of data (for a given `QueryCriteria`)
* Use `trackBy` to obtain a both a current snapshot and a future stream of updates (for a given `QueryCriteria`)

{{< note >}}
Streaming updates are only filtered based on contract type and state status (UNCONSUMED, CONSUMED, ALL)

{{< /note >}}
Simple pagination (page number and size) and sorting (directional ordering using standard or custom property attributes) is also specifiable.
Defaults are defined for Paging (pageNumber = 1, pageSize = 200) and Sorting (direction = ASC).

The `QueryCriteria` interface provides a flexible mechanism for specifying different filtering criteria, including and/or composition and a rich set of operators to include: binary logical (AND, OR), comparison (LESS_THAN, LESS_THAN_OR_EQUAL, GREATER_THAN, GREATER_THAN_OR_EQUAL), equality (EQUAL, NOT_EQUAL), likeness (LIKE, NOT_LIKE), nullability (IS_NULL, NOT_NULL), and collection based (IN, NOT_IN). Standard SQL-92 aggregate functions (SUM, AVG, MIN, MAX, COUNT) are also supported.

There are four implementations of this interface which can be chained together to define advanced filters.


* `VaultQueryCriteria` provides filterable criteria on attributes within the Vault states table: status (UNCONSUMED, CONSUMED), state reference(s), contract state type(s), notaries, soft locked states, timestamps (RECORDED, CONSUMED).> 
> {{< note >}}
> Sensible defaults are defined for frequently used attributes (status = UNCONSUMED, always include soft locked states).{{< /note >}}


* `FungibleAssetQueryCriteria` provides filterable criteria on attributes defined in the Corda Core `FungibleAsset` contract state interface, used to represent assets that are fungible, countable and issued by a specific party (eg. `Cash.State` and `CommodityContract.State` in the Corda finance module). Filterable attributes include: participants(s), owner(s), quantity, issuer party(s) and issuer reference(s).> 
> {{< note >}}
> All contract states that extend the `FungibleAsset` now automatically persist that interfaces common state attributes to the **vault_fungible_states** table.{{< /note >}}


* `LinearStateQueryCriteria` provides filterable criteria on attributes defined in the Corda Core `LinearState` and `DealState` contract state interfaces, used to represent entities that continuously supercede themselves, all of which share the same *linearId* (eg. trade entity states such as the `IRSState` defined in the SIMM valuation demo). Filterable attributes include: participant(s), linearId(s), uuid(s), and externalId(s).> 
> {{< note >}}
> All contract states that extend `LinearState` or `DealState` now automatically persist those interfaces common state attributes to the **vault_linear_states** table.{{< /note >}}


* `VaultCustomQueryCriteria` provides the means to specify one or many arbitrary expressions on attributes defined by a custom contract state that implements its own schema as described in the [Persistence](api-persistence.md) documentation and associated examples. Custom criteria expressions are expressed using one of several type-safe `CriteriaExpression`: BinaryLogical, Not, ColumnPredicateExpression, AggregateFunctionExpression. The `ColumnPredicateExpression` allows for specification arbitrary criteria using the previously enumerated operator types. The `AggregateFunctionExpression` allows for the specification of an aggregate function type (sum, avg, max, min, count) with optional grouping and sorting. Furthermore, a rich DSL is provided to enable simple construction of custom criteria using any combination of `ColumnPredicate`. See the `Builder` object in `QueryCriteriaUtils` for a complete specification of the DSL.> 
> {{< note >}}
> custom contract schemas are automatically registered upon node startup for CorDapps. Please refer to{{< /note >}}
> [Persistence](api-persistence.md) for mechanisms of registering custom schemas for different testing purposes.


All `QueryCriteria` implementations are composable using `and` and `or` operators.

All `QueryCriteria` implementations provide an explicitly specifiable set of common attributes:


* State status attribute (`Vault.StateStatus`), which defaults to filtering on UNCONSUMED states.
When chaining several criterias using AND / OR, the last value of this attribute will override any previous.
* Contract state types (`<Set<Class<out ContractState>>`), which will contain at minimum one type (by default this will be `ContractState` which resolves to all state types).
When chaining several criteria using `and` and `or` operators, all specified contract state types are combined into a single set.

An example of a custom query is illustrated here:

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
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1786-L1797' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample20' end='DOCEND VaultQueryExample20' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
Custom contract states that implement the `Queryable` interface may now extend common schemas types `FungiblePersistentState` or, `LinearPersistentState`.  Previously, all custom contracts extended the root `PersistentState` class and defined repeated mappings of `FungibleAsset` and `LinearState` attributes. See `SampleCashSchemaV2` and `DummyLinearStateSchemaV2` as examples.

{{< /note >}}
Examples of these `QueryCriteria` objects are presented below for Kotlin and Java.

{{< note >}}
When specifying the Contract Type as a parameterised type to the QueryCriteria in Kotlin, queries now include all concrete implementations of that type if this is an interface. Previously, it was only possible to query on Concrete types (or the universe of all Contract States).

{{< /note >}}
The Vault Query API leverages the rich semantics of the underlying JPA [Hibernate](https://docs.jboss.org/hibernate/jpa/2.1/api/) based [Persistence](api-persistence.md) framework adopted by Corda.


{{< note >}}
Permissioning at the database level will be enforced at a later date to ensure authenticated, role-based, read-only access to underlying Corda tables.

{{< /note >}}
{{< note >}}
API’s now provide ease of use calling semantics from both Java and Kotlin. However, it should be noted that Java custom queries are significantly more verbose due to the use of reflection fields to reference schema attribute types.

{{< /note >}}
An example of a custom query in Java is illustrated here:

```java
                QueryCriteria generalCriteria = new VaultQueryCriteria(Vault.StateStatus.ALL);

                Field attributeCurrency = CashSchemaV1.PersistentCashState.class.getDeclaredField("currency");
                Field attributeQuantity = CashSchemaV1.PersistentCashState.class.getDeclaredField("pennies");

                CriteriaExpression currencyIndex = Builder.equal(attributeCurrency, "USD");
                CriteriaExpression quantityIndex = Builder.greaterThanOrEqual(attributeQuantity, 10L);

                QueryCriteria customCriteria2 = new VaultCustomQueryCriteria(quantityIndex);
                QueryCriteria customCriteria1 = new VaultCustomQueryCriteria(currencyIndex);


                QueryCriteria criteria = generalCriteria.and(customCriteria1).and(customCriteria2);
                Vault.Page<ContractState> results = vaultService.queryBy(Cash.State.class, criteria);

```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L214-L227' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample3' end='DOCEND VaultJavaQueryExample3' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)
{{< note >}}
Queries by `Party` specify the `AbstractParty` which may be concrete or anonymous. In the later case, where an anonymous party does not resolve to an X500Name via the IdentityService, no query results will ever be produced. For performance reasons, queries do not use PublicKey as search criteria.

{{< /note >}}

## Pagination

The API provides support for paging where large numbers of results are expected (by default, a page size is set to 200 results).
Defining a sensible default page size enables efficient checkpointing within flows, and frees the developer from worrying about pagination where
result sets are expected to be constrained to 200 or fewer entries. Where large result sets are expected (such as using the RPC API for reporting and/or UI display), it is strongly recommended to define a `PageSpecification` to correctly process results with efficient memory utilistion. A fail-fast mode is in place to alert API users to the need for pagination where a single query returns more than 200 results and no `PageSpecification`
has been supplied.

{{< note >}}
A pages maximum size `MAX_PAGE_SIZE` is defined as `Int.MAX_VALUE` and should be used with extreme caution as results returned may exceed your JVM’s memory footprint.

{{< /note >}}

## Example usage


### Kotlin

**General snapshot queries using** `VaultQueryCriteria`

Query for all unconsumed states (simplest query possible):

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
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L148-L159' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample1' end='DOCEND VaultQueryExample1' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for unconsumed states for some state references:

```kotlin
            val sortAttribute = SortAttribute.Standard(Sort.CommonStateAttribute.STATE_REF_TXN_ID)
            val criteria = VaultQueryCriteria(stateRefs = listOf(stateRefs.first(), stateRefs.last()))
            val results = vaultService.queryBy<DummyLinearContract.State>(criteria, Sort(setOf(Sort.SortColumn(sortAttribute, Sort.Direction.ASC))))

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L309-L311' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample2' end='DOCEND VaultQueryExample2' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for unconsumed states for several contract state types:

```kotlin
            val criteria = VaultQueryCriteria(contractStateTypes = setOf(Cash.State::class.java, DealState::class.java))
            val results = vaultService.queryBy<ContractState>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L332-L333' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample3' end='DOCEND VaultQueryExample3' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for unconsumed states for a given notary:

```kotlin
            val criteria = VaultQueryCriteria(notary = listOf(CASH_NOTARY))
            val results = vaultService.queryBy<ContractState>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L434-L435' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample4' end='DOCEND VaultQueryExample4' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for unconsumed states for a given set of participants:

```kotlin
            val criteria = LinearStateQueryCriteria(participants = listOf(BIG_CORP, MINI_CORP))
            val results = vaultService.queryBy<ContractState>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L468-L469' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample5' end='DOCEND VaultQueryExample5' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for unconsumed states recorded between two time intervals:

```kotlin
            val start = TODAY
            val end = TODAY.plus(30, ChronoUnit.DAYS)
            val recordedBetweenExpression = TimeCondition(
                    QueryCriteria.TimeInstantType.RECORDED,
                    ColumnPredicate.Between(start, end))
            val criteria = VaultQueryCriteria(timeCondition = recordedBetweenExpression)
            val results = vaultService.queryBy<ContractState>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L963-L969' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample6' end='DOCEND VaultQueryExample6' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
This example illustrates usage of a `Between` `ColumnPredicate`.

{{< /note >}}
Query for all states with pagination specification (10 results per page):

```kotlin
            val pagingSpec = PageSpecification(DEFAULT_PAGE_NUM, 10)
            val criteria = VaultQueryCriteria(status = Vault.StateStatus.ALL)
            val results = vaultService.queryBy<ContractState>(criteria, paging = pagingSpec)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1012-L1014' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample7' end='DOCEND VaultQueryExample7' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
The result set metadata field *totalStatesAvailable* allows you to further paginate accordingly as demonstrated in the following example.

{{< /note >}}
Query for all states using pagination specification and iterate using *totalStatesAvailable* field until no further pages available:

```kotlin
        var pageNumber = DEFAULT_PAGE_NUM
        val states = mutableListOf<StateAndRef<ScheduledState>>()
        do {
            val pageSpec = PageSpecification(pageSize = PAGE_SIZE, pageNumber = pageNumber)
            val results = vaultService.queryBy<ScheduledState>(VaultQueryCriteria(), pageSpec, SORTING)
            states.addAll(results.states)
            pageNumber++
        } while ((pageSpec.pageSize * (pageNumber)) <= results.totalStatesAvailable)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/events/ScheduledFlowTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/events/ScheduledFlowTests.kt#L186-L193' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/events/ScheduledFlowTests.kt' start='DOCSTART VaultQueryExamplePaging' end='DOCEND VaultQueryExamplePaging' */}}[ScheduledFlowTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/events/ScheduledFlowTests.kt)
**LinearState and DealState queries using** `LinearStateQueryCriteria`

Query for unconsumed linear states for given linear ids:

```kotlin
            val linearIds = issuedStates.states.map { it.state.data.linearId }.toList()
            val criteria = LinearStateQueryCriteria(linearId = listOf(linearIds.first(), linearIds.last()))
            val results = vaultService.queryBy<LinearState>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1241-L1243' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample8' end='DOCEND VaultQueryExample8' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for all linear states associated with a linear id:

```kotlin
            val linearStateCriteria = LinearStateQueryCriteria(linearId = listOf(linearId), status = Vault.StateStatus.ALL)
            val vaultCriteria = VaultQueryCriteria(status = Vault.StateStatus.ALL)
            val results = vaultService.queryBy<LinearState>(linearStateCriteria and vaultCriteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1297-L1299' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample9' end='DOCEND VaultQueryExample9' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for unconsumed deal states with deals references:

```kotlin
            val criteria = LinearStateQueryCriteria(externalId = listOf("456", "789"))
            val results = vaultService.queryBy<DealState>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1425-L1426' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample10' end='DOCEND VaultQueryExample10' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for unconsumed deal states with deals parties:

```kotlin
            val criteria = LinearStateQueryCriteria(participants = parties)
            val results = vaultService.queryBy<DealState>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1460-L1461' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample11' end='DOCEND VaultQueryExample11' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
**FungibleAsset and DealState queries using** `FungibleAssetQueryCriteria`

Query for fungible assets for a given currency:

```kotlin
            val ccyIndex = builder { CashSchemaV1.PersistentCashState::currency.equal(USD.currencyCode) }
            val criteria = VaultCustomQueryCriteria(ccyIndex)
            val results = vaultService.queryBy<FungibleAsset<*>>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1560-L1562' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample12' end='DOCEND VaultQueryExample12' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Query for fungible assets for a minimum quantity:

```kotlin
            val fungibleAssetCriteria = FungibleAssetQueryCriteria(quantity = builder { greaterThan(2500L) })
            val results = vaultService.queryBy<Cash.State>(fungibleAssetCriteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1625-L1626' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample13' end='DOCEND VaultQueryExample13' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
This example uses the builder DSL.

{{< /note >}}
Query for fungible assets for a specifc issuer party:

```kotlin
            val criteria = FungibleAssetQueryCriteria(issuer = listOf(BOC))
            val results = vaultService.queryBy<FungibleAsset<*>>(criteria)

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L1643-L1644' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample14' end='DOCEND VaultQueryExample14' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
**Aggregate Function queries using** `VaultCustomQueryCriteria`

{{< note >}}
Query results for aggregate functions are contained in the *otherResults* attribute of a results Page.

{{< /note >}}
Aggregations on cash using various functions:

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
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L730-L749' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample21' end='DOCEND VaultQueryExample21' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
*otherResults* will contain 5 items, one per calculated aggregate function.

{{< /note >}}
Aggregations on cash grouped by currency for various functions:

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
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L772-L787' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample22' end='DOCEND VaultQueryExample22' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
*otherResults* will contain 24 items, one result per calculated aggregate function per currency (the grouping attribute - currency in this case - is returned per aggregate result).

{{< /note >}}
Sum aggregation on cash grouped by issuer party and currency and sorted by sum:

```kotlin
            val sum = builder {
                CashSchemaV1.PersistentCashState::pennies.sum(groupByColumns = listOf(CashSchemaV1.PersistentCashState::issuerParty,
                        CashSchemaV1.PersistentCashState::currency),
                        orderBy = Sort.Direction.DESC)
            }

            val results = vaultService.queryBy<FungibleAsset<*>>(VaultCustomQueryCriteria(sum))

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L833-L839' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample23' end='DOCEND VaultQueryExample23' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
*otherResults* will contain 12 items sorted from largest summed cash amount to smallest, one result per calculated aggregate function per issuer party and currency (grouping attributes are returned per aggregate result).

{{< /note >}}
**Dynamic queries** (also using `VaultQueryCriteria`) are an extension to the snapshot queries by returning an additional `QueryResults` return type in the form of an `Observable<Vault.Update>`. Refer to [ReactiveX Observable](http://reactivex.io/documentation/observable.html) for a detailed understanding and usage of this type.

Track unconsumed cash states:

```kotlin
                    vaultService.trackBy<Cash.State>().updates     // UNCONSUMED default

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L2017-L2017' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample15' end='DOCEND VaultQueryExample15' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
Track unconsumed linear states:

```kotlin
                    val (snapshot, updates) = vaultService.trackBy<LinearState>()

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L2160-L2160' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample16' end='DOCEND VaultQueryExample16' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
This will return both Deal and Linear states.

{{< /note >}}
Track unconsumed deal states:

```kotlin
                    val (snapshot, updates) = vaultService.trackBy<DealState>()

```
{{/* github src='node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' url='https://github.com/corda/corda/blob/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt#L2209-L2209' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt' start='DOCSTART VaultQueryExample17' end='DOCEND VaultQueryExample17' */}}[VaultQueryTests.kt](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/kotlin/net/corda/node/services/vault/VaultQueryTests.kt)
{{< note >}}
This will return only Deal states.

{{< /note >}}

### Java examples

Query for all unconsumed linear states:

```java
            Vault.Page<LinearState> results = vaultService.queryBy(LinearState.class);

```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L82-L82' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample0' end='DOCEND VaultJavaQueryExample0' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)
Query for all consumed cash states:

```java
            VaultQueryCriteria criteria = new VaultQueryCriteria(Vault.StateStatus.CONSUMED);
            Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, criteria);

```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L139-L140' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample1' end='DOCEND VaultJavaQueryExample1' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)
Query for consumed deal states or linear ids, specify a paging specification and sort by unique identifier:

```java
            Vault.StateStatus status = Vault.StateStatus.CONSUMED;
            @SuppressWarnings("unchecked")
            Set<Class<LinearState>> contractStateTypes = new HashSet(Collections.singletonList(LinearState.class));

            QueryCriteria vaultCriteria = new VaultQueryCriteria(status, contractStateTypes);

            List<UniqueIdentifier> linearIds = Collections.singletonList(ids.getSecond());
            QueryCriteria linearCriteriaAll = new LinearStateQueryCriteria(null, linearIds, Vault.StateStatus.UNCONSUMED, null);
            QueryCriteria dealCriteriaAll = new LinearStateQueryCriteria(null, null, dealIds);

            QueryCriteria compositeCriteria1 = dealCriteriaAll.or(linearCriteriaAll);
            QueryCriteria compositeCriteria2 = compositeCriteria1.and(vaultCriteria);

            PageSpecification pageSpec = new PageSpecification(DEFAULT_PAGE_NUM, MAX_PAGE_SIZE);
            Sort.SortColumn sortByUid = new Sort.SortColumn(new SortAttribute.Standard(Sort.LinearStateAttribute.UUID), Sort.Direction.DESC);
            Sort sorting = new Sort(ImmutableSet.of(sortByUid));
            Vault.Page<LinearState> results = vaultService.queryBy(LinearState.class, compositeCriteria2, pageSpec, sorting);

```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L170-L186' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample2' end='DOCEND VaultJavaQueryExample2' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)
**Aggregate Function queries using** `VaultCustomQueryCriteria`

Aggregations on cash using various functions:

```java
                Field pennies = CashSchemaV1.PersistentCashState.class.getDeclaredField("pennies");

                QueryCriteria sumCriteria = new VaultCustomQueryCriteria(Builder.sum(pennies));
                QueryCriteria countCriteria = new VaultCustomQueryCriteria(Builder.count(pennies));
                QueryCriteria maxCriteria = new VaultCustomQueryCriteria(Builder.max(pennies));
                QueryCriteria minCriteria = new VaultCustomQueryCriteria(Builder.min(pennies));
                QueryCriteria avgCriteria = new VaultCustomQueryCriteria(Builder.avg(pennies));

                QueryCriteria criteria = sumCriteria.and(countCriteria).and(maxCriteria).and(minCriteria).and(avgCriteria);
                Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, criteria);

```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L339-L348' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample21' end='DOCEND VaultJavaQueryExample21' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)
Aggregations on cash grouped by currency for various functions:

```java
                Field pennies = CashSchemaV1.PersistentCashState.class.getDeclaredField("pennies");
                Field currency = CashSchemaV1.PersistentCashState.class.getDeclaredField("currency");

                QueryCriteria sumCriteria = new VaultCustomQueryCriteria(Builder.sum(pennies, Collections.singletonList(currency)));
                QueryCriteria countCriteria = new VaultCustomQueryCriteria(Builder.count(pennies));
                QueryCriteria maxCriteria = new VaultCustomQueryCriteria(Builder.max(pennies, Collections.singletonList(currency)));
                QueryCriteria minCriteria = new VaultCustomQueryCriteria(Builder.min(pennies, Collections.singletonList(currency)));
                QueryCriteria avgCriteria = new VaultCustomQueryCriteria(Builder.avg(pennies, Collections.singletonList(currency)));

                QueryCriteria criteria = sumCriteria.and(countCriteria).and(maxCriteria).and(minCriteria).and(avgCriteria);
                Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, criteria);

```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L387-L397' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample22' end='DOCEND VaultJavaQueryExample22' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)
Sum aggregation on cash grouped by issuer party and currency and sorted by sum:

```java
                Field pennies = CashSchemaV1.PersistentCashState.class.getDeclaredField("pennies");
                Field currency = CashSchemaV1.PersistentCashState.class.getDeclaredField("currency");
                Field issuerParty = CashSchemaV1.PersistentCashState.class.getDeclaredField("issuerParty");

                QueryCriteria sumCriteria = new VaultCustomQueryCriteria(Builder.sum(pennies, Arrays.asList(issuerParty, currency), Sort.Direction.DESC));

                Vault.Page<Cash.State> results = vaultService.queryBy(Cash.State.class, sumCriteria);

```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L458-L464' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample23' end='DOCEND VaultJavaQueryExample23' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)
Track unconsumed cash states:

```java
            @SuppressWarnings("unchecked")
            Set<Class<ContractState>> contractStateTypes = new HashSet(Collections.singletonList(Cash.State.class));

            VaultQueryCriteria criteria = new VaultQueryCriteria(Vault.StateStatus.UNCONSUMED, contractStateTypes);
            DataFeed<Vault.Page<ContractState>, Vault.Update<ContractState>> results = vaultService.trackBy(ContractState.class, criteria);

            Vault.Page<ContractState> snapshot = results.getSnapshot();
            Observable<Vault.Update<ContractState>> updates = results.getUpdates();


```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L259-L267' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample4' end='DOCEND VaultJavaQueryExample4' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)
Track unconsumed deal states or linear states (with snapshot including specification of paging and sorting by unique identifier):

```java
            @SuppressWarnings("unchecked")
            Set<Class<ContractState>> contractStateTypes = new HashSet(Collections.singletonList(Cash.State.class));

            VaultQueryCriteria criteria = new VaultQueryCriteria(Vault.StateStatus.UNCONSUMED, contractStateTypes);
            DataFeed<Vault.Page<ContractState>, Vault.Update<ContractState>> results = vaultService.trackBy(ContractState.class, criteria);

            Vault.Page<ContractState> snapshot = results.getSnapshot();
            Observable<Vault.Update<ContractState>> updates = results.getUpdates();


```
{{/* github src='node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' url='https://github.com/corda/corda/blob/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java#L259-L267' raw='https://raw.githubusercontent.com/corda/corda/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java' start='DOCSTART VaultJavaQueryExample4' end='DOCEND VaultJavaQueryExample4' */}}[VaultQueryJavaTests.java](https://github.com/corda/corda/blob/release/os/1.0/node/src/test/java/net/corda/node/services/vault/VaultQueryJavaTests.java)

## Troubleshooting

If the results your were expecting do not match actual returned query results we recommend you add an entry to your
`log4j2.xml` configuration file to enable display of executed SQL statements:

```kotlin
<Logger name="org.hibernate.SQL" level="debug" additivity="false">

    <AppenderRef ref="Console-Appender"/>

</Logger>
```


## Behavioural notes


* **TrackBy** updates do not take into account the full criteria specification due to different and more restrictive syntax
in [observables](https://github.com/ReactiveX/RxJava/wiki) filtering (vs full SQL-92 JDBC filtering as used in snapshot views).
Specifically, dynamic updates are filtered by `contractStateType` and `stateType` (UNCONSUMED, CONSUMED, ALL) only.
* **QueryBy** and **TrackBy snapshot views** using pagination may return different result sets as each paging request is a
separate SQL query on the underlying database, and it is entirely conceivable that state modifications are taking
place in between and/or in parallel to paging requests.
When using pagination, always check the value of the `totalStatesAvailable` (from the `Vault.Page` result) and
adjust further paging requests appropriately.


## Other use case scenarios

For advanced use cases that require sophisticated pagination, sorting, grouping, and aggregation functions, it is recommended that the CorDapp developer utilise one of the many proven frameworks that ship with this capability out of the box. Namely, implementations of JPQL (JPA Query Language) such as **Hibernate** for advanced SQL access, and **Spring Data** for advanced pagination and ordering constructs.

The Corda Tutorials provide examples satisfying these additional Use Cases:

> 
> > 
> > 
> > * Template / Tutorial CorDapp service using Vault API Custom Query to access attributes of IOU State
> > * Template / Tutorial CorDapp service query extension executing Named Queries via [JPQL](http://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#hql)
> > * [Advanced pagination](https://docs.spring.io/spring-data/commons/docs/current/api/org/springframework/data/repository/PagingAndSortingRepository.html) queries using Spring Data [JPA](https://docs.spring.io/spring-data/jpa/docs/current/reference/html)
> 
> 
> 
> 

