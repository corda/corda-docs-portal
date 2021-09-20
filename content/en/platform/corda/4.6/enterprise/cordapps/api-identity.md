---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-cordapps-identity
    name: "Identities in a CorDapp"
    parent: corda-enterprise-4-6-cordapps
tags:
- api
- identity
title: CorDapp Identities
weight: 9
---




# CorDapp Identities

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



