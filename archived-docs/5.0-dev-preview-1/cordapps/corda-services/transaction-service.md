---
title: "TransactionService"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 7000
section_menu: corda-5-dev-preview
description: >
  Signing transactions with and without `TransactionService`.
expiryDate: '2022-09-28'  
---

Use this guide to learn how to sign transactions with the `TransactionService`, and how to sign `TransactionBuilders` directly, without `TransactionService`.

## Sign transactions using the `TransactionService`

`TransactionService` can be injected into flows and services. You can sign transactions using `TransactionService`. This includes signing both `TransactionBuilder`s and `SignedTransaction`s.

### Sign a `TransactionBuilder`

To sign a `TransactionBuilder`:

{{< tabs name="TransactionBuilder">}}
{{% tab name="Kotlin"%}}
  ```kotlin
  // Sign with the system's default identity key
  val signedTransaction: SignedTransaction = transactionService.sign(transactionBuilder)

  // Sign with a single [PublicKey]
  val signedTransaction: SignedTransaction = transactionService.sign(transactionBuilder, publicKey)

  // Sign with multiple [PublicKey]s
  val signedTransaction: SignedTransaction = transactionService.sign(transactionBuilder, listOf(publicKey, anotherPublicKey))
  ```
  {{% /tab %}}

  {{% tab name="Java"%}}
  ```java
  // Sign with the system's default identity key
  SignedTransaction signedTransaction = transactionService.sign(transactionBuilder)

  // Sign with a single [PublicKey]
  SignedTransaction signedTransaction = transactionService.sign(transactionBuilder, publicKey)

  // Sign with multiple [PublicKey]s
  SignedTransaction signedTransaction = transactionService.sign(transactionBuilder, List.of(publicKey, anotherPublicKey))
  ```
  {{% /tab %}}
  {{< /tabs >}}
### Sign a `SignedTransaction`

To sign a `SignedTransaction`:

{{< tabs name="SignedTransaction">}}
{{% tab name="Kotlin"%}}
  ```kotlin
  // Sign with the system's default identity key
  val signedTransactionWithAnotherSignature: SignedTransaction = transactionService.sign(signedTransaction)

  // Sign with a single [PublicKey]
  val signedTransactionWithAnotherSignature: SignedTransaction = transactionService.sign(signedTransaction, publicKey)
  ```
  {{% /tab %}}

  {{% tab name="Java"%}}
  ```java
  // Sign with the system's default identity key
  SignedTransaction signedTransactionWithAnotherSignature = transactionService.sign(signedTransaction)

  // Sign with a single [PublicKey]
  SignedTransaction signedTransactionWithAnotherSignature = transactionService.sign(signedTransaction, publicKey)
  ```
  {{% /tab %}}
  {{< /tabs >}}
### Create a signature

You can also create the signature without signing the input transaction itself by using `TransactionService.createSignature`.

There are overloads to create signatures for `SignedTransaction`s and `FilteredTransaction`s.

To create a signature for a `SignedTransaction` or `FilteredTransaction`:

{{< tabs name="FilteredTransaction">}}
{{% tab name="Kotlin"%}}
  ```kotlin
  // Create a signature with the system's default identity key
  val signature: DigitalSignatureAndMeta = transactionService.createSignature(transaction)

  // Create a signature with a [PublicKey]
  val signature: DigitalSignatureAndMeta = transactionService.createSignature(transaction, publicKey)
  ```
  {{% /tab %}}

  {{% tab name="Java"%}}
  ```java
  // Create a signature with the system's default identity key
  DigitalSignatureAndMeta signature = transactionService.createSignature(transaction)

  // Create a signature with a [PublicKey]
  DigitalSignatureAndMeta signature = transactionService.createSignature(transaction, publicKey)
  ```
  {{% /tab %}}
  {{< /tabs >}}

If the input transaction to `createSignature` was a `SignedTransaction`, then the returned `DigitalSignatureAndMeta` can be combined with it after operations using the signature are complete, returning a copy of the `SignedTransaction` with the signature. This is equivalent to using `TransactionService.sign`, but allows you to interact with the `DigitalSignatureAndMeta` as your application requires.

## Sign a `TransactionBuilder` directly

You can sign a `TransactionBuilder` directly without accessing a `TransactionService`. This is a convenience function to make building transactions simpler. It is functionally equivalent to the `TransactionService.sign` method.

{{< tabs name="TransactionBuilder">}}
{{% tab name="Kotlin"%}}

  ```kotlin
  // Sign with the system's default identity key
  val signedTransaction: SignedTransaction = transactionBuilder.sign()

  // Sign with a single [PublicKey]
  val signedTransaction: SignedTransaction = transactionBuilder.sign(publicKey)

  // Sign with multiple [PublicKey]s
  val signedTransaction: SignedTransaction = transactionBuilder.sign(listOf(publicKey, anotherPublicKey))
  ```
  {{% /tab %}}

  {{% tab name="Java"%}}
  ```java
  // Sign with the system's default identity key
  SignedTransaction signedTransaction = transactionBuilder.sign()

  // Sign with a single [PublicKey]
  SignedTransaction signedTransaction = transactionBuilder.sign(publicKey)

  // Sign with multiple [PublicKey]s
  SignedTransaction signedTransaction = transactionBuilder.sign(List.of(publicKey, anotherPublicKey))
  ```
  {{% /tab %}}
  {{< /tabs >}}
