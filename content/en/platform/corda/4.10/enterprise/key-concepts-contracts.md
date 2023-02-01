---
aliases:
- /head/key-concepts-contracts.html
- /HEAD/key-concepts-contracts.html
- /key-concepts-contracts.html
date: '2023-1-30'
menu:
  corda-enterprise-4-10:
    identifier: corda-enterprise-4-10-key-concepts-contracts
    parent: corda-enterprise-4-10-key-concepts
    weight: 1050
tags:
- concepts
- contracts
- smart contracts
- validity
- contractual validity
title: Smart contracts
---


# Smart contracts

## Summary

* Smart contract digitize agreements by turning them into code that executes automatically if the contract terms are met.
* Nodes don't need to trust each other to follow through on contract terms, because the terms are enforced by the code.
* Smart contracts govern the evolution of [states](key-concepts-states.md) over time.
* Even if a [transaction](key-concepts-transactions.md) gathers all the required signatures, it can't be committed to the ledger unless it is contractually valid.

## Video

{{% vimeo 214168839 %}}


*Smart contracts* digitize agreements by turning the contract terms into code that executes automatically when the terms are met. This means:
* Parties don’t have to trust each other to follow through on the agreement terms.
* No external enforcement is required.
* The contract is always interpreted the same way.

The contract code is replicated on the [nodes](key-concepts-node.md) in a [network](key-concepts-ecosystem.md). The network members have to reach a [consensus](key-concepts-consensus.md) that the terms of the agreement have been met before they execute the contract.

Putting a contract on Corda gives it unique features:
* It can't be changed, only replaced with an updated version.
* Once executed, the results are irreversible.

## Smart contract languages
Corda smart contracts must be written in [Kotlin](https://kotlinlang.org/) or [Java](https://www.java.com/en/).

## Contractual validity

[Transactions](key-concepts-transactions.md) must be digitally signed by all required signers. However, even if a
transaction gathers all the required signatures, it can't be executed unless it is also *contractually valid*. A transaction that is not contractually valid is not a valid proposal to update the ledger, and can never be committed to the ledger. This means that contracts can impose rules on the evolution of states over time that are independent of the willingness of the required signers to sign a given transaction.

Each transaction [state](key-concepts-states.md) specifies a *contract type*. The contract specified takes the transaction as input, and determines if the transaction is valid based on the
contract's internal rules. The contract must evaluate every input state and every output state.

{{< figure alt="tx validation" width=80% zoom="/en/images/tx-validation.png" >}}
The contract code can:

* Check the number of inputs, outputs, commands, or attachments.
* Check for [time windows](key-concepts-time-windows.md).
* Check the contents of all components.
* Evaluate looping constructs, variable assignments, function calls, helper methods, and other aspects of the transaction code.
* Group similar states to validate them as a group. For example, it can impose a rule on the combined value of all the cash
states.

{{< note >}}
See [Reissuing states](cordapps/reissuing-states.md) for information about reissuing states with a guaranteed state replacement, which allows you to break transaction backchains.
{{< /note >}}

## Determinism

For the nodes on a network to reach consensus about a proposed update to the [ledger](key-concepts-ledger.md), transaction verification must be *deterministic*. That means contracts must **always accept** or **always reject** a given transaction. For example, a transaction's validity cannot depend on the time it was validated, or the amount of information the node running the contract holds.

Developers can pre-verify that their CorDapps are deterministic by linking them to [deterministic modules](deterministic-modules.md)).

## Contract limitations

By design, contracts don't have access to information from the outside world (unless they use an [oracle](key-concepts-oracles.md). They can only check transactions for internal validity. For example, a contract wouldn't know that the transaction is in accordance with what the parties involved originally agreed.

You should check the contents of a transaction before signing it, *even if the transaction is
contractually valid*, to see if you agree with the proposed ledger update. You have no obligation to
sign a transaction just because it is contractually valid. For example, you may not want to take on a loan that
is too large, or may disagree on the amount of cash offered for an asset.

## Legal prose

{{% vimeo 213879293 %}}

Smart contracts refer to legal prose documents that state the rules governing the evolution of the [state](key-concepts-states.md) over
time in a way that is compatible with traditional legal systems. This document can be relied upon in the case of
legal disputes.

## Encumbrances

You may want to restrict a specific state with an *encumberance*. The encumbrance state, if present, forces additional controls over the encumbered state, because the encumbrance state contract is also verified during the transaction execution. For example, a contract state could be
encumbered with a time-lock contract state. In that case, the state can only be processed in a transaction that verifies that the
time specified in the encumbrance time-lock has passed.

The encumbered state refers to its encumbrance by index, and the referred encumbrance state is an output state in a
particular position on the same transaction that created the encumbered state. Encumbered states and their encumberances must be consumed in the same transaction, otherwise the transaction is not valid.

When you construct a transaction that generates an encumbered state, you must place the encumbrance in the corresponding output
position of that transaction. When you consume that encumbered state, the same encumbrance state must be
available in the input set of states.

See an example of an encumbrance in the <a href="https://github.com/corda/reissue-cordapp/blob/master/contracts/src/main/kotlin/com/r3/corda/lib/reissuance/contracts/ReissuanceLockContract.kt">`ReissuanceLockContract`</a> and <a href="https://github.com/corda/reissue-cordapp/blob/master/workflows/src/main/kotlin/com/r3/corda/lib/reissuance/flows/ReissueStates.kt">`ReissueStatesFlow`</a> of the [Reissuance CorDapp](https://github.com/corda/reissue-cordapp).
