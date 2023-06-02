---
date: '2023-06-01'
title: "Advanced Contract Design"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-utxo-ledger-extensions-advanced-design
    parent: corda5-utxo-advanced-ledger-extensions
    weight: 4500
section_menu: corda5
---

# Advanced Contract Design

All the contract design issues that have been highlighted above are implemented by the Corda 5 Advanced UTXO Extensions library, and are included in all the specific implementations; for example, chainable, fungible and identifiable contracts.

## Base API

Module: base

Package: com.r3.corda.ledger.utxo.base

The base API provides the underlying component model for designing extensible contracts with delegated contract verification constraint logic, as well as other components which allow CorDapp developers to better express intent throughout their applications.

## Chainable API

Module: chainable

Package: com.r3.corda.ledger.utxo.chainable

The chainable API provides the component model for designing chainable states and contracts. Chainable states represent strictly linear state chains, where every state in the chain points to the previous state in the chain. This could be thought of as a similar concept to a blockchain, where each new block points to the previous block.

## Designing a Chainable State

A chainable state can be implemented by implementing the `ChainableState<T>` interface; for example:

```kotlin
@BelongsToContract(ExampleChainableContract.class)
public final class ExampleChainableState extends ChainableState<ExampleChainableState> {
  @Nullable
  private final StaticPointer<ExampleChainableState> pointer;
  
  public ExampleChainableState(@NotNull final StaticPointer<ExampleChainableState> pointer) {
    this.pointer = pointer;
  }
  
  @Nullable 
  public StaticPointer<ExampleChainableState> getPreviousStatePointer() {
    return pointer;
  }
  
  @NotNull
  public List<PublicKey> getParticipants() {
    return List.of(...);
  }
}
```

## Designing Chainable Commands

Chainable commands allows users to create, update, and delete chainable states.
The `ChainableContractCreateCommand` creates new chainable states and will verify the following constraints:

* On chainable state(s) creating, at least one chainable state must be created.
* On chainable state(s) creating, the previous state pointer of every created chainable state must be null.

```kotlin
public final class Create extends ChainableContractCreateCommand<ExampleChainableState> {
  @NotNull
  public Class<ExampleChainableState> getContractStateType() {
    return ExampleChainableState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {
    // Verify additional Create constraints
  }
}

The `ChainableContractUpdateCommand` supports updating existing chainable states and will verify the following constraints:

* On chainable state(s) updating, at least one chainable state must be consumed.
* On chainable state(s) updating, at least one chainable state must be created.
* On chainable state(s) updating, the previous state pointer of every created chainable state must not be null.
* On chainable state(s) updating, the previous state pointer of every created chainable state must be pointing to exactly one consumed chainable state, exclusively.

```kotlin
public final class Update extends ChainableContractUpdateCommand<ExampleChainableState> {
  @NotNull
  public Class<ExampleChainableState> getContractStateType() {
    return ExampleChainableState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {    
    // Verify additional Update constraints
  }
}

The `ChainableContractDeleteCommand` supports deleting existing chainable states and will verify the following constraint:

* On chainable state(s) deleting, at least one chainable state must be consumed.

```kotlin
public final class Delete extends ChainableContractDeleteCommand<ExampleChainableState> {
  @NotNull
  public Class<ExampleChainableState> getContractStateType() {
    return ExampleChainableState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {
    // Verify additional Delete constraints
  }
}

## Designing a Chainable Contract

A chainable contract can be implemented by extending the `ChainableContract` class; for example:

```kotlin
public final class ExampleChainableContract extends ChainableContract {
  @Override
  public List<Class<? extends ChainableContractCommand<?>>> getPermittedCommandTypes() {
    return List.of(Create.class, Update.class, Delete.class);  
  }
}

## Fungible API

Module: fungible

Package: com.r3.corda.ledger.utxo.fungible

The fungible API provides the component model for designing fungible states and contracts. Fungible states represent states that have a scalar numeric quantity, and can be split, merged and mutually exchanged with other fungible states of the same class. Fungible states represent the building blocks for states like tokens.

## Designing a Fungible State

A fungible state can be implemented by implementing the `FungibleState<T>` interface; for example:

```kotlin
public final class ExampleFungibleState extends FungibleState<NumericDecimal> {  
  @NotNull
  private final NumericDecimal quantity;
  
  public ExampleFungibleState(@NotNull final NumericDecimal quantity) {
    this.quantity = quantity;
  }
  
  @NotNull
  public NumericDecimal getQuantity() {
    return quantity;
  }
  
  @NotNull
  public List<PublicKey> getParticipants() {
    return List.of(...);
  }
  
  @Override
  public boolean isFungibleWith(@NotNull final FungibleState<NumericDecimal> other) {
    return this == other || other instanceof ExampleFungibleState // && other fungibility rules.
  }
}

## Designing Fungible Commands

Fungible commands allows users to create, update and delete fungible states.
The `FungibleContractCreateCommand` creates new fungible states and will verify the following constraints:

* On fungible state(s) creating, at least one fungible state must be created.
* On fungible state(s) creating, the quantity of every created fungible state must be greater than zero.

```kotlin
public final class Create extends FungibleContractCreateCommand<ExampleFungibleState> {
  @NotNull
  public Class<ExampleFungibleState> getContractStateType() {
    return ExampleFungibleState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {
    // Verify additional Create constraints
  }
}

The `FungibleContractUpdateCommand` supports updating existing fungible states and will verify the following constraints:

* On fungible state(s) updating, at least one fungible state must be consumed.
* On fungible state(s) updating, at least one fungible state must be created.
* On fungible state(s) updating, the quantity of every created fungible state must be greater than zero.
* On fungible state(s) updating, the sum of the unscaled values of the consumed states must be equal to the sum of the unscaled values of the created states.
* On fungible state(s) updating, the sum of the consumed states that are fungible with each other must be equal to the sum of the created states that are fungible with each other.

```kotlin
public final class Update extends FungibleContractUpdateCommand<ExampleFungibleState> {
  @NotNull
  public Class<ExampleFungibleState> getContractStateType() {
    return ExampleFungibleState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {
    // Verify additional Update constraints
  }
}

The `FungibleContractDeleteCommand` supports deleting existing fungible states and will verify the following constraints:

* On fungible state(s) deleting, at least one fungible state input must be consumed.
* On fungible state(s) deleting, the sum of the unscaled values of the consumed states must be greater than the sum of the unscaled values of the created states.
* On fungible state(s) deleting, the sum of consumed states that are fungible with each other must be greater than the sum of the created states that are fungible with each other.

```kotlin
public final class Delete extends FungibleContractDeleteCommand<ExampleFungibleState> {
  @NotNull
  public Class<ExampleFungibleState> getContractStateType() {
    return ExampleFungibleState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {
    // Verify additional Delete constraints
  }
}

## Designing a Fungible Contract

A fungible contract can be implemented by extending the `FungibleContract` class, for example:

```kotlin
public final class ExampleFungibleContract extends FungibleContract {
  @Override
  public List<Class<? extends FungibleContractCommand<?>>> getPermittedCommandTypes() {
    return List.of(Create.class, Update.class, Delete.class);
  }
}

## Identifiable API

Module: identifiable

Package: com.r3.corda.ledger.utxo.identifiable

The identifiable API provides the component model for designing identifiable states and contracts. Identifiable states represent states that have a unique identifier that is guaranteed unique at the network level. Identifiable states are designed to evolve over time, where unique identifiers can be used to resolve the history of the identifiable state.

## Designing an Identifiable State

An identifiable state can be implemented by implementing the `IdentifiableState` interface, for example:

```kotlin
public final class ExampleIdentifiableState extends IdentifiableState {
  @Nullable
  private final StateRef id;
  
  public ExampleIdentifiableState(@Nullable final StateRef id) {
    this.id = id;
  }
  
  @Nullable
  public StateRef getId() {
    return id;
  }
  
  @NotNull
  public List<PublicKey> getParticipants() {
    return List.of(...);
  }
}

## Designing Identifiable Commands

Identifiable commands support creating, updating and deleting identifiable states.
The `IdentifiableContractCreateCommand` supports creating new identifiable states and verifies the identifiable state(s) creation, at least one identifiable state must be created.

```kotlin
public final class Create extends IdentifiableContractCreateCommand<ExampleIdentifiableState> {
  @NotNull
  public Class<ExampleIdentifiableState> getContractStateType() {
    return ExampleIdentifiableState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {
    // Verify additional Create constraints
  }
}

The `IdentifiableContractUpdateCommand` updates existing identifiable states and will verify the following constraints:

* On identifiable state(s) updating, at least one identifiable state must be consumed.
* On identifiable state(s) updating, at least one identifiable state must be created.
* On identifiable state(s) updating, each created identifiable state's identifier must match one consumed identifiable state's state ref or identifier, exclusively.

```kotlin
public final class Update extends IdentifiableContractUpdateCommand<ExampleIdentifiableState> {
  @NotNull
  public Class<ExampleIdentifiableState> getContractStateType() {
    return ExampleIdentifiableState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {
    // Verify additional Update constraints
  }
}

The `IdentifiableContractDeleteCommand` deletes existing identifiable states and verifies the identifiable state(s) deletion, at least one identifiable state must be consumed.

```kotlin
public final class Delete extends IdentifiableContractDeleteCommand<ExampleIdentifiableState> {
  @NotNull
  public Class<ExampleIdentifiableState> getContractStateType() {
    return ExampleIdentifiableState.class;
  }
  
  @Override
  protected void onVerify(@NotNull final UtxoLedgerTransaction transaction) {
    // Verify additional Delete constraints
  }
}

## Designing an Identifiable Contract

An identifiable contract can be implemented by extending the `IdentifiableContract` class, for example:

```kotlin
public final class ExampleIdentifiableContract extends IdentifiableContract {
  
   @Override
   
   public List<Class<? extends IdentifiableContractCommand<?>>> getPermittedCommandTypes() {
   return List.of(Create.class, Update.class, Delete.class);
   
  }
}
```
