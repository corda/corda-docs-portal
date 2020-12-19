---
aliases:
- /head/release-notes.html
- /HEAD/release-notes.html
- /release-notes.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-7:
    identifier: corda-os-4-7-release-notes
    weight: 1
tags:
- release
- notes
title: Release notes
---


# Corda release notes

## Corda 4.7

Welcome to the Corda 4.7 release notes. This release introduces several new features and enhancements, and fixes a number of known issues from previous releases.

Just as prior releases have brought with them commitments to wire and API stability, Corda 4.7 comes with those same guarantees.

States and apps valid in Corda 3.0 and above are usable in Corda 4.7.

### New features and enhancements

#### Ability to break transaction backchains by reissuing a state with a guaranteed state replacement

Reissuing a state is usually considered for privacy reasons or to optimise performance. This has already been possible in Corda, using an approach where a CorDapp developer could write custom logic to allow a state to periodically be exited and then reissued onto the ledger in separate transactions. However, this approach relies on the developer's foresight in anticipating performance issues when chains would grow to a certain size, and its implementation varies in consistency and success.

Corda 4.7 introduces a new mechanism to reissue states, bringing platform support for creating breaks in transaction chains where state owners can request a transaction break through a flow and rest assured that a state is not removed without being replaced. Nodes can now request the reissuance of a state by returning it to the issuer or to another trusted party. This reissuance mechanism is atomic and risk-free and provides better support for a developer pattern known as “chain snipping" - once a state is reissued, its pre-reissuance transaction history is no longer shared as part of transaction resolution. This improves performance for applications that build up very long transaction chains, and can help avoid leakage of information regarding the state’s history.

For more information about this feature, see [Reissuing a state](reissuing-states.md).

#### Business Network Membership version 1.1

Corda 4.7 introduces enhancements to the [Business Network Membership extension](business-network-membership.md) to allow for access control group reporting, batch onboarding, membership group querying, and a way to log and report actions to membership attestations.

#### Ability to interact with a Corda node via the new Multi RPC Client

A new RPC Client, called the Multi RPC Client, has been added in Corda 4.7. Node operators can use the Multi RPC client to interact with a Corda node via the `net.corda.core.messaging.CordaRPCOps` remote RPC interface.

For more information, see the [Interacting with a node](clientrpc.md) documentation section.

### Featured apps

#### Reference app: Bank in a Box

[Bank in a Box](../../apps/bankinabox/_index.md) is a new, production-ready [CorDapp](cordapp-overview.md) that includes accounts, transactions, and other features typical of a retail banking application.

The app is designed to showcase key Corda features:

- Corda [Accounts](https://github.com/corda/accounts/blob/master/docs.md).
- [Scheduled states](event-scheduling.md).
- [Oracles](key-concepts-oracles.md).
- CorDapp integration with external systems.

Using a set of [flows](key-concepts-flows.md) and [APIs](../../apps/bankinabox/api-guide.md), Bank in a Box provides the ability to create intrabank payments, recurring payments, issue loans, set account limits, and more. It offers a complete solution with a straightforward UI and authenticated roles, all delivered in a [Kubernetes container](https://kubernetes.io/docs/concepts/containers/) for easy deployment.

The application highlights best practices and examples for developers who wish to build banking applications using Corda.

### Platform version change

The platform version of Corda 4.7 has been bumped up from 8 to 9.

For more information about platform versions, see [Versioning](versioning.md).


### Fixed issues

* We have fixed an issue where vault queries using the `OR` combinator and filter condition would incorrectly throw pagination errors even when the result of the queries was below the defined pagination limit (so the the page limit was not exceeded). This fix has also been propagated back to Corda Enterprise 4.5 and 4.6. [[CORDA-3874](https://r3-cev.atlassian.net/browse/CORDA-3874)].

### Known issues

* Flows responders do not perform sufficient validation checks of Business Network permissions. This could be an issue due to the potential for incorrect handling of BNO permissions by Business Network nodes, where potentially any node in the Business Network is able to modify a flow and turn the validations off. [[CORDA-4078](https://r3-cev.atlassian.net/browse/CORDA-4078)].

{{< note >}}
The list above contains known issues specific to Corda 4.7. See the release notes for previous Corda releases further down on this page for information about known issues specific to those versions.
{{< /note >}}
