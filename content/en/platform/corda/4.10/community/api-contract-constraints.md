---
aliases:
- /head/api-contract-constraints.html
- /HEAD/api-contract-constraints.html
- /api-contract-constraints.html
date: '2021-08-11'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-api-contract-constraints
    parent: corda-community-4-10-corda-api
    weight: 200
tags:
- api
- contract
- constraints
title: 'API: Contract Constraints'
---

# Contract constraints
**Contract constraints** let users know which versions of a CorDapp they can use to provide the contract for a transaction. The constraints property is stored in each state.

Contract constraints also solve upgrade-related security problems. If an attacker were to force an upgrade to the CorDapp, they could add security vulnerabilities and create or edit states. You can protect states from this type of attack by only allowing states to be affected by contracts in known versions of a CorDapp.

This document explains:

* What contract constraints are and which types to use.
* How to sign a CorDapp.
* How to store and retrieve a CorDapp.
* What blacklisting is.
* What contract/state agreement is and how to achieve it.
* How to use contract constraints in transactions.
* How to propagate constraints.
* How to a troubleshoot a `MissingContractAttachments` exception.


## Glossary
These terms are used throughout this document:

*contract constraints* Instructions in a CorDapp's attachments that determine which versions of a CorDapp parties in a transaction can use to provide contracts.

**composite key** A key that consists of two or more attributes that together uniquely identify an entity occurrence.

*signature constraint* A constraint that lets participants use any version of the CorDapp signed by the `CompositeKey`.

*blacklisting* A process that prevents a transaction signer from processing transactions.



## Implicit and explicit contract upgrades

You can upgrade smart contracts via:

* **Implicit upgrade**. Pre-authorise multiple implementations of the contract ahead of time using constraints. This lets you upgrade contracts without needing to upgrade transactions for every state on the ledger. However, with implicit upgrade, you place more faith in third parties, who could change the CorDapp in ways you do not expect or agree with.
* **Explicit upgrade**. Create a special *contract upgrade transaction* and get all the participants listed on a state to sign it using the contract upgrade flows. This lets you upgrade states even if they have a constraint. Unlike implicit upgrade, this is a complex method which requires all participants to sign and manually authorise the upgrade, and consumes notary and ledger resources.


This article focuses on implicit contract upgrades. To learn about the explicit upgrades see [Release new CorDapp versions](upgrading-cordapps.md).



### Types of contract constraints

You can use two types of contract constraints:

* **Signature constraints**: This constraint lets participants use any version of the CorDapp signed by the `CompositeKey`. This allows CorDapp issuers to express the complex social and business relationships that arise around code ownership. You could release a new version of a CorDapp and apply it to an existing state as long as it has been signed by the same key(s) as the original version.
* **Always accept constraint**: Allows any version of the CorDapp. This is insecure and only intended for testing.

Before signature constraints were released with Corda 4.0, constraints were managed with hash and compatibility zone whitelist constraints. These constraints are still available, but make it difficult to upgrade your CorDapp:

* **Hash constraint**: Participants can only use one version of the CorDapp state. This prevents the CorDapp from being upgraded in the future while still making use of any states created using the original version.
* **Compatibility zone whitelisted (or CZ whitelisted) constraint**: The compatibility zone operator lists the hashes of the versions that can be used with a contract class name.

You can [migrate CorDapp contraints](cordapp-constraint-migration.md) from older versions by consuming and evolving pre-Corda 4 issued hash or CZ whitelisted constrained states using a Corda 4 signed CorDapp with signature constraints.


## Signature constraints


**Signature constraints** let you express complex social and business relationships while allowing smooth migration of existing data to new versions of your CorDapp.

You can use signature constraints to specify flexible threshold policies. However, if you use the automatic support, then a state requires that the attached CorDapp is signed by every key that signed the first attachment. For example, if Alice and Bob signed a CorDapp that was used to issue some states, every transaction must include an attachment signed by Alice and Bob. This allows the CorDapp to be upgraded and changed while still remaining valid for use with the previously issued states.

You can create a more complex policy that will release the constraint with fewer signatures than the total number of possible signers. This makes it possible for multiple versions to be valid across the network as long as the designated number of signers agree with the updates.

The `TransactionBuilder` uses signature constraints when adding output states for all signed transactions by default. See [Using Contract Constraints in Transactions](#using-contract-constraints-in-transactions).

## Signing CorDapps

CorDapps that use signature constraints must be signed by a `CompositeKey` or a simpler `PublicKey`. CorDapps can be signed by a single organisation or multiple organisations. After the CorDapp is signed, it can be distributed to the relevant Corda nodes. Signed CorDapps require a [version number](versioning.md).

{{< note >}}
The platform currently supports `CompositeKey`s, up to a maximum of 20 keys.
This maximum limit assumes keys that are either 2048-bit `RSA` keys or 256-bit elliptic curve (`EC`) keys.
{{< /note >}}

When a node receives a transaction, it verifies that the CorDapps attached to it have the signatures required by the transaction's signature constraints. This ensures that the versions of each CorDapp are acceptable to the transaction’s input states.

Nodes will also trust attachments that:
* Have a common signature with another attachment on the node. This means that nodes do not need to have every version of a CorDapp uploaded to verify transactions running older versions of a CorDapp - it only needs one version of the CorDapp contract.
* Are installed manually.
* Are uploaded via RPC.

You can [sign a CorDapp directly from Gradle](cordapp-build-systems.html#signing-the-cordapp-jar).


### CorDapp contract storage and retrieval

If a CorDapp JAR contains classes implementing the `Contract` interface, the node automatically loads the JAR into its `AttachmentStorage` and makes it available in `ContractAttachments`.

You can retrieve a JAR by hash using `AttachmentStorage.openAttachment`. You can install JARs on the node, or they will be fetched automatically over the network when the node receives a transaction.


{{< warning >}}
Follow best practices by [structuring your CorDapp](cordapp-structure.md) as two modules: one that only contains contracts, states, and core data types, and another containing the rest of the CorDapp elements. If you structure your CorDapp as a single module, your entire CorDapp is published to the ledger. This causes the ledger to view changes to your flows or other parts of your CorDapp as a new CorDapp, and could trigger unnecessary upgrade procedures.
{{< /warning >}}


## Blacklisting

If you need to prevent a signer from processing transactions, you can *blacklist* them. The signer will not be able to upload attachments or process transactions. It only takes one blacklisted signer for a node to consider an attachment untrusted.

CorDapps and other attachments installed on a node still run, even if they are signed by a blacklisted key. Only attachments
received from a peer are affected.

You can also [blacklist keys](corda-configuration-file.html#corda-configuration-file-blacklisted-attachment-signer-keys).

Below are two examples of scenarios involving blacklisted signing keys. In each example:

* Alice has `Contracts CorDapp` installed.
* Bob has an upgraded version of `Contracts CorDapp` (known as `Contracts CorDapp V2`) installed.
* Both Alice and Bob have the `Workflows CorDapp`, allowing them to transact with each other.
* `Contracts CorDapp` is signed by both Alice and Bob.
* `Contracts CorDapp V2` is signed by both Alice and Bob.



### Example without blacklisting

In this example, `Alice` has not blacklisted any attachment signing keys.

1. `Bob` initiates a transaction with `Alice`.
2. `Alice` receives `Contracts CorDapp V2` and stores it.
3. `Alice` verifies the attachments in the contract verification code and accepts `Contracts CorDapp V2`.
4. `Alice` runs the contract verification code in `Contracts CorDapp V2`.



### Example with blacklisting

In this example, `Alice` blacklists `Bob`’s attachment signing key.

1.  `Bob` initiates a transaction with `Alice`.
2.  `Alice` receives `Contracts CorDapp V2` and stores it.
3.  `Alice` checks the attachments in the contract verification code and rejects `Contracts CorDapp V2` because it is signed by `Bob`’s blacklisted key.
4. The transaction fails.



### Contract/state agreement

A `ContractState` must explicitly indicate which `Contract` it belongs to. The node checks that the "owning" contract is bundled with each state. Otherwise we would not be able to guarantee that the transition of the `ContractState` will be verified against the business rules that should apply to it.

There are two mechanisms for indicating ownership. One is to annotate the `ContractState` with the `BelongsToContract` annotation, indicating the `Contract` class to which it is tied:

{{< tabs name="tabs-1" >}}
{{% tab name="java" %}}
```java
@BelongsToContract(MyContract.class)
public class MyState implements ContractState {
    // implementation goes here
}
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
@BelongsToContract(MyContract::class)
data class MyState(val value: Int) : ContractState {
    // implementation goes here
}
```
{{% /tab %}}

{{< /tabs >}}

The other is to define the `ContractState` class as an inner class of the `Contract` class:

{{< tabs name="tabs-2" >}}
{{% tab name="java" %}}
```java
public class MyContract implements Contract {

    public static class MyState implements ContractState {
        // state implementation goes here
    }

    // contract implementation goes here
}
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
class MyContract : Contract {

    data class MyState(val value: Int) : ContractState {
        // state implementation goes here
    }

    // contract implementation goes here
}
```
{{% /tab %}}

{{< /tabs >}}

If a `ContractState`’s owning `Contract` cannot be identified by either of these mechanisms, and the `targetVersion` of the
CorDapp is 4 or greater, then transaction verification will fail with a `TransactionRequiredContractUnspecifiedException`. If
the owning `Contract` *can* be identified, but the `ContractState` has been bundled with a different contract, then
transaction verification will fail with a `TransactionContractConflictException`.



### Using contract constraints in transactions

Transactions use the CorDapp version defined in its attachments. The JAR containing the state and contract classes, and any optional dependencies, is attached to the transaction. If a node has not received a specific JAR before, it will download other copies of it from other nodes on the network for verification.

The `TransactionBuilder` manages the details of constraints for you by selecting both constraints
and attachments to ensure they line up correctly. By default, the `TransactionBuilder` uses [Signature Constraints](#signature-constraints) for any issuance transactions if the CorDapp attached to it is signed.

To manually define the contract constraint of an output state, see the example below:

{{< tabs name="tabs-3" >}}
{{% tab name="java" %}}
```java
TransactionBuilder transaction() {
    TransactionBuilder transaction = new TransactionBuilder(notary());
    // Signature Constraint used if CorDapp is signed
    transaction.addOutputState(state);
    // Explicitly using a Signature Constraint
    transaction.addOutputState(state, CONTRACT_ID, new SignatureAttachmentConstraint(getOurIdentity().getOwningKey()));
    // Explicitly using a Hash Constraint
    transaction.addOutputState(state, CONTRACT_ID, new HashAttachmentConstraint(getServiceHub().getCordappProvider().getContractAttachmentID(CONTRACT_ID)));
    // Explicitly using a Whitelisted by Zone Constraint
    transaction.addOutputState(state, CONTRACT_ID, WhitelistedByZoneAttachmentConstraint.INSTANCE);
    // Explicitly using an Always Accept Constraint
    transaction.addOutputState(state, CONTRACT_ID, AlwaysAcceptAttachmentConstraint.INSTANCE);

    // other transaction stuff
    return transaction;
}
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
private fun transaction(): TransactionBuilder {
    val transaction = TransactionBuilder(notary())
    // Signature Constraint used if CorDapp is signed
    transaction.addOutputState(state)
    // Explicitly using a Signature Constraint
    transaction.addOutputState(state, constraint = SignatureAttachmentConstraint(ourIdentity.owningKey))
    // Explicitly using a Hash Constraint
    transaction.addOutputState(state, constraint = HashAttachmentConstraint(serviceHub.cordappProvider.getContractAttachmentID(CONTRACT_ID)!!))
    // Explicitly using a Whitelisted by Zone Constraint
    transaction.addOutputState(state, constraint = WhitelistedByZoneAttachmentConstraint)
    // Explicitly using an Always Accept Constraint
    transaction.addOutputState(state, constraint = AlwaysAcceptAttachmentConstraint)

    // other transaction stuff
    return transaction
}
```
{{% /tab %}}

{{< /tabs >}}




### Constraints propagation

The `TransactionBuilder` API gives developers the option to construct output states with a constraint.

For the ledger to remain consistent, the expected behavior is for output states to inherit the constraints of input states.
This guarantees that, for example, a transaction cannot output a state with the `AlwaysAcceptAttachmentConstraint` when the
corresponding input state was the `SignatureAttachmentConstraint`. If the rule is enforced, the output state is spent under similar conditions to the state it was created in.

The platform implements and enforces the constraint propagation logic unless disabled with `@NoConstraintPropagation` on the `Contract` class. In this case, the CorDapps enforce the logic.

For contracts that are not annotated with `@NoConstraintPropagation`, the platform implements a constraint transition policy to ensure security and allow the possibility to transition to the new `SignatureAttachmentConstraint`.

During transaction building the `AutomaticPlaceholderConstraint` for output states is resolved and the best contract attachment versions are selected based on a variety of factors. If it can’t find attachments in storage or there are no
possible constraints, the `TransactionBuilder` will throw an exception.


## Troubleshooting


If the node cannot resolve an attachment constraint it will throw a `MissingContractAttachments` exception. There are three common sources of`MissingContractAttachments` exceptions:


### Not setting CorDapp packages in tests

You must specify which CorDapp packages to scan when you run tests. Provide a package containing the contract class in `MockNetworkParameters`. See [Testing CorDapps](api-testing.md).

You must also specify a package when testing using `DriverDSl`. `DriverParameters` has a property `cordappsForAllNodes` (Kotlin)
or method `withCordappsForAllNodes` in Java. Pass the collection of `TestCordapp` created by utility method `TestCordapp.findCordapp(String)`.

This is how you would create two Cordapps with Finance CorDapp flows and Finance CorDapp contracts:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
Driver.driver(DriverParameters(
    cordappsForAllNodes = listOf(
        TestCordapp.findCordapp("net.corda.finance.schemas"),
        TestCordapp.findCordapp("net.corda.finance.flows")
    )
) {
    // Your test code goes here
})
```
{{% /tab %}}

{{% tab name="java" %}}
```java
Driver.driver(
    new DriverParameters()
        .withCordappsForAllNodes(
            Arrays.asList(
                TestCordapp.findCordapp("net.corda.finance.schemas"),
                TestCordapp.findCordapp("net.corda.finance.flows")
            )
        ),
    dsl -> {
      // Your test code goes here
    }
);
```
{{% /tab %}}

{{< /tabs >}}


### Starting a node that is missing CorDapp(s)

Make sure you place all CorDapp JARs in the `cordapps` directory of each node. The Gradle Cordform task `deployNodes` copies all JARs by default, if you have specified CorDapps to deploy. See [Creating nodes locally](generating-a-node.html#creating-nodes-locally) for detailed instructions.


### Including an incorrect fully-qualified contract name

Make sure you specify the fully-qualified name of the contract correctly. For example, if you defined `MyContract` in
the package `com.mycompany.myapp.contracts`, but the fully-qualified contract name you pass to the
`TransactionBuilder` is `com.mycompany.myapp.MyContract` (instead of `com.mycompany.myapp.contracts.MyContract`), then `TransactionBuilder` will throw a `MissingContractAttachments` exception.
