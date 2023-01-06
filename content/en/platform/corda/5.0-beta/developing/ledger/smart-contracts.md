---
date: '2023-01-05'
title: "Smart Contracts"
menu:
  corda-5-beta:
    parent: corda-5-beta-ledger
    identifier: corda-5-beta-smart-contracts
    weight: 3000
section_menu: corda-5-beta
---


Smart contracts digitize agreements by turning them into code that executes automatically if the contract terms are met. Participants do not need to trust each other to follow through on contract terms, because the terms are enforced by the code. No external enforcement is required, and contracts are always interpreted the same way. Smart contracts govern the evolution of states over time. 

The contract code is replicated on the virtual nodes in an application network. The network members have to reach a consensus that the terms of the agreement have been met before they execute the contract.

Putting a contract on Corda gives it unique features:

* A smart contract cannot be changed: it can only be replaced with an updated version.

* Once executed, the results are irreversible.

## Smart contract languages

Corda smart contracts must be written in Kotlin or Java.

## Contractual validity

Transactions must be digitally signed by all required signatories. However, even if a transaction gathers all the required signatures, it cannot be executed unless it is also contractually valid. A transaction that is not contractually valid is not a valid proposal to update the ledger, and can never be committed to the ledger. This means that contracts can impose rules on the evolution of states over time that are independent of the willingness of the required signatories to sign a given transaction.

Each transaction state specifies a contract type. The contract specified takes the transaction as input, and determines if the transaction is valid based on the contract’s internal rules. The contract must evaluate every input state and every output state.

{{< 
  figure
	 src="tx-validation.png"
	 figcaption="Transaction Validation"
>}}

The contract code can:

* Check the number of inputs, outputs, commands, or attachments.

* Check for time windows.

* Check the contents of all components.

* Evaluate looping constructs, variable assignments, function calls, helper methods, and other aspects of the transaction code.

* Group similar states to validate them as a group. For example, it can impose a rule on the combined value of all the cash states.

## Determinism

For the nodes on a network to reach consensus about a proposed update to the ledger, transaction verification must be deterministic. That means contracts must always accept or always reject a given transaction. For example, a transaction’s validity cannot depend on the time it was validated, or the amount of information the node running the contract holds.

## Contract limitations

By design, contracts do not have access to information from the outside world. They can only check transactions for internal validity. For example, a contract cannot know that the transaction is in accordance with what the parties involved originally agreed.

You should check the contents of a transaction before signing it, even if the transaction is contractually valid, to ensure that you agree with the proposed ledger update. You have no obligation to sign a transaction just because it is contractually valid. For example, you may not want to take on a loan that is too large, or may disagree with the amount of cash offered for an asset.

## Encumbrances

You may want to restrict a specific state with an encumbrance. An encumbrance forces two or more output states in a transaction into a group, where either all or none of the states in that group can be consumed by another transaction.

The encumbrance state, if present, forces additional controls over the encumbered state, because the encumbrance state contract is also verified during the transaction execution. For example, a contract state could be encumbered with a time-lock contract state. In that case, the state can only be processed in a transaction that verifies that the time specified in the encumbrance time-lock has passed.

The encumbered state and its encumbrance are output states on the same transaction, and need to be in the same encumbrance group that was specified when adding the states to the transaction. Encumbered states and their encumbrances must be consumed in the same transaction, otherwise the transaction is not valid.

When you construct a transaction that generates an encumbered state, you must add the encumbered state and the encumbrance state at the same time along with an encumbrance group ID. When you consume that encumbered state, the same encumbrance state must be available in the input set of states.