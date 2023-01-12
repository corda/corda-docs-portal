---
date: '2021-07-07T12:00:00Z'
menu:
  corda-enterprise-4-10:
    identifier: corda-enterprise-4-10-financial-model
    name: "Financial model"
    parent: corda-enterprise-4-10-component-library-index
tags:
- financial
- model
title: Financial model
weight: 20
---




# Financial model

Corda includes a standard library of data types used in financial applications and contract state objects.
These provide a common language for states and contracts.

## Glossary

**Fungible**

If you could exchange an asset for an identical asset, and the asset can be split and merged, then it is fungible. For example, US dollars are fungible because you could exchange a $5 bill for another $5 bill, which you could break down into five $1 bills. However, there is only one *Mona Lisa*, which cannot be subdivided - so the *Mona Lisa* is not a fungible asset.


**Token**

A type used to define the underlying financial product in a transaction.

## Amount

The [Amount](../../../../../en/api-ref/corda/4.10/community/kotlin/corda/net.corda.core.contracts/-amount/index.html) class represents an amount of
a fungible asset. It is a generic class which wraps around the token. For example, the `Amount` could be:
* The standard JDK type `Currency`.
* An `Issued` instance.
* A more complex asset type, such as an obligation contract issuance definition. The issuance definition contains a token definition, which defines the currency the obligation must be settled in. Custom token types should implement `TokenizableAssetInfo` to allow the
`Amount` conversion helpers `fromDecimal` and `toDecimal` to calculate the correct `displayTokenSize`.


Here are some examples:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
// A quantity of some specific currency like pounds, euros, dollars etc.
Amount<Currency>
// A quantity of currency that is issued by a specific issuer, for instance central bank vs other bank dollars
Amount<Issued<Currency>>
// A quantity of a product governed by specific obligation terms
Amount<Obligation.Terms<P>>
```
{{% /tab %}}

{{< /tabs >}}

`Amount` represents quantities as integers. You cannot use `Amount` to represent negative quantities
or fractional quantities—use a different type, typically `BigDecimal`.
For currencies, the quantity represents the smallest integer amount for that currency, such as cents.
Other assets are more flexible—the quantity could be 1,000 tons of coal or kilowatt hours. You define how the amounts display using the precise conversion ratio in the `displayTokenSize` property, which is the `BigDecimal` numeric representation of
a single token. `Amount` also defines methods to perform overflow/underflow-checked addition and subtraction.
These are operator overloads in Kotlin—you can use them as regular methods from Java). Perform more complex calculations in `BigDecimal`, then convert them back to `Amount` to make sure the rounding and token conservation works as expected.

`Issued` refers to any countable product—for example, cash, a cash-like item, or assets—and an associated `PartyAndReference` that describes the issuer of that product.
An issued product typically follows a lifecycle which includes issuance, movement, and an exit from the ledger (for example,
see the `Cash` contract and its associated *state* and *commands*).

To represent movements of `Amount` tokens use the `AmountTransfer` type, which records the quantity and perspective
of a transfer. Positive values will indicate a movement of tokens from a `source`, for example, a `Party` or `CompositeKey`
to a `destination`. Negative values can be used to indicate a retrograde motion of tokens from `destination`
to `source`. `AmountTransfer` supports addition (as a Kotlin operator, or Java method) to provide netting
and aggregation of flows. The `apply` method can be used to process a list of attributed `Amount` objects in a
`List<SourceAndAmount>` to carry out the actual transfer.


## Financial states

In addition to the common state types, several interfaces extend `ContractState` to model financial states such as:

* `LinearState`: A state that has a unique identifier beyond its `StateRef`, which it carries through state transitions.
`LinearState`s cannot be duplicated, merged, or split in a transaction: only continued or deleted. Use `LinearState`s to model non-fungible items like a specific deal, or an asset that can’t be
split, like an airplane.
* `DealState`: A `LinearState` representing an agreement between two or more parties. Intended to simplify implementing generic
protocols that manipulate many agreement types.
* `FungibleAsset`: Used for contract states that represent countable, fungible assets issued by a
specific party. States contain assets which are equivalent (such as cash of the same currency), so records of their existence
can be merged or split as needed where the issuer is the same. For example, US dollars issued by the Federal Reserve are fungible and
countable (in cents), barrels of oil are fungible and countable (oil from two small containers can be poured into one large
container), shares of the same class in a specific company are fungible and countable, and so on.
This diagram illustrates the complete contract state hierarchy:

{{< figure alt="financialContractStateModel" width=80% zoom="/en/images/financialContractStateModel.png" >}}
Corda provides two packages: a core library and a finance model-specific library.
You can re-use or extend the finance types directly, or write your own by extending the base types from the core library.
