---
date: '2023-06-20'
description: "Learn how to query the Corda database using vault-named queries."
title: "Vault-Named Queries"
menu:
  corda52:
    identifier: corda52-api-vault-queries
    parent: corda52-api-ledger-utxo
    weight: 3000
---

# Vault-Named Queries

Vault-named queries enable you to query the Corda database. The user can define the following:

* The name of the query
* The query functionality (the type that the query works on and the `WHERE` clause)
* Optional filtering logic of the result set
* Optional transformation logic of the result set
* Optional collection logic of the result set

The query creator must follow pre-defined steps so that the query is registered and usable.

This section contains the following:

* [Representing a State in the Database](#representing-a-state-in-the-database)
* [Creating and Registering a Vault-Named Query](#creating-and-registering-a-vault-named-query)
* [Vault-Named Query Operators](#vault-named-query-operators)

## Representing a State in the Database

Each {{< tooltip >}}state{{< /tooltip >}} type can be represented as a pre-defined JSON string (`custom_representation` column in the database). Use this JSON representation to write the vault-named queries.
Implement the `net.corda.v5.ledger.utxo.query.json.ContractStateVaultJsonFactory<T>` interface. The `<T>` parameter is the type of the state that we want to represent.

For example, a state type called `TestState` and a simple contract called `TestContract`, would look like the following:

{{< tabs name="tabs-1" >}}
{{% tab name="Kotlin" %}}
```kotlin
package com.r3.corda.demo.contract
class TestContract : Contract {
    override fun verify(transaction: UtxoLedgerTransaction) {}
}
@BelongsToContract(TestContract::class)
class TestState(
    val testField: String,
    private val participants: List<PublicKey>
) : ContractState {
    override fun getParticipants(): List<PublicKey> = participants
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
package com.r3.corda.demo.contract;
class TestContract implements Contract {
    @Override
    public void verify(@NotNull UtxoLedgerTransaction transaction) {}
}
@BelongsToContract(TestContract.class)
public class TestState implements ContractState {
    private final List<PublicKey> participants;
    private final String testField;
    public TestState(@NotNull String testField, @NotNull List<PublicKey> participants) {
        this.testField = testField;
        this.participants = participants;
    }
    @NotNull
    @Override
    public List<PublicKey> getParticipants() {
        return new LinkedList<>(this.participants);
    }
    @NotNull
    public String getTestField() {
        return testField;
    }
}
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
This contract has no verification logic and should only be used for testing purposes. The state itself has a `testField` property defined for JSON representation and constructing queries.
{{</ note >}}

To represent a state as a JSON string, use `ContractStateVaultJsonFactory` as follows:

{{< tabs name="tabs-2" >}}
{{% tab name="Kotlin" %}}
```kotlin
class TestStateJsonFactory : ContractStateVaultJsonFactory<TestState> {
    override fun getStateType(): Class<TestState> = TestState::class.java
    override fun create(state: TestState, jsonMarshallingService: JsonMarshallingService): String {
        return jsonMarshallingService.format(state)
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
class TestUtxoStateJsonFactory implements ContractStateVaultJsonFactory<TestUtxoState> {
    @NotNull
    @Override
    public Class<TestUtxoState> getStateType() {
        return TestUtxoState.class;
    }
    @Override
    @NotNull
    public String create(@NotNull TestUtxoState state, @NotNull JsonMarshallingService jsonMarshallingService) {
        return jsonMarshallingService.format(state);
    }
}
```
{{% /tab %}}
{{< /tabs >}}

After the output state finalizes, it is represented as the following in the database (`custom_representation` column)
with a `stateRef` field stored under the `ContractState` JSON object:

```json
{
  "net.corda.v5.ledger.utxo.ContractState" : {
    "stateRef": "<TransactionID>:<StateIndex>"
  },
  "com.r3.corda.demo.contract.TestState" : {
    "testField": ""
  }
}
```

{{< note >}}

* The `net.corda.v5.ledger.utxo.ContractState` field is a part of the JSON representation for all state types.
* The implementation of the JSON factory must be defined in the same CPK as the state that it is working on, so that the platform can get hold of it when persisting a state to the database.
{{< /note >}}

Use this representation to create the vault-named queries in the next section.

## Creating and Registering a Vault-Named Query

Registration means that the query is stored on {{< tooltip >}}sandbox{{< /tooltip >}} creation time and can be executed later.
Vault-named queries must be part of a contract CPK. Corda installs the vault-named query when the contract CPK is uploaded.
To create and register a query, the `net.corda.v5.ledger.utxo.query.VaultNamedQueryFactory` interface must be implemented.

### Basic Vault-Named Query Registration Example

A simple vault-named query implementation for this `TestState` would look like this:

{{< note >}}
This example has no filtering, mapping, or collecting logic.
{{< /note >}}

{{< tabs name="tabs-3" >}}
{{% tab name="Kotlin" %}}
```kotlin
class DummyCustomQueryFactory : VaultNamedQueryFactory {
    override fun create(vaultNamedQueryBuilderFactory: VaultNamedQueryBuilderFactory) {
        vaultNamedQueryBuilderFactory.create("DUMMY_CUSTOM_QUERY")
            .whereJson(
                "WHERE visible_states.custom_representation -> 'com.r3.corda.demo.contract.TestState' " +
                        "->> 'testField' = :testField"
            )
            .register()
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
public class DummyCustomQueryFactory implements VaultNamedQueryFactory {
    @Override
    public void create(@NotNull VaultNamedQueryBuilderFactory vaultNamedQueryBuilderFactory) {
        vaultNamedQueryBuilderFactory.create("DUMMY_CUSTOM_QUERY")
                .whereJson(
                        "WHERE visible_states.custom_representation -> 'com.r3.corda.demo.contract.TestState' " +
                                "->> 'testField' = :testField"
                )
                .register();
    }
}
```
{{% /tab %}}
{{< /tabs >}}

The interface called `VaultNamesQueryFactory` has one method:
`void create(@NotNull VaultNamedQueryBuilderFactory vaultNamedQueryBuilderFactory);`.

This function is called during start-up and it defines how a query operates in it with the following steps:

* To create a vault-named query with a given name, in this case it is `DUMMY_CUSTOM_QUERY`, call `vaultNamedQueryBuilderFactory.create()`.
* To define how a query's `WHERE` clause will work, call `whereJson()`.
  {{< note >}}
  * Always start with the actual `WHERE` statement and then write the rest of the clause. You must prefix fields with the `visible_states.` qualifier. Since `visible_states.custom_representation` is a JSON column, you can use some JSON-specific operations.
  * Parameters can be used in the query in a `:parameter` format. In this example, use a parameter called `:testField` which can be set when executing this query. This works similarly to popular Java SQL libraries such as Hibernate.
  {{< /note >}}

* To finalize query creation and to store the created query in the registry to be executed later, call `register()`. This call must be the last step when defining a query.

### Complex Query Example

For example, to add some extra logic to the query:

* Only keep the results that have “Alice” in their participant list.
* Transform the result set to only keep the {{< tooltip >}}transaction{{< /tooltip >}} IDs.
* Collect the result set into one single integer.

These optional logics are always applied in the following order:

1. [Filtering](#filtering)
2. [Transforming](#transforming)
3. [Collecting](#collecting)

{{< note >}}
The query `whereJson` returns `StateAndRef` objects and the data going into the filtering and transforming logic consists of `StateAndRefs`.
{{< /note >}}

#### Filtering

To create a filtering logic, implement the `net.corda.v5.ledger.utxo.query.VaultNamedQueryStateAndRefFilter<T>` interface. The `<T>` type here is the state type that will be returned from the database, which in this case is `TestState`. This interface has only one function.
This defines whether or not to keep the given element (`row`) from the result set. Elements returning true are kept and the rest are discarded.

In this example, keep the elements that have “Alice” in their participant list:
{{< tabs name="tabs-4" >}}
{{% tab name="Kotlin" %}}
```kotlin
class DummyCustomQueryFilter : VaultNamedQueryStateAndRefFilter<TestState> {
    override fun filter(data: StateAndRef<TestUtxoState>, parameters: MutableMap<String, Any>): Boolean {
        return data.state.contractState.participantNames.contains("Alice")
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
class DummyCustomQueryFilter implements VaultNamedQueryStateAndRefFilter<TestUtxoState> {
    @NotNull
    @Override
    public Boolean filter(@NotNull StateAndRef<TestUtxoState> data, @NotNull Map<String, Object> parameters) {
        return data.getState().getContractState().getParticipantNames().contains("Alice");
    }
}
```
{{% /tab %}}
{{< /tabs >}}

#### Transforming

To create a transformer class, only keep the transaction IDs of each record. Transformer classes must implement the `VaultNamedQueryStateAndRefTransformer<T, R>` interface, where:

* `<T>` is the type of results returned from the database, which in this case is `TestState`.
* `<R>` is the type to transform the results into.
* Transaction IDs are specified as `Strings`.

This interface has one function:

```java
@NotNull`
`R transform(@NotNull T data, @NotNull Map<String, Object> parameters);
```

This defines how each record (“row”) will be transformed (mapped):

{{< tabs name="tabs-5" >}}
{{% tab name="Kotlin" %}}
```kotlin
class DummyCustomQueryTransformer : VaultNamedQueryStateAndRefTransformer<TestState, String> {
    override fun transform(data: StateAndRef<TestState>, parameters: MutableMap<String, Any>): String {
        return data.ref.transactionId.toString()
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
class DummyCustomQueryMapper implements VaultNamedQueryStateAndRefTransformer<TestUtxoState, String> {
    @NotNull
    @Override
    public String transform(@NotNull StateAndRef<TestUtxoState> data, @NotNull Map<String, Object> parameters) {
        return data.getRef().getTransactionId().toString();
    }
}
```
{{% /tab %}}
{{< /tabs >}}
This transforms each element to a `String` object, which is the given state’s transaction ID.

#### Collecting

Collecting is used to collect results set into one single integer.
For this, implement the `net.corda.v5.ledger.utxo.query.VaultNamedQueryCollector<R, T>` interface, where:

* `<T>` is the type collected into (in this case, an `Int`).
* `<R>` is the type of the original result set (in this case `String` because of transformation).

This interface has only one method:

```java
@NotNull
Result<T> collect(@NotNull List<R> resultSet, @NotNull Map<String, Object> parameters);
```
This defines how to collect the result set. The collector class should look like the following:
{{< tabs name="tabs-6" >}}
{{% tab name="Kotlin" %}}
```kotlin
class DummyCustomQueryCollector : VaultNamedQueryCollector<String, Int> {
    override fun collect(
        resultSet: MutableList<String>,
        parameters: MutableMap<String, Any>
    ): VaultNamedQueryCollector.Result<Int> {
        return VaultNamedQueryCollector.Result(
            listOf(resultSet.size),
            true
        )
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
class DummyCustomQueryCollector implements VaultNamedQueryCollector<String, Integer> {
    @NotNull
    @Override
    public Result<Integer> collect(@NotNull List<String> resultSet, @NotNull Map<String, Object> parameters) {
        return new Result<>(
                List.of(resultSet.size()),
                true
        );
    }
}
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
The query `isDone` should only be set to `true` if the result set is complete.
{{< /note >}}

#### Registering a Complex Query

Register a complex query with a filter, a transformer, and a collector with the following example:
{{< tabs name="tabs-7" >}}
{{% tab name="Kotlin" %}}
```kotlin
class DummyCustomQueryFactory : VaultNamedQueryFactory {
    override fun create(vaultNamedQueryBuilderFactory: VaultNamedQueryBuilderFactory) {
        vaultNamedQueryBuilderFactory.create("DUMMY_CUSTOM_QUERY")
            .whereJson(
                "WHERE visible_states.custom_representation -> 'com.r3.corda.demo.contract.TestState' " +
                        "->> 'testField' = :testField"
            )
            .filter(DummyCustomQueryFilter())
            .map(DummyCustomQueryMapper())
            .collect(DummyCustomQueryCollector())
            .register()
    }
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
public class JsonQueryFactory implements VaultNamedQueryFactory {
    @Override
    public void create(@NotNull VaultNamedQueryBuilderFactory vaultNamedQueryBuilderFactory) {
        vaultNamedQueryBuilderFactory.create("DUMMY_CUSTOM_QUERY")
                .whereJson(
                        "WHERE visible_states.custom_representation -> 'com.r3.corda.demo.contract.TestState' " +
                                "->> 'testField' = :testField"
                )
                .filter(new DummyCustomQueryFilter())
                .map(new DummyCustomQueryMapper())
                .collect(new DummyCustomQueryCollector())
                .register();
    }
}
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
The collector must always be the last one in the chain as all previous filtering and mapping functionality is applied before collecting.
{{< /note >}}

### Executing a Vault-Named Query

To execute a query use `UtxoLedgerService`. This can be injected to a {{< tooltip >}}flow{{< /tooltip >}} via `@CordaInject`.
To instantiate a query call the following:

{{< tabs name="tabs-8" >}}
{{% tab name="Kotlin" %}}
```kotlin
utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Int::class.java)
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class)
```
{{% /tab %}}
{{< /tabs >}}

Provide the name of the query (in this case `DUMMY_CUSTOM_QUERY`) and the return type. Since the result set is collected into an integer in the complex query example, use `Int` (or `Integer` in Java).
Before executing, define the following:

* How many results each page of the query should return (`setLimit`). The default value is `Int.MAX` (2,147,483,647).
* Named parameters that are in the query and the actual value for them (`setParameter` or `setParameters`). All parameters must be defined, otherwise the execution will fail.
* An upper limit (`setTimestampLimit`) to only return states that were inserted before a given time. Each state in the database has a timestamp value for when it was inserted.

It is not necessary to call `ParameterizedQuery.setOffset` as the query pages the results based on each state's created timestamp.

In this case it would look like this:
{{< tabs name="tabs-9" >}}
{{% tab name="Kotlin" %}}
```kotlin
val resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Int::class.java) // Instantiate the query
            .setLimit(1000) // Only return 1000 records per page
            .setParameter("testField", "dummy") // Set the parameter to a dummy value
            .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
            .execute() // execute the query
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
PagedQuery.ResultSet<Integer> resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class) // Instantiate the query
                .setLimit(1000) // Only return 1000 records per page
                .setParameter("testField", "dummy") // Set the parameter to a dummy value
                .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
                .execute(); // execute the query
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
A dummy value is assigned for the `testField` parameter in this query, but it can be replaced. There is only one parameter in this example query: `:testField`.
{{</ note >}}

Results can be acquired by calling `getResults()` on the `ResultSet`.  Call `hasNext()` to check if there are more results to retrieve and `next()` to move onto the next page:

{{< tabs name="tabs-11" >}}
{{% tab name="Kotlin" %}}
```kotlin
val resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Int::class.java) // Instantiate the query
            .setLimit(1000) // Only return 1000 records
            .setParameter("testField", "dummy") // Set the parameter to a dummy value
            .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
            .execute()
var results = resultSet.results
while (resultSet.hasNext()) {
    results = resultSet.next()
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
ResultSet<Integer> resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class) // Instantiate the query
                .setLimit(1000) // Only return 1000 records
                .setParameter("testField", "dummy") // Set the parameter to a dummy value
                .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
                .execute();
List<Integer> results = resultSet.getResults();
while (resultSet.hasNext()) {
    results = resultSet.next();
}
```
{{% /tab %}}
{{< /tabs >}}

## Vault-Named Query Operators

The following are the standard operators for vault-named queries:

* `IN`
* `LIKE`
* `IS NOT NULL`
* `IS NULL`
* `AS`
* `OR`
* `AND`
* `!=`
* `>`
* `<`
* `>=`
* `<=`
* `->`
* `->>`
* `?`
* `::`

Where the behavior is not standard, the operators are explained with examples in the following table:

<style>
table th:first-of-type {
    width: 15%;
}
table th:nth-of-type(2) {
    width: 15%;
}
table th:nth-of-type(3) {
    width: 15%;
}
table th:nth-of-type(4) {
    width: 55%;
}
</style>

<table>
<thead>
<tr>
<th>Operator</th>
<th>Right Operand Type</th>
<th>Description</th>
<th>Example</th>
</tr>
</thead>
<tbody>
<tr>
<td>-></td>
<td>Int</td>
<td>Gets JSON array element.</td>
<td><code>custom_representation -&gt; &#39;com.r3.corda.demo.ArrayObjState&#39; -&gt; 0</code><br>For example, for the following JSON:

```json
{
  "com.r3.corda.demo.ArrayObjState": [
    {"A": 1},
    {"B": 2}
  ]
}
```
the following is returned:
```json
{
  "A": 1
}
```

</td>
</tr>
<tr>
<td>-></td>
<td>Text</td>
<td>Gets JSON object field. </td>
<td><code>custom_representation -> 'com.r3.corda.demo.TestState'</code> selects the top-level JSON field called <code>com.r3.corda.demo.TestState</code> from the JSON object in the <code>custom_representation</code> database column.<br>For example, for the following JSON:

```json
{
  "com.r3.corda.demo.TestState": {
    "testField": "ABC"
  }
}
```
the following is returned:
```json
{
  "testField": "ABC"
}
```

</td>
</tr>
<tr>
<td>->></td>
<td>Int</td>
<td>Get JSON array element as text.  </td>
<td><code>custom_representation -> 'com.r3.corda.demo.ArrayState' ->> 2</code> selects the third element (indexing from 0) of the array type top-level JSON field called <code>com.r3.corda.demo.ArrayState</code> from the JSON object in the <code>custom_representation</code> database column. <br>For example, <code>7</code> is returned for the following JSON:

```json
{
  "com.r3.corda.demo.ArrayState": [
    5, 6, 7
  ]
}
```

</td>
</tr>
<tr>
<td>->></td>
<td>Text</td>
<td>Get JSON object field as text. </td>
<td><code>custom_representation -> 'com.r3.corda.demo.TestState' ->> 'testField'</code> selects  the `testField` JSON field from the top-level JSON object called <code>com.r3.corda.demo.TestState</code> in the <code>custom_representation</code> database column.<br>For example, <code>ABC</code> is returned for the following JSON:

```json
{
  "com.r3.corda.demo.TestState": {
    "testField": "ABC"
  }
}
```

</td>
</tr>
<tr>
<td>?</td>
<td>Text</td>
<td> Checks if JSON object field exists.</td>
<td><code>custom_representation ? 'com.r3.corda.demo.TestState'</code> checks if the object in the <code>custom_representation database</code>  column has a top-level field called <code>com.r3.corda.demo.TestState</code>.<br>For example, <code>true</code> is returned for the following JSON:

```json
{
  "com.r3.corda.demo.TestState": {
    "testField": "ABC"
  }
}
```

</td>
</tr>
<tr>
<td>::</td>
<td>A type, for example, Int.</td>
<td>Casts the element/object field to the specified type.</td>
<td><code>(visible_states.field ->> property)::int = 1234</code>

</td>
</tr>
</tbody>
</table>
