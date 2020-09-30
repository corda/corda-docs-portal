---
date: '2020-05-10T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-token-sdk
weight: 100
tags:
- Tokens SDK
- Selection
- Database selection
- In Memory
- in-Memory
- inMemory
- selectionType
- selection type
title: Selection in the Tokens SDK
---

# Token selection using the Tokens SDK

When you move or redeem tokens using the Tokens SDK, you can choose which balance of tokens you want to use, and how much from each reserve, in any given transaction.

This process is called **Selection**.

You can write flows for moving your tokens that allow selection from either:

* The database which stores token data.
* In-memory data, which is like a cache of a node's current token data.

**In-memory selection** is a much faster method of choosing the right token reserves to use in a transaction. However, you may decide you prefer **Database** selection as it keeps the database as the only active source of truth for your tokens.

## Token selection with multithreaded SMM

A multithreaded environment is characterised by running tokens with Corda Enterprise where the number of flow workers is configured to be > 1.

You can only use in-memory selection in a multithreaded environment. This is  because a cache of available tokens balances are maintained for querying in the JVM. This means the query time to select available tokens is extremely fast, preventing the need for soft-locking tokens in the DB. Tokens are simply selected, added to a transaction and spent.

In DB selection, token states must be queried from the vault and “selected” by soft locking the record in the database. This doesn’t work in a multi-threaded environment and multiple threads running at the same time may end up selecting the same token state to be spent. This will lead to the node throwing an `InsufficientBalanceException` as all available token states (and associated records) are reserved for other concurrent transactions. While this won’t jeopardize data, it could impact the performance of your application.

## Move tokens using Database Selection

In the Tokens SDK, database (DB) selection is the default method of selection for each transaction.

In move flows of multiple tokens using database selection, you specify the method of selection to modify the `TransactionBuilder`, along with the preferred selection source of payment.

In the example below, multiple fungible token moves are added to a token using DB selection:


```kotlin
@Suspendable
@JvmOverloads
fun addMoveFungibleTokens(
        transactionBuilder: TransactionBuilder,
        serviceHub: ServiceHub,
        partiesAndAmounts: List<PartyAndAmount<TokenType>>,
        changeHolder: AbstractParty,
        queryCriteria: QueryCriteria? = null
): TransactionBuilder {
    // Instantiate a DatabaseTokenSelection class which you will use to select tokens
    val selector = DatabaseTokenSelection(serviceHub)
    // Use the generateMove utility on the DatabaseTokenSelection class to determine the input and output token states
    val (inputs, outputs) = selector.generateMove(partiesAndAmounts.toPairs(), changeHolder, TokenQueryBy(queryCriteria = queryCriteria), transactionBuilder.lockId)
    // Add those input and output token states to the transaction
    // This step also calculates and adds the appropriate commands to the transaction so that Token contract verification rules may be applied
    return addMoveTokens(transactionBuilder = transactionBuilder, inputs = inputs, outputs = outputs)
}
```

## Move tokens using in-memory selection

You can use in-memory token in much the same way as DB selection, you are able to call the `generateMove` method to select tokens available for the transaction being constructed.

In the example below where the only change is `LocalTokenSelector` in place of `DBTokenSelector`.

You can see that the `addMoveFungibleTokens` defaults to database selection. If you wish to use in-memory selection you should write your own utility method, like this:

```kotlin
@Suspendable
@JvmOverloads
fun addMoveFungibleTokensInMemory(
        transactionBuilder: TransactionBuilder,
        serviceHub: ServiceHub,
        partiesAndAmounts: List<PartyAndAmount<TokenType>>,
        changeHolder: AbstractParty,
        queryCriteria: QueryCriteria? = null
): TransactionBuilder {
    // Instantiate a LocalTokenSelection class which you will use to select tokens
    val selector = LocalTokenSelection(serviceHub)
    // Use the generateMove utility on the DatabaseTokenSelection class to determine the input and output token states
    val (inputs, outputs) = selector.generateMove(partiesAndAmounts.toPairs(), changeHolder, TokenQueryBy(queryCriteria = queryCriteria), transactionBuilder.lockId)
    // Add those input and output token states to the transaction
    // This step also calculates and adds the appropriate commands to the transaction so that Token contract verification rules may be applied
    return addMoveTokens(transactionBuilder = transactionBuilder, inputs = inputs, outputs = outputs)
}
```

{{< note >}}
You can use generic versions of `MoveTokensFlow` or `addMoveTokens` (not `addMoveFungibleTokens`), because you already performed selection and provide input and output states directly. `addMoveFungibleTokens` must always use database selection.
{{< /note >}}


### Initialise `VaultWatcherService`

To use in-memory selection, you must ensure the CorDapp `VaultWatcherService` is installed and the service is running. This comes as part of the Tokens SDK.

To initialise this service, you must select an `indexingStrategy`. An indexing strategy is used to apply an index to recorded records of Token States in in the `VaultWatcherService`. This improves querying time (and ultimately the performance of your application). As always - you can tune different use cases for better performance by selecting the appropriate indexing strategy.

* **Token_Only** selection strategy indexes states only using token type and identifier.
* **External_ID** strategy can be used to group states from many public keys connected to a given unique user ID. If you use **Accounts**, this strategy is ideal because it allows for faster querying of tokens that belong to accounts.
* **Public_key** strategy makes a token 'bucket' for each public key.


Enter the following into your **CorDapp config**, choosing a single indexing strategy:

```
stateSelection {
    inMemory {
           indexingStrategies: ["EXTERNAL_ID"|"PUBLIC_KEY"|"TOKEN_ONLY"]
           cacheSize: Int
    }
}
```

In this example, token selection is configured in the `deployNodes` with `TOKEN_ONLY` as the indexing strategy, added under task `deployNodes(type: net.corda.plugins.Cordform)`.


```kotlin
nodeDefaults {
    cordapp ("$corda_tokens_sdk_release_group:tokens-selection:$corda_tokens_sdk_version"){
        config '''
            stateSelection {
                inMemory {
                       indexingStrategies: ["TOKEN_ONLY"]
                       cacheSize: 1024
                }
            }
        '''
    }
}
```

## Redeem tokens using `LocalTokenSelection`

You can create a flow for redeeming tokens using `LocalTokenSelection` in a similar way to moving tokens:

1. Choose states that cover the required amount.

2. Create exit states and get possible change outputs.

3. Call the subflow to redeem states with the issuer.

```kotlin
val vaultWatcherService = serviceHub.cordaService(VaultWatcherService::class.java)
val localTokenSelector = LocalTokenSelector(serviceHub, vaultWatcherService, autoUnlockDelay = autoUnlockDelay)

// Choose states that cover the required amount.
val exitStates: List<StateAndRef<FungibleToken>> = localTokenSelector.selectStates(
    lockID = transactionBuilder.lockId, // Defaults to FlowLogic.currentTopLevel?.runId?.uuid ?: UUID.randomUUID()
    requiredAmount = requiredAmount,
    queryBy = queryBy) // See section below on queries

// Exit states and get possible change output.
val (inputs, changeOutput) =  generateExit(
    exitStates = exitStates,
    amount = requiredAmount,
    changeHolder = changeHolder
)
// Call subflow to redeem states with the issuer
val issuerSession: FlowSession = ...
subflow(RedeemTokensFlow(inputs, changeOutput, issuerSession, observerSessions))
// or use utilities functions.
addTokensToRedeem(
    transactionBuilder = transactionBuilder,
    inputs = inputs,
    changeOutput = changeOutput
)
```


## Provide queries to `LocalTokenSelector`

You can provide additional queries to `LocalTokenSelector` by constructing `TokenQueryBy` and passing it to `generateMove` or `selectStates` methods.

`TokenQueryBy` requires issuer to specify selection of token from given issuing party.

You can also provide any states filtering as predicate function.

```kotlin
val issuerParty: Party = ...
val notaryParty: Party = ...
// Get list of input and output states that can be passed to addMove or MoveTokensFlow
val (inputs, outputs) = localTokenSelector.generateMove(
        partiesAndAmounts = listOf(Pair(receivingParty,  tokensAmount)),
        changeHolder = this.ourIdentity,
        // Get tokens issued by issuerParty and notarised by notaryParty
        queryBy = TokenQueryBy(issuer = issuerParty, predicate = { it.state.notary == notaryParty }))
```
