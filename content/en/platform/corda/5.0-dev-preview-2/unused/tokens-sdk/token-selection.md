---
date: '2020-09-10'
title: "Token selection"

---

When you move or redeem tokens using the Tokens SDK, you can choose which balance of tokens you want to use, and how much from each reserve, in any given transaction.

This process is called **Selection**.

You can write flows for moving your tokens that allow selection from either:

* The database which stores token data.
* In-memory data, which is like a cache of a node's current token data.

**In-memory selection** is a much faster method of choosing the right token reserves to use in a transaction. However, you may decide you prefer **Database** selection as it keeps the database as the only active source of truth for your tokens.

## Token selection and soft-locking

Soft-locking of tokens is the process where tokens are held temporarily before they are moved/redeemed so that they cannot be moved/redeemed by other flows while our flow is in the process of running.

In Corda 5, soft-locking of token states will be moved out of the corda platform and into the tokens sdk codebase. The tokens SDK has a version of in-memory soft-locking at the moment, but this will be improved upon by allowing the tokens sdk soft-locking to listen for failed flows and release locked tokens when a flow which has soft-locked tokens fails.

This is not currently a part of the developer preview of corda 5. As a result, any flow which fails while tokens have been soft-locked will be unable to release the soft-lock it has acquired. This is no different to how the tokens sdk handled soft-locking in corda 4. If you find yourself in this situation the best thing to do is to restart your node to clear it’s in-memory locked states.

## Token selection with multithreaded SMM

A multithreaded environment is characterised by running tokens with Corda Enterprise where the number of flow workers is configured to be > 1.

You can only use in-memory selection in a multithreaded environment. This is  because a cache of available tokens balances are maintained for querying in the JVM. This means the query time to select available tokens is extremely fast, preventing the need for soft-locking tokens in the DB. Tokens are simply selected, added to a transaction and spent.

In DB selection, token states must be queried from the vault and “selected” by soft-locking the record in the database. This doesn’t work in a multi-threaded environment and multiple threads running at the same time may end up selecting the same token state to be spent. This will lead to the node throwing an `InsufficientBalanceException` or `InsufficientNotLockedBalanceException` as all available token states (and associated records) are reserved for other concurrent transactions. While this won’t jeopardize data, it could impact the performance of your application.

## Move tokens using Database Selection

In the Tokens SDK, database (DB) selection is the default method of selection for each transaction.

In move flows of multiple tokens using database selection, you specify the method of selection to modify the `TransactionBuilder`, along with the preferred selection source of payment.

In the example below, multiple fungible token moves are added to a token using DB selection:


```kotlin
@Suspendable
fun addMoveFungibleTokens(
    transactionBuilder: TransactionBuilder,
    persistenceService: PersistenceService,
    identityService: IdentityService,
    hashingService: HashingService,
    flowEngine: FlowEngine,
    memberInfo: MemberInfo,
    partiesAndAmounts: List<PartyAndAmount<TokenType>>,
    changeHolder: AbstractParty,
    queryBy: TokenQueryBy
): TransactionBuilder {
    // Instantiate a DatabaseTokenSelection class which you will use to select tokens
    val selector = DatabaseTokenSelection(persistenceService, identityService, flowEngine)
    // Use the generateMove utility on the DatabaseTokenSelection class to determine the input and output token states
    val (inputs, outputs) =
        selector.generateMove(
            identityService,
            hashingService,
            memberInfo,
            partiesAndAmounts.toPairs(),
            changeHolder,
            queryBy,
            transactionBuilder.lockId
        )
    // Add those input and output token states to the transaction
    // This step also calculates and adds the appropriate commands to the transaction so that Token contract verification rules may be applied
    return addMoveTokens(transactionBuilder = transactionBuilder, inputs = inputs, outputs = outputs)
}
```


### Initialise `TokenSelectionService`

To use in-memory selection, you must ensure the CorDapp `TokenSelectionService` is installed and the service is running. This comes as part of the Tokens SDK.

To initialise this service, you must select an `indexingStrategy`. An indexing strategy is used to apply an index to recorded records of Token States in the `TokenSelectionService`. This improves querying time (and ultimately the performance of your application). As always - you can tune different use cases for better performance by selecting the appropriate indexing strategy:

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

## Redeem tokens using `LocalTokenSelection`

You can create a flow for redeeming tokens using `LocalTokenSelection` in a similar way to moving tokens:

1. Choose states that cover the required amount.

2. Create exit states and get possible change outputs.

3. Call the subflow to redeem states with the issuer.

```kotlin
val localTokenSelector = LocalTokenSelector(tokenSelectionService, autoUnlockDelay = autoUnlockDelay)

// Choose states that cover the required amount.
val exitStates: List<StateAndRef<FungibleToken>> = localTokenSelector.selectTokens(
    lockId = transactionBuilder.lockId,
    requiredAmount = requiredAmount,
    queryBy = queryBy
)

// Exit states and get possible change output.
val (inputs, changeOutputs) = localTokenSelector.generateExit(
    exitStates = exitStates,
    amount = requiredAmount,
    changeHolder = changeHolder,
    hashingService = hashingService
)

// Call subflow to redeem states with the issuer
val issuerSession: FlowSession = flowEngine.subFlow(
    RedeemTokensFlow(
        inputs,
        changeOutput,
        issuerSession,
        observerSessions
    )
)
// or use utilities functions.
changeOutputs.forEach {
    addTokensToRedeem(
        transactionBuilder = transactionBuilder,
        inputs = inputs,
        changeOutput = it
    )
}
```


## Provide queries to `LocalTokenSelector`

You can provide additional post-processing to named queries called by `LocalTokenSelector` by constructing `TokenQueryBy` with a post processor and passing it to `generateMove` or `selectTokens` methods.

`TokenQueryBy` requires issuer to specify selection of token from given issuing party.

You can also provide any states filtering as predicate function.

```kotlin
val issuerParty: Party = ...
val notaryParty: Party = ...
// Get list of input and output states that can be passed to addMove or MoveTokensFlow
val (inputs, outputs) = localTokenSelector.generateMove(
        identityService = identityService,
        hashingService = hashingService,
        memberInfo = memberLookupService.myInfo(),
        lockId = transactionBuilder.lockId,
        partiesAndAmounts = listOf(Pair(receivingParty,  tokensAmount)),
        changeHolder = this.ourIdentity,
        // Get tokens issued by issuerParty and notarised by notaryParty
        queryBy = TokenQueryBy(issuer = issuerParty, predicate = { it.state.notary == notaryParty }))
```
