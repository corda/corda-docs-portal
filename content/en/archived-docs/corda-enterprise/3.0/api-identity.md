---
aliases:
- /releases/3.0/api-identity.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-api-identity
    parent: corda-enterprise-3-0-corda-api
    weight: 1080
tags:
- api
- identity
title: 'API: Identity'
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# API: Identity

{{< note >}}
Before reading this page, you should be familiar with the key concepts of [Identity](key-concepts-identity.md).

{{< /note >}}

{{< warning >}}
The `confidential-identities` module is still not stabilised, so this API may change in future releases.
See [Corda API](corda-api.md).

{{< /warning >}}




## Party

Parties on the network are represented using the `AbstractParty` class. There are two types of `AbstractParty`:


* `Party`, identified by a `PublicKey` and a `CordaX500Name`
* `AnonymousParty`, identified by a `PublicKey` only

Using `AnonymousParty` to identify parties in states and commands prevents nodes from learning the identities
of the parties involved in a transaction when they verify the transaction’s dependency chain. When preserving the
anonymity of each party is not required (e.g. for internal processing), `Party` can be used instead.

The identity service allows flows to resolve `AnonymousParty` to `Party`, but only if the anonymous party’s
identity has already been registered with the node (typically handled by `SwapIdentitiesFlow` or
`IdentitySyncFlow`, discussed below).

Party names use the `CordaX500Name` data class, which enforces the structure of names within Corda, as well as
ensuring a consistent rendering of the names in plain text.

Support for both `Party` and `AnonymousParty` classes in Corda enables sophisticated selective disclosure of
identity information. For example, it is possible to construct a transaction using an `AnonymousParty` (so nobody can
learn of your involvement by inspection of the transaction), yet prove to specific counterparts that this
`AnonymousParty` actually corresponds to your well-known identity. This is achieved using the
`PartyAndCertificate` data class, which contains the X.509 certificate path proving that a given `AnonymousParty`
corresponds to a given `Party`. Each `PartyAndCertificate` can be propagated to counterparties on a need-to-know
basis.

The `PartyAndCertificate` class is also used by the network map service to represent well-known identities, with the
certificate path proving the certificate was issued by the doorman service.


## Confidential identities

Confidential identities are key pairs where the corresponding X.509 certificate (and path) are not made public, so that
parties who are not involved in the transaction cannot identify the owner. They are owned by a well-known identity,
which must sign the X.509 certificate. Before constructing a new transaction the involved parties must generate and
exchange new confidential identities, a process which is managed using `SwapIdentitiesFlow` (discussed below). The
public keys of these confidential identities are then used when generating output states and commands for the
transaction.

Where using outputs from a previous transaction in a new transaction, counterparties may need to know who the involved
parties are. One example is the `TwoPartyTradeFlow`, where an existing asset is exchanged for cash. If confidential
identities are being used, the buyer will want to ensure that the asset being transferred is owned by the seller, and
the seller will likewise want to ensure that the cash being transferred is owned by the buyer. Verifying this requires
both nodes to have a copy of the confidential identities for the asset and cash input states. `IdentitySyncFlow`
manages this process. It takes as inputs a transaction and a counterparty, and for every confidential identity involved
in that transaction for which the calling node holds the certificate path, it sends this certificate path to the
counterparty.


### SwapIdentitiesFlow

`SwapIdentitiesFlow` is typically run as a subflow of another flow. It takes as its sole constructor argument the
counterparty we want to exchange confidential identities with. It returns a mapping from the identities of the caller
and the counterparty to their new confidential identities. In the future, this flow will be extended to handle swapping
identities with multiple parties at once.

You can see an example of using `SwapIdentitiesFlow` in `TwoPartyDealFlow.kt`:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
@Suspendable
override fun call(): SignedTransaction {
    progressTracker.currentStep = GENERATING_ID
    val txIdentities = subFlow(SwapIdentitiesFlow(otherSideSession.counterparty))
    val anonymousMe = txIdentities[ourIdentity] ?: ourIdentity.anonymise()
    val anonymousCounterparty = txIdentities[otherSideSession.counterparty] ?: otherSideSession.counterparty.anonymise()

```
{{% /tab %}}



{{< /tabs >}}

`SwapIdentitiesFlow` goes through the following key steps:


* Generate a new confidential identity from our well-known identity
* Create a `CertificateOwnershipAssertion` object containing the new confidential identity (X500 name, public key)
* Sign this object with the confidential identity’s private key
* Send the confidential identity and aforementioned signature to counterparties, while receiving theirs
* Verify the signatures to ensure that identities were generated by the involved set of parties
* Verify the confidential identities are owned by the expected well known identities
* Store the confidential identities and return them to the calling flow

This ensures not only that the confidential identity X.509 certificates are signed by the correct well-known
identities, but also that the confidential identity private key is held by the counterparty, and that a party cannot
claim ownership of another party’s confidential identities.


### IdentitySyncFlow

When constructing a transaction whose input states reference confidential identities, it is common for counterparties
to require knowledge of which well-known identity each confidential identity maps to. `IdentitySyncFlow` handles this
process. You can see an example of its use in `TwoPartyTradeFlow.kt`.

`IdentitySyncFlow` is divided into two parts:


* `IdentitySyncFlow.Send`
* `IdentitySyncFlow.Receive`

`IdentitySyncFlow.Send` is invoked by the party initiating the identity synchronization:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// Now sign the transaction with whatever keys we need to move the cash.
val partSignedTx = serviceHub.signInitialTransaction(ptx, cashSigningPubKeys)

// Sync up confidential identities in the transaction with our counterparty
subFlow(IdentitySyncFlow.Send(sellerSession, ptx.toWireTransaction(serviceHub)))

// Send the signed transaction to the seller, who must then sign it themselves and commit
// it to the ledger by sending it to the notary.
progressTracker.currentStep = COLLECTING_SIGNATURES
val sellerSignature = subFlow(CollectSignatureFlow(partSignedTx, sellerSession, sellerSession.counterparty.owningKey))
val twiceSignedTx = partSignedTx + sellerSignature

```
{{% /tab %}}



{{< /tabs >}}

The identity synchronization flow goes through the following key steps:


* Extract participant identities from all input and output states and remove any well known identities. Required
signers on commands are currently ignored as they are presumed to be included in the participants on states, or to
be well-known identities of services (such as an oracle service)
* For each counterparty node, send a list of the public keys of the confidential identities, and receive back a list
of those the counterparty needs the certificate path for
* Verify the requested list of identities contains only confidential identities in the offered list, and abort
otherwise
* Send the requested confidential identities as `PartyAndCertificate` instances to the counterparty

{{< note >}}
`IdentitySyncFlow` works on a push basis. The initiating node can only send confidential identities it has
the X.509 certificates for, and the remote nodes can only request confidential identities being offered (are
referenced in the transaction passed to the initiating flow). There is no standard flow for nodes to collect
confidential identities before assembling a transaction, and this is left for individual flows to manage if
required.

{{< /note >}}
Meanwhile, `IdentitySyncFlow.Receive` is invoked by all the other (non-initiating) parties involved in the identity
synchronization process:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
// Sync identities to ensure we know all of the identities involved in the transaction we're about to
// be asked to sign
subFlow(IdentitySyncFlow.Receive(otherSideSession))

```
{{% /tab %}}



{{< /tabs >}}

`IdentitySyncFlow` will serve all confidential identities in the provided transaction, irrespective of well-known
identity. This is important for more complex transaction cases with 3+ parties, for example:


* Alice is building the transaction, and provides some input state *x* owned by a confidential identity of Alice
* Bob provides some input state *y* owned by a confidential identity of Bob
* Charlie provides some input state *z* owned by a confidential identity of Charlie

Alice may know all of the confidential identities ahead of time, but Bob not know about Charlie’s and vice-versa.
The assembled transaction therefore has three input states *x*, *y* and *z*, for which only Alice possesses
certificates for all confidential identities. `IdentitySyncFlow` must send not just Alice’s confidential identity but
also any other identities in the transaction to the Bob and Charlie.
