---
title: Multiplicities
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-smart-contract-view"
    identifier: "cdl-smart-contract-view-multiplicities"
    weight: 100

tags:
- cdl
- cordapp design language
- smart contract
- cordapp diagram
- multiplicities
---

# Multiplicities

The multiplicities indicate how many of the State type can/ must be in the transaction.

Input multiplicities are shown at the beginning of the Path constraint arrow, and can take the following values:

* 0 : There must be no input states of the primary type in the transaction.
* 1 : There must be exactly one input state of the primary type in the transaction.
* n : There can be n input states of the primary type in the transaction.

Output multiplicities are shown at the end of the Path constraint arrows, and can take the following values:

* 0 : There must be no output states of the primary type in the transaction.
* 1 : There must be exactly one output state of the primary type in the transaction.
* 1: Matched : There must be exactly one output state of the primary type in the transaction and the output state’s `linearId` must match the input state’s `linearId`.
* m : There are m output States of this type in the Transaction.

The options above can be combined to form ranges, eg

* 0..n : there can be zero to n states of the primary state type

For example, in the diagram below,  Path 1 'PROPOSED -- Agree --> AGREED':

* The input multiplicity is 1, indicating there must be one and only one input state of type AgreementState in status 'PROPOSED'
* The output multiplicity is 1: Matched, indicating there must be one and only one output state of type AgreementState and that the LinearID must match that of the input state.

{{< figure zoom="../resources/cdl-agreement-smart-contract-paths.png" width="1000" title="Click to zoom image in new tab/window" >}}

Where the Path starts or ends at a black circle, the implied Multiplicity = 0..0

The following example of a CashState shows how multiplicities can be expressed as ranges:

{{< figure zoom="../resources/cdl-overview-cashstate.png" width="700" title="Click to zoom image in new tab/window" >}}
