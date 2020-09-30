---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-cordapps-flows
tags:
- api
- transactions
title: Understanding transactions
weight: 6
---

# Understanding transactions

## Transaction lifecycle

Between its creation and its final inclusion on the ledger, a transaction will generally occupy one of three states:

* `TransactionBuilder`. A transaction’s initial state. This is the only state during which the transaction is
mutable, so we must add all the required components before moving on.
* `SignedTransaction`. The transaction now has one or more digital signatures, making it immutable. This is the
transaction type that is passed around to collect additional signatures and that is recorded on the ledger.
* `LedgerTransaction`. The transaction has been “resolved” - for example, its inputs have been converted from
references to actual states - allowing the transaction to be fully inspected.

We can visualise the transitions between the three stages as follows:

{{< figure alt="transaction flow" zoom="../resources/transaction-flow.png" >}}

## Transaction components

A transaction consists of six types of components:


* 1+ states:
    * 0+ input states
    * 0+ output states
    * 0+ reference input states


* 1+ commands
* 0+ attachments
* 0 or 1 time-window
    * A transaction with a time-window must also have a notary



Each component corresponds to a specific class in the Corda API. The following section describes each component class,
and how it is created.


### Input states

An input state is added to a transaction as a `StateAndRef`, which combines:


* The `ContractState` itself
* A `StateRef` identifying this `ContractState` as the output of a specific transaction

{{< tabs name="tabs-1" >}}
{{< /tabs >}}

A `StateRef` uniquely identifies an input state, allowing the notary to mark it as historic. It is made up of:


* The hash of the transaction that generated the state
* The state’s index in the outputs of that transaction

{{< tabs name="tabs-2" >}}
{{< /tabs >}}

The `StateRef` links an input state back to the transaction that created it. This means that transactions form
“chains” linking each input back to an original issuance transaction. This allows nodes verifying the transaction
to “walk the chain” and verify that each input was generated through a valid sequence of transactions.


#### Reference input states


{{< warning >}}
Reference states are only available on Corda networks with a minimum platform version >= 4.

{{< /warning >}}


A reference input state is added to a transaction as a `ReferencedStateAndRef`. A `ReferencedStateAndRef` can be
obtained from a `StateAndRef` by calling the `StateAndRef.referenced()` method which returns a `ReferencedStateAndRef`.

{{< tabs name="tabs-3" >}}
{{< /tabs >}}

**Handling of update races:**

When using reference states in a transaction, it may be the case that a notarisation failure occurs. This is most likely
because the creator of the state (being used as a reference state in your transaction), has just updated it.

Typically, the creator of such reference data will have implemented flows for syndicating the updates out to users.
However it is inevitable that there will be a delay between the state being used as a reference being consumed, and the
nodes using it receiving the update.

This is where the `WithReferencedStatesFlow` comes in. Given a flow which uses reference states, the
`WithReferencedStatesFlow` will execute the the flow as a subFlow. If the flow fails due to a `NotaryError.Conflict`
for a reference state, then it will be suspended until the state refs for the reference states are consumed. In this
case, a consumption means that:


* the owner of the reference state has updated the state with a valid, notarised transaction
* the owner of the reference state has shared the update with the node attempting to run the flow which uses the
reference state
* The node has successfully committed the transaction updating the reference state (and all the dependencies), and
added the updated reference state to the vault.

At the point where the transaction updating the state being used as a reference is committed to storage and the vault
update occurs, then the `WithReferencedStatesFlow` will wake up and re-execute the provided flow.


{{< warning >}}
Caution should be taken when using this flow as it facilitates automated re-running of flows which use
reference states. The flow using reference states should include checks to ensure that the reference data is
reasonable, especially if the economics of the transaction depends upon the data contained within a reference state.

{{< /warning >}}



### Output states

Since a transaction’s output states do not exist until the transaction is committed, they cannot be referenced as the
outputs of previous transactions. Instead, we create the desired output states as `ContractState` instances, and
add them to the transaction directly:

{{< tabs name="tabs-4" >}}
{{< /tabs >}}

In cases where an output state represents an update of an input state, we may want to create the output state by basing
it on the input state:

{{< tabs name="tabs-5" >}}
{{< /tabs >}}

Before our output state can be added to a transaction, we need to associate it with a contract. We can do this by
wrapping the output state in a `StateAndContract`, which combines:


* The `ContractState` representing the output states
* A `String` identifying the contract governing the state

{{< tabs name="tabs-6" >}}
{{< /tabs >}}


### Commands

A command is added to the transaction as a `Command`, which combines:


* A `CommandData` instance indicating the command’s type
* A `List<PublicKey>` representing the command’s required signers

{{< tabs name="tabs-7" >}}
{{< /tabs >}}


### Attachments

Attachments are identified by their hash:

{{< tabs name="tabs-8" >}}
{{< /tabs >}}

The attachment with the corresponding hash must have been uploaded ahead of time via the node’s RPC interface.


### Time-windows

Time windows represent the period during which the transaction must be notarised. They can have a start and an end
time, or be open at either end:

{{< tabs name="tabs-9" >}}
{{< /tabs >}}

We can also define a time window as an `Instant` plus/minus a time tolerance (e.g. 30 seconds):

{{< tabs name="tabs-10" >}}
{{< /tabs >}}

Or as a start-time plus a duration:

{{< tabs name="tabs-11" >}}
{{< /tabs >}}


## TransactionBuilder


### Creating a builder

The first step when creating a transaction proposal is to instantiate a `TransactionBuilder`.

If the transaction has input states or a time-window, we need to instantiate the builder with a reference to the notary
that will notarise the inputs and verify the time-window:

{{< tabs name="tabs-12" >}}
{{< /tabs >}}

We discuss the selection of a notary in [Writing CorDapp Flows](api-flows.md).

If the transaction does not have any input states or a time-window, it does not require a notary, and can be
instantiated without one:

{{< tabs name="tabs-13" >}}
{{< /tabs >}}


### Adding items

The next step is to build up the transaction proposal by adding the desired components.

We can add components to the builder using the `TransactionBuilder.withItems` method:

{{< tabs name="tabs-14" >}}
{{< /tabs >}}

`withItems` takes a `vararg` of objects and adds them to the builder based on their type:


* `StateAndRef` objects are added as input states
* `ReferencedStateAndRef` objects are added as reference input states
* `TransactionState` and `StateAndContract` objects are added as output states
    * Both `TransactionState` and `StateAndContract` are wrappers around a `ContractState` output that link the
output to a specific contract


* `Command` objects are added as commands
* `SecureHash` objects are added as attachments
* A `TimeWindow` object replaces the transaction’s existing `TimeWindow`, if any

Passing in objects of any other type will cause an `IllegalArgumentException` to be thrown.

Here’s an example usage of `TransactionBuilder.withItems`:

{{< tabs name="tabs-15" >}}
{{< /tabs >}}

There are also individual methods for adding components.

Here are the methods for adding inputs and attachments:

{{< tabs name="tabs-16" >}}
{{< /tabs >}}

An output state can be added as a `ContractState`, contract class name and notary:

{{< tabs name="tabs-17" >}}
{{< /tabs >}}

We can also leave the notary field blank, in which case the transaction’s default notary is used:

{{< tabs name="tabs-18" >}}
{{< /tabs >}}

Or we can add the output state as a `TransactionState`, which already specifies the output’s contract and notary:

{{< tabs name="tabs-19" >}}
{{< /tabs >}}

Commands can be added as a `Command`:

{{< tabs name="tabs-20" >}}
{{< /tabs >}}

Or as `CommandData` and a `vararg PublicKey`:

{{< tabs name="tabs-21" >}}
{{< /tabs >}}

For the time-window, we can set a time-window directly:

{{< tabs name="tabs-22" >}}
{{< /tabs >}}

Or define the time-window as a time plus a duration (e.g. 45 seconds):

{{< tabs name="tabs-23" >}}
{{< /tabs >}}


### Signing the builder

Once the builder is ready, we finalize it by signing it and converting it into a `SignedTransaction`.

We can either sign with our legal identity key:

{{< tabs name="tabs-24" >}}
{{< /tabs >}}

Or we can also choose to use another one of our public keys:

{{< tabs name="tabs-25" >}}
{{< /tabs >}}

Either way, the outcome of this process is to create an immutable `SignedTransaction` with our signature over it.


## SignedTransaction

A `SignedTransaction` is a combination of:


* An immutable transaction
* A list of signatures over that transaction

{{< tabs name="tabs-26" >}}
{{< /tabs >}}

Before adding our signature to the transaction, we’ll want to verify both the transaction’s contents and the
transaction’s signatures.


### Verifying the transaction’s contents

If a transaction has inputs, we need to retrieve all the states in the transaction’s dependency chain before we can
verify the transaction’s contents. This is because the transaction is only valid if its dependency chain is also valid.
We do this by requesting any states in the chain that our node doesn’t currently have in its local storage from the
proposer(s) of the transaction. This process is handled by a built-in flow called `ReceiveTransactionFlow`.
See [Writing CorDapp Flows](api-flows.md) for more details.

We can now verify the transaction’s contents to ensure that it satisfies the contracts of all the transaction’s input
and output states:

{{< tabs name="tabs-27" >}}
{{< /tabs >}}

Checking that the transaction meets the contract constraints is only part of verifying the transaction’s contents. We
will usually also want to perform our own additional validation of the transaction contents before signing, to ensure
that the transaction proposal represents an agreement we wish to enter into.

However, the `SignedTransaction` holds its inputs as `StateRef` instances, and its attachments as `SecureHash`
instances, which do not provide enough information to properly validate the transaction’s contents. We first need to
resolve the `StateRef` and `SecureHash` instances into actual `ContractState` and `Attachment` instances, which
we can then inspect.

We achieve this by using the `ServiceHub` to convert the `SignedTransaction` into a `LedgerTransaction`:

{{< tabs name="tabs-28" >}}
{{< /tabs >}}

We can now perform our additional verification. Here’s a simple example:

{{< tabs name="tabs-29" >}}
{{< /tabs >}}


### Verifying the transaction’s signatures

Aside from verifying that the transaction’s contents are valid, we also need to check that the signatures are valid. A
valid signature over the hash of the transaction prevents tampering.

We can verify that all the transaction’s required signatures are present and valid as follows:

{{< tabs name="tabs-30" >}}
{{< /tabs >}}

However, we’ll often want to verify the transaction’s existing signatures before all of them have been collected. For
this we can use `SignedTransaction.verifySignaturesExcept`, which takes a `vararg` of the public keys for
which the signatures are allowed to be missing:

{{< tabs name="tabs-31" >}}
{{< /tabs >}}

There is also an overload of `SignedTransaction.verifySignaturesExcept`, which takes a `Collection` of the
public keys for which the signatures are allowed to be missing:

{{< tabs name="tabs-32" >}}
{{< /tabs >}}

If the transaction is missing any signatures without the corresponding public keys being passed in, a
`SignaturesMissingException` is thrown.

We can also choose to simply verify the signatures that are present:

{{< tabs name="tabs-33" >}}
{{< /tabs >}}

Be very careful, however - this function neither guarantees that the signatures that are present are required, nor
checks whether any signatures are missing.


### Signing the transaction

Once we are satisfied with the contents and existing signatures over the transaction, we add our signature to the
`SignedTransaction` to indicate that we approve the transaction.

We can sign using our legal identity key, as follows:

{{< tabs name="tabs-34" >}}
{{< /tabs >}}

Or we can choose to sign using another one of our public keys:

{{< tabs name="tabs-35" >}}
{{< /tabs >}}

We can also generate a signature over the transaction without adding it to the transaction directly.

We can do this with our legal identity key:

{{< tabs name="tabs-36" >}}
{{< /tabs >}}

Or using another one of our public keys:

{{< tabs name="tabs-37" >}}
{{< /tabs >}}


### Notarising and recording

Notarising and recording a transaction is handled by a built-in flow called `FinalityFlow`. See [Writing CorDapp Flows](api-flows.md) for
more details.

