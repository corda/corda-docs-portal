---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    identifier: corda-enterprise-4-7-reissuing-states
    parent: corda-enterprise-4-7-cordapps
    weight: 65
tags:
- state
- reissue
- reissuing
title: Reissuing states
---


# Reissuing states

The state reissuance mechanism described on this page enables you to break transaction backchains by reissuing a state with a guaranteed state replacement.

## Overview

When a new transaction is created, input states are included in the proposed transaction by reference. These input state references link transactions together over time, forming a transaction backchain.

Long transaction backchains are undesirable for two reasons:
* **Performance**: Resolution along the chain slows down significantly.
* **Privacy**: All backchain transactions are shared with the new owner.

Prior to Corda 4.7, the only possible approach to resolve the problem with long transaction backchains was for a trusted issuing party to simply reissue the state. This meant that the state could simply be exited from the ledger and then reissued. As there would be no links remaining between the exit transaction and the reissuance transactions, the transaction backchain would be pruned.

However, this approach does not provide a guarantee that the issuing party would reissue the exited state as the actions described above are not atomic.

The new state reissuance functionality provides a state reissuance algorithm that eliminates the risk of being left without a usable state if the issuing party fails to reissue the state for some reason (for example, if they are not online at the required time). This is achieved through the reissuing of an **encumbered state** before the original state is deleted. This allows the requesting party to unlock the reissued state immediately after the original state is deleted.

{{< note >}}
State encumbrance refers to a state pointing to another state that must also appear as an input to any transaction consuming this state. A state may be encumbered by up to one other state, which is called an "encumbrance" state. The encumbrance state, if present, forces additional controls over the encumbered state, since the encumbrance state contract will also be verified during the execution of the transaction.

See [Defining encumbrances](../../../corda-os/4.7/tutorial-contract.md#defining-encumbrances) for more information.
{{< /note >}}

In addition, a single trusted issuing party is allowed to reissue multiple fungible states at once, provided that all these states are of the same type. For example, you can issue at once a number of tokens with different quantities but with the same `TokenType` and issued by the same party.

{{< note >}}
This functionality is part of Corda open source 4.7 and can be fully leveraged by Corda Enterprise 4.7 users as well.
{{< /note >}}

## How it works

A trusted issuer reissues an encumbered state before the original state is deleted, thus enabling the requester to unlock that reissued state immediately after the original state is deleted.

### High-level steps

1. The issuing party issues an encumbered state (State B) based on the original state (State A).
2. The original state (State A) is deleted.
3. Requester unlocks the reissued state (State B) immediately after the original state (State A) is deleted.

### Detailed steps

#### Step 1: The requesting party creates a reissuance request for one state or for multiple fungible states of the same type

The requesting party requests state reissuance using the `RequestReIssuance` flow with the following arguments:

* `issuer: AbstractParty`.
* `stateRefsToReIssue: List<StateRef>`.
* `assetIssuanceCommand: CommandData`: This command issues the new asset state.
* `extraAssetIssuanceSigners: List<AbstractParty>`: An optional list of required state issuance signers, which are different than the issuing party. The default value is an empty list.
* `requester: AbstractParty?`: This argument is only required when the requesting party is an account. The default value is `null`.

{{< note >}}
Alternatively, the requesting party can use the `RequestReIssuanceAndShareRequiredTransactions` flow to combine the actions in both Step 1 (this step) and Step 2 (next step) in one go: create a reissuance request, and share transactions proving that the states included in the reissuance request are valid with the issuing party.

The `RequestReIssuanceAndShareRequiredTransactions` flow uses the same arguments as the `RequestReIssuance` flow described in the previous step. The flow:

1. Calls the `RequestReIssuance` workflow.
2. Determines which transactions are required for the issuing party to validate the requested states.
3. Uses the `SendTransactionFlow` flow to share these transactions.
{{< /note >}}

#### Step 2: The requesting party shares a proof of validity for the requested states

The requesting party can use the `SendTransactionFlow` to send a transaction to the issuing party that wishes to verify it.

{{< note >}}
This flow is not specific to the state reissuance functionality. Also, see the note in Step 1 above about using the `RequestReIssuanceAndShareRequiredTransactions` flow.
{{< /note >}}

#### Step 3: The issuing party consumes the request

 When the issuing party gets a state reissuance request, it can reject it or accept it.

#### Use case 1: The issuing party rejects the request

To reject a request, the issuing party must call the `RejectReIssuanceRequest` flow, which simply deletes the request. The flow requires only one parameter to be provided:

* `reIssuanceRequestStateAndRef: StateAndRef<ReIssuanceRequest>`.

#### Use case 2: The issuing party accepts the request

To accept a request, the issuing party must call the `ReIssueStates` flow with the following parameters:

* `reIssuanceRequestStateAndRef: StateAndRef<ReIssuanceRequest>`.
* `extraAssetExitCommandSigners: List<AbstractParty>`: A list of parties, which need to sign the asset state exit transaction. By default this list includes the issuing party - the default value is `listOf(reissuanceRequestStateAndRef.state.data.issuer)`. This is used in asset state exit transaction verification (see [Step 5: Consume the reissued states](#step-5-consume-the-reissued-states) further below).

Before accepting a request, the issuing party needs to make sure the request is valid. They must verify if the states requested for reissuance are valid and also ensure that these states have not already been reissued (see [The issuing party is corrupted](#the-issuing-party-is-corrupted) further below).

When the issuing party accepts a state reissuance request:

* They generate encumbered copies of the states provided in the request.
* They generate a lock state, which enforces successful state reissuance and ensures that the entire state reissuance process is successful.
* The status of the newly created `ReIssuanceLock` object is set to `ACTIVE`.
* The value of the `extraAssetExitCommandSigners: List<AbstractParty>` property is used for the `ReIssuanceLock` state.

#### Step 4: The requesting party exits the original states

The requesting party can exit an original state by using the general redeem/delete command for the respective asset. For example, for tokens the respective command would be `RedeemTokens`.

{{< note >}}
In case multiple states are reissued, there is no requirement that all the original states should be deleted at the same time.
{{< /note >}}

Constraints:
* The command to run the transaction, which exits the original state(s) and serves as proof of exit, cannot produce any outputs.
* There cannot be anything in the contract preventing lock being a transaction input.
* If the `extraAssetExitCommandSigners` property of `ReIssuanceLock` is not empty, it must be signed by the listed parties as per the value of `extraAssetExitCommandSigners: List<AbstractParty>`.

{{< note >}}
Multiple exit transactions are supported because the requesting party may prefer to delete states through a number of transactions, or may simply forget to include some of the original states in the (single) exit transaction. However, multiple states should be exited using a single exit transaction so that the requesting party can ensure that all original states are still available, and also to eliminate the risk of exiting states whose reissued copies cannot be unlocked (this could happen when some original states have been
consumed).

In the case that the requesting party is unable to exit all states as some of them have been consumed, they should delete the reissued states and then use the `DeleteReIssuedStatesAndLock` flow to lock the original states and create a new reissuance request, excluding consumed states. When the issuing party approves the reissuance request, the requesting party can use the already executed exit transaction to unlock the reissued states. Please note that this solution should be a last resort as it still carries the risk that the issuing party may not accept the reissuance request.
{{< /note >}}

#### Step 5: Consume the reissued states

Depending on whether the original states have been consumed, there are two possible actions.

##### Use case 1: Unlock the reissued states if the original states have not been consumed

To unlock a reissued state, call the `UnlockReIssuedStates` flow. The contract code for reissuance lock objects verifies if the status of the `ReIssuanceLock` object is updated to `INACTIVE`, and that the reissued states can be unencumbered. To perform the latter check, an asset exit transaction is added as an attachment - it is serialised and transformed into a `Zip` stream with an entry called `SignedTransaction_[transactionId]`.

The `UnlockReIssuedStates` flow has the following arguments:

* `reIssuedStateAndRefs: List<StateAndRef<T>>`.
* `reIssuanceLock: StateAndRef<ReIssuanceLock<T>>`.
* `assetExitTransactionIds: List<SecureHash>`.
* `assetUnencumberCommand: CommandData`: This command reverses the encumbrance of asset states.
* `extraAssetUnencumberCommandSigners: List<AbstractParty>`: This command performs a required update of signers that are different from the requesting party. The default value is an empty list.

##### Use case 2: Exit the reissued states if the original states have been consumed

If the original states have already been consumed, it is impossible to unlock reissued states. Reissued states and corresponding `ReIssuanceLock` objects are redundant and should be deleted from the ledger.

To do that, `DeleteReIssuedStatesAndLock` flow should be called with the following arguments:

* `reIssuanceLockStateAndRef: StateAndRef<ReIssuanceLock<T>>`.
* `reIssuedStateAndRefs: List<StateAndRef<T>>`.
* `assetExitCommand: CommandData` - command which should be used to exit encumbered asset states.
* `assetExitSigners: List<AbstractParty>` - `assetExitCommand` signers, by default a list of issuer and requester.

### Flow responders

As business logic differs per asset, customised responders should be implemented for the following flows: `ReissueStates`, `UnlockReissuedStates`, and `DeleteReissuedStatesAndLock`.

You can derive custom responder implementations from the abstract responder classes `ReissueStatesResponder`, `UnlockReissuedStatesResponder`, and `DeleteReissuedStatesAndLock`, which handle signing flags and contain basic checks.

### How to verify if the transaction backchain has been pruned

To verify if the transaction backchain has really been pruned, use the new `GetTransactionBackChain` flow.

It has a single argument: `transactionId: SecureHash`.

This flow returns a set of backchain transactions. Based on the fact that state reference is created as concatenated
transaction id and index, transaction inputs can be used recursively to generate a directed graph of backchain transactions.

{{< note >}}
The flow returns a set because the exact order of backchain transactions is not of critical importance for the purpose of this verification, and also it is impossible to reconstruct it via the flow.
{{< /note >}}

## Useful diagrams

### Reissuance - state machine

State machine [CDL](../../../cdl/cdl/cdl-overview.md) chart:

{{% figure zoom="/en/images/reissuance-state-machine.png" alt="State reissuance - state machine CDL chart"%}}

### Reissuance - state evolution

State evolution [CDL](../../../cdl/cdl/cdl-overview.md) chart:

{{% figure zoom="/en/images/reissuance-state-evolution.png" alt="State reissuance - state evolution CDL chart"%}}

## Limitations

### Reissuance of encumbered states is not supported

You cannot issue an encumbered state based on another encumbered state serving as your original state.

### Support for extra signers for state reissuance

In some cases the issuing party is not the only issuance command signer and signatures must be collected from other parties.

If only some participants are signers, the implementation of responders is achieved through sending a flag. The alternative solution to use an additional flow that collects signatures is not possible because there is no way to create a state that stores workflow data.

### When exiting a reissued state, the exit transaction needs to be a `WireTransaction`

In the contract code, the `CoreTransaction`, which is part of the `SignedTransaction` (which is an asset exit proof), is casted to a `WireTransaction`.

Transactions of type `FilteredTransaction` cannot be used as asset exit proof.

## Cheating prevention

### Ways to prevent cheating in the new state reissuance mechanism

#### Required validation of states that are to be reissued

The requesting party cannot be trusted to provide valid states for reissuance. Therefore, the request must only contain state references - the issuing party then reissues states available for them. If the issuing party is not a participant, the requesting party must share with the issuing party the transactions proving that those states are valid.

#### Required proof of exit for the original states

To prove that the original state or states have been exited from the ledger, the requesting party must attach one or more notarised `SignedTransaction`.

* The inputs of all notarised `SignedTransaction`s must contain references of all the original states.
* A notarised `SignedTransaction` must not contain any outputs.

{{< note >}}
The attached transaction must be of type `SignedTransaction` because other types of transactions can be forged or may not contain transaction signatures, which are crucial for determining whether a transaction is notarised.
{{< /note >}}

#### Using the same exit proof multiple times

{{< warning >}}
To use the same proof twice or more, states would have to be reissued many times.

It is possible to create many `ReIssuanceRequest` requests for the same states. Therefore, before reissuing states, the issuing party must check if the requested states have already been reissued. The CorDapp performs a check through querying `ReIssuanceLock` objects to prevent accidental reapproval, but in parallelized environments a form of request de-duplication must be used in the calling application.

{{< /warning >}}

#### Detection of invalid `equals` function implementation

As state references are compared in the contract code, it is impossible to cheat by implementing an `equals` function that always returns `true`. So any such attempts are detected.

#### Consuming an original state instead of deleting it

If the issuing party is not a participant, they do not get updated if the original state is consumed. It is therefore possible for the issuing party to reissue a state, which has already been consumed. However, in that case the requesting party will not be able to prove that such a state has been exited, and therefore be unable to unlock (consume) it.

### Preventing other cheating possibilities

The issuing party must be a trusted party and is expected to act in an appropriate way. The use cases described below provide recommendations on state implementations that could prevent other cheating possibilities.

#### Possibility of other party reissuing the state

If the issuing party is not a participant and issuer information is not included in state to be reissued, any party can reissue a state. Therefore, it is recommended to include issuer information inside the state.

#### The issuing party is corrupted

The issuing party, contrary to a requesting party, is trusted to start the appropriate flows. If the issuing party is corrupted, they can implement their own version of a reissuance flow that does not check if the requested states have already been reissued. If such verification is disabled, the requesting party can create many reissuance requests, pointing to the same state, and use the same exit proof to unlock all of them.

## Sample CorDapps

State reissuance CorDapp: [https://github.com/corda/reissue-cordapp](https://github.com/corda/reissue-cordapp).

State reissuance sample CorDapp: [https://github.com/corda/reissue-sample-cordapp](https://github.com/corda/reissue-sample-cordapp).
