---
date: '2021-07-15'
menu:
  corda-enterprise-4-10:
    identifier: corda-enterprise-4-9-contract-catalogue
    name: "Contract catalogue"
    parent: corda-enterprise-4-10-component-library-index
tags:
- contract
- catalogue
title: Contract catalogue
weight: 10
---


# Contract catalogue

Corda comes with several sample contracts, which cover both core functionality (such as cash on ledger) and
demonstrates how to model complex contracts (such as interest rate swaps). You can use the provided `Dummy` contract for testing.


## Cash

The `Cash` contract’s state objects represent an amount of an issued currency, owned by a party. Any currency
can be issued by any party, and it is up to the recipient to determine whether they trust the issuer. Generally, nodes
have criteria (such as a whitelist) that issuers must fulfil before the node accepts cash from them.

Cash state objects implement the `FungibleAsset` interface, and can be used by the commercial paper and obligation
contracts as part of settlement of an outstanding debt. The contracts’ verification functions require that cash state
objects of the correct value are received by the beneficiary as part of the settlement transaction.

The cash contract supports issuing, moving, and exiting (destroying) states. Issuance cannot be part
of the same transaction as other cash commands, to minimise complexity in balance verification.

Cash shares a common superclass, `OnLedgerAsset`, with the Commodity contract. This implements common behaviour of
assets which can be issued, moved, and exited on chain, with the subclasses handling asset-specific data types and
behaviour.

{{< note >}}
Corda supports a pluggable cash selection algorithm by implementing the `CashSelection` interface.
The default implementation uses an H2 specific query that can be overridden for different database providers.
See `CashSelectionH2Impl` and its associated declaration in
`META-INF\services\net.corda.finance.contracts.asset.CashSelection`

{{< /note >}}

## Commodity

The `Commodity` contract is an early stage example of a non-currency contract whose states implement the `FungibleAsset`
interface. This is used as a proof of concept for non-cash obligations.


## Commercial paper

`CommercialPaper` is a simple obligation to pay an amount of cash at a future point in time (the maturity
date), and exists primarily as a simplified contract for use in tutorials. Commercial paper supports issuing, moving,
and redeeming (settling) states. Unlike the full obligation contract, it does not support locking the state so it cannot
be settled if the obligor defaults on payment or netting of state objects. All commands are exclusive of the other
commercial paper commands. Use the `Obligation` contract for more advanced functionality.


## Interest rate swap

The Interest Rate Swap (IRS) contract is a bilateral contract to implement a vanilla fixed / floating same currency
interest rate swap. In general, an IRS allows two counterparties to modify their exposure from changes in the underlying
interest rate. Interest rate swaps can be used as hedging instruments or to convert loan types, for example, converting a fixed rate loan to a floating rate loan or vice versa.

See [Interest rate swaps](../../../../../en/platform/corda/4.9/enterprise/contract-irs.md) for full details on the IRS contract.


## Obligation

The obligation contract’s state objects represent an obligation to provide some asset, which would generally be a
cash state object, but can be any contract state object fulfilling the `FungibleAsset` interface, including other
obligations. The obligation contract uses objects referred to as `Terms` to group commands and state objects together.
Terms are a subset of an obligation state object, including details of what should be paid, when, and to whom.

Obligation state objects can be issued, moved, and exited, as with any fungible asset. The contract also supports state
object netting and lifecycle changes (marking the obligation that a state object represents as having defaulted, or
reverting it to the normal state after marking as having defaulted). The `Net` command cannot be included with any
other obligation commands in the same transaction, as it applies to state objects with different beneficiaries, and
as such applies across multiple terms.

All other obligation contract commands specify obligation terms (what is to be delivered, by whom and by when)
which are used as a grouping key for input/output states and commands. Issuance and lifecycle commands are mutually
exclusive of other commands (move/exit) which apply to the same obligation terms, but multiple commands can be present
in a single transaction if they apply to different terms. For example, a contract can have two different `Issue`
commands as long as they apply to different terms, but could not have an `Issue` and a `Net`, or an `Issue` and
`Move` that apply to the same terms.

Netting of obligations supports close-out netting (which can be triggered by either obligor or beneficiary, but is
limited to bilateral netting), and payment netting (which requires signatures from all involved parties, but supports
multilateral netting).
