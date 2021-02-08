---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-7:
    identifier: "corda-enterprise-4-7-release-notes"
    name: "Release notes"
tags:
- release
- notes
- enterprise
title: Corda Enterprise release notes
weight: 1

---


# Corda Enterprise release notes

## Corda Enterprise 4.7 release overview

This release introduces a number of new features and enhancements, and fixes for known issues from previous releases.

Just as prior releases have brought with them commitments to wire and API stability, Corda 4.7 comes with those same guarantees.

States and apps valid in Corda 3.0 and above are usable in Corda 4.7.

The main new features and enhancements in Corda Enterprise 4.7 are listed below:

* [Archiving Service](#archiving-service).
* [Improved notary backpressure (ETA) mechanism](#improved-notary-back-pressure-eta-mechanism).
* [New management consoles for node management and flow management](#new-management-consoles-for-node-management-and-flow-management).
* [Certificate rotation](#certificate-rotation).
* [Single sign-on for Azure AD](#other-changes-and-improvements).
* [HSM integration support](#other-changes-and-improvements).
* [Ability to store confidential identity keys in HSMs](#other-changes-and-improvements).
* [HSM APIs](#other-changes-and-improvements).

{{< note >}}
This page only describes functionality specific to Corda Enterprise 4.7. However, as a Corda Enterprise customer, you can also make full use of the entire range of features available as part of Corda open source releases.

See the [Corda open source release notes](../../corda-os/4.7/release-notes.md) for information about new features, enhancements, and fixes shipped as part of Corda 4.7, such as:

* [Ability to break transaction backchains by reissuing a state with a guaranteed state replacement](../../corda-os/4.7/release-notes.md#ability-to-break-transaction-backchains-by-reissuing-a-state-with-a-guaranteed-state-replacement).
* [Business Network Membership version 1.1](../../corda-os/4.7/release-notes.md#business-network-membership-version-11).
* [Ability to interact with a Corda node via the new Multi RPC Client](../../corda-os/4.7/release-notes.md#ability-to-interact-with-a-corda-node-via-the-new-multi-rpc-client).
* [Reference application: Bank in a Box](../../corda-os/4.7/release-notes.md#reference-app-bank-in-a-box).
{{< /note >}}

## New features and enhancements

### Archiving Service

The Archiving Service is a new tool that allows you, as a node operator, to archive ledger data for entirely spent transactions. This saves space and reduces pressure on node databases.

Some features of the Archiving Service:

* Use the Archiving Service with Corda command-line interface (CLI) commands. This allows you to rapidly check archiving jobs, delete data that is no longer required from the vault, import, export, and restore snapshots of the vault’s contents.
* Use the application entity manager to allow your CorDapps to access off-ledger databases.
* Integrate your archiving service with [Collaborative Recovery CorDapps](node/collaborative-recovery/introduction-cr.md) to ensure smooth running of data recovery after a disaster scenario.

See the [Archiving Service documentation section](node/archiving/archiving-setup.md) for more information.

### Improved notary backpressure (ETA) mechanism

To optimise the way notaries handle traffic, we have updated the notary backpressure mechanism (also referred to as [backpressure mechanism](notary/faq/eta-mechanism.md#what-is-the-eta-mechanism)) to improve notary performance when there is a sudden increase in notarisation requests. This change increases the accuracy of transaction retry estimates that the notary provides to the node.

As a result, the notary backpressure mechanism is now [more precise and responsive](notary/notary-load-handling.md) under "heavy traffic conditions", which leads to fewer node retries, optimised performance, and a better end-user experience for node operators.

{{< note >}}
What is the notary backpressure mechanism?

By design, a notary can operate normally under extremely high loads of traffic. The notary backpressure mechanism makes this possible through handling the notarisation requests queue and ensuring that any node retries that happen due to a timeout (usually during periods of high traffic) are a function of the notary's capacity. This mechanism ensures that nodes are guaranteed the time and capacity for notarisation requests and retries when needed. It also preserves the notary's level of efficiency by preventing the notarisation request queue from being artificially increased due to unnecessary node retries.
{{< /note >}}

### New management consoles for node management and flow management

Corda Enterprise 4.7 comes with two new management consoles:

* The **Flow management console** allows you to see the state of the flows running on a node and perform some operations on them. For more information, see [Flow management console](node/node-flow-management-console.md).
* The **Node management console** allows you to see information about a node and perform some operations on it. For more information, see [Node management console](node/management-console/_index.md).

They both run as part of the CENM [Gateway service](../../cenm/1.5/gateway-service.md).

### Certificate rotation

Corda Enterprise 4.7 introduces a capability for reissuing node legal identity keys and certificates, allowing for re-registration of a node (including a notary node) with a new certificate in the Network Map in [Corda Enterprise Network Manager](../../cenm/1.5/_index.md). For more information about this feature, contact [R3 support](https://www.r3.com/support/).

### Other changes and improvements

* **Single sign-on for Azure AD.** You can now operate a single sign on (SSO) set-up between Corda services and Azure AD, with a [simple configuration](../../cenm/1.5/azure-ad-sso.md) to both your Azure AD and Corda Auth services.
* **HSM integration support.** Corda Enterprise now supports users to integrate unsupported HSMs with their Corda Enterprise instance. This release includes a sample Java implementation to be used as an example, and a testing suite that can be used to test an implementation before deployment. For guidance on writing an HSM integration, see [HSM documentation](operations/deployment/hsm-integration.md/).
* **Ability to store confidential identity keys in HSMs.** Corda Enterprise now provides support for storing the keys associated with confidential identities in nCipher, Futurex, and Azure Key Vault HSMs. nCipher and Azure Key Vault HSMs support native use of confidential identity keys, and Futurex HSMs support the wrapped key mode. For more information on configuring these HSMs to store confidential identity keys, see the [HSM documentation](operations/deployment/hsm-deployment-confidential.md#using-an-hsm-with-confidential-identities/).
* **HSM APIs.** Corda Enterprise 4.7 introduces an HSM library with its own API that external tooling developers can use to expand Corda Enterprise HSM support.
* Node `initial-registration` now includes the creation of the `identity-private-key` keystore alias. For more information, see the documentation about [node folder structure](node/setup/node-structure.md#node-folder-structure). Previously, only `cordaclientca` and `cordaclienttls` aliases were created during `initial-registration`, while `identity-private-key` was generated on demand on the first node run. Therefore in Corda Enterprise 4.7 the content of `nodekeystore.jks` is never altered during a regular node run (except for `devMode = true`, where the certificates directory can be filled with pre-configured keystores).
* We have added documentation clarifying some potential performance gains when adjusting the notary `batchTimeoutMs` [configuration option](node/setup/corda-configuration-fields.md#notary), though the default has not been changed.

## Platform version change

The platform version of Corda 4.7 has been bumped up from 8 to 9.

For more information about platform versions, see [Versioning](cordapps/versioning.md).

## Fixed issues

* We have fixed a [Collaborative recovery](node/collaborative-recovery/introduction-cr.md) issue where, when using Accounts, [LedgerSync](node/collaborative-recovery/ledger-sync.md) returned no differences if the party that initiated the transaction wanted to recover against the receiving party.
* We have fixed an issue where the flow metadata finish time was set in a different time zone than the flow metadata start time.
* We have fixed an issue where, in case of hot/cold node failover, ongoing flows would sometimes get stuck on a new hot node and/or counterparty nodes while waiting to receive messages from the counterparty.
* We have fixed an issue where the Corda 4.6 RPC Client could not execute the method `NodeFlowStatusRpcOps::getFlowStatus` against a Corda 4.7 node due to failing to deserialise some enums when querying the node states.
* We have fixed an issue with JPA notaries where, if there were 10 or more input states, the `StateRef` was correctly encoded as `<hash>:a` but then was incorrectly decoded due to an expected integer input.
* We have fixed an issue where Float handled two connection attempts from the same Bridge at the same time, creating a binding exception as a result.

## Known issues

* The Corda 4.6 RPC Client cannot execute the method `NodeFlowStatusRpcOps::getFlowsMatching` against a Corda 4.7 node as it fails to deserialise some enums when querying the node states.
* In some cases the RPC Client may fail to connect to the node. This error is more likely to occur when using a lower-spec machine.
* The HA Utilities tool does not log information about the used `freshIdentitiesConfiguration` as it is implemented for Legal Identities and TLS keys.
* The HA Utilities tool does not log a message stating that the master key is not needed when using `NATIVE` mode. Such a message is only recorded in the node log when the node is registered using the `initial-registration` command.
* During node registration with confidential identities on HSM in `NATIVE` mode, the HA Utilities tool log contains an inaccurate log entry "Confidential identity wrapping key created" although no keys are generated as the master key is not required for confidential identities in `NATIVE` mode.
* A transaction without inputs and references can have different notaries for its output states. As a result, the node issuing the transaction could assign an arbitrary notary to its output state without notarising the transaction with this notary.
* Corda still depends on an outdated Azure Java SDK version (1.2.1) for Azure KeyVault support. This may result in the need for node operators to build a `shadedJar` themselves.
* In the new Flow Management Console, columns filtering/sorting may be incorrectly reset after page reload instead of showing the same results as when the filter was applied.
* In the new Flow Management Console and the Node Management Console, the "Change password" / "Log out" drop-down menu may not be fully visible when the user's name is short.
* In the new Flow Management Console, the "FLOW START FROM / TO" field in the Calendar on the "Query Flows" page must be clicked twice to open.
* A Collaborative Recovery 1.1 (or 1.0) initiator could fail when attempting to recover transactions archived by a Collaborative Recovery 1.2 responder.
* When performing certificate rotation (introduced in this release), flows could fail with an error when trying to use a state signed by the old key that is not in the `previousIdentityKeyAliases` list.
* The Health Survey Tool always tries to save its report in the Corda node directory instead of the current directory. This could be a problem for node operators who do not have write access to the Corda node directory.
* There are some formatting inconsistencies between the Corda HSM Technology Compatibility Kit (TCK) tests console help and the [Corda shell](node/operating/shell.md) CLI help.
* When running `samples:attachment-demo:deployNodes`, the `runSender` task fails to send the attachment because it uses `myLegalName` instead of `serviceLegalName` for notarisation.
* When running `run-migration-scripts --core-schemas --app-schemas` to migrate [the custom IOU CorDapp](https://github.com/corda/production-qa-steps/tree/toropovd/rpc-client/rpc-client/cordapp-example), the migration script fails when running on a MS SQL database. The migration works fine against H2, PostgreSQL, and Oracle databases.
* In some cases, the node keeps trying to reconnect to the counterparty even when the counterparty is down / the flow is killed.

{{< note >}}
The list above contains known issues specific to Corda Enterprise 4.7. See the release notes for previous Corda Enterprise releases for information about known issues specific to those versions.
{{< /note >}}
