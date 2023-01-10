---
date: '2022-11-15'
title: "Release Notes"
menu:
  corda-5-beta:
    identifier: corda-5-beta-release-notes
    weight: 6000
section_menu: corda-5-beta
---

Corda 5.0 Beta is a pre-release version for testing purposes only.
{{< note >}}
If you are not part of the current beta program, the Corda 5.0 Beta documentation is for information only.
R3 will be running a beta program for Corda 5.0 beginning in 2023. Contact R3 to register your interest.
{{< /note >}}

## Enhancements

This section describes the new features in Corda 5.0 Beta 1.

### Deployment 

#### Red Hat OpenShift Container Platform
Deployment of Corda 5 to Red Hat OpenShift Container Platform has now been tested and the [documentation](../deploying/deployment-tutorials/deploy-corda-cluster.md) updated.

#### Multiple Kafka Users
It is now possible to specify separate Kafka credentials for bootstrapping and for each type of worker in the deployment configuration file.
For more information, see [Deploying a Corda Cluster](../deploying/deployment-tutorials/deploy-corda-cluster.html#kafka).

#### Custom Annotations for Worker Pods
It is now possible to add custom annotations to worker pods. You can add these globally or for individual workers. You can see an example in the [Deployment tutorial](../deploying/deployment-tutorials/deploy-corda-cluster.html#custom-annotations-for-worker-pods).

### MGM

#### End-to-End Session Certificates
It is now possible to use certificates, in addition to cryptographic keys, in end-to-end sessions. The use of certificates is specified at a network level when onboarding the MGM.

### Ledger

The Ledger Layer has now been implemented to enable initial testing and development of ledger CorDapps. For more information, see the [Ledger section](../developing/ledger/ledger.md).

{{< note >}}
The UTXO Finality Flow does not yet support notarisation.
{{< /note >}}

#### Smart Contract Interfaces
Interfaces are now available to define and handle smart contracts in the Corda 5 UTXO ledger.

#### Filtered UTXO Wire Transactions
A public view has been added for filtered UTXO wire transactions.

#### UtxoSignedTransaction Accessors
Accessors have been added to `UtxoSignedTransaction` to make the following information available without any further resolution:
- Input state refs
- Reference state refs
- Output states and refs
- Notary information
- Transaction Metadata

### Notary

#### Non-Validating Notary Protocol
The non-validating notary protocol is now available for use by CorDapps that utilize the UTXO ledger. This behaves similarly to the Corda 4 non-validating notary protocol. However, transactions that require notarization must specify an upper-bounded time window.
{{< note >}}
In Beta 1, successful notarization requests are signed using the ledger key of the notary virtual node that processed the notarization request. You should take this into account when using the notary key for verification purposes. In a future release, Corda will use a dedicated notary key for signing.
{{< /note >}}

See the [Notaries section](../developing/notaries/overview.html) for more information.

### API

#### Filtered Transactions on the Public API
Filtered transactions are now available on the public API. This enables the implementation of the notary plug-in. Filtered transactions enable the amount of data that is revealed to a counterparty to be restricted, whilst still facilitating verification of the signatures/hashes of the transaction (using Merkle proofs under the hood to calculate the hash on a subset of the data).

#### Certificates
The certificates API has changed:
* To import a cluster-level certificate, use PUT with `cluster/<usage>` where `usage` is one of the following:
   * 'p2p-tls' — TLS certificate to be used in P2P communication
   * 'p2p-session' — session certificate to be used in P2P communication
   * 'rpc-api-tls' — TLS certificate to be used in RPC API communication
   * 'code-signer' — certificate of the code signing service
   The unique alias and the certificate should be in the request body.
* To import a virtual node certificate, use PUT with `vnode/<holdingIdentityId>/<usage>` where `usage` is one of the following:
   * 'p2p-tls' — TLS certificate to be used in P2P communication
   * 'p2p-session' — session certificate to be used in P2P communication
   * 'rpc-api-tls' — TLS certificate to be used in RPC API communication
   * 'code-signer' — certificate of the code signing service
   The unique alias and the certificate should be in the request body.
* To list all of the cluster-level certificate aliases, use GET with `cluster/<usage>`.
* To list all of the virtual node certificate aliases, use GET with `vnode/<holdingIdentityId>/<usage>`.
* To get a specific cluster-level certificate, use GET with `cluster/<usage>/<alias>`.
* To get a specific virtual node certificate, use GET with `vnode/<holdingIdentityId>/<usage>/<alias>`.

### Logging

#### Worker Startup
The following information is now written to the logs during the worker startup process:
* Platform version
* Worker software version
* Process ID
* Process information

#### Flow Worker Logging
The logs generated by flow workers have been improved:
* The client ID and node ID are now included.
* The logging level of information logs has been reduced.

### Configuration

#### Customised URL Endpoints for the P2P Gateway
A Corda operator can now modify the URL path that the P2P gateway's HTTP server listens on for requests. This is achieved by changing the `urlPath` field in the gateway's configuration. The URL path must be the same as the path of the endpoint in the member's registration context.

#### E2E Sessions Refreshed Periodically
E2E sessions are now refreshed automatically. By default, the sessions refresh every 5 days but this can be changed by updating the `sessionRefreshThreshold` field in the Link Manager's configuration. This value is defined in seconds.

## Resolved Issues

This section describes the issues resolved in Corda 5.0 Beta 1.

### Multiple CPIs with Same Group ID in Same Cluster

It was not possible to upload a CPI that contained a group policy file associated to a group ID of a CPI that was already present in the cluster.
As of this release, this validation has been removed and Corda only checks that a CPI does not have the same name, version, and signer of an existing CPI. 
This facilitates Notary plugin CPIs and other scenarios where two different CPBs must use the same group ID to interact with each other on the same cluster.

### Link Manager Session Certificate
The Link Manager sometimes sent the wrong session certificate to a counterparty during session negotiation.

## Known Limitations and Issues

* Corda 4 CorDapps will not run on Corda 5; it is a different set of incompatible APIs.
* Upgrade from Corda 4 to Corda 5 is not supported; a future version will provide migration guidance and tooling.
* There is no support for the Corda 4 Accounts SDK.
* There is no support for the Corda 4 Tokens SDK.
* There is no support for upgrades from the early access beta versions.

### UTXO Ledger 

#### State Relevancy Flag
Context: When building a transaction, newly created states (outputs) MUST be marked as relevant once the transaction is finalized.
Issue: The State relevancy flag can be inconsistently set due to a difference in the way transactions are finalized between `UtxoReceivedFinalityFlow` and `UtxoFinalityFlow`.
`UtxoReceivedFinalityFlow` on the counterparty side correctly persists State relevancy when the transaction is verified. `UtxoFinalityFlow` on the initiating side incorrectly persists State relevancy when the transaction is still unverified.
Impact: For the initiating participant on a transaction, a Relevant State could be flagged as available when the State should still be flagged as unavailable.
This also has a knock-on effect on the feed into the token selection mechanism.

#### Transaction Failures
Context: States must be marked as consumed in the vault when they have been used as input for a successful transaction. They should not be marked as consumed when used in a transaction that eventually fails to transact.
Issue: Input states to a UTXO transaction are marked as consumed when the transaction is first persisted, before it is completely signed and notarised. Should counter-signing or notarisation fail, states will be wrongly marked as consumed in the initiating's node vault and no longer be available as inputs.
Impact: In the case of transaction failures, states will be wrongly marked as consumed and thus unusable. Transaction rollback does not behave correctly in the current version of the UTXO ledger.