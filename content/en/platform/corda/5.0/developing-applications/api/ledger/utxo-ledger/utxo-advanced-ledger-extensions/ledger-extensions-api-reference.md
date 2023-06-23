---
date: '2023-06-01'
title: "Ledger Extensions API Reference"
project: corda
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-utxo-ledger-extensions-api-reference
    parent: corda5-utxo-advanced-ledger-extensions
    weight: 4600
section_menu: corda5
---

# Ledger Extensions API Reference

## Advanced Contract Design

All the contract design issues described in [Building Basic Contract Design]({{< relref "building-basic-contract-design.md" >}}) are implemented by the Corda 5 Advanced UTXO Extensions library, and are included in all the specific implementations; for example, chainable, fungible and identifiable contracts.

## Advanced Ledger Types

### Base API

Module: base

Package: com.r3.corda.ledger.utxo.base

The Base API provides the underlying component model for designing extensible contracts with delegated contract verification constraint logic, as well as other components which allow CorDapp developers to better express intent throughout their applications.

### Chainable API

Module: chainable

Package: com.r3.corda.ledger.utxo.chainable

The Chainable API provides the component model for designing chainable states and contracts. Chainable states represent strictly linear state chains, where every state in the chain points to the previous state in the chain. This could be thought of as a similar concept to a blockchain, where each new block points to the previous block.

#### Designing Chainable States

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

#### Designing Chainable Commands

Chainable commands allow users to create, update, and delete chainable states.
The `ChainableContractCreateCommand` creates new chainable states and verifies the following constraints:

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
```

The `ChainableContractUpdateCommand` supports updating existing chainable states and verifies the following constraints:

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
```

The `ChainableContractDeleteCommand` supports deleting existing chainable states and verifies the following constraint:

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
```

#### Designing Chainable Contracts

A chainable contract can be implemented by extending the `ChainableContract` class; for example:

```kotlin
public final class ExampleChainableContract extends ChainableContract {
  @Override
  public List<Class<? extends ChainableContractCommand<?>>> getPermittedCommandTypes() {
    return List.of(Create.class, Update.class, Delete.class);  
  }
}
```

### Fungible API

Module: fungible

Package: com.r3.corda.ledger.utxo.fungible

The fungible API provides the component model for designing fungible states and contracts. Fungible states represent states that have a scalar numeric quantity, and can be split, merged and mutually exchanged with other fungible states of the same class. Fungible states represent the building blocks for states like tokens.

#### Designing Fungible States

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
```

#### Designing Fungible Commands

Fungible commands allow users to create, update and delete fungible states.
The `FungibleContractCreateCommand` creates new fungible states and verifies the following constraints:

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
```

The `FungibleContractUpdateCommand` supports updating existing fungible states and verifies the following constraints:

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
```

The `FungibleContractDeleteCommand` supports deleting existing fungible states and verifies the following constraints:

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
```

#### Designing Fungible Contracts

A fungible contract can be implemented by extending the `FungibleContract` class, for example:

```kotlin
public final class ExampleFungibleContract extends FungibleContract {
  @Override
  public List<Class<? extends FungibleContractCommand<?>>> getPermittedCommandTypes() {
    return List.of(Create.class, Update.class, Delete.class);
  }
}
```


### Identifiable API

Module: identifiable

Package: com.r3.corda.ledger.utxo.identifiable

The Identifiable API provides the component model for designing identifiable states and contracts. Identifiable states represent states that have a unique identifier that is guaranteed unique at the network level. Identifiable states are designed to evolve over time, where unique identifiers can be used to resolve the history of the identifiable state.

#### Designing Identifiable States

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
```

#### Designing Identifiable Commands

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
```

The `IdentifiableContractUpdateCommand` updates existing identifiable states and verifies the following constraints:

* On identifiable state(s) updating, at least one identifiable state must be consumed.
* On identifiable state(s) updating, at least one identifiable state must be created.
* On identifiable state(s) updating, each created identifiable state's identifier must match one consumed identifiable state's state reference or identifier, exclusively.

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
```

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
```

#### Designing Identifiable Contracts

An identifiable contract can be implemented by extending the `IdentifiableContract` class, for example:

```kotlin
public final class ExampleIdentifiableContract extends IdentifiableContract {
  @Override
  public List<Class<? extends IdentifiableContractCommand<?>>> getPermittedCommandTypes() {
    return List.of(Create.class, Update.class, Delete.class);
  }
}
```

### Ownable API

Module: ownable

Package: com.r3.corda.ledger.utxo.ownable

The Ownable API provides the component to design ownable states and contracts; that is, states that have a defined owner and need the owner's signature to be consumed.

#### Designing Ownable States

An ownable state can be designed by implementing the `OwnableState` interface:

``` kotlin
class ExampleOwnableState(private val owner: PublicKey) : OwnableState {

    override fun getOwner(): PublicKey {
        return owner
    }

    override fun getParticipants(): List<PublicKey> {
        return listOf(getOwner())
    }
}
```
#### Designing Ownable Contracts

The contract for an ownable state must check in the `verify` method that the owner of consumed ownable
states have signed the transaction. To simplify writing such a contract, the library provides
`OwnableConstraints` helpers. You must include and invoke the appropriate helper in your contract
to get this behaviour.

``` kotlin
class ExampleOwnableContract : DelegatedContract<ExampleOwnableContract.ExampleOwnableContractCommand>() {

    override fun getPermittedCommandTypes(): List<Class<out ExampleOwnableContractCommand>> {
        return listOf(Update::class.java)
    }

    sealed interface ExampleOwnableContractCommand : VerifiableCommand, ContractStateType<ExampleOwnableState>

    object Update : ExampleOwnableContractCommand {

        override fun getContractStateType(): Class<ExampleOwnableState> {
            return ExampleOwnableState::class.java
        }

        override fun verify(transaction: UtxoLedgerTransaction) {
            OwnableConstraints.verifyUpdate(transaction, contractStateType)
        }
    }
}
```

### Issuable API

Module: issuable

Package: com.r3.corda.ledger.utxo.issuable

The Issuable API allows you to design states that have an issuer as part of the state, verifying that 
any issuance of the state has been signed by the issuer, thus restricting who can issue states
of this particular type.

#### Designing Issuable States

An issuable state can be designed by implementing the `IssuableState` interface:

``` kotlin
@BelongsToContract(ExampleIssuableContract::class)
class ExampleIssuableState(private val issuer: PublicKey) : IssuableState {

    override fun getIssuer(): PublicKey {
        return issuer
    }

    override fun getParticipants(): List<PublicKey> {
        return listOf(getIssuer())
    }
}
```

#### Designing Issuable Contracts

The contract for issuable states needs to verify that the issuance rules are adhered to; that is, that
the issuer signs for issuance and deletion of any issuable states. This can be achieved by invoking
the `IssuableConstraints` helpers provided in the library.

``` kotlin
class ExampleIssuableContract : DelegatedContract<ExampleIssuableContract.ExampleIssuableContractCommand>() {

    override fun getPermittedCommandTypes(): List<Class<out ExampleIssuableContractCommand>> {
        return listOf(Create::class.java, Delete::class.java)
    }

    sealed interface ExampleIssuableContractCommand : VerifiableCommand, ContractStateType<ExampleIssuableState>


    object Create : ExampleIssuableContractCommand {
        override fun getContractStateType(): Class<ExampleIssuableState> {
            return ExampleIssuableState::class.java
        }

        override fun verify(transaction: UtxoLedgerTransaction) {
            IssuableConstraints.verifyCreate(transaction, contractStateType)
        }
    }

    object Delete : ExampleIssuableContractCommand {
        override fun getContractStateType(): Class<ExampleIssuableState> {
            return ExampleIssuableState::class.java
        }

        override fun verify(transaction: UtxoLedgerTransaction) {
            IssuableConstraints.verifyDelete(transaction, contractStateType)
        }
    }
}
```