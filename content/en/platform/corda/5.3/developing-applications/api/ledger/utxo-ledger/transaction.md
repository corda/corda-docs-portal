---
date: '2023-11-13'
title: "ledger.utxo.transaction"
menu:
  corda53:
    identifier: corda53-api-ledger-utxo-transaction
    parent: corda53-api-ledger-utxo
    weight: 2000
---
# net.corda.v5.ledger.utxo.transaction

The `net.corda.v5.ledger.utxo.transaction` package contains the following interfaces:

* [UtxoLedgerTransaction](#utxoledgertransaction)
* [UtxoSignedTransaction](#utxosignedtransaction)
* [UtxoTransactionBuilder](#utxotransactionbuilder)
* [UtxoTransactionValidator](#utxotransactionvalidator)

## UtxoLedgerTransaction

`UtxoLedgerTransaction` is a representation of a `UtxoSignedTransaction` that contains all of the data needed to perform contract verification. This includes the resolved input and reference states of the transaction.

## UtxoSignedTransaction

`UtxoSignedTransaction` defines a signed UTXO transaction. `UtxoLedgerTransaction` differs from `UtxoSignedTransaction` as follows:

* It does not have access to the deserialized details.
* It has direct access to the signatures.
* It does not require a serializer.

## UtxoTransactionBuilder

`UtxoTransactionBuilder` defines a builder for UTXO transactions.

## UtxoTransactionValidator

`UtxoTransactionValidator` defines a functional interface that validates a `UtxoLedgerTransaction`.
