---
aliases:
- /releases/release-V3.2/tutorial-custom-notary.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-2:
    identifier: corda-os-3-2-tutorial-custom-notary
    parent: corda-os-3-2-tutorials-index
    weight: 1140
tags:
- tutorial
- custom
- notary
title: Writing a custom notary service (experimental)
---


# Writing a custom notary service (experimental)


{{< warning >}}
Customising a notary service is still an experimental feature and not recommended for most use-cases. The APIs
for writing a custom notary may change in the future. Additionally, customising Raft or BFT notaries is not yet
fully supported. If you want to write your own Raft notary you will have to implement a custom database connector
(or use a separate database for the notary), and use a custom configuration file.

{{< /warning >}}


Similarly to writing an oracle service, the first step is to create a service class in your CorDapp and annotate it
with `@CordaService`. The Corda node scans for any class with this annotation and initialises them. The custom notary
service class should provide a constructor with two parameters of types `AppServiceHub` and `PublicKey`.

```kotlin
@CordaService
class MyCustomValidatingNotaryService(override val services: AppServiceHub, override val notaryIdentityKey: PublicKey) : TrustedAuthorityNotaryService() {
    override val uniquenessProvider = PersistentUniquenessProvider()

    override fun createServiceFlow(otherPartySession: FlowSession): FlowLogic<Void?> = MyValidatingNotaryFlow(otherPartySession, this)

    override fun start() {}
    override fun stop() {}
}

```

[MyCustomNotaryService.kt](https://github.com/corda/corda/blob/release/os/3.2/samples/notary-demo/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt)

The next step is to write a notary service flow. You are free to copy and modify the existing built-in flows such
as `ValidatingNotaryFlow`, `NonValidatingNotaryFlow`, or implement your own from scratch (following the
`NotaryFlow.Service` template). Below is an example of a custom flow for a *validating* notary service:

```kotlin
class MyValidatingNotaryFlow(otherSide: FlowSession, service: MyCustomValidatingNotaryService) : NotaryFlow.Service(otherSide, service) {
    /**
     * The received transaction is checked for contract-validity, for which the caller also has to to reveal the whole
     * transaction dependency chain.
     */
    @Suspendable
    override fun receiveAndVerifyTx(): TransactionParts {
        try {
            val stx = receiveTransaction()
            val notary = stx.notary
            checkNotary(notary)
            verifySignatures(stx)
            resolveAndContractVerify(stx)
            val timeWindow: TimeWindow? = if (stx.coreTransaction is WireTransaction) stx.tx.timeWindow else null
            return TransactionParts(stx.id, stx.inputs, timeWindow, notary!!)
        } catch (e: Exception) {
            throw when (e) {
                is TransactionVerificationException,
                is SignatureException -> NotaryInternalException(NotaryError.TransactionInvalid(e))
                else -> e
            }
        }
    }

    @Suspendable
    private fun receiveTransaction(): SignedTransaction {
        return otherSideSession.receive<NotarisationPayload>().unwrap {
            val stx = it.signedTransaction
            validateRequest(NotarisationRequest(stx.inputs, stx.id), it.requestSignature)
            stx
        }
    }

    @Suspendable
    private fun resolveAndContractVerify(stx: SignedTransaction) {
        subFlow(ResolveTransactionsFlow(stx, otherSideSession))
        stx.verify(serviceHub, false)
        customVerify(stx)
    }

    private fun verifySignatures(stx: SignedTransaction) {
        val transactionWithSignatures = stx.resolveTransactionWithSignatures(serviceHub)
        checkSignatures(transactionWithSignatures)
    }

    private fun checkSignatures(tx: TransactionWithSignatures) {
        try {
            tx.verifySignaturesExcept(service.notaryIdentityKey)
        } catch (e: SignatureException) {
            throw NotaryInternalException(NotaryError.TransactionInvalid(e))
        }
    }

    private fun customVerify(stx: SignedTransaction) {
        // Add custom verification logic
    }
}

```

[MyCustomNotaryService.kt](https://github.com/corda/corda/blob/release/os/3.2/samples/notary-demo/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt)

To enable the service, add the following to the node configuration:

```kotlin
notary : {
    validating : true # Set to false if your service is non-validating
    custom : true
}
```

