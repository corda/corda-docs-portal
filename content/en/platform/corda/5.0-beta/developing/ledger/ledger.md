---
date: '2023-01-05'
title: "Ledger"
menu:
  corda-5-beta:
    identifier: corda-5-beta-ledger
    parent: corda-5-beta-develop
    weight: 3000
section_menu: corda-5-beta
---

A distributed ledger is a database of facts that’s replicated, shared, and synchronized across multiple participants on a network. 
Participants are members in the same [application network](../../introduction/key-concepts.html#application-networks), represented by [virtual nodes](../../introduction/key-concepts.html#virtual-nodes), and each participant's copy of the ledger is held in their [vault](**). Each participant has a different view of the ledger, depending on the facts it shares. Participants who share a fact must reach consensus before it is committed to the ledger. Two participants always see the exact same version of any on-ledger facts they share.

DEVELOPING LEDGER CORDAPP

**Overview**


UTXO ledger CorDapps should be split in to two parts:

* A contract CPK that contains all code defining the states and the smart contract ruling the creation, evolution, and consumption of the states. The contract CPK needs to be marked as such and can only have dependencies on other contract CPKs, so that it can be loaded into a verify sandbox.

* Workflow CPKs that contain all other code (workflows, persistence, business logic, etc) that can depend on any other CPK, including the contract CPKs.

All of these CPKs can be compiled into one CPB that has both workflows and contracts. A UTXO ledger CPB must also include a notary client and be configured to use a notary. <!--add link-->



**State and Contracts**


## States
Currently, only contract states are defined at the platform level. A contract state must implement the `ContractState` interface and provide a list of participants in the form of their public keys that will be used for signing the relevant transaction. States must be linked to a contract using the `@BelongsToContract` annotation on the state implementation class.

## Contracts
Contracts must implement the `Contract` interface, providing an implementation of the `verify` method. This method gets given a `UtxoLedgerTransaction` and has to verify that the given combination of inputs, reference states, outputs, and commands forms a valid transaction. This is were the actual contract enforcement happens.

### Commands
To this end, the contract implementation needs to define the commands it supports by providing one or more classes implementing the `Command` interface. Commands can be added to the transaction builder and define what the transaction does.

### Relevancy
Optionally, contracts can override the `isRelevant` method on the `Contract` interface. This method is given each produced state in a transaction and a set of keys owned by the current virtual node.
The default implementation returns `true` (and thus marks the state as relevant), if any of the keys of the current node is among the participants of the state. However, for specific contracts, the relevancy definitions might be different. For example, if the state has an owner, it might only be relevant to the owning node by checking that the owning key is among the keys of the current virtual node.

**Interacting with the ledger**

The main API to interact with the UTXO ledger is the `UtxoLedgerService`. This is a `@CordaInjectable` service that flows must request for injection by declaring an appropriately annotated member variable:

```kotlin
@CordaInjectable
lateinit var ledgerService: UtxoLedgerService
```

TransactionBuilder
The Ledger service gives access to the UtxoTransactionBuilder that can be used to build a transaction by passing in inputs, outputs, reference states etc. - very similar to Corda 4. One difference is that all transactions need a time window with an end date, and need a notary. In Corda 5 every UTXO transaction needs to be notarised, even if there are no inputs.

Finding transactions and states
The ledger service has methods to find states (unconsumed, relevant states of a specific type). In Corda 5 beta 1, no further specialised queries are possible, so you will have to load the state of the required type and filter in the flow code. Custom queries are coming for Beta 2

It’s also possible to load transactions by id.

Finality
To finalize a transaction (verify, store, distribute to participants, collect signatures, notarize, distribute signatures), you need to call the finalize function on the ledger service. On the counterparty (initiated flow), you need a matching call to receiveFinality. These calls will start subflows under the hood that deal with the messaging and finality.

Note: In Beta 1, it is strongly recommended to wrap the call to finalize/ receiveFinality in a try...catch` block, and in the case of an exception

log the exception

suppress the exception

jump to the end of the flow to stop any further processing.

The reason for that is that a verification or notarization failure will throw an exception, but letting an exception escape out of an initializing or initialized flow will unravel the flow session, so error messages might not be handled correctly, and the error payload send by the finality responder might get lost