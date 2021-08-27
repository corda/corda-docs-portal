---
date: 2021-08-24
section_menu: tutorials
menu:
  tutorials:
    parent: corda-5-building-template-cordapp-intro
    name: Modify the state
    weight: 150
    identifier: corda-5-template-cordapp-modify-state
title: Modify the state
---

In Corda, facts on the blockchain are represented as states. States are instances of classes that implement [`ContractState`](https://docs.corda.net/docs/corda-os/4.8/api-states.html#contractstate).  

This tutorial shows you how to modify the template state to define a new state type that records probes being sent between two parties.

## Before you start

Before you start modifying the template state, familiarize yourself with:

* [Key concepts: States](XXX)
* [API: States](https://docs.corda.net/docs/corda-os/4.8/api-states.html#contractstate)

<!-- In some places I'm adding full links to 4.8 docs. These must be replaced with relative links before release, but I wanted to note the pages for now.  -->

## Define the `ProbeState`

The `ProbeState` is used to record probes being sent between two celestial bodies on the ledger. This state contains the following information:

{{< table >}}
| Parameter       | Definition                                                                                             | Type      |
|:--------------- |:------------------------------------------------------------------------------------------------------ |:--------- |
| `message`       | A message to send with the probe.                                                                      | `Party`  |    
| `target`        | The party being visited by the probe and returning data.                                               | `Party`  |  
| `launcher`      | The party launching the probe.                                                                         | `String`  |  
| `planetaryOnly` | Determines whether the probe is only able to travel to planets, or if it can visit any celestial body. | `Boolean` |
{{< /table >}}

### Open the `TemplateState`

You will be modifying the `TemplateState` file in this tutorial. Open the file in IntelliJ.

<!-- Explain in small chunks, with code snippets in each section, how to define the state. I'm following the general steps from 4.8, but I don't think all of these things are present in the `ProbeState`. -->

### Add the `@BelongsToContract` annotation

The first thing you should do when writing a state is add the `@BelongsToContract` annotation. This annotation establishes the relationship between a state and a contract. Without this, your state does not know which contract is used to verify it.

1. If you've copied in the template state, change the `TemplateContract::class` to `ProbeContract::class`.

2. Add the annotation `@BelongsToContract(ProbeContract::class)` to your state.

This what your code should look like so far:

```kotlin
@BelongsToContract(ProbeContract::class)
```

{{< note >}}
Adding this annotation will trigger an error in IntelliJ because you haven't created the `ProbeContract` yet. Ignore this error for now - you will add the contract class in the [Modify the contract](modify-contract.md) tutorial.
{{< /note >}}

When naming your CorDapp files, it's best practice to match your contract and state names. In this case the state is called `ProbeState`, so the contract is called `ProbeContract`. Follow this naming convention when you write an original CorDapp to avoid confusion.

### Implement the state and add variables.

The next line of code you add defines the type of `ContractState` you implement with the `ProbeState` class. Add this line to ensure that Corda recognizes the `ProbeState` as a state.

In this case, use a `LinearState` to tie the `ProbeState` to a `LinearID`. Add your variables now too.

1. Add the public class `ProbeState` implementing a `LinearState`.

2. Add state data variables: `message` and `planetaryOnly`.

3. Add the parties involved: `launcher` and `target`.

This is what your code should look like now:

```kotlin
@BelongsToContract(ProbeContract::class)

    // State Data
    val message: String,
    val planetaryOnly: Boolean,

    //  Parties Involved
    val launcher: Party,
    val target: Party,

    override val linearId: UniqueIdentifier = UniqueIdentifier()
) :
```

### Add imports

## Outcome

You have now created the `ProbeState`. Your code should look something like this:

<!-- Insert code sample.-->

## Next steps

Follow the [Modify the contract](modify-contract.md) tutorial to continue on this learning path.
