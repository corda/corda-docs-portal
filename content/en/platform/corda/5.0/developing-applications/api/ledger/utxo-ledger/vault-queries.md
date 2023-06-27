---
date: '2023-06-20'
version: 'Corda 5.0 Beta 4'
title: "Vault Queries"
menu:
  corda5:
    identifier: corda5-api-vault-queries
    parent: corda5-api-ledger-utxo
    weight: 3000
section_menu: corda5
---

# Vault Queries

## Vault Named Query

A vault named query is a database query that can be defined by Corda users. The user can define the following:

* The name of the query
* The query functionality (state type the query will work on and the `WHERE` clause)
* Optional filtering logic of the result set
* Optional transformation logic of the result set
* Optional collection logic of the result set
* The query creator needs to follow a few pre-defined steps in order for the query to be registered and to be usable.

## How a State is Represented in the Database

Each state type can be represented as a pre-defined JSON string (`custom_representation` column in the database). Use that JSON representation to write the vault-named queries. 

Implement the `net.corda.v5.ledger.utxo.query.json.ContractStateVaultJsonFactory<T>` interface. The `<T>` parameter is the type of the state we want to represent.

For example, a state type called `TestState` and a simple contract called `TestContract`, would look like the following:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}

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
{{% tab name="java" %}}

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

This contract has no verification logic and should only be used for testing purposes. The state itself has a `testField` property defined for JSON representation and constructing queries.

To represent a state as a JSON string, use `ContractStateVaultJsonFactory` as follows:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}

```kotlin
class TestStateJsonFactory : ContractStateVaultJsonFactory<TestState> {
    override fun getStateType(): Class<TestState> = TestState::class.java

    override fun create(state: TestState, jsonMarshallingService: JsonMarshallingService): String {
        return jsonMarshallingService.format(state)
    }
}
```
{{% /tab %}}
{{% tab name="java" %}}

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

After the output state has been finalized it will be represented as the following in the database (`custom_representation column`):

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
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
The `net.corda.v5.ledger.utxo.ContractState` field is a part of the JSON representation for all state types.
{{< /note >}}

Use this representation to create the vault named queries in the next section.

## How to Create and Register a Vault Named Query

Registration means the query is stored on sandbox creation time and can be executed later on.

Vault named queries need to be part of a contract CPK. The contract CPK needs to be uploaded in order for a vault named query to be installed.

To create and register a query the `net.corda.v5.ledger.utxo.query.VaultNamedQueryFactory` interface must be implemented.

### Basic Vault Named Query Registration Example

A simple vault named query implementation for this `TestState` would look like this:

{{< note >}}
This example has no filtering, mapping, or collecting logic.
{{< /note >}}

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}

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
{{% tab name="java" %}}


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

This function is called upon start-up and should define how a query will operate in it with the following steps:

* To create a vault named query with a given name, in this case it is `DUMMY_CUSTOM_QUERY`, call `vaultNamedQueryBuilderFactory.create()`.
* To define how a query's `WHERE` clause will work, call `whereJson()`.
  {{< note >}}
  Always start with the actual `WHERE` statement and then write the rest of the clause. Fields need to be prefixed with the `visible_states. qualifier`. Since `visible_states.custom_representation` is a JSON column, we can use some JSON specific  operations, more info here.
  * Parameters can be used in the query in a :parameter format. In this example, use a parameter called :testField which can be set when executing this query. This works similarly to popular Java SQL libraries such as Hibernate.
  {{< /note >}}
* To finalize query creation and to store the created query in the registry to be executed later, call `register()`. This call needs to be the last step when defining a query.

### Complex Query Example

 To add some extra logic to the query:

* Only keep the results that have “Alice” in their participant list.
* Transform the result set to only keep the transaction IDs.
* Collect the result set into one single integer.

These optional logics will always be applied in the following order:

1. Filtering
2. Transforming
3. Collecting

{{< note >}}
The query `whereJson` will return `StateAndRef` objects and the data going into the filtering and transforming logic consists of `StateAndRefs`.
{{< /note >}}

#### Filtering

To create a filtering logic implement the `net.corda.v5.ledger.utxo.query.VaultNamedQueryStateAndRefFilter<T>` interface. The `<T>` type here is the state type that will be returned from the database, in this case it’s `TestState`. This interface has only one function:

`@NotNull Boolean filter(@NotNull StateAndRef<T> data, @NotNull Map<String, Object> parameters);`

This will define whether or not to keep the given element (`row`) from the result set. Elements returning true will be kept and the rest will be discarded.

In this example, keep the elements that have “Alice” in their participant list. This filter would look like this:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}

```kotlin
class DummyCustomQueryFilter : VaultNamedQueryStateAndRefFilter<TestState> {
    override fun filter(data: StateAndRef<TestUtxoState>, parameters: MutableMap<String, Any>): Boolean {
        return data.state.contractState.participantNames.contains("Alice")
    }
}
```

{{% /tab %}}
{{% tab name="java" %}}

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

To create a transformer class make sure to only keep the transaction IDs of each record. Transformer classes need to implement the `VaultNamedQueryStateAndRefTransformer<T, R>` interface. The `<T>` is the type of results returned from the database, in this case `TestState` and `<R>` is the type to transform the results into and to have transaction IDs which are `Strings`.

This interface has one function:

```java
@NotNull`
`R transform(@NotNull T data, @NotNull Map<String, Object> parameters);
```

This defines how each record (“row”) will be transformed (mapped):

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}

```kotlin
class DummyCustomQueryTransformer : VaultNamedQueryStateAndRefTransformer<TestState, String> {
    override fun transform(data: StateAndRef<TestState>, parameters: MutableMap<String, Any>): String {
        return data.ref.transactionId.toString()
    }
}
```

{{% /tab %}}
{{% tab name="java" %}}

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

This transforms each element to a `String` object which is the given state’s transaction ID.

#### Collecting

Collecting is used to collect results set into one single integer.

For this, implement the `net.corda.v5.ledger.utxo.query.VaultNamedQueryCollector<R, T>` interface. The `<R>` parameter is the type of the original result set (in this case `String` because of transformation) and `<T>` is the type  collected into (in our case this is an `Int`).

This interface has only one method:

```java
@NotNull
Result<T> collect(@NotNull List<R> resultSet, @NotNull Map<String, Object> parameters);
```

This will define how to collect the result set, the collector class should look like the following:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}

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
{{% tab name="java" %}}

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
 The query `isDone` should only be set to true if the result set is complete.
{{< /note >}}

#### Registering our Complex Query

 Register a complex query with a filter, a transformer, and a collector with the following example:

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}

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
{{% tab name="java" %}}

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
The collector always needs to be the last one in the chain as all previous filtering and mapping functionality will be applied before collecting.
{{< /note >}}

### How to Execute a Vault Named Query

To execute a query use `UtxoLedgerService`. This can be injected to a flow via `@CordaInject`.
To instantiate a query call the following:

```kotlin
utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Int::class.java)
```

```java
utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class)
```

Provide the name of the query (in this case `DUMMY_CUSTOM_QUERY`) and the return type. Since the result set is collected into an integer in the complex query example use `Int` (or `Integer` in Java).

Before executing define the following:

* Which index the result set should start (`setOffset`), default 0.
* How many results should the query return (`setLimit`), default Int.MAX (2,147,483,647).
* Define named parameters that are in the query and the actual value for them. {{< note >}} All parameters must be defined otherwise the execution will fail. (`setParameter` or `setParameters`) {{</ note >}}
* Each state in the database has a timestamp value for when it was inserted. Set an * upper limit to only return states that were inserted before a given time. (`setTimestampLimit`)

    In this case it would look like this:

    {{< tabs name="tabs-7" >}}
    {{% tab name="kotlin" %}}

    ```kotlin
    val resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Int::class.java) // instantiate the query
                .setOffset(0) // Start from the beginning
                .setLimit(1000) // Only return 1000 records
                .setParameter("testField", "dummy") // Set the parameter to a dummy value
                .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
                .execute() // execute the query
    ```

    {{% /tab %}}
    {{% tab name="java" %}}

    ```java
    PagedQuery.ResultSet<Integer> resultSet = utxoLedgerService.query("DUMMY_CUSTOM_QUERY", Integer.class) // instantiate the query
                    .setOffset(0) // Start from the beginning
                    .setLimit(1000) // Only return 1000 records
                    .setParameter("testField", "dummy") // Set the parameter to a dummy value
                    .setCreatedTimestampLimit(Instant.now()) // Set the timestamp limit to the current time
                    .execute(); // execute the query
    ```

    {{% /tab %}}
    {{< /tabs >}}

{{< note >}} 
A dummy value is assigned for the `testField` parameter in this query but it can be replaced. There is only one parameter in this example query which is `:testField`.
{{</ note >}} 

Results can be acquired by calling `getResults()` on the `ResultSet`.
Paging can be achieved by increasing the offset until the result set has elements:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
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
{{% tab name="java" %}}
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

{{< tabs name="tabs-9" >}}
{{% tab name="kotlin" %}}
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
{{% tab name="java" %}}
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
