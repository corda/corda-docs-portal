---
date: '2021-09-23'
title: HTTP-RPC Named Query API
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-persistence
    identifier: corda-5-dev-preview-1-cordapps-persistence-http
    weight: 1500
section_menu: corda-5-dev-preview
expiryDate: '2022-09-28'
---

In the Corda 5 Developer Preview, the [Query API](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.md) is exposed as part of the HTTP-RPC Persistence API. It
allows you to invoke named-queries via HTTP requests and receive results marshalled to JSON.

You can invoke the HTTP Named Query API by sending an HTTP `POST` request to the
`https://{host}:{port}/persistence/query` endpoint. The request requires a body payload containing a
`RpcNamedQueryRequest` and a `DurableStreamContext`.

You can use the native [HTTP-RPC Client](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/http-rpc-client.md) `HttpRpcClient` to instantiate a durable stream and poll for results.

You can also manually invoke the API via a `curl` request or using Swagger UI.

To generate your own client capable of calling this API, see [generating client code](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/generate-code/generate-code.md).

## Overview of the Query API

The HTTP-RPC Named Query API creates a durable cursor object capable of polling for batches of results.

Each poll will:
* Execute a pre-defined named query with the given named parameters.
* Execute additional post-processing to transform entities/results into JSON serializable objects.
* Return a batch of `RpcNamedQueryResponseItem`s containing the JSON results.

## `PersistenceRPCOps`

The definition of the `PersistenceRPCOps` is:

```kotlin
@HttpRpcResource(
    name = "PersistenceRPCOps",
    description = "Persistence APIs",
    path = "persistence"
)
interface PersistenceRPCOps : RPCOps {
    @HttpRpcPOST(description = "Execute a pre-defined named query")
    fun query(
        @HttpRpcRequestBodyParameter(
            description = "Request object containing information to execute a pre-defined named query",
            required = true
        ) request: RpcNamedQueryRequest
    ): DurableCursorBuilder<RpcNamedQueryResponseItem>
}
```

## `RpcNamedQueryRequest`

The endpoint expects a body parameter object `RpcNamedQueryRequest` which has the definition:

```kotlin
data class RpcNamedQueryRequest internal constructor(
    val queryName: String,
    val namedParameters: Map<String, RpcNamedQueryParameterJson>,
    val postProcessorName: String?
)
```
`RpcNamedQueryRequest` includes:

* `queryName` which is the name of a pre-defined named query.
* `namedParameters` which is a map of named parameters to be set on the named query:
  * Key: name of named-parameter.
  * Value: `RpcNamedQueryParameterJson` object which contains the JSON marshalled representation of the named-parameter value.
  Corda detects the type of the named parameter set on the named-query and unmarshalls the JSON value to that type.
* `postProcessorName` which is the name of a pre-defined post-processor used to transform named query results into JSON serializable objects.
  * A post-processor must be used to convert entities to JSON serializable objects. See [when to use a post-processor](#use-a-post-processor).

Post-processor implementations must override `availableForRpc` and set this flag to `true` to be usable from the HTTP Named Query API.

Clients can use the `RpcNamedQueryRequestBuilder` to build the request.

For more information on the Query API, see:
- [How to create your own named queries](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#create-your-own-named-queries).
- [How to implement your own post-processor](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#implementing-your-own-post-processor).
- [How to use post processors](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#using-post-processors).

## `DurableCursorBuilder<RpcNamedQueryResponseItem>`

The HTTP Named Query API creates a [durable stream](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/durable-streams/durable-streams-homepage.md) which allows polling for named query results.

Each poll executes the given named-query with the provided request in the context of a `DurableStreamContext`. This context contains the start position, max number of results and a timeout and is used to control the paging positions to page through the results. When using the `HttpRpcClient`, this is encapsulated in the `DurableCursor` object that is built and hidden from the user. Otherwise, the context is required for each poll request.

Each poll response contains a batch of results. Each result item is wrapped in a `RpcNamedQueryResponseItem` containing the JSON representation of the item. The user is responsible for unmarshalling these items.

## Use a post-processor

The `postProcessorName` parameter is optional, but in most scenarios you will need one.

These are examples when you won't need a `postProcessorName` parameter:
- Your named-query returns a simple basic type (such as, when using an aggregate function or selecting a simple field).
- You use constructor expressions in the named query to create a JSON serializable object.
- Your named-query returns an entity with only simple types and is JSON serializable.
- Your named-query returns an entity that implements `JsonRepresentable`.

You will need to provide a post-processor when:
- You want to return custom states.
  - If your state implements `JsonRepresentable`, you can use the `"Corda.IdentityContractStatePostProcessor"`.
  - Otherwise, you will have to implement your own `StateAndRefPostProcessor`.
- You want to return `StateAndRefs` (implement `StateAndRefPostProcessor` and create a serializable POJO).
- You have large entities which need to be transformed into smaller objects for transmission.
- You get a serialization exception when trying to return entities from the HTTP API.

{{< table >}}

| Example named-query         | Returns     | User wants | Post-processor? |
|--------------|-----------|------------|----------------|
| `"ShoppingCart.sumTotalItemsCostByCartId"` | `Long`      | The `Long` result. | Not needed, as `Long` will serialize to JSON.         |
| `"VaultState.findByStateStatus"` | `VaultState` entities | `CustomState`s | An implementation of `StateAndRefPostProcessor` to convert the `CustomStates` into JSON serializable objects. |
| `"PersistentPet.findUnconsumedByName"` | `PersistentPet` entities | `PetStatePojo`s | The [PetStatePostProcessor](#petstatepostprocessor). |

{{< /table >}}

The named-query `"VaultState.findByStateStatus"` quite literally queries for `VaultState` entities. To obtain actual state data, you must use a post-processor that implements `StateAndRefPostProcessor`.

For more details see [how to use post-processors](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#using-post-processors). The [CustomStatePostProcessor](../../../../../../en/platform/corda/5.0-dev-preview-1/cordapps/persistence/query-api.html#using-post-processors) is an example which converts `StateAndRef`s containing `CustomState`s to `PostProcessedObject` POJOs which can be easily serialized to JSON. Since this particular named query is quite generic, it is possible that some states are not of type `CustomState`, hence why the additional type filtering is required in the post-processor.

## Call the API from Swagger UI

Since the HTTP Named Query API creates a durable stream, requests require a `DurableStreamContext` which provide positional information, page size and timeout durations. It is defined as:

```kotlin
@CordaSerializable
data class DurableStreamContext(val currentPosition: Long, val maxCount: Int, val awaitForResultTimeout: Duration)
```

This can be provided in the request along with the `RpcNamedQueryRequest`. In this example:
- Fetch results with starting position (exclusive) `-1` (to start from the beginning).
- Poll for a maximum of `100` results.
- With a timeout duration of 1 hour 30 minutes.

```json
  "context": {
    "awaitForResultTimeout": "PT1H30M",
    "currentPosition": -1,
    "maxCount": 100
  }
```

### Example polling from Swagger UI

This request executes the named-query `VaultState.findByStateStatusAndContractStateClassName`.
- It sets the named parameters `stateStatus` and `contractStateClassName` to find unconsumed `PersistentPet` entities.
- It uses the `"linearstate-sample.PetStatePostProcessor"` to convert `PersistentPet` entities into serializable `PetStatePojos`.
- It sets the durable stream context to have a timeout of 15 minutes, start at position `-1` (exclusive) and fetch a max of `10` results.

```json
{
  "request": {
    "namedParameters": {
      "stateStatus": {
        "parametersInJson": "\"UNCONSUMED\""
      },
      "contractStateClassName": {
        "parametersInJson": "\"net.corda.linearstatesample.schema.PetSchemaV1$PersistentPet\""
      }
    },
    "queryName": "VaultState.findByStateStatusAndContractStateClassName",
    "postProcessorName": "linearstate-sample.PetStatePostProcessor"
  },
  "context": {
    "awaitForResultTimeout": "PT15M",
    "currentPosition": -1,
    "maxCount": 10
  }
}
```

Here is a sample response:

```json
{
  "positionedValues": [
    {
      "value": {
        "json": "{\"name\":\"Tim the Cat\",\"initiatorId\":\"sample\",\"owner\":\"O\\u003dPartyA, L\\u003dParis, C\\u003dFR\", \"linearId\": \"971e60f5-eb22-4ac6-990e-0ccdb68f6b2e\"}"
      },
      "position": 1
    },
    {
      "value": {
        "json": "{\"name\":\"Roger the Dog\",\"initiatorId\":\"sample\",\"owner\":\"O\\u003dPartyA, L\\u003dParis, C\\u003dFR\", \"linearId\": \"231a60f5-cb82-4ac6-990e-0ccdb68f6b2e\"}"
      },
      "position": 1
    },
  "remainingElementsCountEstimate": null
}
```


When using non-sequentially ordered queries, "position" will be (start count + number of results) for all items.

## Sequential queries

The HTTP Named Query API supports durable streams and the `PersistenceRPCOps.query` function returns a `DurableCursorBuilder`.

Some clients may require an infinite stream of sequentially ordered entities which are reliable with no data loss, and pick up new entities when they are added.

You can create named-queries for your entities which apply an ordering on a timestamp or sequential numbering in ascending order.

The Corda 5 Developer Preview provides some pre-built sequential named queries that guarantee sequential ordering of states and can be used for infinite durable streaming.

{{< table >}}

| Query name                                                              | Named Parameters                     |
|-------------------------------------------------------------------------|--------------------------------------|
| `VaultStateEvent.sequential.findByStateStatus`                          | `stateStatus`                        |
| `VaultStateEvent.sequential.findByStateStatusAndContractStateClassNameIn` | `stateStatus`, `contractStateClassNames` |

{{< /table >}}

These queries are compatible with custom post-processors which convert states into serializable POJOs (while preserving the original sequential state order).

## Call the API using the HTTP-RPC Client

These examples use the Corda 5 Developer Preview implementation of [HTTP-RPC Client](../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/durable-streams/java-client/java-client.md) (`HttpRpcClient`).

See [appendix](#appendix) for additional classes used in the examples, such as post-processors and simple POJOs.

### Example 1 - Durable stream vault query to find `PetStates` with sequential order

Find `UNCONSUMED` `PetState`s with the sequential named query `"VaultStateEvent.sequential.findByStateStatusAndContractStateClassNameIn"`.
* Sequential named queries apply sequential ordering to states and guarantee states in the order of events.
* Query takes named parameters `"stateStatus"` and `"contractStateClassNames"`
* `IdentityContractStatePostProcessor` is applied, which loads actual `PetState` data from transactions.
* `PetState` implements `JsonRepresentable` which is responsible for marshalling each `PetState` to JSON.
* Polls for batches of size `100` and unmarshalls the response items to `PetStatePojo`s.

```kotlin
val client = HttpRpcClient(
    baseAddress = "http://$host:$port/api/v1/",
    PersistenceRPCOps::class.java,
    HttpRpcClientConfig()
        .username(username)
        .password(password)
)

client.use {
    val connection = client.start()
    with(connection.proxy) {
        val cursor = this.query(
            RpcNamedQueryRequestBuilder("VaultStateEvent.sequential.findByStateStatusAndContractStateClassNameIn")
                .withNamedParameters(
                    mapOf(
                        "stateStatus" to RpcNamedQueryParameterJson(GsonBuilder().create().toJson(RpcVaultStateStatus.UNCONSUMED)),
                        "contractStateClassNames" to RpcNamedQueryParameterJson(
                            GsonBuilder().create().toJson(listOf(PetState::class.java.name))
                        )
                    )
                )
              .withPostProcessorName("Corda.IdentityContractStatePostProcessor")
              .build())
            .build()

        val accumulator: MutableList<PetStatePojo> = mutableListOf()
        while (accumulator.size < totalPets) {
            val poll = cursor.poll(100, 20.seconds)
            val petStates = poll.values
                .map { Gson().fromJson(it.json, PetStatePojo::class.java) }
                .filter { it.initiatorId == testId }
            accumulator.addAll(petStates)
            cursor.commit(poll)
        }
    }
}
```

### Example 2 - Selecting a nullable field from an entity

Find nullable `name` fields from a `HttpItem` entity using the query `"HttpItem.findNamesByInitiatorId"`.
- Query takes a named parameter `"initiatorId"` of type `String`.
- Query applies a post-processor called `"data-persistence.StringCapitalizationJavaPostProcessor"` to capitalize names.
- Cursor is polled in batches of `100` and unmarshalls response items to `String`s.

```kotlin
val client = HttpRpcClient(
    baseAddress = "http://$host:$port/api/v1/",
    PersistenceRPCOps::class.java,
    HttpRpcClientConfig()
        .username(username)
        .password(password)
)

client.use {
    val connection = client.start()
    with(connection.proxy) {
        val cursor = this.query(
            RpcNamedQueryRequestBuilder("HttpItem.findNamesByInitiatorId")
                .withNamedParameters(
                    mapOf(
                        "initiatorId" to RpcNamedQueryParameterJson("\"$testId\"")
                    )
                )
                .withPostProcessorName("data-persistence.StringCapitalizationJavaPostProcessor")
                .build())
            .build()

        val postProcessedStringList: MutableList<String?> = mutableListOf()
        while (postProcessedStringList.size < repsCount) {
            val pollResult = cursor.poll(100, 15.seconds)
            val eventsBatch = pollResult.values
            val strings = eventsBatch.map {
                Gson().fromJson(it.json, String::class.java)
            }
            postProcessedStringList.addAll(strings)
            cursor.commit(pollResult)
        }
    }
}
```

### Example 3 - Find `PetStates` with the given name

Find `PetState`s with the given name and use the `PetStatePostProcessor` to transform the states into simple marshallable `PetStatePojo`s.
- Use the query `"PersistentPet.findUnconsumedByName"` which takes a named parameter `"name"`.
- Use the post-processor called `"linearstate-sample.PetStatePostProcessor"` to transform the states into JSON serializable `PetStatePojo`s.
- Cursor is polled once to return a single JSON marshalled `PetStatePojo` result.

```kotlin
val client = HttpRpcClient(
    baseAddress = "http://$host:$port/api/v1/",
    PersistenceRPCOps::class.java,
    HttpRpcClientConfig()
        .username(username)
        .password(password)
)

client.use {
    val connection = client.start()
    with(connection.proxy) {
        val cursor = this.query(
            RpcNamedQueryRequestBuilder("PersistentPet.findUnconsumedByName")
                .withNamedParameters(
                    mapOf(
                        "name" to RpcNamedQueryParameterJson(GsonBuilder().create().toJson("Roger the Rabbit"))
                    )
                )
                .withPostProcessorName("linearstate-sample.PetStatePostProcessor")
                .build())
            .build()

        val singlePoll = queryByTxId.poll(1, 20.seconds)
        val petJson = singlePoll.values.first().json
        val petPojo = Gson().fromJson(petJson, PetStatePojo::class.java)
    }
}
```

This is not a sequential named-query. As a result, you cannot guarantee that there will be no data lost between polls. For example, new `PetStates` could have been persisted between polls. These new states may not be picked up by the next poll, or there may be unexpected side effects. To avoid this problem, you can use the built-in sequential named-queries.

## Appendix

### `PetState`

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
```

### `PersistentPet`

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

### `PetStatePostProcessor`

```kotlin
class PetStatePostProcessor : StateAndRefPostProcessor<PetStatePojo> {
    /**
     * Name of this post-processor to be used in PersistenceService and HTTP RPC APIs.
     */
    override val name: String
        get() = "linearstate-sample.PetStatePostProcessor"

    /**
     * Type check and convert a state into a serializable [PetStatePojo].
     */
    override fun postProcess(inputs: Stream<StateAndRef<ContractState>>): Stream<PetStatePojo> {
        return inputs
            .filter { it.state.data is PetState }
            .map {
                val state = it.state.data as PetState
                PetStatePojo(state.name, state.initiatorId, state.owner.toString(), state.linearId.toString())
            }
    }

    /**
     * This can be used from RPC APIs.
     */
    override val availableForRPC: Boolean
        get() = true
}

/**
 * Simple Pojo representing a PetState that can be easily serialized.
 */
@CordaSerializable
data class PetStatePojo(
    val name: String,
    val initiatorId: String,
    val owner: String,
    val linearId: String
)
```

### `StringCapitalizationJavaPostProcessor`

This post-processor written in Java takes `String`s and capitalizes them. It also performs a null check, and returns nulls.

```java
public class StringCapitalizationJavaPostProcessor implements CustomQueryPostProcessor<String> {

    public static final String POST_PROCESSOR_NAME = "data-persistence.StringCapitalizationJavaPostProcessor";

    @NotNull
    @Override
    public String getName() {
        return POST_PROCESSOR_NAME;
    }

    @Override
    public boolean getAvailableForRPC() {
        return true;
    }

    @NotNull
    @Override
    public Stream<String> postProcess(@NotNull Stream<Object> inputs) {
        return inputs.map((o) -> {
            if (o instanceof String) {
                return ((String) o).toUpperCase();
            } else {
                return null;
            }
        });
    }
}
```

### `HttpItem`

A `HttpItem` with named queries defined for finding `HttpItems` and `HttpItem.name` fields.

```kotlin
object HttpItemSchemaV1 : MappedSchema(
    schemaFamily = HttpItemSchema.javaClass,
    version = 1,
    mappedTypes = listOf(HttpItem::class.java)
) {
    @Entity
    @NamedQueries(
        NamedQuery(
            name = "HttpItem.findByInitiatorId",
            query = "FROM net.corda.httprpcdemo.schema.HttpItemSchemaV1\$HttpItem " +
                    "WHERE initiatorId = :initiatorId ORDER BY timestamp ASC"
        ),
        NamedQuery(
            name = "HttpItem.findNamesByInitiatorId",
            query = "SELECT it.name FROM net.corda.httprpcdemo.schema.HttpItemSchemaV1\$HttpItem it " +
                    "WHERE it.initiatorId = :initiatorId ORDER BY timestamp ASC"
        )
    )
    @Table(name = "http_item")
    @CordaSerializable
    data class HttpItem(
        @Id
        @Column(name = "id")
        var id: String,
        @Column(name = "name")
        var name: String?,
        @Column(name = "initiator_id")
        var initiatorId: String,
        @Column(name = "timestamp")
        var timestamp: java.time.Instant
    ) : Serializable
}

@CordaSerializable
data class HttpItemPojo(
    val id: String,
    val name: String?,
    val initiatorId: String,
    val timestamp: String
)
```
