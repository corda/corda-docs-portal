---
date: '2020-05-10T12:00:00Z'
menu:
  corda-enterprise-4-5:
    identifier: corda-enterprise-4-5-token-sdk
    name: "Tokens SDK"
    parent: corda-enterprise-4-5-cordapps
tags:
- building
- against
- release
title: Tokens SDK
weight: 15
---

# The Tokens SDK

The Tokens SDK provides you with the fastest and easiest way to create tokens that represent any kind of asset on your network. This asset can be anything you want it to be - conceptual, physical, valuable or not. You can create a token to represent something outside of the network, or something that only exists on the ledger - like a Corda-native digital currency.

With the SDK, you can define your token and its attributes, then add functionality to a CorDapp so the token can be **issued**, **moved**, and **redeemed** on a ledger.

Use this guide to:

1. Determine the type of token you want to create.

2. Design a token with the correct characteristics for its intended use.

3. Create flows that issue your token correctly onto the ledger, move it from party to party, and have it redeemed.

{{< note >}}

If you are new to Corda, and want a guided tutorial on using the Tokens SDK for the first time, take a look at the [Corda training section on tokens](https://training.corda.net/libraries/tokens-sdk/).

{{< /note >}}

## Upgrade from V1.1 to V1.2

If you have developed a CorDapp that uses the Tokens SDK V1.1, you can upgrade to 1.2.

### Compatibility

Both versions 1.1 and 1.2 of the Tokens SDK are compatible with **platform version 5 (Corda release 4.3)** and higher.

### Changes in V1.2

The main changes in the Tokens SDK V1.2 are designed to improve application of the SDK for those using a Java code base.

Overview of changes:

* All of the utility methods, subflows and RPC enabled flows have been annotated with @JVMOverloads to ensure the appropriate Java constructors are generated where the source Kotlin constructor contains nullable arguments. This ensures a seamless experience when using the Tokens SDK from a Java code base.
* The `selection` and `money` `.jar` files have been moved into the `workflows` `.jar` file.

To upgrade from Tokens SDK V1.1 to V1.2:

1. Change the V number (version number) in your CorDapp's relevant Gradle file from 1.1 to 1.2.

2. Remove all references to `selection` and `money` `.jar` files from your build function (in many cases, Gradle). The functions of these JARS has been moved into `workflows` in V1.2.

3. Recompile your CorDapp.

4. Communicate the change to parties consuming your CorDapp accordingly, along with your recommended steps for upgrading.


## What's inside the Tokens SDK

The Tokens SDK is contained in two `.jar`  files which includes all the required dependencies for your CorDapp, including:

* **Contracts**, which contains the base token types, states and contracts needed to create a token, including token type definitions for fiat and digital currencies.
* **Workflows**, which contains the flows for issuing, moving, redeeming tokens, and selection workflows, which allow a party to select which source of fungible tokens they will use to pay with in a transaction.

As the **Contracts** `.jar` file contains the ability to define and create tokens, and the **Workflows** `.jar` file contains the flows required to use them, you must add both `.jar` files to your CorDapp's folder in order to use the Tokens SDK.

## Choose the anatomy of your token

You can create tokens in Corda to represent anything you like. This could be a representation of an asset that exists outside of your network, like diamonds, or US dollars. Or, it could represent something that only exists inside your network, like a new digital currency that is native to the ledger. In the case of a ledger-native digital currency, the token itself is the object of value - it *is* the asset.

Before using the SDK to create a token, you need to have a clear understanding of what it represents, and how it needs to behave. You need to know if the token is *fungible* or *non-fungible*, and you need to know if certain characteristics of the token need to evolve over time.

* **Fungible tokens** are represented by the `FungibleToken` *class* and can be split and merged – just as the assets they represent, like money or stocks - can be split and merged.

* **Non-fungible tokens** are represented by the `NonFungibleTokens` *state*, and cannot be split and merged - just as the assets they represent, like physical diamonds or a house – cannot be split and merged.

* **Evolvable assets** change over time - not just in value, but in other ways, such as the condition of a car, or size of a house. These tokens are represented by the `EvolvableTokenType`

* **Non-evolvable assets** have no way of changing over time. While the FX markets may fluctuate, a US dollar bill does not change into a different state. It cannot evolve into a 1 Euro coin.

{{< table >}}
| Asset  |   Fungibility   | Evolvability | On / off ledger asset |
| :------------- | :------------- | :------------- | :------------- |
| US Dollar  | Fungible       | non-evolvable      | Off-ledger asset       |
| Ledger-native coin | Fungible  | non-evolvable | On-ledger asset  |
| Diamonds | Non-Fungible | Evolvable | Off-ledger asset |
{{< /table >}}

## Create tokens using the Tokens SDK

When you know what kind of token you want to introduce into the network, you can start defining it. The requirements for each token depend on whether it is fungible, and whether it can evolve over time.  

Use the list below to understand what needs to be included in the token you want to create.

## The process of using the Tokens SDK  

Once you have established what type of token you want to create, you can use the Tokens SDK to perform the following key tasks:

* **Define** your token. Using the readymade utilities contained in the contract `.jar` file, you can define all the required attributes and custom attributes of your tokens.

* **Issue** tokens onto your ledger so they can be used as part of a transaction.

* **Move** the token from at least one party to at least one other party in a transaction.

    * **Select** which specific tokens are to be used to settle a transaction. This applies when a party has more than one 'wallet' or 'pot' of tokens that can be used to settle a transaction.

* **Redeem** and remove the token from the ledger, for example when a party finally takes ownership of their real-life diamond and the token it represents can no longer be used.

### `Tokentype` - the units of a token

A `TokenType` defines the unit of your token.

To create a new `TokenType`, you must give it:

* An identifier, like USD.
* Fractional digits to define how much it can be broken down by. USD has two fractional digits because the smallest possible unit is 0.01 USD (a cent).

You can also give a `TokenType` an optional custom identifier, which is then fixed to that customised `TokenType` and *cannot change* over time. If your tokens represent wines, and you create a custom `WineColor` identifier, a **white wine** token cannot turn into a **red wine** token.

### `EvolvableTokenType` - a token type that can change over time

An `EvolvableTokenType` has properties that can change over time. This is represented in Corda by a `LinearState`. To create and issue an `EvolvableTokenType`, you must:

* Define the `TokenType` - the unit and fractional digits.
* Define the evolvable attributes that can change over time.
* Identify at least one signatory service that can approve the newly evolved state. This is called a `Maintainer`.

In the example below, the evolvable token is for a diamond. You can see the evolvable attributes, which are the attributes included in a grading report for a diamond. You can also see a full [walk-through of this example](token-diamond-example) for a fuller picture.

{{< tabs name="tabs-1234" >}}
{{% tab name="kotlin" %}}
```kotlin
/** Creating an evolveable TokenType */
@BelongsToContract(DiamondGradingReportContract::class)
data class DiamondGradingReport(
        val caratWeight: BigDecimal,
        val color: ColorScale,
        val clarity: ClarityScale,
        val cut: CutScale,
        val assessor: Party,
        val requester: Party,
        override val linearId: UniqueIdentifier = UniqueIdentifier()
) : EvolvableTokenType() {
        override val maintainers: List<Party>
            get() = listOf()             
        override val fractionDigits: Int
            get() = 2
}

val diamond = DiamondGradingReport("1.0", DiamondGradingReport.ColorScale.A, DiamondGradingReport.ClarityScale.A, DiamondGradingReport.CutScale.A, gic.legalIdentity(), denise.legalIdentity())
```
{{% /tab %}}

{{% tab name="java" %}}
```java
public final class DiamondGradingReport extends EvolvableTokenType {
    private final BigDecimal caratWeight;
    private final ColorScale color;
    private final ClarityScale clarity;
    private final CutScale cut;
    private final Party assessor;
    private final Party requester;
    private final UniqueIdentifier linearId;

    @NotNull
    public List getMaintainers() {
        return CollectionsKt.emptyList();
    }

    public int getFractionDigits() {
        return 2;
    }

    @NotNull
    public final BigDecimal getCaratWeight() {
        return this.caratWeight;
    }

    @NotNull
    public final ColorScale getColor() {
        return this.color;
    }

    @NotNull
    public final ClarityScale getClarity() {
        return this.clarity;
    }

    @NotNull
    public final CutScale getCut() {
        return this.cut;
    }

    @NotNull
    public final Party getAssessor() {
        return this.assessor;
    }

    @NotNull
    public final Party getRequester() {
        return this.requester;
    }

    @NotNull
    public UniqueIdentifier getLinearId() {
        return this.linearId;
    }

    public DiamondGradingReport(
            BigDecimal caratWeight,
            ColorScale color,
            ClarityScale clarity,
            CutScale cut,
            Party assessor,
            Party requester,
            UniqueIdentifier linearId) {
        super();
        this.caratWeight = caratWeight;
        this.color = color;
        this.clarity = clarity;
        this.cut = cut;
        this.assessor = assessor;
        this.requester = requester;
        this.linearId = linearId;
    }
}

DiamondGradingReport diamond = new DiamondGradingReport("1.0", DiamondGradingReport.ColorScale.A, DiamondGradingReport.ClarityScale.A, DiamondGradingReport.CutScale.A, gic.getLegalIdentity(), denise.getLegalIdentity())
```
{{% /tab %}}
{{< /tabs >}}

### `FungibleToken` class

A fungible token is represented by the `FungibleToken` class.

To create and issue a fungible token, you must ensure it has:

* A `TokenType` - which you can define manually, or use define using a specified fiat or digital currency.
* A `Holder` so the person holding the token is clear.
* An `Amount` to show how many units the token is worth.
* An `IssuedTokenType` which defines who issued the token. A fungible token can only be exchanged for fungible tokens with the same issuer.

Fungible tokens can be split using a flow initiated by the **Move** command. This allows a party to send some of the value of a single token to more than one recipient. Just like you can split a 10 USD bill between two people (as long as someone has change).

In the below example, Alice instantiates a token representing a BitCoin. This token is generated using the Tokens SDK's built-in `money` library.

{{< tabs name="tabs-1234" >}}
{{% tab name="kotlin" %}}
```kotlin
val fungibleToken = 1 of DigitalCurrency.getInstance("BTC") issuedBy aliceParty heldBy aliceParty
```
{{% /tab %}}
{{% tab name="java" %}}
```java
FungibleToken fungibleToken = new FungibleTokenBuilder()
        .withAmount(1)
        .ofTokenType(DigitalCurrency.getInstance("BTC"))
        .issuedBy(aliceParty)
        .heldBy(aliceParty)
        .buildFungibleToken();
```{{% /tab %}}
{{< /tabs >}}

### `NonFungibleToken` class

A non-fungible token cannot be split and merged, and represents a unique asset. To create a `NonFungibleToken` you must:

* Define the `TokenType` - the name of the unit of your token. As the token cannot be split, the digital fraction value can only be 1.
* Define the first `Holder` of the token type. The holder of the token must be approved by a maintainer each time the token moves from party to party.
* Define any custom attributes of the token.
* Define the issuer of the token using the `IssuedTokenType`.

In this example, Alice issues a collectible item - a vintage baseball card (Babe Ruth) - that cannot be split into any smaller pieces, and does not have attributes that evolve over time.

```kotlin
val issuer = alice.legalIdentity()
val myTokenType = TokenType("BabeRuthCard", 1)
val myIssuedTokenType: IssuedTokenType = myTokenType issuedBy issuer
val myBaseBallCardToken: NonFungibleToken = NonFungibleToken(
    token = myIssuedTokenType,
    holder = issuer,
    linearId = UniqueIdentifier()
)
```


## Write the flows for your token

You can use the Tokens SDK to create flows for your tokens in the following ways:

* **Utility methods** - methods by which you can compose your own flows.
* **Subflows** - ready made processes that need to be initiated by another flow.
* **RPC Enabled flows** - out-of-the-box flows that have been produced for testing purposes. These may not be suitable for commercial use.

{{< attention >}}
All of the utility methods, subflows and RPC enabled flows for Tokens SDK have been annotated with @JVMOverloads to ensure the appropriate Java constructors are generated where the source Kotlin constructor contains nullable arguments. This ensures a seamless experience when using the Tokens SDK from a Java code base.
{{< /attention >}}

### Utility method - Issue

Use this utility method to write a flow that issues your token onto the ledger.

```
@file:JvmName("IssueTokensUtilities")
package com.r3.corda.lib.tokens.workflows.flows.issue

import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.commands.IssueTokenCommand
import com.r3.corda.lib.tokens.contracts.states.AbstractToken
import com.r3.corda.lib.tokens.contracts.types.IssuedTokenType
import net.corda.core.identity.Party
import net.corda.core.transactions.TransactionBuilder
```

Below are three samples of a function that adds a list of output `AbstractToken` states to a `TransactionBuilder`. Each flow sample automatically adds `IssueTokenCommand` commands for each `IssuedTokenType`.

A notary `Party` must be added to the `TransactionBuilder` before this function can be called.

**Sample 1**

```kotlin
@Suspendable
fun addIssueTokens(transactionBuilder: TransactionBuilder, outputs: List<AbstractToken>): TransactionBuilder {
    val outputGroups: Map<IssuedTokenType, List<AbstractToken>> = outputs.groupBy { it.issuedTokenType }
    return transactionBuilder.apply {
        outputGroups.forEach { (issuedTokenType: IssuedTokenType, states: List<AbstractToken>) ->
            val issuers = states.map { it.issuer }.toSet()
            require(issuers.size == 1) { "All tokensToIssue must have the same issuer." }
            val issuer = issuers.single()
            var startingIndex = outputStates().size
            val indexesAdded = states.map { state ->
                addOutputState(state)
                startingIndex++
            }
            addCommand(IssueTokenCommand(issuedTokenType, indexesAdded), issuer.owningKey)
        }
    }
}
```

**Sample 2**

```kotlin
@Suspendable
fun addIssueTokens(transactionBuilder: TransactionBuilder, vararg outputs: AbstractToken): TransactionBuilder {
    return addIssueTokens(transactionBuilder, outputs.toList())
}
```

**Sample 3**

```kotlin
@Suspendable
fun addIssueTokens(transactionBuilder: TransactionBuilder, output: AbstractToken): TransactionBuilder {
    return addIssueTokens(transactionBuilder, listOf(output))
}
```

### Utility method - move

Use the sample methods below to write flows that allow your token to be moved from party to party. This includes transactions in which the token (if fungible) is split in order to transact with multiple parties.

{{< note >}}
Check each sample before use, to make sure it is suitable for the characteristics of your token.
{{< /note >}}

```
@file:JvmName("MoveTokensUtilities")
package com.r3.corda.lib.tokens.workflows.flows.move

import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.commands.MoveTokenCommand
import com.r3.corda.lib.tokens.contracts.states.AbstractToken
import com.r3.corda.lib.tokens.contracts.types.IssuedTokenType
import com.r3.corda.lib.tokens.contracts.types.TokenType
import com.r3.corda.lib.tokens.selection.TokenQueryBy
import com.r3.corda.lib.tokens.selection.database.selector.DatabaseTokenSelection
import com.r3.corda.lib.tokens.workflows.internal.selection.generateMoveNonFungible
import com.r3.corda.lib.tokens.workflows.types.PartyAndAmount
import com.r3.corda.lib.tokens.workflows.types.PartyAndToken
import com.r3.corda.lib.tokens.workflows.types.toPairs
import com.r3.corda.lib.tokens.workflows.utilities.addTokenTypeJar
import net.corda.core.contracts.Amount
import net.corda.core.contracts.StateAndRef
import net.corda.core.identity.AbstractParty
import net.corda.core.node.ServiceHub
import net.corda.core.node.services.vault.QueryCriteria
import net.corda.core.transactions.TransactionBuilder
```

#### Sample 1 - move fungible tokens

Use this flow to add a set of token moves to a transaction using specific inputs and outputs.

```kotlin
 */
@Suspendable
fun addMoveTokens(
        transactionBuilder: TransactionBuilder,
        inputs: List<StateAndRef<AbstractToken>>,
        outputs: List<AbstractToken>
): TransactionBuilder {
    val outputGroups: Map<IssuedTokenType, List<AbstractToken>> = outputs.groupBy { it.issuedTokenType }
    val inputGroups: Map<IssuedTokenType, List<StateAndRef<AbstractToken>>> = inputs.groupBy {
        it.state.data.issuedTokenType
    }

    check(outputGroups.keys == inputGroups.keys) {
        "Input and output token types must correspond to each other when moving tokensToIssue"
    }

    transactionBuilder.apply {
        // Add a notary to the transaction.
        notary = inputs.map { it.state.notary }.toSet().single()
        outputGroups.forEach { issuedTokenType: IssuedTokenType, outputStates: List<AbstractToken> ->
            val inputGroup = inputGroups[issuedTokenType]
                    ?: throw IllegalArgumentException("No corresponding inputs for the outputs issued token type: $issuedTokenType")
            val keys = inputGroup.map { it.state.data.holder.owningKey }

            var inputStartingIdx = inputStates().size
            var outputStartingIdx = outputStates().size

            val inputIdx = inputGroup.map {
                addInputState(it)
                inputStartingIdx++
            }

            val outputIdx = outputStates.map {
                addOutputState(it)
                outputStartingIdx++
            }

            addCommand(MoveTokenCommand(issuedTokenType, inputs = inputIdx, outputs = outputIdx), keys)
        }
    }

    addTokenTypeJar(inputs.map { it.state.data } + outputs, transactionBuilder)

    return transactionBuilder
}
```

**Add a single fungible token move to a transaction:**

```Kotlin
@Suspendable
fun addMoveTokens(
        transactionBuilder: TransactionBuilder,
        input: StateAndRef<AbstractToken>,
        output: AbstractToken
): TransactionBuilder {
    return addMoveTokens(transactionBuilder = transactionBuilder, inputs = listOf(input), outputs = listOf(output))
}
```
**Add multiple fungible token moves to a transaction:**

Use this method to add multiple token moves to a transaction. The [partiesAndAmounts] parameter specifies which parties should receive amounts of the token, with possible change paid to [changeHolder].

{{< note >}}
Change refers to any change due to the party using their token for something that doesn't come to the full value of the token. Like when you pay in a shop with cash, and you might get change from your $100 bill.
{{< /note >}}

You can use this method to combine multiple token amounts from different issuers if needed.

To choose only tokens from one issuer, you can provide optional [queryCriteria] for move generation.

{{< note >}}

This method always uses database token selection, to use [in-memory selection](token-selection.html), use `addMoveTokens` with already selected input and output states.

{{< /note >}}

```Kotlin
@Suspendable
@JvmOverloads
fun addMoveFungibleTokens(
        transactionBuilder: TransactionBuilder,
        serviceHub: ServiceHub,
        partiesAndAmounts: List<PartyAndAmount<TokenType>>,
        changeHolder: AbstractParty,
        queryCriteria: QueryCriteria? = null
): TransactionBuilder {
    val selector: Selector = ConfigSelection.getPreferredSelection(serviceHub)
    val selector = DatabaseTokenSelection(serviceHub)
    val (inputs, outputs) = selector.generateMove(partiesAndAmounts.toPairs(), changeHolder, TokenQueryBy(queryCriteria = queryCriteria), transactionBuilder.lockId)
    return addMoveTokens(transactionBuilder = transactionBuilder, inputs = inputs, outputs = outputs)
}
```

**Add a single fungible token move to a transaction:**

Use this method to add a single token move of `amount` to the new `holder`, with possible change paid to `changeHolder`.

{{< note >}}
Change refers to any change due to the party using their token for something that doesn't come to the full value of the token. Like when you pay in a shop with cash, and you might get change from your $100 bill.
{{< /note >}}

You can use this method to combine multiple token amounts from different issuers if needed.

To choose only tokens from one issuer, you can provide optional [queryCriteria] for move generation.

{{< note >}}

This method always uses database token selection, to use in memory [token selection](token-selection.html), use `addMoveTokens` with already selected input and output states.

{{< /note >}}

```kotlin
@Suspendable
@JvmOverloads
fun addMoveFungibleTokens(
        transactionBuilder: TransactionBuilder,
        serviceHub: ServiceHub,
        amount: Amount<TokenType>,
        holder: AbstractParty,
        changeHolder: AbstractParty,
        queryCriteria: QueryCriteria? = null
): TransactionBuilder {
    return addMoveFungibleTokens(
            transactionBuilder = transactionBuilder,
            serviceHub = serviceHub,
            partiesAndAmounts = listOf(PartyAndAmount(holder, amount)),
            changeHolder = changeHolder,
            queryCriteria = queryCriteria
    )
}
```

#### Non-fungible token moves

Add single move of `token` to the new `holder`. Provide optional `queryCriteria` for move generation.

```kotlin
 */
@Suspendable
@JvmOverloads
fun addMoveNonFungibleTokens(
        transactionBuilder: TransactionBuilder,
        serviceHub: ServiceHub,
        token: TokenType,
        holder: AbstractParty,
        queryCriteria: QueryCriteria? = null
): TransactionBuilder {
    return generateMoveNonFungible(transactionBuilder, PartyAndToken(holder, token), serviceHub.vaultService, queryCriteria)
}
```

**Add a single token move for a non-fungible token**

Add single move of token to the new holder specified using [partyAndToken] parameter.

Provide optional [queryCriteria] for move generation.

```Kotlin
 */
@Suspendable
@JvmOverloads
fun addMoveNonFungibleTokens(
        transactionBuilder: TransactionBuilder,
        serviceHub: ServiceHub,
        partyAndToken: PartyAndToken,
        queryCriteria: QueryCriteria? = null
): TransactionBuilder {
    return generateMoveNonFungible(transactionBuilder, partyAndToken, serviceHub.vaultService, queryCriteria)
}
```
### Utility method - redeem

Use this utility method to write flows that redeem a token and removes it from the ledger.

```
@file:JvmName("RedeemFlowUtilities")
package com.r3.corda.lib.tokens.workflows.flows.redeem

import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.commands.RedeemTokenCommand
import com.r3.corda.lib.tokens.contracts.states.AbstractToken
import com.r3.corda.lib.tokens.contracts.states.FungibleToken
import com.r3.corda.lib.tokens.contracts.types.TokenType
import com.r3.corda.lib.tokens.contracts.utilities.sumTokenStateAndRefs
import com.r3.corda.lib.tokens.selection.TokenQueryBy
import com.r3.corda.lib.tokens.selection.database.selector.DatabaseTokenSelection
import com.r3.corda.lib.tokens.workflows.internal.checkSameIssuer
import com.r3.corda.lib.tokens.workflows.internal.checkSameNotary
import com.r3.corda.lib.tokens.workflows.internal.selection.generateExitNonFungible
import com.r3.corda.lib.tokens.workflows.utilities.addNotaryWithCheck
import com.r3.corda.lib.tokens.workflows.utilities.addTokenTypeJar
import com.r3.corda.lib.tokens.workflows.utilities.heldTokensByTokenIssuer
import com.r3.corda.lib.tokens.workflows.utilities.tokenAmountWithIssuerCriteria
import net.corda.core.contracts.Amount
import net.corda.core.contracts.StateAndRef
import net.corda.core.identity.AbstractParty
import net.corda.core.identity.Party
import net.corda.core.node.ServiceHub
import net.corda.core.node.services.vault.QueryCriteria
import net.corda.core.transactions.TransactionBuilder
```

**Redeem multiple fungible tokens, with possible change returned**

Use this method to write a redeeming flow of multiple `inputs` to the `transactionBuilder` with possible `changeOutput`.

{{< note >}}
Change refers to any change due to the party using their token for something that doesn't come to the full value of the token. Like when you pay in a shop with cash, and you might get change from your $100 bill.
{{< /note >}}

```kotlin
@Suspendable
@JvmOverloads
fun addTokensToRedeem(
        transactionBuilder: TransactionBuilder,
        inputs: List<StateAndRef<AbstractToken>>,
        changeOutput: AbstractToken? = null
): TransactionBuilder {
    checkSameIssuer(inputs, changeOutput?.issuer)
    checkSameNotary(inputs)
    if (changeOutput != null && changeOutput is FungibleToken) {
        check(inputs.filterIsInstance<StateAndRef<FungibleToken>>().sumTokenStateAndRefs() > changeOutput.amount) {
            "Change output should be less than sum of inputs."
        }
    }
    val firstState = inputs.first().state
    addNotaryWithCheck(transactionBuilder, firstState.notary)
    val issuerKey = firstState.data.issuer.owningKey
    val moveKeys = inputs.map { it.state.data.holder.owningKey }

    var inputIdx = transactionBuilder.inputStates().size
    val outputIdx = transactionBuilder.outputStates().size
    transactionBuilder.apply {
        val inputIndicies = inputs.map {
            addInputState(it)
            inputIdx++
        }
        val outputs = if (changeOutput != null) {
            addOutputState(changeOutput)
            listOf(outputIdx)
        } else {
            emptyList()
        }
        addCommand(RedeemTokenCommand(firstState.data.issuedTokenType, inputIndicies, outputs), moveKeys + issuerKey)
    }
    val states = inputs.map { it.state.data } + if (changeOutput == null) emptyList() else listOf(changeOutput)
    addTokenTypeJar(states, transactionBuilder)
    return transactionBuilder
}
```

**Redeem an amount of a fungible token issued by a specific issuer**

Redeem an amount of a token issued by `issuer`. Pay possible change to the `changeHolder` - this can be a confidential identity.

You can provide additional query criteria  using `additionalQueryCriteria`.


```kotlin
@Suspendable
@JvmOverloads
fun addFungibleTokensToRedeem(
        transactionBuilder: TransactionBuilder,
        serviceHub: ServiceHub,
        amount: Amount<TokenType>,
        issuer: Party,
        changeHolder: AbstractParty,
        additionalQueryCriteria: QueryCriteria? = null
): TransactionBuilder {
    val selector: Selector = ConfigSelection.getPreferredSelection(serviceHub)
    val selector = DatabaseTokenSelection(serviceHub)
    val baseCriteria = tokenAmountWithIssuerCriteria(amount.token, issuer)
    val queryCriteria = additionalQueryCriteria?.let { baseCriteria.and(it) } ?: baseCriteria
    val fungibleStates = selector.selectTokens(amount, TokenQueryBy(issuer = issuer, queryCriteria = queryCriteria), transactionBuilder.lockId)
    checkSameNotary(fungibleStates)
    check(fungibleStates.isNotEmpty()) {
        "Received empty list of states to redeem."
    }
    val notary = fungibleStates.first().state.notary
    addNotaryWithCheck(transactionBuilder, notary)
    val (exitStates, change) = selector.generateExit(
            exitStates = fungibleStates,
            amount = amount,
            changeHolder = changeHolder
    )

    addTokensToRedeem(transactionBuilder, exitStates, change)
    return transactionBuilder
}
```

**Redeem a non-fungible token**

Use this method to write a flow that redeems non-fungible `heldToken` issued by the `issuer` and add it to the `transactionBuilder`.

```kotlin
@Suspendable
fun addNonFungibleTokensToRedeem(
        transactionBuilder: TransactionBuilder,
        serviceHub: ServiceHub,
        heldToken: TokenType,
        issuer: Party
): TransactionBuilder {
    val heldTokenStateAndRef = serviceHub.vaultService.heldTokensByTokenIssuer(heldToken, issuer).states
    check(heldTokenStateAndRef.size == 1) {
        "Exactly one held token of a particular type $heldToken should be in the vault at any one time."
    }
    val nonFungibleState = heldTokenStateAndRef.first()
    addNotaryWithCheck(transactionBuilder, nonFungibleState.state.notary)
    generateExitNonFungible(transactionBuilder, nonFungibleState)
    return transactionBuilder
}
```

## Issue, move and redeem tokens using subflows

Use these ready-made subflows to issue, move and redeem tokens. These flows are triggered automatically by existing transaction flows.


### Issue fungible or non-fungible tokens


Use this flow to issue fungible or non-fungible tokens. It should be called as an in-line sub-flow, so you must have flow `participantSessions` set up prior to calling this flow.

Tokens are usually constructed before calling this flow. This flow is to be used in conjunction with the `IssueTokensFlowHandler`.

This flow:

1. Creates a `TransactionBuilder` with the preferred notary, which is set in the Tokens SDK config file.

2. Adds the requested set of `tokensToIssue` as outputs to the transaction builder and adds `IssueTokenCommand`s for each group of states, grouped by `IssuedTokenType`.

3. Finalises the transaction and updates the evolvable token distribution list, if necessary.

Key points:

* If you are issuing to self, there is no need to pass in a flow session. Instead, pass in an emptyList for `participantSessions` or use one of the overloads that doesn't require sessions.
* This flow can only be used by one issuer at a time.
* Tokens can be issued to well-known identities or confidential identities. To issue tokens with confidential keys, use the `ConfidentialIssueTokensFlow` as demonstrated below.
* This flow supports issuing many tokens to a single or multiple parties, of the same or different types of tokens.
* Transaction observers can be specified.
* Observers can also be specified.
* This flow supports the issuance of fungible and non fungible tokens in the same transaction.
* The notary is selected from a config file or picked at random if no notary preference is available.
* This is not an initiating flow. There will also be an initiating version which is startable from the rpc.

```
package com.r3.corda.lib.tokens.workflows.flows.issue
import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.commands.IssueTokenCommand
import com.r3.corda.lib.tokens.contracts.states.AbstractToken
import com.r3.corda.lib.tokens.contracts.states.FungibleToken
import com.r3.corda.lib.tokens.contracts.states.NonFungibleToken
import com.r3.corda.lib.tokens.contracts.types.IssuedTokenType
import com.r3.corda.lib.tokens.workflows.internal.flows.distribution.UpdateDistributionListFlow
import com.r3.corda.lib.tokens.workflows.internal.flows.finality.ObserverAwareFinalityFlow
import com.r3.corda.lib.tokens.workflows.utilities.addTokenTypeJar
import com.r3.corda.lib.tokens.workflows.utilities.getPreferredNotary
import net.corda.core.flows.FlowLogic
import net.corda.core.flows.FlowSession
import net.corda.core.transactions.SignedTransaction
import net.corda.core.transactions.TransactionBuilder
```

```kotlin
class IssueTokensFlow
@JvmOverloads
constructor(
        val tokensToIssue: List<AbstractToken>,
        val participantSessions: List<FlowSession>,
        val observerSessions: List<FlowSession> = emptyList()
) : FlowLogic<SignedTransaction>() {

    /** Issue a single [FungibleToken]. */
    @JvmOverloads
    constructor(
            token: FungibleToken,
            participantSessions: List<FlowSession>,
            observerSessions: List<FlowSession> = emptyList()
    ) : this(listOf(token), participantSessions, observerSessions)

    /** Issue a single [FungibleToken] to self with no observers. */
    constructor(token: FungibleToken) : this(listOf(token), emptyList(), emptyList())

    /** Issue a single [NonFungibleToken]. */
    @JvmOverloads
    constructor(
            token: NonFungibleToken,
            participantSessions: List<FlowSession>,
            observerSessions: List<FlowSession> = emptyList()
    ) : this(listOf(token), participantSessions, observerSessions)

    /** Issue a single [NonFungibleToken] to self with no observers. */
    constructor(token: NonFungibleToken) : this(listOf(token), emptyList(), emptyList())

    @Suspendable
    override fun call(): SignedTransaction {
        // Initialise the transaction builder with a preferred notary or choose a random notary.
        val transactionBuilder = TransactionBuilder(notary = getPreferredNotary(serviceHub))
        // Add all the specified tokensToIssue to the transaction. The correct commands and signing keys are also added.
        addIssueTokens(transactionBuilder, tokensToIssue)
        addTokenTypeJar(tokensToIssue, transactionBuilder)
        // Create new participantSessions if this is started as a top level flow.
        val signedTransaction = subFlow(
                ObserverAwareFinalityFlow(
                        transactionBuilder = transactionBuilder,
                        allSessions = participantSessions + observerSessions
                )
        )
        // Update the distribution list.
        subFlow(UpdateDistributionListFlow(signedTransaction))
        // Return the newly created transaction.
        return signedTransaction
    }
}
```

### Issue tokens to confidential keys


Use this flow to issue tokens to confidential keys. This should be used in conjunction with the `ConfidentialIssueTokensFlowHandler`.

Properties in this flow:

* `tokens` a list of tokens to issue.
* `participantSessions` a list of sessions for the parties being issued tokens.
* `observerSessions` a list of sessions for any observers.


```
com.r3.corda.lib.tokens.workflows.flows.issue

import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.states.AbstractToken
import com.r3.corda.lib.tokens.contracts.states.FungibleToken
import com.r3.corda.lib.tokens.contracts.states.NonFungibleToken
import com.r3.corda.lib.tokens.workflows.flows.confidential.ConfidentialTokensFlow
import com.r3.corda.lib.tokens.workflows.internal.flows.finality.TransactionRole
import net.corda.core.flows.FlowLogic
import net.corda.core.flows.FlowSession
import net.corda.core.transactions.SignedTransaction
```

```Kotlin
class ConfidentialIssueTokensFlow
@JvmOverloads
constructor(
        val tokens: List<AbstractToken>,
        val participantSessions: List<FlowSession>,
        val observerSessions: List<FlowSession> = emptyList()
) : FlowLogic<SignedTransaction>() {

    /** Issue a single [FungibleToken]. */
    @JvmOverloads
    constructor(
            token: FungibleToken,
            participantSessions: List<FlowSession>,
            observerSessions: List<FlowSession> = emptyList()
    ) : this(listOf(token), participantSessions, observerSessions)

    /** Issue a single [FungibleToken] to self with no observers. */
    constructor(token: FungibleToken) : this(listOf(token), emptyList(), emptyList())

    /** Issue a single [NonFungibleToken]. */
    @JvmOverloads
    constructor(
            token: NonFungibleToken,
            participantSessions: List<FlowSession>,
            observerSessions: List<FlowSession> = emptyList()
    ) : this(listOf(token), participantSessions, observerSessions)

    /** Issue a single [NonFungibleToken] to self with no observers. */
    constructor(token: NonFungibleToken) : this(listOf(token), emptyList(), emptyList())

    @Suspendable
    override fun call(): SignedTransaction {
        participantSessions.forEach { it.send(TransactionRole.PARTICIPANT) }
        observerSessions.forEach { it.send(TransactionRole.OBSERVER) }
        // Request new keys pairs from all proposed token holders.
        val confidentialTokens = subFlow(ConfidentialTokensFlow(tokens, participantSessions))
        // Issue tokens using the existing participantSessions.
        return subFlow(IssueTokensFlow(confidentialTokens, participantSessions, observerSessions))
    }
}
```

### Create evolvable tokens

Use this flow to create and update evolvable token states.

Properties in this flow:

 * `transactionStates` - a list of state to create evolvable token types with.
 * `participantSessions` - a list of sessions for participants in the evolvable token types.
 * `observerSessions` - a list of sessions for any observers to the create observable token transaction.
```
package com.r3.corda.lib.tokens.workflows.flows.evolvable
import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.states.EvolvableTokenType
import com.r3.corda.lib.tokens.workflows.internal.flows.finality.ObserverAwareFinalityFlow
import net.corda.core.contracts.TransactionState
import net.corda.core.flows.CollectSignaturesFlow
import net.corda.core.flows.FlowLogic
import net.corda.core.flows.FlowSession
import net.corda.core.identity.AbstractParty
import net.corda.core.identity.Party
import net.corda.core.serialization.CordaSerializable
import net.corda.core.transactions.SignedTransaction
import net.corda.core.transactions.TransactionBuilder
```
```Kotlin
class CreateEvolvableTokensFlow
@JvmOverloads
constructor(
        val transactionStates: List<TransactionState<EvolvableTokenType>>,
        val participantSessions: List<FlowSession>,
        val observerSessions: List<FlowSession> = emptyList()
) : FlowLogic<SignedTransaction>() {
    @JvmOverloads
    constructor(transactionState: TransactionState<EvolvableTokenType>, participantSessions: List<FlowSession>, observerSessions: List<FlowSession> = emptyList()) :
            this(listOf(transactionState), participantSessions, observerSessions)

    @CordaSerializable
    data class Notification(val signatureRequired: Boolean = false)

    private val evolvableTokens = transactionStates.map { it.data }

    @Suspendable
    override fun call(): SignedTransaction {
        checkLinearIds(transactionStates)
        // TODO what about... preferred notary
        checkSameNotary()
        val transactionBuilder = TransactionBuilder(transactionStates.first().notary) // todo

        // Create a transaction which updates the ledger with the new evolvable tokens.
        transactionStates.forEach {
            addCreateEvolvableToken(transactionBuilder, it)
        }

        // Sign the transaction proposal
        val ptx: SignedTransaction = serviceHub.signInitialTransaction(transactionBuilder)

        // Gather signatures from other maintainers
        // Check that we have sessions with all maitainers but not with ourselves
        val otherMaintainerSessions = participantSessions.filter { it.counterparty in evolvableTokens.otherMaintainers(ourIdentity) }
        otherMaintainerSessions.forEach { it.send(Notification(signatureRequired = true)) }
        val stx = subFlow(CollectSignaturesFlow(
                partiallySignedTx = ptx,
                sessionsToCollectFrom = otherMaintainerSessions
        ))
        // Finalise with all participants, including maintainers, participants, and subscribers (via distribution list)
        val wellKnownObserverSessions = participantSessions.filter { it.counterparty in wellKnownObservers }
        val allObserverSessions = (wellKnownObserverSessions + observerSessions).toSet()
        allObserverSessions.forEach { it.send(Notification(signatureRequired = false)) }
        return subFlow(ObserverAwareFinalityFlow(signedTransaction = stx, allSessions = otherMaintainerSessions + allObserverSessions))
    }

    private fun checkLinearIds(transactionStates: List<TransactionState<EvolvableTokenType>>) {
        check(transactionStates.map { it.data.linearId }.toSet().size == transactionStates.size) {
            "Shouldn't create evolvable tokens with the same linearId."
        }
    }

    private fun checkSameNotary() {
        check(transactionStates.map { it.notary }.toSet().size == 1) {
            "All states should have the same notary"
        }
    }

    // TODO Refactor it more.
    private val otherObservers
        get(): Set<AbstractParty> {
            return evolvableTokens.participants().minus(evolvableTokens.maintainers()).minus(this.ourIdentity)
        }

    private val wellKnownObservers
        get(): List<Party> {
            return otherObservers.map { serviceHub.identityService.wellKnownPartyFromAnonymous(it)!! }
        }
}
```

### Update evolvable token


Use this flow to update an existing evolvable token type which is already recorded on the ledger. This is an **In-line** flow, which means it must be invoked with a `subFlow` call from an Initiating Flow.

Properties in this flow:

 * `oldStateAndRef` - the existing evolvable token type to update.
 * `newState` - the new version of the evolvable token type.
 * `participantSessions` - a list of sessions for participants in the evolvable token types.
 * `observerSessions` - a list of sessions for any observers to the create observable token transaction.

```
package com.r3.corda.lib.tokens.workflows.flows.evolvable

import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.states.EvolvableTokenType
import com.r3.corda.lib.tokens.workflows.internal.flows.finality.ObserverAwareFinalityFlow
import net.corda.core.contracts.StateAndRef
import net.corda.core.flows.CollectSignaturesFlow
import net.corda.core.flows.FlowLogic
import net.corda.core.flows.FlowSession
import net.corda.core.identity.AbstractParty
import net.corda.core.identity.Party
import net.corda.core.serialization.CordaSerializable
import net.corda.core.transactions.SignedTransaction
import net.corda.core.transactions.TransactionBuilder
```
```Kotlin
class UpdateEvolvableTokenFlow @JvmOverloads constructor(
        val oldStateAndRef: StateAndRef<EvolvableTokenType>,
        val newState: EvolvableTokenType,
        val participantSessions: List<FlowSession>,
        val observerSessions: List<FlowSession> = emptyList()
) : FlowLogic<SignedTransaction>() {
    /**
     * Simple notification class to inform counterparties of their role. In this instance, informs participants if
     * they are required to sign the command. This is intended to allow maintainers to sign commands while participants
     * and other observers merely finalise the transaction.
     */
    @CordaSerializable
    data class Notification(val signatureRequired: Boolean = false)

    @Suspendable
    override fun call(): SignedTransaction {
        require(ourIdentity in oldStateAndRef.state.data.maintainers) {
            "This flow can only be started by existing maintainers of the EvolvableTokenType."
        }

        // Create a transaction which updates the ledger with the new evolvable token.
        // The tokenHolders listed as maintainers in the old state should be the signers.
        val utx = addUpdateEvolvableToken(
                TransactionBuilder(notary = oldStateAndRef.state.notary),
                oldStateAndRef,
                newState
        )

        // Sign the transaction proposal (creating a partially signed transaction, or ptx)
        val ptx: SignedTransaction = serviceHub.signInitialTransaction(utx)

        // Gather signatures from other maintainers
        val otherMaintainerSessions = participantSessions.filter { it.counterparty in evolvableTokens.otherMaintainers(ourIdentity) }
        otherMaintainerSessions.forEach { it.send(Notification(signatureRequired = true)) }
        val stx = subFlow(CollectSignaturesFlow(
                partiallySignedTx = ptx,
                sessionsToCollectFrom = otherMaintainerSessions
        ))

        // Distribute to all observers, including maintainers, participants, and subscribers (via distribution list)
        val wellKnownObserverSessions = participantSessions.filter { it.counterparty in wellKnownObservers }
        val allObserverSessions = (wellKnownObserverSessions + observerSessions).toSet()
        observerSessions.forEach { it.send(Notification(signatureRequired = false)) }
        return subFlow(ObserverAwareFinalityFlow(signedTransaction = stx, allSessions = otherMaintainerSessions + allObserverSessions))
    }

    private val oldState get() = oldStateAndRef.state.data
    private val evolvableTokens = listOf(oldState, newState)

    private fun otherObservers(subscribers: Set<Party>): Set<AbstractParty> {
        return (evolvableTokens.participants() + subscribers).minus(evolvableTokens.maintainers()).minus(this.ourIdentity)
    }

    private val wellKnownObservers
        get(): List<Party> {
            return otherObservers(subscribersForState(newState, serviceHub)).map { serviceHub.identityService.wellKnownPartyFromAnonymous(it)!! }
        }
}
```

### Move tokens

Use this general, in-line flow to move any type of tokens. This flow builds a transaction containing input and output states passed as parameters. You must ensure all checks are done before calling this flow as a subflow.

You can only call this flow for one `TokenType` at a time. If you need to handle multiple token types in one transaction, create a new flow, calling `addMoveTokens` for each token type.

Parameters for this flow:

* `inputs` - list of token inputs to move.
* `outputs` - list of result token outputs.
* `participantSessions` - session with the participants of move tokens transaction.
* `observerSessions` - session with optional observers of the redeem transaction.

```
package com.r3.corda.lib.tokens.workflows.flows.move

import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.states.AbstractToken
import com.r3.corda.lib.tokens.contracts.types.TokenType
import net.corda.core.contracts.StateAndRef
import net.corda.core.flows.FlowSession
import net.corda.core.transactions.TransactionBuilder
```

```Kotlin
class MoveTokensFlow
@JvmOverloads
constructor(
        val inputs: List<StateAndRef<AbstractToken>>,
        val outputs: List<AbstractToken>,
        override val participantSessions: List<FlowSession>,
        override val observerSessions: List<FlowSession> = emptyList()
) : AbstractMoveTokensFlow() {
    @JvmOverloads
    constructor(
            input: StateAndRef<AbstractToken>,
            output: AbstractToken,
            participantSessions: List<FlowSession>,
            observerSessions: List<FlowSession> = emptyList()
    ) : this(listOf(input), listOf(output), participantSessions, observerSessions)

    @Suspendable
    override fun addMove(transactionBuilder: TransactionBuilder) {
        addMoveTokens(transactionBuilder, inputs, outputs)
    }
}
```

### Move tokens with confidential keys

Use this responder flow to confidentially move tokens flows: `ConfidentialMoveNonFungibleTokensFlow` and `ConfidentialMoveFungibleTokensFlow`.

```
 package com.r3.corda.lib.tokens.workflows.flows.move

 import co.paralleluniverse.fibers.Suspendable
 import com.r3.corda.lib.tokens.workflows.flows.confidential.ConfidentialTokensFlowHandler
 import com.r3.corda.lib.tokens.workflows.internal.flows.finality.ObserverAwareFinalityFlowHandler
 import com.r3.corda.lib.tokens.workflows.internal.flows.finality.TransactionRole
 import net.corda.core.flows.FlowLogic
 import net.corda.core.flows.FlowSession
 import net.corda.core.utilities.unwrap
```

```Kotlin
class ConfidentialMoveTokensFlowHandler(val otherSession: FlowSession) : FlowLogic<Unit>() {
    @Suspendable
    override fun call() {
        val role = otherSession.receive<TransactionRole>().unwrap { it }
        if (role == TransactionRole.PARTICIPANT) {
            subFlow(ConfidentialTokensFlowHandler(otherSession))
        }
        subFlow(ObserverAwareFinalityFlowHandler(otherSession))
    }
}
```

### Redeem tokens

Use this general in-lined flow to redeem any type of tokens with the issuer.

The flow must be be called on tokens owner's side.

You can see in the flow below that token selection and change output generation should be done beforehand. This flow builds a transaction containing those states, but all checks should have be done before calling this flow as a subflow.

You can can only call this flow for one `TokenType` at a time. To handle multiple token types in one transaction, you must create a new flow, calling `addTokensToRedeem` for each token type.

Parameters in this flow:

 * `inputs` - list of token inputs to redeem.
 * `changeOutput` - possible change output to be paid back to the tokens owner.
 * `issuerSession` - session with the issuer of the tokens.
 * `observerSessions` - session with optional observers of the redeem transaction.

```
package com.r3.corda.lib.tokens.workflows.flows.redeem

import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.states.AbstractToken
import com.r3.corda.lib.tokens.contracts.types.TokenType
import net.corda.core.contracts.StateAndRef
import net.corda.core.flows.FlowSession
import net.corda.core.transactions.TransactionBuilder
```

```Kotlin
///called on the owner side.
class RedeemTokensFlow
@JvmOverloads
constructor(
        val inputs: List<StateAndRef<AbstractToken>>,
        val changeOutput: AbstractToken?,
        override val issuerSession: FlowSession,
        override val observerSessions: List<FlowSession> = emptyList()
) : AbstractRedeemTokensFlow() {
    @Suspendable
    override fun generateExit(transactionBuilder: TransactionBuilder) {
        addTokensToRedeem(transactionBuilder, inputs, changeOutput)
    }
}
```

### Redeem token with confidential keys

Use this version of `RedeemFungibleTokensFlow` to allow a party with confidential identity redeem a token. There is no `NonFungibleToken` version of this flow, because there is no output paid. Identities are synchronised during normal redeem call.

Parameters in this flow:

 * `amount` - amount of token to redeem.
 * `issuerSession` - session with the issuer tokens should be redeemed with.
 * `observerSessions` - optional sessions with the observer nodes, to witch the transaction will be broadcasted.
 * `additionalQueryCriteri` - a additional criteria for token selection.
 * `changeHolder` - optional change key, if using accounts you should generate the change key prior to calling this flow then pass it in to the flow via this parameter.

```
package com.r3.corda.lib.tokens.workflows.flows.redeem

import co.paralleluniverse.fibers.Suspendable
import com.r3.corda.lib.tokens.contracts.types.TokenType
import net.corda.core.contracts.Amount
import net.corda.core.flows.FlowLogic
import net.corda.core.flows.FlowSession
import net.corda.core.identity.AbstractParty
import net.corda.core.identity.AnonymousParty
import net.corda.core.node.services.vault.QueryCriteria
import net.corda.core.transactions.SignedTransaction
```

```
class ConfidentialRedeemFungibleTokensFlow
@JvmOverloads
constructor(
        val amount: Amount<TokenType>,
        val issuerSession: FlowSession,
        val observerSessions: List<FlowSession> = emptyList(),
        val additionalQueryCriteria: QueryCriteria? = null,
        val changeHolder: AbstractParty? = null
) : FlowLogic<SignedTransaction>() {
    @Suspendable
    override fun call(): SignedTransaction {
        // If a change holder key is not specified then one will be created for you. NB. If you want to use accounts
        // with tokens, then you must generate and allocate the key to an account up-front and pass the key in as the
        // "changeHolder".
        val confidentialHolder = changeHolder ?: let {
            val key = serviceHub.keyManagementService.freshKey()
            AnonymousParty(key)
        }
        return subFlow(RedeemFungibleTokensFlow(
                amount = amount,
                issuerSession = issuerSession,
                changeHolder = confidentialHolder,  // This will never be null.
                observerSessions = observerSessions,
                additionalQueryCriteria = additionalQueryCriteria
        ))
    }
}
```

## Install the Tokens SDK

Depending on your plan for issuing tokens onto your network - whether you are ready to deploy tokens in an enterprise scenario or experimenting - there are two different ways to install the Tokens SDK:

* [Use the kotlin Tokens SDK template](###get-started-using-the-kotlin-token-sdk-template) template to get started and issue tokens locally. This is a great way to learn about the Tokens SDK through practical application, but may not be suitable for your enterprise deployment.
* [Clone the latest repo](###build-token-sdk-against-corda-release-branch).


For each of the these steps, follow the instructions below.

### Create a local testing environment using the Kotlin Tokens SDK template

To get started quickly with the Tokens SDK, use the **Tokens template** which is a branch on the kotlin version of the **CorDapp template**.

To use the tokens template:

1. Use the following commands to clone the Kotlin CorDapp template, and checkout the token-template branch:

```
    git clone http://github.com/corda/cordapp-template-kotlin
    cd cordapp-template-kotlin
    git checkout token-template
```

2. Open the token-template branch of the repo with your preferred coding tool. The recommended tool is IntelliJ because it works well with Gradle.

You now have a template repo with the Tokens SDK dependencies
included and some example code to illustrate how to use the Tokens SDK.

**To test your Tokens SDK set up locally:**

1. Use command line to create three nodes:

    .```
    /gradlew clean deployNodes
    ./build/nodes/runnodes
    ```

2. Issue some currency tokens from `PartyA` to `PartyB` from Party A's shell with the following command:

    ```
    start ExampleFlowWithFixedToken currency: GBP, amount: 100, recipient: PartyB
    ```

See the token template code [here](https://github.com/corda/cordapp-template-kotlin/tree/token-template)
for more information.

### Build Tokens SDK against Corda release branch

You can build the Tokens SDK against the master branch with the following commands:

```
git clone https://github.com/corda/token-sdk.git
git fetch
git checkout origin master
```

{{< note >}}
Checkout the version of Corda you wish to install. In the example above master is used.
{{< /note >}}

Then run `./gradlew clean install` from the root directory.

### Add Tokens SDK dependencies to an existing CorDapp

1. Add a variable for the tokens release group and the version you
wish to use. Set the Corda version to the one you have installed locally:

```
    buildscript {
        ext {
            tokens_release_version = '1.2'
            tokens_release_group = 'com.r3.corda.lib.tokens'
        }
    }
```

2.  Add the tokens development artifactory repository to the
list of repositories for your project:

```
    repositories {
        maven { url 'https://ci-artifactory.corda.r3cev.com/artifactory/corda-lib' }
        maven { url 'https://ci-artifactory.corda.r3cev.com/artifactory/corda-lib-dev' }
    }
```

3. Add the `token-sdk` dependencies to the `dependencies` block
in each module of your CorDapp. For contract modules add:

    cordaCompile "$tokens_release_group:tokens-contracts:$tokens_release_version"

4. In your workflow `build.gradle` add:

    cordaCompile "$tokens_release_group:tokens-workflows:$tokens_release_version"

5. To use the `deployNodes` task, add the following dependencies to your root `build.gradle` file:

    cordapp "$tokens_release_group:tokens-contracts:$tokens_release_version"
    cordapp "$tokens_release_group:tokens-workflows:$tokens_release_version"

6. Add the following to the `deployNodes` task with the following syntax:

```
    nodeDefaults {
        projectCordapp {
            deploy = false
        }
        cordapp("$tokens_release_group:tokens-contracts:$tokens_release_version")
        cordapp("$tokens_release_group:tokens-workflows:$tokens_release_version")
    }
```
You have installed the Tokens SDK.
