---
date: '2023-08-10'
version: 'Corda 5.1'
title: "Vault-Named Queries"
menu:
  corda51:
    identifier: corda51-api-vault-queries
    parent: corda51-api-ledger-utxo
    weight: 3000
section_menu: corda51
---

# Vault-Named Queries

A vault-named query is a database query that can be defined by Corda users. The user can define the following:

* The name of the query
* The query functionality (state the type that the query will work on and the `WHERE` clause)
* Optional filtering logic of the result set
* Optional transformation logic of the result set
* Optional collection logic of the result set

 The query creator must follow a few pre-defined steps so that the query is registered and usable.

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

After the output state finalizes, it is represented as the following in the database (`custom_representation column`)
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

`void create(@NotNull VaultNamedQueryBuilderFactory vaultNamedQueryBuilderFactory);`

This function is called during start-up and it defines how a query will operate in it with the following steps:

* To create a vault-named query with a given name, in this case it is `DUMMY_CUSTOM_QUERY`, call `vaultNamedQueryBuilderFactory.create()`.
* To define how a query's `WHERE` clause will work, call `whereJson()`.
  {{< note >}}
  Always start with the actual `WHERE` statement and then write the rest of the clause. Fields need to be prefixed with the `visible_states.` qualifier. Since `visible_states.custom_representation` is a JSON column, we can use some JSON specific  operations.
  * Parameters can be used in the query in a `:parameter` format. In this example, use a parameter called `:testField` which can be set when executing this query. This works similarly to popular Java SQL libraries such as Hibernate.
  {{< /note >}}
* To finalize query creation and to store the created query in the registry to be executed later, call `register()`. This call must be the last step when defining a query.

### Complex Query Example

 To add some extra logic to the query:

* Only keep the results that have “Alice” in their participant list.
* Transform the result set to only keep the {{< tooltip >}}transaction{{< /tooltip >}} IDs.
* Collect the result set into one single integer.

These optional logics will always be applied in the following order:

1. Filtering
2. Transforming
3. Collecting

{{< note >}}
The query `whereJson` returns `StateAndRef` objects and the data going into the filtering and transforming logic consists of `StateAndRefs`.
{{< /note >}}

#### Filtering

To create a filtering logic, implement the `net.corda.v5.ledger.utxo.query.VaultNamedQueryStateAndRefFilter<T>` interface. The `<T>` type here is the state type that will be returned from the database, which in this case is `TestState`. This interface has only one function:


This defines whether or not to keep the given element (`row`) from the result set. Elements returning true are kept and the rest are discarded.

In this example, keep the elements that have “Alice” in their participant list. This filter would look like this:

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

To create a transformer class, make sure to only keep the transaction IDs of each record. Transformer classes must implement the `VaultNamedQueryStateAndRefTransformer<T, R>` interface. The `<T>` is the type of results returned from the database, which in this case is `TestState`, `<R>` is the type to transform the results into, and transaction IDs should be `Strings`.

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

For this, implement the `net.corda.v5.ledger.utxo.query.VaultNamedQueryCollector<R, T>` interface. The `<R>` parameter is the type of the original result set (in this case `String` because of transformation) and `<T>` is the type collected into (in this can an `Int`).

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
 The query `isDone` should only be set to 'true' if the result set is complete.
{{< /note >}}

#### Registering our Complex Query

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
The collector always must be the last one in the chain as all previous filtering and mapping functionality is applied before collecting.
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

* Which index the result set should start (`setOffset`), default 0.
* How many results should the query return (`setLimit`), default Int.MAX (2,147,483,647).
* Define named parameters that are in the query and the actual value for them. {{< note >}} All parameters must be defined, otherwise the execution will fail. (`setParameter` or `setParameters`) {{</ note >}}
* Each state in the database has a timestamp value for when it was inserted. Set an * upper limit to only return states that were inserted before a given time. (`setTimestampLimit`)

In this case it would look like this:

{{< tabs name="tabs-9" >}}
{{% tab name="Kotlin" %}}

```kotlin
    val resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Int::class.java) // Instantiate the query
                .setOffset(0) // Start from the beginning
                .setLimit(1000) // Only return 1000 records
                .setParameter("testField", "dummy") // Set the parameter to a dummy value
                .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
                .execute() // execute the query
```

{{% /tab %}}
{{% tab name="Java" %}}

```java
    PagedQuery.ResultSet<Integer> resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class) // Instantiate the query
                    .setOffset(0) // Start from the beginning
                    .setLimit(1000) // Only return 1000 records
                    .setParameter("testField", "dummy") // Set the parameter to a dummy value
                    .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
                    .execute(); // execute the query
```

{{% /tab %}}
{{< /tabs >}}

{{< note >}}
A dummy value is assigned for the `testField` parameter in this query, but it can be replaced. There is only one parameter in this example query which is `:testField`.
{{</ note >}}

Results can be acquired by calling `getResults()` on the `ResultSet`.
Paging can be achieved by increasing the offset until the result set has elements:

{{< tabs name="tabs-10" >}}
{{% tab name="Kotlin" %}}
```kotlin
var currentOffset = 0;

val resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class) // instantiate the query
                .setOffset(0) // Start from the beginning
                .setLimit(1000) // Only return 1000 records
                .setParameter("testField", "dummy") // Set the parameter to a dummy value
                .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
                .execute()

while (resultSet.results.isNotEmpty()) {
    currentOffset += 1000
    query.setOffset(currentOffset)
    resultSet = query.execute()
}
```
{{% /tab %}}
{{% tab name="Java" %}}
```java
int currentOffset = 0;

ResultSet<Integer> resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class) // instantiate the query
                .setOffset(0) // Start from the beginning
                .setLimit(1000) // Only return 1000 records
                .setParameter("testField", "dummy") // Set the parameter to a dummy value
                .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
                .execute();

while (resultSet.results.isNotEmpty()) {
    currentOffset += 1000;
    query.setOffset(currentOffset);
    resultSet = query.execute();
}
```

{{% /tab %}}
{{< /tabs >}}

Or just calling the `hasNext()` and `next()` functionality:

{{< tabs name="tabs-11" >}}
{{% tab name="Kotlin" %}}
```kotlin
val resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class) // instantiate the query
                .setOffset(0) // Start from the beginning
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
ResultSet<Integer> resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class) // instantiate the query
                .setOffset(0) // Start from the beginning
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

# Vault-Named Query Operators

The following is the list of the standard operators for the vault-named query syntax:

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

Where the behaviour is not standard, the operators are explained in detail in the following sections.

**Name:** `->`

**Right Operand Type:** `Int`

**Description:**  Gets JSON array element.

**Example:**

`custom_representation`
`->`
`com.r3.corda.demo.ArrayObjState`
`->`
`0`

Example JSON:

```java

{
  "com.r3.corda.demo.ArrayObjState": [
    {"A": 1},
    {"B": 2}
  ]
}
```

This example returns:

```java
{
  "A": 1
}
```

**Name:** `->`

**Right Operand Type:** </b> `Text`

**Description:** Get JSON object field.

**Example:**

`custom_representation`
`-> 'com.r3.corda.demo.TestState'`

Selects the top-level JSON field called `com.r3.corda.demo.TestState` from the JSON object in the `custom_representation` database column.

Example JSON:

```java
{
  "com.r3.corda.demo.TestState": {
    "testField": "ABC"
  }
}
```

This example returns:

```java
{
  "testField": "ABC"
}

```

**Name:** `->>`

**Right Operand Type:** `Int`

**Description:** Get JSON array element as text.

**Example:**

`custom_representation`
`-> 'com.r3.corda.demo.ArrayState'`
`->> 2`

Selects the third element (indexing from 0)  of the array type top-level JSON field called `com.r3.corda.demo.ArrayState` from the JSON object in the `custom_representation` database column.

Example JSON:

```java

{
  "com.r3.corda.demo.ArrayState": [
    5, 6, 7
  ]
}

```

This example returns: `7`.

**Name:** `->>`

**Right Operand Type:** `Text`

**Description:** Get JSON object field as text.

**Example:**

`custom_representation`
`-> 'com.r3.corda.demo.TestState'`
`->> 'testField'`

Selects the `testField` JSON field from the top-level JSON object called `com.r3.corda.demo.TestState` in the `custom_representation` database column.

Example JSON:

```java
{
  "com.r3.corda.demo.TestState": {
    "testField": "ABC"
  }
}
```

This example returns: `ABC`.

**Name:** `?`

**Right Operand Type:** `Text`

**Description:** Checks if JSON object field exists.

**Example:**

`custom_representation ?`
`'com.r3.corda.demo.TestState'`

Checks if the object in the `custom_representation` database column has a top-level field called `com.r3.corda.demo.TestState`.

Example JSON:

```java
{
  "com.r3.corda.demo.TestState": {
    "testField": "ABC"
  }
}

```

This example returns: `true`.

**Name:** `::`

**Right Operand Type:** A type, for example, `Int`

**Description:** Casts the element/object field to the specified type.

**Example:**

`(visible_states.field ->> property)::int = 1234`
