---
date: '2023-01-12'
menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-tutorial-tear-offs
    parent: corda-enterprise-4-9-supplementary-tutorials-index
    weight: 180
tags:
- tutorial
- tear
- offs
title: Defining transaction tear-offs
---




# Defining transaction tear-offs

This tutorial will take you through the steps involved in defining a transaction tear-off.

## Introduction

A transaction tear-off is a form of filtered transaction, in which the transaction proposer(s) uses a nested Merkle tree approach to “tear off” any parts of the transaction that the oracle/notary doesn’t need to see before presenting it to them for signing. Transaction tear-offs are used to hide transaction components for privacy purposes. With a transaction tear-off, oracles and non-validating notaries can only see their “related” transaction components, but not the full transaction details.

## Filtering the transaction fields

Suppose we want to construct a transaction that includes commands containing interest rate fix data as in
[Writing oracle services]({{< relref "oracles.md" >}}). Before sending the transaction to the oracle to obtain its signature, we need to filter out every part
of the transaction except for the `Fix` commands.

To do so, we need to create a filtering function that specifies which fields of the transaction should be included.
Each field will only be included if the filtering function returns *true* when the field is passed in as input.

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
val filtering = Predicate<Any> {
    when (it) {
        is Command<*> -> oracle.owningKey in it.signers && it.value is Fix
        else -> false
    }
}

```
{{% /tab %}}
{{< /tabs >}}

## Constructing a filtered transaction

We can now use our filtering function to construct a `FilteredTransaction`:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
val ftx: FilteredTransaction = stx.buildFilteredTransaction(filtering)

```
{{% /tab %}}
{{< /tabs >}}

In the oracle example, this step takes place in `RatesFixFlow` by overriding the `filtering` function. See
[Using an oracle]({{< relref "oracles.md#using-an-oracle" >}}).

Both `WireTransaction` and `FilteredTransaction` inherit from `TraversableTransaction`, so access to the
transaction components is exactly the same. Note that unlike `WireTransaction`,
`FilteredTransaction` only holds data that we wanted to reveal (after filtering).

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
// Direct access to included commands, inputs, outputs, attachments etc.
val cmds: List<Command<*>> = ftx.commands
val ins: List<StateRef> = ftx.inputs
val timeWindow: TimeWindow? = ftx.timeWindow
// ...

```
{{% /tab %}}

{{< /tabs >}}

## Implementing transaction signing

The following code snippet is taken from `NodeInterestRates.kt` and implements a signing part of an Oracle.

```kotlin
fun sign(ftx: FilteredTransaction): TransactionSignature {
    ftx.verify()
    // Performing validation of obtained filtered components.
    fun commandValidator(elem: Command<*>): Boolean {
        require(services.myInfo.legalIdentities.first().owningKey in elem.signers && elem.value is Fix) {
            "Oracle received unknown command (not in signers or not Fix)."
        }
        val fix = elem.value as Fix
        val known = knownFixes[fix.of]
        if (known == null || known != fix)
            throw UnknownFix(fix.of)
        return true
    }

    fun check(elem: Any): Boolean {
        return when (elem) {
            is Command<*> -> commandValidator(elem)
            else -> throw IllegalArgumentException("Oracle received data of different type than expected.")
        }
    }

    require(ftx.checkWithFun(::check))
    ftx.checkCommandVisibility(services.myInfo.legalIdentities.first().owningKey)
    // It all checks out, so we can return a signature.
    //
    // Note that we will happily sign an invalid transaction, as we are only being presented with a filtered
    // version so we can't resolve or check it ourselves. However, that doesn't matter much, as if we sign
    // an invalid transaction the signature is worthless.
    return services.createSignature(ftx, services.myInfo.legalIdentities.first().owningKey)
}

```

[NodeInterestRates.kt](https://github.com/corda/corda/blob/release/os/4.9/samples/irs-demo/cordapp/workflows-irs/src/main/kotlin/net.corda.irs/api/NodeInterestRates.kt)

{{< note >}}
The way the `FilteredTransaction` is constructed ensures that after signing of the root hash, it is impossible to add or remove
components (leaves). However, it can happen that having transaction with multiple commands one party reveals only subset of them to the Oracle.
As signing is done now over the Merkle root hash, the service signs all commands of a given type, even though it didn’t see
all of them. In the case, however, where all of the commands should be visible to an oracle, you can add `ftx.checkAllComponentsVisible(COMMANDS_GROUP)` before invoking `ftx.verify`.
`checkAllComponentsVisible` uses a sophisticated, underlying partial Merkle tree check to guarantee that all of the components of a particular group that existed in the original `WireTransaction` are included in the received `FilteredTransaction`.
{{< /note >}}
