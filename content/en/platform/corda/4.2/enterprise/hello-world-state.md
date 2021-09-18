---
aliases:
- /releases/4.2/hello-world-state.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-hello-world-state
    parent: corda-enterprise-4-2-hello-world-introduction
    weight: 1020
tags:
- state
title: Writing the state
---




# Writing the state

In Corda, shared facts on the blockchain are represented as states. Our first task will be to define a new state type to
represent an IOU.


## The ContractState interface

A Corda state is any instance of a class that implements the `ContractState` interface. The `ContractState`
interface is defined as follows:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
interface ContractState {
    // The list of entities considered to have a stake in this state.
    val participants: List<AbstractParty>
}
```
{{% /tab %}}

{{< /tabs >}}

We can see that the `ContractState` interface has a single field, `participants`. `participants` is a list of the
entities for which this state is relevant.

Beyond this, our state is free to define any fields, methods, helpers or inner classes it requires to accurately
represent a given type of shared fact on the blockchain.

{{< note >}}
The first thing you’ll probably notice about the declaration of `ContractState` is that its not written in Java
or another common language. The core Corda platform, including the interface declaration above, is entirely written
in Kotlin.

Learning some Kotlin will be very useful for understanding how Corda works internally, and usually only takes an
experienced Java developer a day or so to pick up. However, learning Kotlin isn’t essential. Because Kotlin code
compiles to JVM bytecode, CorDapps written in other JVM languages such as Java can interoperate with Corda.

If you do want to dive into Kotlin, there’s an official
[getting started guide](https://kotlinlang.org/docs/tutorials/), and a series of
[Kotlin Koans](https://kotlinlang.org/docs/tutorials/koans.html).

{{< /note >}}

## Modelling IOUs

How should we define the `IOUState` representing IOUs on the blockchain? Beyond implementing the `ContractState`
interface, our `IOUState` will also need properties to track the relevant features of the IOU:


* The value of the IOU
* The lender of the IOU
* The borrower of the IOU

There are many more fields you could include, such as the IOU’s currency, but let’s ignore those for now. Adding them
later is often as simple as adding an additional property to your class definition.


## Defining IOUState

Let’s get started by opening `TemplateState.java` (for Java) or `StatesAndContracts.kt` (for Kotlin) and updating
`TemplateState` to define an `IOUState`:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// Add this import:
import net.corda.core.identity.Party

// Replace TemplateState's definition with:
class IOUState(val value: Int,
               val lender: Party,
               val borrower: Party) : ContractState {
    override val participants get() = listOf(lender, borrower)
}

```
{{% /tab %}}



{{% tab name="java" %}}
```java
// Add this import:
import net.corda.core.identity.Party;

// Replace TemplateState's definition with:
public class IOUState implements ContractState {
    private final int value;
    private final Party lender;
    private final Party borrower;

    public IOUState(int value, Party lender, Party borrower) {
        this.value = value;
        this.lender = lender;
        this.borrower = borrower;
    }

    public int getValue() {
        return value;
    }

    public Party getLender() {
        return lender;
    }

    public Party getBorrower() {
        return borrower;
    }

    @Override
    public List<AbstractParty> getParticipants() {
        return Arrays.asList(lender, borrower);
    }
}

```
{{% /tab %}}




[IOUState.kt](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/kotlin/net/corda/docs/kotlin/tutorial/helloworld/IOUState.kt) | [IOUState.java](https://github.com/corda/corda/blob/release/os/4.1/docs/source/example-code/src/main/java/net/corda/docs/java/tutorial/helloworld/IOUState.java) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

If you’re following along in Java, you’ll also need to rename `TemplateState.java` to `IOUState.java`.

To define `IOUState`, we’ve made the following changes:


* We’ve renamed the `TemplateState` class to `IOUState`
* We’ve added properties for `value`, `lender` and `borrower`, along with the required getters and setters in
Java:
    * `value` is of type `int` (in Java)/`Int` (in Kotlin)
    * `lender` and `borrower` are of type `Party`
        * `Party` is a built-in Corda type that represents an entity on the network




* We’ve overridden `participants` to return a list of the `lender` and `borrower`
    * `participants` is a list of all the parties who should be notified of the creation or consumption of this state



The IOUs that we issue onto a ledger will simply be instances of this class.


## Progress so far

We’ve defined an `IOUState` that can be used to represent IOUs as shared facts on a ledger. As we’ve seen, states in
Corda are simply classes that implement the `ContractState` interface. They can have any additional properties and
methods you like.

All that’s left to do is write the `IOUFlow` that will allow a node to orchestrate the creation of a new `IOUState`
on the blockchain, while only sharing information on a need-to-know basis.


## What about the contract?

If you’ve read the white paper or Key Concepts section, you’ll know that each state has an associated contract that
imposes invariants on how the state evolves over time. Including a contract isn’t crucial for our first CorDapp, so
we’ll just use the empty `TemplateContract` and `TemplateContract.Commands.Action` command defined by the template
for now. In the next tutorial, we’ll implement our own contract and command.
