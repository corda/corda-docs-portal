---
aliases:
- /releases/release-V1.0/tutorial-custom-notary.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- tutorial
- custom
- notary
title: Writing a custom notary service
---


# Writing a custom notary service


{{< warning >}}
Customising a notary service is an advanced feature and not recommended for most use-cases. Currently,
customising Raft or BFT notaries is not yet fully supported. If you want to write your own Raft notary you will have to
implement a custom database connector (or use a separate database for the notary), and use a custom configuration file.

{{< /warning >}}


Similarly to writing an oracle service, the first step is to create a service class in your CorDapp and annotate it
with `@CordaService`. The Corda node scans for any class with this annotation and initialises them. The only requirement
is that the class provide a constructor with a single parameter of type `ServiceHub`.

```kotlin
@CordaService
class MyCustomValidatingNotaryService(override val services: ServiceHub, override val notaryIdentityKey: PublicKey) : TrustedAuthorityNotaryService() {
    override val timeWindowChecker = TimeWindowChecker(services.clock)
    override val uniquenessProvider = PersistentUniquenessProvider()

    override fun createServiceFlow(otherPartySession: FlowSession): FlowLogic<Void?> = MyValidatingNotaryFlow(otherPartySession, this)

    override fun start() {}
    override fun stop() {}
}

```

[CustomNotaryTutorial.kt](https://github.com/corda/corda/blob/release/os/1.0/docs/source/example-code/src/main/kotlin/net/corda/docs/CustomNotaryTutorial.kt)

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
            val stx = subFlow(ReceiveTransactionFlow(otherSideSession, checkSufficientSignatures = false))
            val notary = stx.notary
            checkNotary(notary)
            var timeWindow: TimeWindow? = null
            val transactionWithSignatures = if (stx.isNotaryChangeTransaction()) {
                stx.resolveNotaryChangeTransaction(serviceHub)
            } else {
                timeWindow = stx.tx.timeWindow
                stx
            }
            checkSignatures(transactionWithSignatures)
            return TransactionParts(stx.id, stx.inputs, timeWindow, notary!!)
        } catch (e: Exception) {
            throw when (e) {
                is TransactionVerificationException,
                is SignatureException -> NotaryException(NotaryError.TransactionInvalid(e))
                else -> e
            }
        }
    }

    private fun checkSignatures(tx: TransactionWithSignatures) {
        try {
            tx.verifySignaturesExcept(service.notaryIdentityKey)
        } catch (e: SignatureException) {
            throw NotaryException(NotaryError.TransactionInvalid(e))
        }
    }
}

```

[CustomNotaryTutorial.kt](https://github.com/corda/corda/blob/release/os/1.0/docs/source/example-code/src/main/kotlin/net/corda/docs/CustomNotaryTutorial.kt)

To ensure the custom notary is installed and advertised by the node, specify it in the configuration file:

```kotlin
extraAdvertisedServiceIds : ["corda.notary.validating.mycustom"]
```

