---
title: Path constraints
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-path-constraints"
    weight: 90

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
- path constraints
---

# Paths Constraints

Once you have defined the statuses, you need to articulate how the Smart Contract can transition between those statuses. You can do this by defining Path constraints.

The path for a transaction consist of:

* The primary input states' status.
* The primary output states' status.
* The transaction command.
* The number of primary input states.
* The number of primary output states.
* Any additional states present other than the Primary state types, including how many of them there are as inputs, references, and outputs.

Correspondingly a Path constraint defines for a given primary input state status a permitted combination of:

* The primary output state status.
* The transaction command.
* The multiplicity of the input states for the primary state type.
* The multiplicity of the output states for the primary state type.
* Additional States, where we specify additional state types which must be present in the transaction and their multiplicities (we won't cover those here).

Path constraints are shown on the diagram as arrows between state statuses, the status at the beginning of the arrow represents an input state in a transaction, the status at the end of the arrow represents an output state in a transaction. The diagram below shows the Path constraints for this smart contract and highlights how when the input status is PROPOSED there are two transitions that can be made:

* Path 1: 'PROPOSED -- Agree --> AGREED'
* Path 2: 'PROPOSED -- Reject --> REJECTED'

{{< figure zoom="../resources/cdl-agreement-smart-contract-paths.png" width="1000" title="Click to zoom image in new tab/window" >}}

A black circle indicates no state, hence an arrow coming out of a black circle means there can be no inputs of the primary state type in the transaction. An arrow going into a black circle means there are no outputs of the primary state type in the transaction.

The command is indicated on the Path constraint arrow and the input and output multiplicities are shown at the start and end of the arrow respectively.

An important aspect of the Smart Contract view is that only paths conforming to a shown path constraint are permitted. In this example the implication is that it is forbidden to go from, say, REJECTED straight to AGREED, or from no-state straight to REJECTED.
