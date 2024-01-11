---
date: '2023-06-20'
title: "Using the UTXO Ledger Token Selection API"
project: corda
version: 'Corda 5.2'
menu:
  corda52:
    identifier: corda52-develop-utxo
    parent: corda52-api-ledger-utxo-token-selection
    weight: 1000
section_menu: corda52
---

# Using the UTXO Ledger Token Selection API
This section contains the following:
* [Using the Token Claim API]({{< relref "#using-the-token-claim-api" >}})
* [Using the Balance Query API]({{< relref "#using-the-balance-query-api" >}})


## Using the Token Claim API

The following example outlines the basic building blocks to consider when using the [token selection API]({{< relref "./_index.md" >}}) with the {{< tooltip >}}UTXO{{< /tooltip >}} ledger. The example only covers the token selection aspects of a {{< tooltip >}}flow{{< /tooltip >}} and omits any details about how to create [UTXO ledger transactions]({{< relref "../../../../ledger/transactions/_index.md" >}}).

1. Define a custom state with enough detail to create a {{< tooltip >}}token{{< /tooltip >}} from:
   ```java
   class CoinState(
       override val participants: List<PublicKey>,
       val issuer: SecureHash,
       val currency: String,
       val value: BigDecimal,
       val tag: String? = null,
       val ownerHash: SecureHash? = null
   ) : ContractState {
      companion object {
         val tokenType = CoinState::class.java.name.toString()
      }
2. Create an observer to convert the state to a token:
   ```java
   class CoinStateObserver : UtxoTokenTransactionStateObserver<CoinState> {
      override val stateType = CoinState::class.java

      override fun onCommit(context: TokenStateObserverContext<CoinState>): UtxoToken {
         return UtxoToken(
            poolKey = UtxoTokenPoolKey(
               tokenType = CoinState.tokenType,
               issuerHash = context.stateAndRef.state.contractState.issuer,
               symbol = context.stateAndRef.state.contractState.currency
            ),
            context.stateAndRef.state.contractState.value,
            filterFields = UtxoTokenFilterFields((context.stateAndRef.state.contractState.tag, context.stateAndRef.state.contractState.ownerHash)
         )
      }
   }
   ```

   Corda can now create pools of tokens for the unconsumed `CoinStates`.

3. You can now begin selecting states to spend in a flow. This example does not show code for creating transactions but in a real example you would need to create a flow to mint the coins (states) by creating and finalizing UTXO transactions that have `CoinStates` as output states. Add the token selection API to a flow as an injected property:
   ```java
   @CordaInject
   lateinit var tokenSelection: TokenSelection
   ```

   a. Create the criteria for the type of tokens you need and set a target amount:

      ```java
      // Assume we have an issuer who has created some coin states
      val bankX500 = MemberX500Name.parse(ISSUING_BANK_X500)
      // Assume we are using a single notrary
      val notary = notaryLookup.notaryServices.single()

      // Create our selection criteria to select a minimum of 100 GBP worth of coins
      val selectionCriteria = TokenClaimCriteria(
        tokenType = CoinState.tokenType,
        issuerHash = bankX500.toSecureHash(),
        notaryX500Name = notary.name,
        symbol = "GBP",
        targetAmount = BigDecimal(100)
      )
      ```

   b. Issue the query, handle the response, and clean-up any claim you make:

      ```java
       // Query for required tokens
      val tokenClaim = tokenSelection.tryClaim(selectionCriteria)

      // A null result indicates the query could not be satisfied
      if (tokenClaim == null) {
       return "FAILED TO FIND ENOUGH TOKENS"
      }

      // You've claimed some tokens you can now try and spend them
      aSpendFunction(tokenClaim.claimedTokens)
      ```

## Using the Balance Query API

The Balance Query API enables users to retrieve the balance of a pool of tokens, taking into account only the tokens that satisfy a certain criteria. Two values are calculated when the query is executed:
* The available balance which only includes tokens that have not been spent nor claimed.
* The total balance which includes all tokens that have not been spent. That is, the total balance is the available balance plus the balance of all claimed tokens.

The following example has similarities to the [Token Claim API example]({{< relref "#using-the-token-claim-api" >}}) and assumes that `CoinState` and `CoinStateObserver` have been implemented as described in that example.

To query the balance of a pool of tokens:

1. Add the token selection API to your flow as an injected property:
   ```java
   @CordaInject
   lateinit var tokenSelection: TokenSelection
   ```
2. Create the criteria that specifies which tokens should be taken into account to calculate the balance:
   ```java
   // Assume there is an issuer who has created some coin states
   val bankX500 = MemberX500Name.parse(ISSUING_BANK_X500)

   // Assume you are using a single notary
   val notary = notaryLookup.notaryServices.single()

   // Create the balance criteria
   val balanceQueryCriteria = TokenBalanceCriteria(
     tokenType = CoinState.tokenType,
     issuerHash = bankX500.toSecureHash(),
     notaryX500Name = notary.name,
     symbol = "GBP"
   )
   ```
3. Issue the query and print the response:
   ```java
   // Query the balance tokens
   val tokenBalance = tokenSelection.queryBalance(balanceQueryCriteria)!!

   // Output the result
   println("Available balance: ${tokenBalance.availableBalance}")
   println("Total balance: ${tokenBalance.totalBalance}")
   ```
