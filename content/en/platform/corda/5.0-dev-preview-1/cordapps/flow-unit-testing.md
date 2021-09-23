---
date: '2020-09-08T12:00:00Z'
title: "Flow unit testing"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps
    weight: 9200
project: corda-5
section_menu: corda-5-dev-preview
---

With the introduction of the `Flow` interface in Corda 5, it is now easier to create unit tests for your flows. It allows you to rely less on bringing up a whole network just to run tests against flows. From Corda 5, flows use injection to retrieve required services, and these services can easily be mocked in order to focus unit testing on functionality within a flow. The one issue that comes with this is that mocking injected services can introduce a lot of boilerplate code among tests, especially in cases where flows require a high number of services to be injected.

To help with unit testing flows, and to avoid boilerplate code for mocking services, we've introduced tooling to simplify unit testing flows.

## How this is different to Corda 4

In previous versions of Corda, such as Corda 4, flows were required to extend the `FlowLogic` abstract class which was a large class providing a lot of functionality, and many services via `ServiceHub`. This abstract class made it very difficult to write unit tests focused on the flow behavior since a lot of mock wiring was necessary before being able to write even basic tests.


## How to include flow test utilities

If this flow mock tooling is required within the Corda repo, you can add a test dependency to your build file for module `:testing:flow-mock-utils`:

``` gradle
dependencies {
    testImplementation project(":testing:flow-test-utils")
}
```

If working in a separate repo, you can pull in the published artifact `corda-flow-test-utils`:

``` gradle
dependencies {
    testImplementation("net.corda:corda-flow-test-utils:$corda_release_version")
}
```

## `FlowMockHelper` class

The `FlowMockHelper` class is the main class provided as part of the flow test tooling. The largest benefit that this class adds to tests is that it provides a function to instantiate flows with all injectable interfaces mocked without making you manage mocking every service. This greatly reduces the amount of boilerplate code required to instantiate a flow, so tests are faster to write and the test author can focus on the actual code testing.

This class also provides access to commonly used mock objects, and a method of overriding default service mocks. The following sections go into more detail around this functionality.

This helper class currently uses the following mocking libraries:
* `com.nhaarman:mockito-kotlin` version `1.6.0`
* `org.mockito:mockito-core` version `2.28.2`


## `createFlow()` function

The `createFlow` function takes as input a function which produces a flow. When called, the `createFlow` function invokes the input function to instantiate the flow and then iterates over all of the flow's injectables and sets up mocking for each service.

``` Kotlin
/**
 * Using the flow initializer passed in as a function parameter, initialize a flow and mock the flow dependencies. [Flow.call] will not
 * be invoked.
 *
 * @param flowInitializer a lambda used to initialize the flow to be tested.
 *
 * @return the initialized flow with mocked properties.
 */
fun createFlow(flowInitializer: FlowMockHelper<T>.() -> T): T
```

By default, the injectables are configured as basic mocks without any special behavior. However, in some cases where certain service functionality is often mocked-up in a common way, these mocks are added as part of the default mocking.
If a you want to customize mocks, you have two options:

* Access the service mock via the flow produced by the `createFlow` function and add your custom mocking to the mock object.
* Create your own mock object and replace the default mocks created by the `FlowMockHelper` class. You can do this by using the `overrideDefaultInjectableMock` function described in the next section.

Sample usage:
``` Kotlin
val fmh: FlowMockHelper
fmh.createFlow { CollectSignaturesFlow(signedTransactionMock, listOf(otherSideSession)) }
```


## `overrideDefaultInjectableMock()` function
The `overrideDefaultInjectableMock` function allows you to provide your own mocks for injectable services. This is required for when specific mock behaviour is needed rather than what is provided by default.

``` Kotlin
/**
 * Override the default mocks created by the [FlowMockHelper] with a custom mock for classes which are injectable into flows.
 * This should be called before creating a flow, for example, before calling [createFlow].
 *
 * @param interfaceClass interface which is injectable into flows.
 * @param implementation an implementation of [interfaceClass] which will be injected into the flow.
 */
fun <U, V : U> overrideDefaultInjectableMock(interfaceClass: Class<U>, implementation: V)
```

One limitation of this is that any mock overrides specified using this function _must_ be specified before calling the `createFlow` function. This is because `createFlow` injects the dependencies, so it's too late to try overriding them after the flow has been created.

Sample usage:
``` Kotlin
val fmh: FlowMockHelper
val mockNetworkParametersStorage = mock<NetworkParametersStorage> {
    on { lookup(eq(fmh.networkParametersHashMock)) } doReturn fmh.networkParametersMock
}
fmh.overrideDefaultInjectableMock(
    NetworkParametersService::class.java,
    mockNetworkParametersStorage
)
```

## `flow` property

When `createFlow` is called, it returns the instantiated flow, but it also stores the flow in a `flow` property within the `FlowMockHelper`. You can refer directly to this property instead of storing the result of `createFlow` yourself if you wish.

``` Kotlin
/**
 * The resulting flow after invoking [createFlow]. It is only accessible after calling one of these two functions.
 */
val flow: T
```

You cannot access `flow` before calling `createFlow`. If you attempt this, an `IllegalAccessError` will be thrown.


Sample usage:
``` Kotlin
val fmh: FlowMockHelper
fmh.createFlow { ResolveTransactionsFlow(fmh.signedTransactionMock, fmh.otherSideSession) }
fmh.flow.call()
```

## Mock objects

The `FlowMockHelper` class also provides access to a number of mock objects to remove further boilerplate code from tests. The list of available mocks isn't extensive, but is limited to those commonly required when writing flows, so in many cases they can be useful.

The mocks currently available include the following:

``` Kotlin
/**
 * Our properties
 */
val ourIdentity: Party
val ourPublicKey: PublicKey
val ourName: CordaX500Name
val ourTransactionSignature: TransactionSignature

/**
 * Other participant properties
 */
val otherSide: Party
val otherSidePublicKey: PublicKey
val otherSideName: CordaX500Name
val otherSideSession: FlowSession
val otherSideNode: MemberInfo
val otherSideTransactionSignature: TransactionSignature

/**
 * Notary properties
 */
val notary: Party
val notaryPublicKey: PublicKey

/**
 * Network parameters
 */
val networkParametersHashMock: SecureHash
val networkParametersMock: NetworkParameters

/**
 * Basic mocked transactions
 */
val signedTransactionHashMock: SecureHash
val signedTransactionMock: SignedTransaction
val wireTransactionMock: WireTransaction
val ledgerTransactionMock: LedgerTransaction
val transactionBuilderMock: TransactionBuilder

/**
 * Basic attachment mocks
 */
val attachmentIdMock: AttachmentId
val attachmentMock: Attachment
```

## Implementation of `FlowMockHelper`

The implementation of the `FlowMockHelper` provides some commonly-required wiring of mocks. This may not be obvious from looking at the mock definitions on the `FlowMockHelper` interface class.

For example, for the mocks listed above relating to `ourIdentity`:
* `ourIdentity.owningKey` returns `ourPublicKey`.
* `ourIdentity.name` returns `ourName`.
* `ourTransactionSignature.by` returns `ourPublicKey`.

Similar wiring has been configured for the other party mocks, and for the transaction mocks.

The implementation class also has some helpful default wiring of certain services. The list of mock wiring isn't extensive, but it does help with some commonly-used services within flows.

For example, `FlowIdentity` has a default mock which returns the `ourIdentity` mock object when `FlowIdentity.ourIdentity` is called. Similarily, `FlowMessaging` returns the `otherSideSession` when `FlowMessaging.initiateSession` is called using the `otherSide` mock object.


# `FlowMockUtils` class

The `FlowMockUtils` class is the main class that you should be interacting with to write a flow unit test. It provides functions which accept test Lambda functions to be run in the context of an instance of `FlowMockHelper` which it creates.

Different functions exist to assist writing tests in either Kotlin or Java. Both cases are detailed below.

This class also provides access to the `mockInjectables` function used to mock the injectable services of a flow if you decide you don't need all of `FlowMockHelper` but instead only need a helper to set up the injectable mocks.


## Kotlin `flowTest` function

The Kotlin-compatible helper function for writing flow unit tests is called `flowTest` and it accepts as an input parameter a Lambda which is run in the context of a `FlowMockHelper` instance. This Lambda is the test code.

``` Kotlin
fun <T : Flow<*>> flowTest(
    testCode: FlowMockHelper<T>.() -> Unit
) = FlowMockHelperImpl<T>().testCode()
```

You must specify the type of flow being tested to be able to directly access flow properties and functions within the test code, and to run any assertions and the result of calling a flow.

``` Kotlin
flowTest<CollectSignatureFlow> {
    // add test code to test `CollectSignatureFlow` here
}
```

## Java `flowTest` function

The Java-compatible helper function for writing flow unit tests is also called `flowTest`. It accepts as an input parameter an implementation of a functional interface called `FlowTest`. This interface has a single `run` function which takes a `FlowMockHelper` instance as an input parameter. The implementation of this interface is the test code. Since this interface is a functional interface with a single method, this can be written as a Lambda.

``` Kotlin
/**
 * Functional SAM interface which has a single method taking in a FlowMockHelper and is annotated as throwing [Exception] so that it is not
 * necessary to wrap [Flow.call] in try/catch in the few valid cases where a checked exception can be thrown.
 */
@FunctionalInterface
interface FlowTest<T : Flow<*>> {
    @Throws(Exception::class)
    fun run(t: FlowMockHelper<T>)
}
```

``` Kotlin
fun <T : Flow<*>> flowTest(
    @Suppress("UNUSED_PARAMETER") flowClass: Class<T>?,
    testCode: FlowTest<T>
) = testCode.run(FlowMockHelperImpl())

fun <T : Flow<*>> flowTest(
    testCode: FlowTest<T>
) = flowTest(null, testCode)
```

You must specify the type of flow being tested to be able to directly access flow properties and functions within the test code, and to run any assertions on the result of calling a flow. When the compiler cannot infer the flow type, the flow class can be passed in as a parameter to the test function.

Sample usage of the first function:
``` Java
flowTest(ReceiveTransactionFlow.class, fmh -> {
    // add test code to test `ReceiveTransactionFlow` here
});
```
Sample usage of the second function:
``` Java
FlowMockUtils.<ReceiveTransactionFlow>flowTest(fmh -> {
    // add test code to test `ReceiveTransactionFlow` here
});
```

## `mockInjectables` function

The `FlowMockUtils` class also provides a `mockInjectables` function. This is the same function which the `FlowMockHelper` class uses to set up the flow mocks after instantiation.

``` Kotlin
/**
 * Mock all injectable services for a flow. Mock overrides can be passed in for any specific mocking behaviour needed.
 * Otherwise services will be mocked as basic mocks.
 *
 * @param mock Overrides a map from interface to implementation to use when mocking the injectable services.
 */
fun Flow<*>.mockInjectables(
    mockOverrides: Map<Class<out Any>, Any>
)

fun Flow<*>.mockInjectables() = mockInjectables(emptyMap())
```

For a given flow, this function iterates over all dependencies annotated with `@CordaInject` and mocks an implementation. Optionally, a map of interfaces to implementations can be provided and this map will be given priority when setting mock implementations. You can pass in a parameter in this map for any injectable service that requires specific mock behavior. If no implementation is present in the map for a injectable service which a flow depends on, then a basic mock is created.

This function has been kept separate to `FlowMockHelper` since it gives the test author the option to just mock a flow's dependencies without using `FlowMockHelper` and all the mock objects it brings with it to allow for more lightweight testing if required.

## Sample usage

### `flowTest` in Kotlin

``` Kotlin
@Test
fun `Collect signatures for a partially signed transaction`() =
    flowTest<CollectSignaturesFlow> {
        createFlow { CollectSignaturesFlow(signedTransactionMock, listOf(otherSideSession)) }

        // Make partially signed transaction
        doReturn(listOf(ourTransactionSignature))
                .whenever(signedTransactionMock)
                .sigs

        doReturn(setOf(ourPublicKey, otherSidePublicKey))
                .whenever(wireTransactionMock)
                .requiredSigningKeys

        doReturn(listOf(otherSideTransactionSignature))
                .whenever(flow.flowEngine)
                .subFlow(any<CollectSignatureFlow>())

        with(flow.call()) {
            assertThat(sigs).contains(ourTransactionSignature)
            assertThat(sigs).contains(otherSideTransactionSignature)
        }

        verify(flow.flowIdentity).ourIdentity
        verify(flow.transactionMappingService).toLedgerTransaction(any<WireTransaction>())
        verify(flow.identityService, times(2)).wellKnownPartyFromAnonymous(any<AbstractParty>())
        verify(flow.flowEngine).subFlow(any<CollectSignatureFlow>())
    }

@Test
fun `Initiator of collect signatures flow must have signed the transaction before initiation`() =
    flowTest<CollectSignaturesFlow> {
        createFlow { CollectSignaturesFlow(signedTransactionMock, listOf(otherSideSession)) }

        // Make partially signed transaction
        doReturn(setOf(ourPublicKey, otherSidePublicKey))
                .whenever(wireTransactionMock)
                .requiredSigningKeys

        assertThrows<IllegalArgumentException> {
            flow.call()
        }

        verify(flow.flowIdentity).ourIdentity
        verify(flow.transactionMappingService, never()).toLedgerTransaction(any<WireTransaction>())
        verify(flow.identityService, never()).wellKnownPartyFromAnonymous(any<AbstractParty>())
        verify(flow.flowEngine, never()).subFlow(any<CollectSignatureFlow>())
    }
```

### `flowTest` in Java

``` Java
@Test
public void greenPathWithDefaultOverrides() {
    flowTest(ReceiveTransactionFlow.class, fmh -> {
        createFlow(fmh).call();
        assertThat(fmh.getSignedTransactionMock()).isEqualTo(fmh.getFlow().call());
        verify(fmh.getOtherSideSession()).receive(SignedTransaction.class);

        verify(fmh.getFlow().networkParametersService).lookup(eq(fmh.getNetworkParametersHashMock()));
        verify(fmh.getFlow().flowEngine).subFlow(Mockito.any(ResolveTransactionsFlow.class));
        verify(fmh.getFlow().transactionVerifierService).verify(eq(fmh.getSignedTransactionMock()), eq(true));
        verify(fmh.getFlow().transactionService).record(eq(StatesToRecord.NONE), eq(of(fmh.getSignedTransactionMock())));
    });
}

@Test
public void exceptionDuringVerification() {
    flowTest(ReceiveTransactionFlow.class, fmh -> {
        createFlow(fmh);

        doThrow(new AttachmentResolutionException(SecureHash.zeroHash))
                .when(fmh.getFlow().transactionVerifierService)
                .verify(eq(fmh.getSignedTransactionMock()), eq(true));

        assertThrows(AttachmentResolutionException.class, fmh.getFlow()::call);
    });
}
```

### `mockInjectables` in Kotlin

``` Kotlin
@Test
fun checkInjectableServicesAreInitialisedAfterMocking() {
    val flow = SampleFlow()
    flow.mockInjectables()
    assertThat(flow.sampleService).isNotNull
}
```

### `mockInjectables` in Java

``` Java
@Test
public void checkInjectableServicesAreInitialisedAfterMocking() {
    SampleFlow flow = new SampleFlow();
    mockInjectables(flow);
    assertThat(flow.sampleService).isNotNull();
}
```
