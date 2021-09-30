---
title: "StateLoaderService"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 6000
section_menu: corda-5-dev-preview
description: >
  Use the StateLoaderService to convert `StateRef` or `StatePointer` inputs into `StateAndRef` objects.
---

Use the `StateLoaderService` to convert `StateRef` or `StatePointer` inputs into `StateAndRef` objects.

## Inject StateLoaderService

`StateLoaderService` is injectable into services using the `CordaInject` mechanism.

This is injectable into both Corda Services and flows.

### Java

Define a property of type `StateLoaderService` and annotate with `@CordaInject`:

```java
@CordaInject
public StateLoaderService stateLoaderService;
```

### Kotlin

Define a `lateinit` property of type `StateLoaderService` and annotate with `@CordaInject`:

```kotlin
@CordaInject
lateinit var stateLoaderService: StateLoaderService
```

## Using the API

### load(LinearPointer<T>, LedgerTransaction): StateAndRef<T>

Resolves a `LinearPointer` to a `StateAndRef` from inside a `LedgerTransaction`. All pointed-to states will be included in the transaction as reference states.

### load(LinearPointer<T>): StateAndRef<T>

Resolves a `LinearPointer` to a `StateAndRef` via a vault query. This method will either return a `StateAndRef` or return an exception.

### load(Set<StateRef>): Set<StateAndRef<ContractState>>

Given a `Set` of `StateRef`'s, this loads each referenced transaction and looks up the specified output `ContractState`s.

### load(StateRef): StateAndRef<ContractState>

Given a `StateRef`, this loads the referenced transaction and looks up the specified output `ContractState`.

### load(StaticPointer<T>, LedgerTransaction): StateAndRef<T>

Resolves a `StaticPointer` to a `StateAndRef` from inside a `LedgerTransaction`. All pointed-to states will be included in the transaction as reference states.

### load(StaticPointer<T>): StateAndRef<T>

Resolves a `StaticPointer` to a `StateAndRef` via a vault query. This method will either return a `StateAndRef` or return an exception.

### loadOrdered(List<StateRef>): List<StateAndRef<ContractState>>

Given a `List` of `StateRef`'s, this loads each referenced transaction and looks up the specified output `ContractState`s.

### Java example

```java
import net.corda.v5.application.flows.Flow;
import net.corda.v5.application.injection.CordaInject;
import net.corda.v5.base.annotations.Suspendable;
import net.corda.v5.ledger.contracts.ContractState;
import net.corda.v5.ledger.contracts.StateAndRef;
import net.corda.v5.ledger.contracts.StateRef;
import net.corda.v5.ledger.services.NotaryLookupService;
import net.corda.v5.ledger.services.StateLoaderService;
import net.corda.v5.ledger.transactions.SignedTransaction;
import net.corda.v5.ledger.transactions.TransactionBuilderFactory;

public class StateLoaderServiceExample implements Flow<String> {

    private StateRef inputStateRef;

    @CordaInject
    private StateLoaderService stateLoaderService;

    @CordaInject
    private TransactionBuilderFactory transactionBuilderFactory;

    @CordaInject
    private NotaryLookupService notaryLookupService;

    public StateLoaderServiceExample(StateRef inputStateRef) {
        this.inputStateRef = inputStateRef;
    }

    @Override
    @Suspendable
    public String call() {

        StateAndRef<ContractState> stateAndRef = stateLoaderService.load(inputStateRef);

        SignedTransaction transaction = transactionBuilderFactory.create()
                .setNotary(notaryLookupService.getNotaryIdentities().get(0))
                .addInputState(stateAndRef)
                .sign();

        return "Example showing stateLoaderService.load";
    }
}
```
