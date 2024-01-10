---
date: '2023-06-01'
title: "Ledger Extensions API Reference"
project: corda
version: 'Corda 5.1'
menu:
  corda51:
    identifier: corda51-utxo-ledger-extensions-api-reference
    parent: corda51-utxo-advanced-ledger-extensions
    weight: 4000
section_menu: corda51
---

# Advanced Ledger Extensions API Reference

* [Advanced Contract Design](#advanced-contract-design)
* [Advanced Ledger Types](#advanced-ledger-types)

## Advanced Contract Design

All of the contract design issues described in [Building Basic Contract Design]({{< relref "building-basic-contract-design.md" >}}) are implemented by the Advanced {{< tooltip >}}UTXO{{< /tooltip >}} Extensions library, and are included in the specific implementations; for example, chainable, fungible, and identifiable contracts.

## Advanced Ledger Types

This section describes the modules of the Advanced UTXO Ledger Extensions library. It contains the following:

* [base](#base)
* [chainable](#chainable)
* [fungible](#fungible)
* [identifiable](#identifiable)
* [ownable](#ownable)
* [issuable](#issuable)

### `base`

`com.r3.corda.ledger.utxo.base`

The `base` module provides the underlying component model for designing extensible contracts with delegated contract verification constraint logic, as well as other components which allow {{< tooltip >}}CorDapp{{< /tooltip >}} Developers to better express intent throughout their applications.

### `chainable`

`com.r3.corda.ledger.utxo.chainable`

The `chainable` module provides the component model for designing chainable {{< tooltip >}}states{{< /tooltip >}} and contracts. Chainable states represent strictly linear state chains, where every state in the chain points to the previous state in the chain. This could be thought of as a similar concept to a blockchain, where each new block points to the previous block.

#### Designing Chainable States

A chainable state can be implemented by implementing the `ChainableState<T>` interface; for example:

```java
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

```java
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

```java
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

```java
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

```java
public final class ExampleChainableContract extends ChainableContract {
    @Override
    public List<Class<? extends ChainableContractCommand<?>>> getPermittedCommandTypes() {
        return List.of(Create.class, Update.class, Delete.class);
    }
}
```

#### Creating, Updating, and Deleting Chainable States

To create a chainable state, create an instance of a `ChainableState` with a `pointer` of `null`:

```java
new ExampleChainableState(null);
```

To update an existing chainable state, retrieve the existing `ChainableState`'s `StateRef` and create a new instance of the `ChainableState`. Pass in the `StateRef` from the previous step as the `pointer` value:

```java
new ExampleChainableState(new StaticPointer(previousStateRef, ExampleChainableState.class));
```

Consume the existing instance in the same transaction that contains the updated instance.

To delete a chainable state, retrieve the existing `ChainableState`'s `StateRef` and consume the state using the `StateRef`.

### `fungible`

`com.r3.corda.ledger.utxo.fungible`

The `fungible` module provides the component model for designing fungible states and contracts. Fungible states represent states that have a scalar numeric quantity, and can be split, merged and mutually exchanged with other fungible states of the same class. Fungible states represent the building blocks for states like tokens.

#### Designing Fungible States

A fungible state can be implemented by implementing the `FungibleState<T>` interface; for example:

```java
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

```java
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

```java
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

```java
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

```java
public final class ExampleFungibleContract extends FungibleContract {
    @Override
    public List<Class<? extends FungibleContractCommand<?>>> getPermittedCommandTypes() {
        return List.of(Create.class, Update.class, Delete.class);
    }
}
```

### `identifiable`

`com.r3.corda.ledger.utxo.identifiable`

The `identifiable` module provides the component model for designing identifiable states and contracts. Identifiable states represent states that have a unique identifier that is guaranteed unique at the network level. Identifiable states are designed to evolve over time, where unique identifiers can be used to resolve the history of the identifiable state.

#### Designing Identifiable States

An identifiable state can be implemented by implementing the `IdentifiableState` interface, for example:

```java
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

```java
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

```java
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

```java
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

```java
public final class ExampleIdentifiableContract extends IdentifiableContract {
    @Override
    public List<Class<? extends IdentifiableContractCommand<?>>> getPermittedCommandTypes() {
        return List.of(Create.class, Update.class, Delete.class);
    }
}
```

#### Creating, Updating, and Deleting Identifiable States

To create a unique identifiable state, create an instance of an `IdentifiableState` with an `id` of `null`.

To update an existing identifiable state, do the following:

1. Retrieve the existing `IdentifiableState`.
2. Extract the `id` from the `IdentifiableState`. If the `id` is `null`, extract the `StateRef` instead.
3. Create a new instance of the `IdentifiableState` and pass in the `id` or `StateRef` from the previous step.
4. Consume the existing instance in the same transaction that contains the updated instance.

To delete an identifiable state, do the following:

1. Retrieve the existing `IdentifiableState`'s `StateRef`.
2. Consume the state using the `StateRef`.

#### Retrieving the Latest Identifiable States

To retrieve the latest `IdentifiableState`s:

1. Call `UtxoLedgerService.query`.
2. Pass in `IdentifiableStateQueries.GET_BY_IDS` as the query name.
3. Set the result class as `StateAndRef`.
4. Call `setParameter` with a key of `ids` and value containing all the `id`s (or `StateRef`s) as `String`s for the states that are retrieved.

For example:

```java
@CordaInject
private UtxoLedgerService utxoLedgerService;

PagedQuery.ResultSet<?> resultSet = utxoLedgerService.query(IdentifiableStateQueries.GET_BY_IDS, StateAndRef.class)
    .setLimit(3)
    .setCreatedTimestampLimit(Instant.now())
    .setParameter("ids", List.of(id1, id2, id3))
    .execute();

List<StateAndRef<ExampleIdentifiableState>> results = (List<StateAndRef<ExampleIdentifiableState>>) resultSet.getResults();
```

### `ownable`

`com.r3.corda.ledger.utxo.ownable`

The `ownable` module provides the component to design ownable states and contracts; that is, states that have a defined owner and need the owner's signature to be consumed.

#### Designing Ownable States

An ownable state can be designed by implementing the `OwnableState` interface:

```java
@BelongsToContract(ExampleOwnableState.class)
public final class ExampleOwnableState implements OwnableState {

    @NotNull
    private final PublicKey owner;

    public ExampleOwnableState(@NotNull PublicKey owner) {
        this.owner = owner;
    }

    @NotNull
    @Override
    public PublicKey getOwner() {
        return owner;
    }

    @NotNull
    @Override
    public List<PublicKey> getParticipants() {
        return List.of(...);
    }
}
```

#### Designing Ownable Contracts

The contract for an ownable state must check in the `verify` method that the owner of consumed ownable
states have signed the transaction. To simplify writing such a contract, the library provides
`OwnableConstraints` helpers. Include and invoke the appropriate helper in the contract
to get this behaviour

```java
public final class ExampleOwnableContract extends DelegatedContract<ExampleOwnableContract.ExampleOwnableContractCommand> {

    @NotNull
    @Override
    protected List<Class<? extends ExampleOwnableContract.ExampleOwnableContractCommand>> getPermittedCommandTypes() {
        return List.of(Update.class);
    }

    interface ExampleOwnableContractCommand extends VerifiableCommand, ContractStateType<ExampleOwnableState> {
    }

    public final static class Update implements ExampleOwnableContractCommand {

        @NotNull
        @Override
        public Class<ExampleOwnableState> getContractStateType() {
            return ExampleOwnableState.class;
        }

        @Override
        public void verify(@NotNull UtxoLedgerTransaction transaction) {
            OwnableConstraints.verifyUpdate(transaction, getContractStateType());
        }
    }
}
```

#### Retrieving Ownable States

To retrieve `OwnableState`s for a particular owner:

1. Call `UtxoLedgerService.query`.
2. Pass in `OwnableStateQueries.GET_BY_OWNER` as the query name.
3. Set the result class as `StateAndRef`.
4. Pass in the following parameters using `setParameter`
    * `owner` - Parse the owner key into a `String` using the `DigestService`.
    * `stateType` - The type of state to retrieve, as a `String`.

For example:

```java
@CordaInject
private UtxoLedgerService utxoLedgerService;

@CordaInject
private DigestService digestService;

PagedQuery.ResultSet<?> resultSet = utxoLedgerService.query(OwnableStateQueries.GET_BY_OWNER, StateAndRef.class)
    .setLimit(50)
    .setCreatedTimestampLimit(Instant.now())
    .setParameter("owner", digestService.hash(ownerPublicKey.getEncoded(), DigestAlgorithmName.SHA2_256).toString())
    .setParameter("stateType", ExampleOwnableState.class.getName())
    .execute();

List<StateAndRef<ExampleOwnableState>> results = (List<StateAndRef<ExampleOwnableState>>) resultSet.getResults();

while (resultSet.hasNext()) {
    results.addAll((List<StateAndRef<ExampleOwnableState>>) resultSet.next());
}
```

#### Designing Wellknown Ownable States

A wellknown ownable state can be designed by implementing the `WellKnownOwnableState` interface. It does not provide any contract functionality:

```java
@BelongsToContract(ExampleContract.class)
public class ExampleWellKnownOwnableState implements WellKnownOwnableState {

    @NotNull
    private final MemberX500Name ownerName;

    public ExampleWellKnownOwnableState(@NotNull MemberX500Name ownerName) {
        this.ownerName = ownerName;
    }

    @NotNull
    @Override
    public MemberX500Name getOwnerName() {
        return ownerName;
    }

    @NotNull
    @Override
    public List<PublicKey> getParticipants() {
        return List.of(...);
    }
}
```

#### Retrieving Wellknown Ownable States

To retrieve `WellKnownOwnableState`s for a particular owner:

1. Call `UtxoLedgerService.query`.
2. Pass in `WellKnownOwnableStateQueries.GET_BY_OWNER_NAME` as the query name.
3. Set the result class as `StateAndRef`.
4. Pass in the following parameters using `setParameter`
    * `ownerName` - The owner name, as a `String`.
    * `stateType` - The type of state to retrieve, as a `String`.

For example:

```java
@CordaInject
private UtxoLedgerService utxoLedgerService;

@CordaInject
private DigestService digestService;

PagedQuery.ResultSet<?> resultSet = utxoLedgerService.query(WellKnownOwnableStateQueries.GET_BY_OWNER_NAME, StateAndRef.class)
    .setLimit(50)
    .setCreatedTimestampLimit(Instant.now())
    .setParameter("ownerName", ownerX500Name.toString())
    .setParameter("stateType", ExampleWellKnownOwnableState.class.getName())
    .execute();

List<StateAndRef<ExampleWellKnownOwnableState>> results = (List<StateAndRef<ExampleWellKnownOwnableState>>) resultSet.getResults();

while (resultSet.hasNext()) {
    results.addAll((List<StateAndRef<ExampleWellKnownOwnableState>>) resultSet.next());
}
```

{{< note >}}
While `WellKnownOwnableState` can be used independently from `OwnableState`, they work well with each other as it can leverage the `OwnableConstraints` while querying for specific owners by name instead of by `PublicKey`s.
{{< /note >}}

### `issuable`

`com.r3.corda.ledger.utxo.issuable`

The `issuable` module designs states that have an issuer as part of the state, verifying that
any issuance of the state has been signed by the issuer, thus restricting who can issue states
of this particular type.

#### Designing Issuable States

An issuable state can be designed by implementing the `IssuableState` interface:

```java
@BelongsToContract(ExampleIssuableContract.class)
public class ExampleIssuableState implements IssuableState {

    @NotNull
    private final PublicKey issuer;

    public ExampleIssuableState(@NotNull PublicKey issuer) {
        this.issuer = issuer;
    }

    @NotNull
    @Override
    public PublicKey getIssuer() {
        return issuer;
    }

    @NotNull
    @Override
    public List<PublicKey> getParticipants() {
        return List.of(...);
    }
}
```

#### Designing Issuable Contracts

The contract for issuable states needs to verify that the issuance rules are adhered to; that is, that
the issuer signs for issuance and deletion of any issuable states. This can be achieved by invoking
the `IssuableConstraints` helpers provided in the library.

```java
public final class ExampleIssuableContract extends DelegatedContract<ExampleIssuableContract.ExampleIssuableContractCommand> {

    @NotNull
    @Override
    protected List<Class<? extends ExampleIssuableContract.ExampleIssuableContractCommand>> getPermittedCommandTypes() {
        return List.of(Create.class, Delete.class);
    }

    interface ExampleIssuableContractCommand extends VerifiableCommand, ContractStateType<ExampleIssuableState> {
    }

    public final static class Create implements ExampleIssuableContractCommand {

        @NotNull
        @Override
        public Class<ExampleIssuableState> getContractStateType() {
            return ExampleIssuableState.class;
        }

        @Override
        public void verify(@NotNull UtxoLedgerTransaction transaction) {
            IssuableConstraints.verifyCreate(transaction, getContractStateType());
        }
    }

    public final static class Delete implements ExampleIssuableContractCommand {

        @NotNull
        @Override
        public Class<ExampleIssuableState> getContractStateType() {
            return ExampleIssuableState.class;
        }

        @Override
        public void verify(@NotNull UtxoLedgerTransaction transaction) {
            IssuableConstraints.verifyCreate(transaction, getContractStateType());
        }
    }
}
```

#### Retrieving Issuable States

To retrieve `IssuableState`s for a particular issuer:

1. Call `UtxoLedgerService.query`.
2. Pass in `IssuableStateQueries.GET_BY_ISSUER` as the query name.
3. Set the result class as `StateAndRef`.
4. Pass in the following parameters using `setParameter`
    * `issuer` - Parse the issuer key into a `String` using the `DigestService`.
    * `stateType` - The type of state to retrieve, as a `String`.

For example:

```java
@CordaInject
private UtxoLedgerService utxoLedgerService;

@CordaInject
private DigestService digestService;

PagedQuery.ResultSet<?> resultSet = utxoLedgerService.query(IssuableStateQueries.GET_BY_ISSUER, StateAndRef.class)
    .setLimit(50)
    .setCreatedTimestampLimit(Instant.now())
    .setParameter("issuer", digestService.hash(issuerPublicKey.getEncoded(), DigestAlgorithmName.SHA2_256).toString())
    .setParameter("stateType", ExampleIssuableState.class.getName())
    .execute();

List<StateAndRef<ExampleIssuableState>> results = (List<StateAndRef<ExampleIssuableState>>) resultSet.getResults();

while (resultSet.hasNext()) {
    results.addAll((List<StateAndRef<ExampleIssuableState>>) resultSet.next());
}
```

#### Designing Wellknown Issuable States

A wellknown issuable state can be designed by implementing the `WellKnownIssuableState` interface:

```java
@BelongsToContract(ExampleContract.class)
public class ExampleWellKnownIssuableState implements WellKnownIssuableState {

    @NotNull
    private final MemberX500Name issuerName;

    public ExampleWellKnownIssuableState(@NotNull MemberX500Name issuerName) {
        this.issuerName = issuerName;
    }

    @NotNull
    @Override
    public MemberX500Name getIssuerName() {
        return issuerName;
    }

    @NotNull
    @Override
    public List<PublicKey> getParticipants() {
        return List.of(...);
    }
}
```

{{< note >}}
While `WellKnownIssuableState` can be used independently from `IssuableState`, they work well with each other as it can leverage the `IssuableConstraints` while querying for specific issuers by name instead of by `PublicKey`s.
{{</note>}}

#### Retrieving Wellknown Issuable States

To retrieve `WellKnownIssuableState`s for a particular owner:

1. Call `UtxoLedgerService.query`.
2. Pass in `WellKnownIssuableStateQueries.GET_BY_ISSUER_NAME` as the query name.
3. Set the result class as `StateAndRef`.
4. Pass in the following parameters using `setParameter`
    * `issuerName` - The issuer name, as a `String`.
    * `stateType` - The type of state to retrieve, as a `String`.

For example:

```java
@CordaInject
private UtxoLedgerService utxoLedgerService;

@CordaInject
private DigestService digestService;

PagedQuery.ResultSet<?> resultSet = utxoLedgerService.query(WellKnownIssuableStateQueries.GET_BY_OWNER_NAME, StateAndRef.class)
    .setLimit(50)
    .setCreatedTimestampLimit(Instant.now())
    .setParameter("issuerName", issuerX500Name.toString())
    .setParameter("stateType", ExampleWellKnownIssuableState.class.getName())
    .execute();

List<StateAndRef<ExampleWellKnownIssuableState>> results = (List<StateAndRef<ExampleWellKnownIssuableState>>) resultSet.getResults();

while (resultSet.hasNext()) {
    results.addAll((List<StateAndRef<ExampleWellKnownIssuableState>>) resultSet.next());
}
```
