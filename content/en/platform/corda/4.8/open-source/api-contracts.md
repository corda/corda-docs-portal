---
aliases:
- /head/api-contracts.html
- /HEAD/api-contracts.html
- /api-contracts.html
date: '2021-08-11'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-api-contracts
    parent: corda-os-4-8-corda-api
    weight: 190
tags:
- api
- contracts
title: CorDapp Contracts
---




# CorDapp contracts

This article explains:

* How Corda nodes run contracts in CorDapps.
* What the `contract` class is and how to use it.
* What the `verify` function is and how to validate transactions with it.
* What the `LedgerTransaction` object is and what it does.
* How to write effective verification logic.

## Glossary

_Contract_
A file that defines the rules for verifying transaction inputs and outputs.
_Verify function_
A function containing all the requirements a Corda node needs to verify a transaction.
_LedgerTransaction object_
An object that contains information describing the transaction being evaluated.

In the context of a CorDapp, contracts define rules for verifying transaction inputs and outputs. A CorDapp
can have more than one contract, and each contract defines the rules for one or more states. The goal of a contract is to ensure
that input and output states in transactions are valid and to prevent invalid transactions.

Contract files implement the `Contract` interface, containing the `verify` method. The `verify` method takes
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

{{< note >}}
See [Reissuing states](reissuing-states.md) for information about reissuing states with a guaranteed state replacement, which lets you break transaction backchains.
{{< /note >}}

## The `Contract` class

Contracts are contained in CorDapps. All parties wishing to transact in a network must have a copy of the CorDapp running
on their Corda node. All parties run the contract for any transaction they’re a party to, verifying the transaction.

The contract interface is:

```kotlin
@KeepForDJVM
@CordaSerializable
interface Contract {
    @Throws(IllegalArgumentException::class)
    fun verify(tx: LedgerTransaction)
```

When a node needs to verify a transaction using a contract, it uses the `verify` function. This function contains all of the rules and requirements that are
applied to the transaction to test whether the proposal is valid.

The `Contract` interface has a single method, `verify`, which takes a `LedgerTransaction` as input and returns
nothing.

The function:

1. Gathers all contracts relevant to the transaction. Many contracts may pertain to a single transaction.
2. Runs the `verify` function of each contract, using the transaction as the `LedgerTransaction` input.
3. Deems the transaction valid if no exceptions are thrown.


### The `verify` function

The `verify` function can only access:

* The properties defined in the specific transaction being evaluated.
* Limited libraries.

These restrictions prevent the function from accessing information outside the transaction, including any sources of randomness, such as the current time or a random number generation.

The two simplest `verify` functions:

* **Accept** all possible transactions:

```kotlin
override fun verify(tx: LedgerTransaction) {
    // Always accepts!
}
```

* **Reject** all possible transactions:

```kotlin
override fun verify(tx: LedgerTransaction) {
    throw IllegalArgumentException("Always rejects!")
}
```


### The `LedgerTransaction` object

The `LedgerTransaction` object contains information describing the transaction being evaluated.
This information is expressed as properties. You can access it using utility methods. The information contained in the
`LedgerTransaction` object is the only information that can be used within the `verify` function.

The `LedgerTransaction` object passed into `verify` has these properties:


* `inputs`: The transaction’s input states as `List<StateAndRef<ContractState>>`.
* `outputs`: The transaction’s output states as `List<TransactionState<ContractState>>`.
* `commands`: The transaction’s commands and associated signers, as `List<CommandWithParties<CommandData>>`.
* `attachments`: The transaction’s attachments as `List<Attachment>`.
* `id`: The hash of the original serialized WireTransaction as `SecureHash`.
* `notary`: The transaction’s notary. All inputs must also use this notary.
* `timeWindow`: Defines when the transaction can be notarized.
* `privacySalt`: Random data used for salting the transaction ID hash.
* `networkParameters`: The network parameters that were in force when the transaction was constructed. This is nullable for backwards compatibility for serialized transactions. In reality this will always be set in expected use.
* `references`: Referenced states required by the transaction, but not consumed by it, as `List<StateAndRed<ContractState>>`.

The `LedgerTransaction` object also exposes a large number of utility methods to access the transaction’s contents:


* `inputStates`: Extracts the input `ContractState` objects from the list of `StateAndRef`.
* `getInput`/`getOutput`/`getCommand`/`getAttachment`: Extracts a component by index.
* `getAttachment`: Extracts an attachment by ID.
* `inputsOfType`/`inRefsOfType`/`outputsOfType`/`outRefsOfType`/`commandsOfType`: Extracts components based on
  their generic type.
* `filterInputs`/`filterInRefs`/`filterOutputs`/`filterOutRefs`/`filterCommands`: Extracts components based on
  a predicate.
* `findInput`/`findInRef`/`findOutput`/`findOutRef`/`findCommand`: Extracts the single component that matches
  a predicate, or throws an exception if there are multiple matches.


## Writing verification logic

To be deemed valid, most transactions have many requirements or verification statements that must be true. For example, in a state issuance transaction, the following verification might apply:


* There should be no input states.
* There should only be one output state.

You could write verification logic that throws an error for each of these requirements. However, it would be more efficient to
use a `requireThat` function to list a series of requirements as string/boolean pairs:

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

The function checks each string and boolean pair within the `requireThat` function. If the boolean condition is false, the function throws an `IllegalArgumentException`
with the corresponding string as the exception message. This exception causes the transaction to be rejected.


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


* `signers`: The list of each signer’s `PublicKey`.
* `signingParties` (deprecated): The list of the signer’s identities, if known.
* `value`: The object being signed.

Usually, different commands require different verification requirements. An issue command may require
very different verification than a transfer command.

You can tailor verification to the command by specifying the command type:

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


## Further reading

* [Contract Constraints](api-contract-constraints.md)
* [Write CorDapp States](api-states.md)
* [Writing CorDapp Flows](api-flows.md)
