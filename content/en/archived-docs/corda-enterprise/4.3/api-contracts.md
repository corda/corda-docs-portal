---
aliases:
- /releases/4.3/api-contracts.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-api-contracts
    parent: corda-enterprise-4-3-corda-api
    weight: 300
tags:
- api
- contracts
title: 'API: Contracts'
---




# API: Contracts

{{< note >}}
Before reading this page, you should be familiar with the key concepts of [Contracts](key-concepts-contracts.md).

{{< /note >}}


## Contract

Contracts are classes that implement the `Contract` interface. The `Contract` interface is defined as follows:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
/**
 * Implemented by a program that implements business logic on the shared ledger. All participants run this code for
 * every [net.corda.core.transactions.LedgerTransaction] they see on the network, for every input and output state. All
 * contracts must accept the transaction for it to be accepted: failure of any aborts the entire thing. The time is taken
 * from a trusted time-window attached to the transaction itself i.e. it is NOT necessarily the current time.
 *
 * TODO: Contract serialization is likely to change, so the annotation is likely temporary.
 */
@KeepForDJVM
@CordaSerializable
interface Contract {
    /**
     * Takes an object that represents a state transition, and ensures the inputs/outputs/commands make sense.
     * Must throw an exception if there's a problem that should prevent state transition. Takes a single object
     * rather than an argument so that additional data can be added without breaking binary compatibility with
     * existing contract code.
     */
    @Throws(IllegalArgumentException::class)
    fun verify(tx: LedgerTransaction)
}

```
{{% /tab %}}




[Structures.kt](https://github.com/corda/corda/blob/release/os/4.3/core/src/main/kotlin/net/corda/core/contracts/Structures.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

`Contract` has a single method, `verify`, which takes a `LedgerTransaction` as input and returns
nothing. This function is used to check whether a transaction proposal is valid, as follows:


* We gather together the contracts of each of the transaction’s input and output states
* We call each contract’s `verify` function, passing in the transaction as an input
* The proposal is only valid if none of the `verify` calls throw an exception

`verify` is executed in a sandbox:


* It does not have access to the enclosing scope
* The libraries available to it are whitelisted to disallow:
* Network access
* I/O such as disk or database access
* Sources of randomness such as the current time or random number generators

This means that `verify` only has access to the properties defined on `LedgerTransaction` when deciding whether a
transaction is valid.

Here are the two simplest `verify` functions:


* A  `verify` that **accepts** all possible transactions:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
override fun verify(tx: LedgerTransaction) {
    // Always accepts!
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
@Override
public void verify(LedgerTransaction tx) {
    // Always accepts!
}
```
{{% /tab %}}

{{< /tabs >}}


* A `verify` that **rejects** all possible transactions:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
override fun verify(tx: LedgerTransaction) {
    throw IllegalArgumentException("Always rejects!")
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
@Override
public void verify(LedgerTransaction tx) {
    throw new IllegalArgumentException("Always rejects!");
}
```
{{% /tab %}}

{{< /tabs >}}


## LedgerTransaction

The `LedgerTransaction` object passed into `verify` has the following properties:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
        /** The resolved input states which will be consumed/invalidated by the execution of this transaction. */
        override val inputs: List<StateAndRef<ContractState>>,
        /** The outputs created by the transaction. */
        override val outputs: List<TransactionState<ContractState>>,
        /** Arbitrary data passed to the program of each input state. */
        val commands: List<CommandWithParties<CommandData>>,
        /** A list of [Attachment] objects identified by the transaction that are needed for this transaction to verify. */
        val attachments: List<Attachment>,
        /** The hash of the original serialised WireTransaction. */
        override val id: SecureHash,
        /** The notary that the tx uses, this must be the same as the notary of all the inputs, or null if there are no inputs. */
        override val notary: Party?,
        /** The time window within which the tx is valid, will be checked against notary pool member clocks. */
        val timeWindow: TimeWindow?,
        /** Random data used to make the transaction hash unpredictable even if the contents can be predicted; needed to avoid some obscure attacks. */
        val privacySalt: PrivacySalt,
        /**
         * Network parameters that were in force when the transaction was constructed. This is nullable only for backwards
         * compatibility for serialized transactions. In reality this field will always be set when on the normal codepaths.
         */
        override val networkParameters: NetworkParameters?,
        /** Referenced states, which are like inputs but won't be consumed. */
        override val references: List<StateAndRef<ContractState>>

```
{{% /tab %}}




[LedgerTransaction.kt](https://github.com/corda/corda/blob/release/os/4.3/core/src/main/kotlin/net/corda/core/transactions/LedgerTransaction.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Where:


* `inputs` are the transaction’s inputs as `List<StateAndRef<ContractState>>`
* `outputs` are the transaction’s outputs as `List<TransactionState<ContractState>>`
* `commands` are the transaction’s commands and associated signers, as `List<CommandWithParties<CommandData>>`
* `attachments` are the transaction’s attachments as `List<Attachment>`
* `notary` is the transaction’s notary. This must match the notary of all the inputs
* `timeWindow` defines the window during which the transaction can be notarised

`LedgerTransaction` exposes a large number of utility methods to access the transaction’s contents:


* `inputStates` extracts the input `ContractState` objects from the list of `StateAndRef`
* `getInput`/`getOutput`/`getCommand`/`getAttachment` extracts a component by index
* `getAttachment` extracts an attachment by ID
* `inputsOfType`/`inRefsOfType`/`outputsOfType`/`outRefsOfType`/`commandsOfType` extracts components based on
their generic type
* `filterInputs`/`filterInRefs`/`filterOutputs`/`filterOutRefs`/`filterCommands` extracts components based on
a predicate
* `findInput`/`findInRef`/`findOutput`/`findOutRef`/`findCommand` extracts the single component that matches
a predicate, or throws an exception if there are multiple matches


## requireThat

`verify` can be written to manually throw an exception for each constraint:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
override fun verify(tx: LedgerTransaction) {
    if (tx.inputs.size > 0)
        throw IllegalArgumentException("No inputs should be consumed when issuing an X.")

    if (tx.outputs.size != 1)
        throw IllegalArgumentException("Only one output state should be created.")
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
public void verify(LedgerTransaction tx) {
    if (tx.getInputs().size() > 0)
        throw new IllegalArgumentException("No inputs should be consumed when issuing an X.");

    if (tx.getOutputs().size() != 1)
        throw new IllegalArgumentException("Only one output state should be created.");
}
```
{{% /tab %}}

{{< /tabs >}}

However, this is verbose. To impose a series of constraints, we can use `requireThat` instead:

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}
```kotlin
requireThat {
    "No inputs should be consumed when issuing an X." using (tx.inputs.isEmpty())
    "Only one output state should be created." using (tx.outputs.size == 1)
    val out = tx.outputs.single() as XState
    "The sender and the recipient cannot be the same entity." using (out.sender != out.recipient)
    "All of the participants must be signers." using (command.signers.containsAll(out.participants))
    "The X's value must be non-negative." using (out.x.value > 0)
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
requireThat(require -> {
    require.using("No inputs should be consumed when issuing an X.",  tx.getInputs().isEmpty());
    require.using("Only one output state should be created.", tx.getOutputs().size() == 1);
    final XState out = (XState) tx.getOutputs().get(0);
    require.using("The sender and the recipient cannot be the same entity.", out.getSender() != out.getRecipient());
    require.using("All of the participants must be signers.", command.getSigners().containsAll(out.getParticipants()));
    require.using("The X's value must be non-negative.", out.getX().getValue() > 0);
    return null;
});
```
{{% /tab %}}

{{< /tabs >}}

For each <`String`, `Boolean`> pair within `requireThat`, if the boolean condition is false, an
`IllegalArgumentException` is thrown with the corresponding string as the exception message. In turn, this
exception will cause the transaction to be rejected.


## Commands

`LedgerTransaction` contains the commands as a list of `CommandWithParties` instances. `CommandWithParties` pairs
a `CommandData` with a list of required signers for the transaction:

{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}
```kotlin
/** A [Command] where the signing parties have been looked up if they have a well known/recognised institutional key. */
@KeepForDJVM
@CordaSerializable
data class CommandWithParties<out T : CommandData>(
        val signers: List<PublicKey>,
        /** If any public keys were recognised, the looked up institutions are available here */
        @Deprecated("Should not be used in contract verification code as it is non-deterministic, will be disabled for some future target platform version onwards and will take effect only for CorDapps targeting those versions.")
        val signingParties: List<Party>,
        val value: T
)

```
{{% /tab %}}




[Structures.kt](https://github.com/corda/corda/blob/release/os/4.3/core/src/main/kotlin/net/corda/core/contracts/Structures.kt) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

Where:


* `signers` is the list of each signer’s `PublicKey`
* `signingParties` is the list of the signer’s identities, if known
* `value` is the object being signed (a command, in this case)


### Branching verify with commands

Generally, we will want to impose different constraints on a transaction based on its commands. For example, we will
want to impose different constraints on a cash issuance transaction to on a cash transfer transaction.

We can achieve this by extracting the command and using standard branching logic within `verify`. Here, we extract
the single command of type `XContract.Commands` from the transaction, and branch `verify` accordingly:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
```kotlin
class XContract : Contract {
    interface Commands : CommandData {
        class Issue : TypeOnlyCommandData(), Commands
        class Transfer : TypeOnlyCommandData(), Commands
    }

    override fun verify(tx: LedgerTransaction) {
        val command = tx.findCommand<Commands> { true }

        when (command.value) {
            is Commands.Issue -> {
                // Issuance verification logic.
            }
            is Commands.Transfer -> {
                // Transfer verification logic.
            }
        }
    }
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
public class XContract implements Contract {
    public interface Commands extends CommandData {
        class Issue extends TypeOnlyCommandData implements Commands {}
        class Transfer extends TypeOnlyCommandData implements Commands {}
    }

    @Override
    public void verify(LedgerTransaction tx) {
        final Commands command = tx.findCommand(Commands.class, cmd -> true).getValue();

        if (command instanceof Commands.Issue) {
            // Issuance verification logic.
        } else if (command instanceof Commands.Transfer) {
            // Transfer verification logic.
        }
    }
}
```
{{% /tab %}}

{{< /tabs >}}
