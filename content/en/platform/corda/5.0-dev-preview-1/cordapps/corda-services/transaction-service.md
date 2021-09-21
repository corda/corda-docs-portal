---
title: "TransactionService"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 7000
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Signing transactions with and without TransactionService.
---

Use this document to learn how to sign transactions with the `TransactionService`, and how to sign `TransactionBuilders` directly, without `TransactionService`.

## Signing transactions using the `TransactionService`

`TransactionService` can be injected into flows and services. You can sign transactions using `TransactionService`. This includes signing both `TransactionBuilder`s and `SignedTransaction`s.

### Signing `TransactionBuilder`s

To sign a `TransactionBuilder`:

- Kotlin

  ```kotlin
  // Sign with the system's default identity key
  val signedTransaction: SignedTransaction = transactionService.sign(transactionBuilder)

  // Sign with a single [PublicKey]
  val signedTransaction: SignedTransaction = transactionService.sign(transactionBuilder, publicKey)

  // Sign with a multiple [PublicKey]s
  val signedTransaction: SignedTransaction = transactionService.sign(transactionBuilder, listOf(publicKey, anotherPublicKey))
  ```

- Java

  ```java
  // Sign with the system's default identity key
  SignedTransaction signedTransaction = transactionService.sign(transactionBuilder)

  // Sign with a single [PublicKey]
  SignedTransaction signedTransaction = transactionService.sign(transactionBuilder, publicKey)

  // Sign with a multiple [PublicKey]s
  SignedTransaction signedTransaction = transactionService.sign(transactionBuilder, List.of(publicKey, anotherPublicKey))
  ```

### Signing `SignedTransaction`s

To sign a `SignedTransaction`:

- Kotlin

  ```kotlin
  // Sign with the system's default identity key
  val signedTransactionWithAnotherSignature: SignedTransaction = transactionService.sign(signedTransaction)

  // Sign with a single [PublicKey]
  val signedTransactionWithAnotherSignature: SignedTransaction = transactionService.sign(signedTransaction, publicKey)
  ```

- Java

  ```java
  // Sign with the system's default identity key
  SignedTransaction signedTransactionWithAnotherSignature = transactionService.sign(signedTransaction)

  // Sign with a single [PublicKey]
  SignedTransaction signedTransactionWithAnotherSignature = transactionService.sign(signedTransaction, publicKey)
  ```

### Creating signatures

You can also create the signature without signing the input transaction itself by using `TransactionService.createSignature`.

There are overloads to create signatures for `SignedTransaction`s and `FilteredTransaction`s.

To create a signature for a `SignedTransaction` or `FilteredTransaction`:

- Kotlin

  ```kotlin
  // Create a signature with the system's default identity key
  val signature: DigitalSignatureAndMeta = transactionService.createSignature(transaction)

  // Create a signature with a [PublicKey]
  val signature: DigitalSignatureAndMeta = transactionService.createSignature(transaction, publicKey)
  ```

- Java

  ```java
  // Create a signature with the system's default identity key
  DigitalSignatureAndMeta signature = transactionService.createSignature(transaction)

  // Create a signature with a [PublicKey]
  DigitalSignatureAndMeta signature = transactionService.createSignature(transaction, publicKey)
  ```


If the input transaction to `createSignature` was a `SignedTransaction`, then the returned `DigitalSignatureAndMeta` can be combined with it after operations using the signature are complete, returning a copy of the `SignedTransaction` with the signature. This is equivalent to using `TransactionService.sign` but allows you to interact with the `DigitalSignatureAndMeta` as your application requires.

## Signing `TransactionBuilder`s directly

You can sign a `TransactionBuilder` directly without accessing a `TransactionService`. This is a convenience function to make building transactions simpler. They are functionally equivalent to the `TransactionService.sign` methods.

- Kotlin

  ```kotlin
  // Sign with the system's default identity key
  val signedTransaction: SignedTransaction = transactionBuilder.sign()

  // Sign with a single [PublicKey]
  val signedTransaction: SignedTransaction = transactionBuilder.sign(publicKey)

  // Sign with a multiple [PublicKey]s
  val signedTransaction: SignedTransaction = transactionBuilder.sign(listOf(publicKey, anotherPublicKey))
  ```

- Java

  ```java
  // Sign with the system's default identity key
  SignedTransaction signedTransaction = transactionBuilder.sign()

  // Sign with a single [PublicKey]
  SignedTransaction signedTransaction = transactionBuilder.sign(publicKey)

  // Sign with a multiple [PublicKey]s
  SignedTransaction signedTransaction = transactionBuilder.sign(List.of(publicKey, anotherPublicKey))
  ```
