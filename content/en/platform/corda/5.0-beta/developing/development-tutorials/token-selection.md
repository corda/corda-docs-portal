---
date: '2023-01-30'
title: "Using the UTXO Ledger Token Selection API"
menu:
  corda-5-beta:
    parent: corda-5-beta-tutorials-develop
    identifier: corda-5-beta-token-selection
    weight: 3000
section_menu: corda-5-beta
---

The following example outlines the basic building blocks to consider when using the [token selection API](../api/api-ledger-token-selection.md) with the UTXO ledger. The example only covers the token selection aspects of a flow and omits any details about how to create [UTXO ledger transactions](****).

1. Define a custom state with enough detail to create a token from:
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
  ```
2. Create an observer to convert the state to a token:
   ```java
   class CoinStateObserver : UtxoLedgerTokenStateObserver<CoinState> {

    override val stateType = CoinState::class.java

    override fun onCommit(state: CoinState): UtxoToken {
        return UtxoToken(
            poolKey = UtxoTokenPoolKey(
                tokenType = CoinState.tokenType,
                issuerHash = state.issuer,
                symbol = state.currency
            ),
            state.value,
            filterFields = UtxoTokenFilterFields(state.tag, state.ownerHash)
        )
    }
  }
   ```

   Corda can now create pools of tokens for the unconsumed `CoinState`s.

3. You can now begin selecting states to spend in a flow. This example does not show code for creating transactions but in a real example you would need to create a flow to mint the coins (states) by creating and finalizing UTXO transactions that have `CoinStates` as output states. Add the token selection API to a flow as an injected property:
   ```java
   @CordaInject
   lateinit var tokenSelection: TokenSelection
   ```

   Create the criteria for the type of tokens we need and set a target amount:
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

   Issue the query, handle the response, and clean-up any claim we make:
   ```java
    // Query for required tokens
   val tokenClaim = tokenSelection.tryClaim(selectionCriteria)
 
   // A null result indicates the query could not be satisfied
   if(tokenClaim == null) {
    return "FAILED TO FIND ENOUGH TOKENS"
   }
 
   // We've claimed some tokens we can now try and spend them,
   // we must release the claim regardless of the outcome, indicating
   // how many tokens were used
   var spentCoins = listOf<StateRef>()
 
   try{
      spentCoins = aSpendFunction(tokenClaim.claimedTokens)
   } finally {
     tokenClaim.useAndRelease(spentCoins)
   }
   ```