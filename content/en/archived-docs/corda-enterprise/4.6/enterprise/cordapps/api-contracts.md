---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-cordapps-contracts
    name: "Writing CorDapp contracts"
    parent: corda-enterprise-4-6-cordapps
tags:
- api
- contracts
title: Writing CorDapp Contracts
weight: 6
---




# Writing CorDapp Contracts

In the context of a CorDapp, contracts define rules that are used to verify transaction inputs and outputs. A CorDapp
can have one more contracts, and each contract defines rules for one or more states. The goal of a contract is to ensure
that input and output states in transactions are valid and to prevent invalid transactions.

Contact files implement the `Contract` interface, containing the `verify` method. The `verify` method takes
transactions as input and evaluates them against rules defined as a `requireThat` element.

Here is an example contract. This contract accepts transactions and verifies them based on verification logic defined for
each type of command.

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


## Understanding the `Contract` class

As a contract is a part of a CorDapp, all parties wishing to transact in a network must have copy of the CorDapp running
on their Node. All parties will run the contract for any transaction they’re a party to, verifying that the transaction
is valid.

The contract interface is defined as follows:

```kotlin
@KeepForDJVM
@CordaSerializable
interface Contract {
    @Throws(IllegalArgumentException::class)
    fun verify(tx: LedgerTransaction)
```

The `Contract` interface has a single method, `verify`, which takes a `LedgerTransaction` as input and returns
nothing. This function is used to check whether a transaction proposal is valid, as follows:


* All contracts relevant to the transaction are gathered. Remember that there may be many contracts pertaining to a single transaction.
* The `verify` function of each contract is run, using the transaction as the `LedgerTransaction` input.
* If no exceptions are thrown, the transaction is deemed valid.


### Understanding the `verify` function

When a contract is used to verify a transaction, the verify function contains all of the rules and requirements that are
applied to the transaction to test whether it is valid.

There are several important factors to consider when writing a `verify` function:


* The `verify` function does not have access to information outside of the transaction
* The `verify` function can only access limited libraries. This disallows access to sources of information outside the transaction, as well as source of randomness like current time, and random number generation.

This means that `verify` only has access to the properties defined in the specific transaction that is being evaluated.

Here are the two simplest `verify` functions:

A `verify` that **accepts** all possible transactions:

```kotlin
override fun verify(tx: LedgerTransaction) {
    // Always accepts!
}
```

A `verify` that **rejects** all possible transactions:

```kotlin
override fun verify(tx: LedgerTransaction) {
    throw IllegalArgumentException("Always rejects!")
}
```


### Understanding the `LedgerTransaction` object

The `LedgerTransaction` object contains a variety of information describing the transaction that is being evaluated.
This information is expressed as properties, and can be accessed using utility methods. The information contained in the
`LedgerTransaction` object is the only information that can be used within the `verify` function.

The `LedgerTransaction` object passed into `verify` has the following properties:


* `inputs` are the transaction’s input states as `List<StateAndRef<ContractState>>`
* `outputs` are the transaction’s output states as `List<TransactionState<ContractState>>`
* `commands` are the transaction’s commands and associated signers, as `List<CommandWithParties<CommandData>>`
* `attachments` are the transaction’s attachments as `List<Attachment>`
* `id` is the hash of the original serialized WireTransaction as `SecureHash`
* `notary` is the transaction’s notary. This must match the notary of all the inputs
* `timeWindow` defines the window during which the transaction can be notarised
* `privacySalt` is random data used for salting the transaction id hash
* `networkParameters` are the network parameters that were in force when the transaction was constructed. This is nullable for backwards compatibility for serialized transactions. In reality this will always be set in expected use.
* `references` are referenced states that are required by the transaction, but not consumed by it, as `List<StateAndRed<ContractState>>`

The `LedgerTransaction` object also exposes a large number of utility methods to access the transaction’s contents:


* `inputStates` extracts the input `ContractState` objects from the list of `StateAndRef`
* `getInput`/`getOutput`/`getCommand`/`getAttachment` extracts a component by index
* `getAttachment` extracts an attachment by ID
* `inputsOfType`/`inRefsOfType`/`outputsOfType`/`outRefsOfType`/`commandsOfType` extracts components based on
their generic type
* `filterInputs`/`filterInRefs`/`filterOutputs`/`filterOutRefs`/`filterCommands` extracts components based on
a predicate
* `findInput`/`findInRef`/`findOutput`/`findOutRef`/`findCommand` extracts the single component that matches
a predicate, or throws an exception if there are multiple matches


## Writing verification logic

In most cases, there are many requirements or verification statements that must be true for a given transaction to be
deemed valid. For example, in a state issuance transaction the following verification might apply:


* There should be no input states
* There should only be one output state

While verification can be written to throw an error for each of these verification requirements, it is often easier to
use a `requireThat` function to list a series of requirements as string/boolean pairs.

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

For each string and boolean pair within `requireThat`, if the boolean condition is false, an `IllegalArgumentException`
is thrown with the corresponding string as the exception message. This exception causes the transaction to be rejected.


### Customising verification by command

The `LedgerTransaction` object contains the commands as a list of `CommandWithParties` instances.
`CommandWithParties` pairs a `CommandData` with a list of required signers for the transaction:

```kotlin
@KeepForDJVM
@CordaSerializable
data class CommandWithParties<out T : CommandData>(
        val signers: List<PublicKey>,
        val signingParties: List<Party>,
        val value: T
)
```


* `signers` is the list of each signer’s `PublicKey`
* `signingParties` is the list of the signer’s identities, if known, although note that this field is deprecated
* `value` is the object being signed (a command, in this case)

In almost all circumstances, different commands will require different verification requirements. An issue command may
very different verification than a transfer command.

Verification can be tailored to the commands by specifying the command type as shown below:

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


## What next?

After learning about writing contracts, we suggest you either learn more about how contract constraints can be used in
[Contract Constraints](api-contract-constraints.md), or learn about [Writing CorDapp States](api-states.md), or [Writing CorDapp Flows](api-flows.md).



