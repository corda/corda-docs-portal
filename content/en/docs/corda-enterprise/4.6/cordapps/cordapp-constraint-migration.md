---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-cordapps-versioning
tags:
- cordapp
- constraint
- migration
title: CorDapp constraints migration
weight: 4
---

# CorDapp constraints migration

{{< note >}}
Before reading this page, you should be familiar with the key concepts of [Contract Constraints](api-contract-constraints.md).
{{< /note >}}

Corda 4 introduces and recommends building signed CorDapps that issue states with signature constraints. When building transactions in Corda 4, existing on-ledger states that were issued before Corda 4 are only automatically transitioned to the new Signature Constraint if they were originally using the CZ Whitelisted Constraint. Here, we explain how to modify existing CorDapp flows to explicitly consume and evolve pre Corda 4 states.

## Upgrading from a Corda 3.x CorDapp to Corda 4

Faced with the exercise of upgrading an existing Corda 3.x CorDapp to Corda 4, you need to consider the following.

### What existing unconsumed states have been issued on ledger by a previous version of this CorDapp and using other constraint types?

If you have existing hash constrained states, see [Migrating hash constraints](#migrating-hash-constraints).

If you have existing CZ whitelisted constrained states, see [Migrating CZ whitelisted constraints](#migrating-cz-whitelisted-constraints).

If you have existing **always accept** constrained states, these are not consumable nor evolvable as they offer no security and should only be used in test environments.

### What type of contract states does my CorDapp use?

Linear states typically evolve over an extended period of time (defined by the lifecycle of the associated business use case), and thus are prime candidates for constraints migration.

Fungible states are created by an issuer and transferred around a Corda network until explicitly exited (by the same issuer). They do not evolve as linear states, but are transferred between participants on a network. Their consumption may produce additional new output states to represent adjustments to the original state (for example, change when spending cash).

For the purposes of constraints migration, it is desirable that any new output states are produced using the new Corda 4 signature constraint types. Where you have long transaction chains of fungible states, it may be advisable to send them back to the issuer for re-issuance (this is called “chain snipping” and has performance advantages as well as simplifying constraints type migration).


### Should I use the **implicit** or **explicit** upgrade path?

The general recommendation for Corda 4 is to use **implicit** upgrades for the reasons described [here](../cordapps/api-contract-constraints.md#implicit-vs-explicit-upgrades). **Implicit** upgrades allow pre-authorising multiple implementations of the contract ahead of time. They do not require additional coding and do not incur a complex choreographed operational upgrade process.

{{< warning >}}
The steps outlined in this page assume you are using the same CorDapp Contract (for example, same state definition, commands and verification code) and
wish to use that CorDapp to leverage the upgradeability benefits of Corda 4 signature constraints. If you are looking to upgrade code within an existing
Contract CorDapp please read [Contract and state versioning](../node/operating/cm-updating-cordapp.md#contract-and-state-versioning) and [CorDapp Upgradeability Guarantees](cordapp-upgradeability.md) to understand your options.
{{< /warning >}}


Please also remember that *states are always consumable if the version of the CorDapp that issued (created) them is installed*.
In the simplest of scenarios, it may be easier to re-issue existing hash or CZ whitelist constrained states (for example, exit them from the ledger using
the original unsigned CorDapp and re-issuing them using the new signed CorDapp).



## Migrating hash constraints

{{< note >}}
These instructions only apply to CorDapp Contract JARs (unless otherwise stated).
{{< /note >}}

### Corda 4.6

Corda 4.6 requires some additional steps to consume and evolve pre-existing on-ledger **hash** constrained states:


* All Corda Nodes in the same CZ or business network that may encounter a transaction chain with a hash constrained state must be started using
relaxed hash constraint checking mode as described in [Hash constrained states in private networks](../cordapps/api-contract-constraints.md#hash-constrained-states-in-private-networks).
* CorDapp flows that build transactions using pre-existing *hash-constrained* states must explicitly set output states to use *signature constraints*
and specify the related public key(s) used in signing the associated CorDapp Contract JAR:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
// This will read the signers for the deployed CorDapp.
val attachment = this.serviceHub.cordappProvider.getContractAttachmentID(contractClass)
val signers = this.serviceHub.attachments.openAttachment(attachment!!)!!.signerKeys

// Create the key that will have to pass for all future versions.
val ownersKey = signers.first()

val txBuilder = TransactionBuilder(notary)
        // Set the Signature constraint on the new state to migrate away from the hash constraint.
        .addOutputState(outputState, constraint = SignatureAttachmentConstraint(ownersKey))
```
{{% /tab %}}

{{% tab name="java" %}}
```java
// This will read the signers for the deployed CorDapp.
SecureHash attachment = this.getServiceHub().getCordappProvider().getContractAttachmentID(contractClass);
List<PublicKey> signers = this.getServiceHub().getAttachments().openAttachment(attachment).getSignerKeys();

// Create the key that will have to pass for all future versions.
PublicKey ownersKey = signers.get(0);

TransactionBuilder txBuilder = new TransactionBuilder(notary)
        // Set the Signature constraint on the new state to migrate away from the hash constraint.
        .addOutputState(outputState, myContract, new SignatureAttachmentConstraint(ownersKey))
```
{{% /tab %}}

{{< /tabs >}}


* As a node operator you need to add the new signed version of the contracts CorDapp to the `/cordapps` folder together with the latest version of the flows jar.
Please also ensure that the original unsigned contracts CorDapp is removed from the `/cordapps` folder (this will already be present in the
node's attachments store) to ensure the lookup code in step 2 retrieves the correct signed contract CorDapp JAR.



## Migrating CZ whitelisted constraints

{{< note >}}
These instructions only apply to CorDapp Contract JARs (unless otherwise stated).

{{< /note >}}

### Corda 4.5

Corda 4.5 requires some additional steps to consume and evolve pre-existing on-ledger **CZ whitelisted** constrained states:


* As the original developer of the CorDapp, the first step is to sign the latest version of the JAR that was released (see [Building and installing a CorDapp](../cordapps/cordapp-build-systems.md)).
The key used for signing will be used to sign all subsequent releases, so it should be stored appropriately. The JAR can be signed by multiple keys owned
by different parties and it will be expressed as a `CompositeKey` in the `SignatureAttachmentConstraint` (see [API: Core types](../api-core-types)).
* The new Corda 4 signed CorDapp JAR must be registered with the CZ network operator (as whitelisted in the network parameters which are distributed
to all nodes in that CZ). The CZ network operator should check that the JAR is signed and not allow any more versions of it to be whitelisted in the future.
From now on the development organisation that signed the JAR is responsible for signing new versions. The process of CZ network CorDapp whitelisting depends on how the Corda network is configured:

* If using a hosted CZ network (such as [Corda Network Foundation](../corda-network/the-corda-network.html) or
[Corda Network Pre-Production/UAT environment](../corda-network/uat.html)) running an Identity Operator (formerly known as Doorman) and
Network Map Service, you should manually send the hashes of the two JARs to the CZ network operator and request these be added using
their network parameter update process.
* If using a local network created using the Network Bootstrapper tool, please follow the instructions in
[Updating the contract whitelist for bootstrapped networks](../network-bootstrapper.md#bootstrapper-updating-whitelisted-contracts) to can add both CorDapp Contract JAR hashes.

* Any flow that builds transactions using this CorDapp will automatically transition states to use the `SignatureAttachmentConstraint` if
no other constraint is specified and the CorDapp continues to be whitelisted. Therefore, there are two ways to alter the existing code.
  * Do not specify a constraint
  * Explicitly add a Signature Constraint



The code below details how to explicitly add a Signature Constraint:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// This will read the signers for the deployed CorDapp.
val attachment = this.serviceHub.cordappProvider.getContractAttachmentID(contractClass)
val signers = this.serviceHub.attachments.openAttachment(attachment!!)!!.signerKeys

// Create the key that will have to pass for all future versions.
val ownersKey = signers.first()

val txBuilder = TransactionBuilder(notary)
        // Set the Signature constraint on the new state to migrate away from the WhitelistConstraint.
        .addOutputState(outputState, constraint = SignatureAttachmentConstraint(ownersKey))
```
{{% /tab %}}

{{% tab name="java" %}}
```java
// This will read the signers for the deployed CorDapp.
SecureHash attachment = this.getServiceHub().getCordappProvider().getContractAttachmentID(contractClass);
List<PublicKey> signers = this.getServiceHub().getAttachments().openAttachment(attachment).getSignerKeys();

// Create the key that will have to pass for all future versions.
PublicKey ownersKey = signers.get(0);

TransactionBuilder txBuilder = new TransactionBuilder(notary)
        // Set the Signature constraint on the new state to migrate away from the WhitelistConstraint.
        .addOutputState(outputState, myContract, new SignatureAttachmentConstraint(ownersKey))
```
{{% /tab %}}

{{< /tabs >}}


* As a node operator, you need to add the new signed version of the contracts CorDapp to the `/cordapps` folder together with the latest version of the flows jar.
Please also ensure that the original unsigned contracts CorDapp is removed from the `/cordapps` folder (this will already be present in the
nodes attachments store) to ensure the lookup code in step 3 retrieves the correct signed contract CorDapp JAR.
