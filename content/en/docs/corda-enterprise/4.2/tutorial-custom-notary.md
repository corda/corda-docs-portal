---
aliases:
- /releases/4.2/tutorial-custom-notary.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- tutorial
- custom
- notary
title: Writing a custom notary service (experimental)
---




# Writing a custom notary service (experimental)


{{< warning >}}
Customising a notary service is still an experimental feature and not recommended for most use-cases. The APIs
for writing a custom notary may change in the future.

{{< /warning >}}


The first step is to create a service class in your CorDapp that extends the `NotaryService` abstract class.
This will ensure that it is recognised as a notary service.
The custom notary service class should provide a constructor with two parameters of types `ServiceHubInternal` and `PublicKey`.
Note that `ServiceHubInternal` does not provide any API stability guarantees.

```kotlin
class MyCustomValidatingNotaryService(override val services: ServiceHubInternal, override val notaryIdentityKey: PublicKey) : SinglePartyNotaryService() {
    override val uniquenessProvider = PersistentUniquenessProvider(services.clock, services.database, services.cacheFactory)

    override fun createServiceFlow(otherPartySession: FlowSession): FlowLogic<Void?> = MyValidatingNotaryFlow(otherPartySession, this)

    override fun start() {}
    override fun stop() {}
}

```
{{/* github src='samples/notary-demo/workflows/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.2/samples/notary-demo/workflows/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt#L25-L32' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.2/samples/notary-demo/workflows/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt' start='START 1' end='END 1' */}}[MyCustomNotaryService.kt](https://github.com/corda/enterprise/blob/release/ent/4.2/samples/notary-demo/workflows/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt)
The next step is to write a notary service flow. You are free to copy and modify the existing built-in flows such
as `ValidatingNotaryFlow`, `NonValidatingNotaryFlow`, or implement your own from scratch (following the
`NotaryFlow.Service` template). Below is an example of a custom flow for a *validating* notary service:

```kotlin
class MyValidatingNotaryFlow(otherSide: FlowSession, service: MyCustomValidatingNotaryService) : ValidatingNotaryFlow(otherSide, service, defaultEstimatedWaitTime) {
    override fun verifyTransaction(requestPayload: NotarisationPayload) {
        try {
            val stx = requestPayload.signedTransaction
            resolveAndContractVerify(stx)
            verifySignatures(stx)
            customVerify(stx)
        } catch (e: Exception) {
            throw  NotaryInternalException(NotaryError.TransactionInvalid(e))
        }
    }

    @Suspendable
    private fun resolveAndContractVerify(stx: SignedTransaction) {
        subFlow(ResolveTransactionsFlow(stx, otherSideSession))
        stx.verify(serviceHub, false)
    }

    private fun verifySignatures(stx: SignedTransaction) {
        val transactionWithSignatures = stx.resolveTransactionWithSignatures(serviceHub)
        checkSignatures(transactionWithSignatures)
    }

    private fun checkSignatures(tx: TransactionWithSignatures) {
        tx.verifySignaturesExcept(service.notaryIdentityKey)
    }

    private fun customVerify(stx: SignedTransaction) {
        // Add custom verification logic
    }
}

```
{{/* github src='samples/notary-demo/workflows/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt' url='https://github.com/corda/enterprise/blob/release/ent/4.2/samples/notary-demo/workflows/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt#L37-L67' raw='https://raw.githubusercontent.com/corda/enterprise/release/ent/4.2/samples/notary-demo/workflows/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt' start='START 2' end='END 2' */}}[MyCustomNotaryService.kt](https://github.com/corda/enterprise/blob/release/ent/4.2/samples/notary-demo/workflows/src/main/kotlin/net/corda/notarydemo/MyCustomNotaryService.kt)
To enable the service, add the following to the node configuration:

```kotlin
notary : {
    validating : true # Set to false if your service is non-validating
    className : "net.corda.notarydemo.MyCustomValidatingNotaryService" # The fully qualified name of your service class
}
```

