---
date: '2020-09-10'
title: "Diamonds as Tokens example"
aliases:
- ./tokens-sdk.html
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-tokens-sdk
    weight: 400
section_menu: corda-5-dev-preview
description: >
    An introduction to the Tokens SDK.
---

In this example workflow, the Tokens SDK is used to create a non-fungible, evolvable token for diamonds. A diamond cannot be split and merged, but its value and other attributes can evolve over time.

## The story so far...

Denise is a diamond dealer. Her client, Alice wants to buy a diamond and then sell it to Bob. Bob is keen to sell the diamond to Charlie.

Before the diamond can change hands, it must be subject to an official grading report. The grading report is maintained by GIC, and contains grading information about the diamond - it does not contain information about the holder of the diamond.

The Tokens SDK is used to create a token for the non-fungible asset, along with the required commands to ensure that the token can be bought and sold with an up-to-date record in the grading report.

## Access the example

You can access the required libraries to run this example here:

```
package com.r3.corda.lib.tokens.demo

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.module.kotlin.KotlinModule
import com.r3.corda.lib.tokens.diamondDemo.flows.CreateEvolvableDiamondTokenFlow
import com.r3.corda.lib.tokens.diamondDemo.flows.GetDiamondReportFlow
import com.r3.corda.lib.tokens.diamondDemo.flows.HasTransactionFlow
import com.r3.corda.lib.tokens.diamondDemo.flows.HasUnconsumedNonFungibleTokenFlow
import com.r3.corda.lib.tokens.diamondDemo.flows.IssueNonFungibleDiamondToken
import com.r3.corda.lib.tokens.diamondDemo.flows.MoveNonFungibleDiamondToken
import com.r3.corda.lib.tokens.diamondDemo.flows.RedeemEvolvableDiamondTokenFlow
import com.r3.corda.lib.tokens.diamondDemo.flows.UpdateEvolvableDiamondTokenFlow
import com.r3.corda.lib.tokens.test.utils.getFlowOutcome
import com.r3.corda.lib.tokens.test.utils.runFlow
import com.r3.corda.lib.tokens.testing.states.DiamondGradingReport.ClarityScale
import com.r3.corda.lib.tokens.testing.states.DiamondGradingReport.ColorScale
import com.r3.corda.lib.tokens.testing.states.DiamondGradingReport.CutScale
import com.r3.corda.lib.tokens.testing.states.DiamondGradingReportDigest
import net.corda.client.rpc.flow.FlowStarterRPCOps
import net.corda.test.dev.network.Node
import net.corda.test.dev.network.httpRpcClient
import net.corda.test.dev.network.withFlow
import net.corda.test.dev.network.x500Name
import net.corda.v5.application.identity.CordaX500Name
import net.corda.v5.ledger.transactions.SignedTransactionDigest
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Assertions.assertNotEquals
import org.junit.jupiter.api.BeforeAll
import org.junit.jupiter.api.Test
import java.math.BigDecimal
```

The nodes to represent the parties can be brought up on your local machine using corda-cli to build a test network. `token-diamond-network.yaml` has been added to configure the required network. This can be found here: `testing/demo/src/diamondDemo/resources/token-diamond-network.yaml`

``` Yaml
registry: engineering-docker.software.r3.com
tag: 5.0.0-devpreview-rc04
nodes:
  alice:
  bob:
  caroline:
  denise:
  gic:
  notary:
    notary: true
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

``` kotlin
val publishedDiamondProperties = DiamondProperties(
   caratWeight = BigDecimal("1.0"),
   colorScale = ColorScale.A,
   clarityScale = ClarityScale.A,
   cutScale = CutScale.A,
)

val publishDiamondTx = gic.createEvolvableDiamondToken(
   publishedDiamondProperties,
   denise.x500Name
)
assertHasTransaction(publishDiamondTx, gic)
assertHasTransaction(publishDiamondTx, denise)

val publishedDiamond = publishDiamondTx.getSingleDiamondOutput()
assertDiamondProperties(publishedDiamond, publishedDiamondProperties)
```


### Denise creates an ownership token

Denise creates an ownership token for the diamond, which points to the grading report created by GIC.

Denise issues the token to Alice. Note that GIC should *not* receive a copy of this issuance. This is because the report is only about the diamond itself, not about who holds it.

``` kotlin
val issueTokenTx = denise.issueNonFungibleTokens(
   tokenLinearId = publishedDiamond.linearId,
   issueTo = alice.x500Name,
   anonymous = true
)
// GIC should *not* receive a copy of this issuance
assertHasTransaction(issueTokenTx, alice)
assertNotHasTransaction(issueTokenTx, gic)
```

### Alice transfers ownership to Bob

Alice moves the diamond token to Bob, continuing the chain of sale.

``` kotlin
val moveTokenToBobTx = alice.moveNonFungibleTokens(
   nftLinearId = issueTokenTx.outputStates.single(),
   moveTo = bob.x500Name,
   anonymous = true
)
assertHasTransaction(moveTokenToBobTx, alice, bob)
assertNotHasTransaction(moveTokenToBobTx, gic, denise)
```

### Bob transfers ownership to Charlie

Bob moves the token to Charlie, continuing the chain of sale.

```kotlin
val moveTokenToCarolineTx = bob.moveNonFungibleTokens(
   nftLinearId = moveTokenToBobTx.outputStates.single(),
   moveTo = caroline.x500Name,
   anonymous = true
)
assertHasTransaction(moveTokenToCarolineTx, bob, caroline)
assertNotHasTransaction(moveTokenToCarolineTx, gic, denise, alice)
```

### GIC amends (updates) the grading report

The grading report of the diamond has been updated. The diamond now has a cut scale and color scale grading of 'B'. This must be reflected to the report participants: Denise, Bob, and Charlie.

Alice no longer holds the token for this diamond, so she does *not* receive an amended report from GIC.

```kotlin
val updatedDiamondProperties = publishedDiamondProperties.copy(colorScale = ColorScale.B)
val updateDiamondTx = gic.updateEvolvableToken(
   tokenLinearId = publishedDiamond.linearId,
   diamondProperties = updatedDiamondProperties
)
assertHasTransaction(updateDiamondTx, gic, denise, bob, caroline)
assertNotHasTransaction(updateDiamondTx, alice)

val updatedDiamond = updateDiamondTx.getSingleDiamondOutput()
assertDiamondProperties(updatedDiamond, updatedDiamondProperties)
```

### Charlie redeems the token with Denise

Charlie is now the owner of the real-world diamond, and wants to collect. She redeems the token with Denise. This information is only reported to Charlie and Denise. GIC, Alice, and Bob do not receive any further information regarding the diamond. This action removes the holdable token from the ledger.

 ``` kotlin
val redeemDiamondTx = caroline.redeemTokens(
   nftLinearId = moveTokenToCarolineTx.outputStates.single(),
   redeemFrom = denise.x500Name,
)
assertHasTransaction(redeemDiamondTx, caroline, denise)
assertNotHasTransaction(redeemDiamondTx, gic, alice, bob)
```

### Final positions

GIC, Denise, Bob and Charlie have the latest evolvable token. Alice does not:

``` kotlin
assertHasDiamondReport(updatedDiamondProperties, updatedDiamond.linearId, gic, denise, bob, caroline)
assertNotHasDiamondReport(updatedDiamondProperties, updatedDiamond.linearId, alice)
```

Alice has an outdated (and unconsumed) evolvable token. GIC, Denise, Bob and Charlie do not:

``` kotlin
assertHasDiamondReport(publishedDiamondProperties, publishedDiamond.linearId, alice)
assertNotHasDiamondReport(publishedDiamondProperties, publishedDiamond.linearId, gic, denise, bob, caroline)
```

No party has non-fungible (discrete) tokens:

``` kotlin
// No one has nonfungible (discrete) tokens
assertNotHasUnconsumedNonFungibleToken(issueTokenTx.outputStates.single(), gic, denise, alice, bob, caroline)
// assert the linear ID was unchanged between transactions so we son't need to check for unconsumed tokens again
assertEquals(issueTokenTx.outputStates.single(), moveTokenToBobTx.outputStates.single())
assertEquals(issueTokenTx.outputStates.single(), moveTokenToCarolineTx.outputStates.single())
```
