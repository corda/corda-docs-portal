---
date: '2020-05-10T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-token-sdk
weight: 200
tags:
title: Tokens SDK evolvable token example
---
# Diamonds as tokens - non-fungible, evolvable tokens using the Tokens SDK

In this example workflow, the Tokens SDK is used to create a non-fungible, evolvable token for diamonds. A diamond cannot be split and merged, but its value and other attributes can evolve over time.

## The story so far...

Denise is a diamond dealer. Her client, Alice wants to buy a diamond and then sell it to Bob. Bob is keen to sell the diamond to Charlie.

Before the diamond can change hands, it must be subject to an official grading report. The grading report is maintained by GIC, and contains grading information about the diamond - it does not contain information about the holder of the diamond.

The Tokens SDK is used to create a token for the non-fungible asset, along with the required commands to ensure that the token can be bought and sold with an up-to-date record in the grading report.

## Access the example

You can access the required libraries to run this example here:

```
package com.r3.corda.lib.tokens.workflows

import com.r3.corda.lib.tokens.contracts.states.NonFungibleToken
import com.r3.corda.lib.tokens.testing.states.DiamondGradingReport
import net.corda.core.utilities.getOrThrow
import net.corda.testing.node.StartedMockNode
import org.junit.Test
import kotlin.test.assertEquals
```

Add the nodes to represent the parties to your local machine:

**Kotlin:**

```Kotlin
class DiamondWithTokenScenarioTests : JITMockNetworkTests() {

   private val gic: StartedMockNode get() = node("Gemological Institute of Corda (GIC)")
   private val denise: StartedMockNode get() = node("Denise")
   private val alice: StartedMockNode get() = node("Alice")
   private val bob: StartedMockNode get() = node("Bob")
   private val charlie: StartedMockNode get() = node("Charlie")
```

## What happens

These are the events that take place in this workflow:

1. GIC creates (publishes) the diamond grading report
2. Denise (the diamond dealer) issues a holdable, discrete (non-fungible) token to Alice
3. Alice transfers the discrete token to Bob
4. Bob transfers the discrete token to Charlie
5. GIC amends (updates) the grading report
6. Charlie redeems the holdable token with Denise.
7. Epilogue: Denise, the original diamond dealer, buys back the diamond and plans to issue a new holdable token as replacement.

```*/
   @Test
   fun `lifecycle example`() {
```

### GIC publishes the diamond report

GIC publishes the grading report on the diamond and shares it with Denise. According to the report, the diamond has a cut scale and color scale grading of 'A':

```val diamond = DiamondGradingReport("1.0", DiamondGradingReport.ColorScale.A, DiamondGradingReport.ClarityScale.A, DiamondGradingReport.CutScale.A, gic.legalIdentity(), denise.legalIdentity())
val publishDiamondTx = gic.createEvolvableToken(diamond, notary.legalIdentity()).getOrThrow()
val publishedDiamond = publishDiamondTx.singleOutput<DiamondGradingReport>()
assertEquals(diamond, publishedDiamond.state.data, "Original diamond did not match the published diamond.")
assertHasTransaction(publishDiamondTx, gic, denise)
```


### Denise creates an ownership token

Denise creates an ownership token for the diamond, which points to the grading report created by GIC.

Denise issues the token to Alice. Note that GIC should *not* receive a copy of this issuance. This is because the report is only about the diamond itself, not about who holds it.

```val diamondPointer = publishedDiamond.state.data.toPointer<DiamondGradingReport>()
val issueTokenTx = denise.issueNonFungibleTokens(
token = diamondPointer,
issueTo = alice,
anonymous = true
).getOrThrow()
// GIC should *not* receive a copy of this issuance
assertHasTransaction(issueTokenTx, alice)
assertNotHasTransaction(issueTokenTx, gic)
```

### Alice transfers ownership to Bob

Alice moves the diamond token to Bob, continuing the chain of sale.

```
val moveTokenToBobTx = alice.moveNonFungibleTokens(diamondPointer, bob, anonymous = true).getOrThrow()
assertHasTransaction(moveTokenToBobTx, alice, bob)
assertNotHasTransaction(moveTokenToBobTx, gic, denise)
```

### Bob transfers ownership to Charlie

Bob moves the token to Charlie, continuing the chain of sale.

```val moveTokenToCharlieTx = bob.moveNonFungibleTokens(diamondPointer, charlie, anonymous = true).getOrThrow()
assertHasTransaction(moveTokenToCharlieTx, bob, charlie)
assertNotHasTransaction(moveTokenToCharlieTx, gic, denise, alice)
```

### GIC amends (updates) the grading report

The grading report of the diamond has been updated. The diamond now has a cut scale and color scale grading of 'B'. This must be reflected to the report participants: Denise, Bob, and Charlie.

Alice no longer holds the token for this diamond, so she does *not* receive an amended report from GIC.

 ```val updatedDiamond = publishedDiamond.state.data.copy(color = DiamondGradingReport.ColorScale.B)
val updateDiamondTx = gic.updateEvolvableToken(publishedDiamond, updatedDiamond).getOrThrow()
assertHasTransaction(updateDiamondTx, gic, denise, bob, charlie)
assertNotHasTransaction(updateDiamondTx, alice)
```

### Charlie redeems the token with Denise

Charlie is now the owner of the real-world diamond, and wants to collect. She redeems the token with Denise. This information is only reported to Charlie and Denise. GIC, Alice, and Bob do not receive any further information regarding the diamond. This action removes the holdable token from the ledger.

 ```val charlieDiamond = moveTokenToCharlieTx.tx.outputsOfType<NonFungibleToken>().first()
val redeemDiamondTx = charlie.redeemTokens(charlieDiamond.token.tokenType, denise).getOrThrow()
assertHasTransaction(redeemDiamondTx, charlie, denise)
assertNotHasTransaction(redeemDiamondTx, gic, alice, bob)
```

### Final positions

GIC, Denise, Bob and Charlie have the latest evolvable token. Alice does not:

```val newDiamond = updateDiamondTx.singleOutput<DiamondGradingReport>()
assertHasStateAndRef(newDiamond, gic, denise, bob, charlie)
assertNotHasStateAndRef(newDiamond, alice)
```

Alice has an outdated (and unconsumed) evolvable token. GIC, Denise, Bob and Charlie do not:

```val oldDiamond = publishDiamondTx.singleOutput<DiamondGradingReport>()
assertHasStateAndRef(oldDiamond, alice)
assertNotHasStateAndRef(oldDiamond, gic, denise, bob, charlie)
```

No party has nonfungible (discrete) tokens:

```assertNotHasStateAndRef(issueTokenTx.singleOutput<NonFungibleToken>(), gic, denise, alice, bob, charlie)
assertNotHasStateAndRef(moveTokenToBobTx.singleOutput<NonFungibleToken>(), gic, denise, alice, bob, charlie)
assertNotHasStateAndRef(moveTokenToCharlieTx.singleOutput<NonFungibleToken>(), gic, denise, alice, bob, charlie)
}
```
