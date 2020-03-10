---
aliases:
- /releases/4.0/index.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0: {}
  versions:
    weight: 160
project: corda-enterprise
section_menu: corda-enterprise-4-0
title: Corda Enterprise 4.0
version: '4.0'
---


# Corda Enterprise 4.0

Welcome to the documentation website for Corda Enterprise 4.0, based on the Corda 4.0 open source release.

Corda Enterprise 4.0 builds on the performance, scalability, high-availability, enhanced DMZ security, and multiple database vendor support
introduced in Corda Enterprise 3.0 with the following important new additions:


* **Multiple nodes behind a single firewall**:
multi-tenancy of Corda Firewall (float and bridge) components enables multiple Corda nodes to multiplex all remote peer-to-peer message traffic
through a single Corda Firewall.
* **Hardware Security Module (HSM) support**:
for Node CA and Legal Identity signing keys in hardware security modules provides increased security.
This release includes full integration with Azure Key Vault, Gemalto Luna and Utimaco HSM devices.
* **High Availability improvements**:
this release builds on the Hot-Cold High Availability configuration available in Corda Enterprise 3.x with improved deployment
configurations to simplify operational management and reduce overall VM footprint.
* **Operational Deployment improvements**:
introduces improvements that optimize larger scale deployments, reduce the cost of infrastructure, and minimize the operational complexity
of multi-node hosting.
* **Performance Test Suite for benchmarking**:
a toolkit to allow customers to test and validate Corda for their infrastructure performance and determine whether or not improvements are needed
before going live.

Corda Enterprise 4.0 also includes the new features of Corda 4, notably:


* **Reference input states**:
these allow smart contracts to read data from the ledger without simultaneously updating it.
* **State pointers**:
these work together with the reference states feature to make it easy for data to point to the latest version of any other piece of data
on the ledger by `StateRef` or linear ID.
* **Signature constraints**:
facilitate upgrading CorDapps in a secure manner using standard public key signing mechanisms and controls.
* **Security upgrades** to include:
    * Sealed JARs are a security upgrade that ensures JARs cannot define classes in each other’s packages, thus ensuring Java’s package-private
visibility feature works.
    * `@BelongsToContract` annotation: allows annotating states with which contract governs them.
    * Two-sided `FinalityFlow` and `SwapIdentitiesFlow` to prevent nodes accepting any finalised transaction, outside of the context of a containing flow.
    * Package namespace ownership: allows app developers to register their keys and Java package namespaces
with the zone operator. Any JAR that defines classes in these namespaces will have to be signed by those keys.


* **Versioning**:
applications can now specify a **target version** in their JAR manifest that declares which version of the platform the app was tested against.
They can also specify a **minimum platform version** which specifies the minimum version a node must be running on
to allow the app to start using new features and APIs of that version.

You can learn more about all new features in the [Enterprise](release-notes-enterprise.md) and [Open Source](release-notes.md) release notes.

{{< note >}}
You can read this site offline by [downloading the PDF](_static/corda-developer-site.pdf).

{{< /note >}}

Corda Enterprise is binary compatible with apps developed for the open source node. This docsite is intended for
administrators and advanced users who wish to learn how to install and configure an enterprise deployment. For
application development please continue to refer to [the main project documentation website](https://docs.corda.net/).

{{< note >}}
Corda Enterprise provides platform API version 4, which matches the API available in open source Corda 4.x releases.

{{< /note >}}



* [Release notes](release-notes-enterprise.md)
    * [Corda Enterprise 4.0](release-notes-enterprise.md#release)
        * [Key new features and components](release-notes-enterprise.md#key-new-features-and-components)
        * [Further improvements, additions and changes](release-notes-enterprise.md#further-improvements-additions-and-changes)
        * [Known issues](release-notes-enterprise.md#known-issues)
        * [Upgrade notes](release-notes-enterprise.md#upgrade-notes)




* [Upgrading CorDapps to Corda Enterprise 4.0](app-upgrade-notes-enterprise.md)
    * [Upgrading from Open Source](app-upgrade-notes-enterprise.md#upgrading-from-open-source)
        * [Running on Corda Enterprise 4.0](app-upgrade-notes-enterprise.md#running-on-release)
        * [Re-compiling for Corda Enterprise 4.0](app-upgrade-notes-enterprise.md#re-compiling-for-release)


    * [Upgrading from Enterprise 3.x](app-upgrade-notes-enterprise.md#upgrading-from-enterprise-3-x)
        * [Example](app-upgrade-notes-enterprise.md#example)




* [Upgrading your node to Corda 4](node-upgrade-notes.md)
    * [Step 1. Drain the node](node-upgrade-notes.md#step-1-drain-the-node)
    * [Step 2. Make a backup of your node directories and/or database](node-upgrade-notes.md#step-2-make-a-backup-of-your-node-directories-and-or-database)
    * [Step 3. Update database](node-upgrade-notes.md#step-3-update-database)
        * [Schema update](node-upgrade-notes.md#schema-update)
        * [Data update](node-upgrade-notes.md#data-update)


    * [Step 4. Replace `corda.jar` with the new version](node-upgrade-notes.md#step-4-replace-corda-jar-with-the-new-version)
    * [Step 5. Start up the node](node-upgrade-notes.md#step-5-start-up-the-node)
    * [Step 6. Undrain the node](node-upgrade-notes.md#step-6-undrain-the-node)


* [Corda API](corda-api.md)
    * [API: States](api-states.md)
        * [ContractState](api-states.md#contractstate)
        * [ContractState sub-interfaces](api-states.md#contractstate-sub-interfaces)
            * [LinearState](api-states.md#linearstate)
            * [OwnableState](api-states.md#ownablestate)
                * [FungibleState](api-states.md#fungiblestate)


            * [Other interfaces](api-states.md#other-interfaces)


        * [User-defined fields](api-states.md#user-defined-fields)
        * [The vault](api-states.md#the-vault)
        * [TransactionState](api-states.md#transactionstate)
        * [Reference States](api-states.md#reference-states)
        * [State Pointers](api-states.md#state-pointers)


    * [API: Persistence](api-persistence.md)
        * [Schemas](api-persistence.md#schemas)
        * [Custom schema registration](api-persistence.md#custom-schema-registration)
        * [Object relational mapping](api-persistence.md#object-relational-mapping)
        * [Persisting Hierarchical Data](api-persistence.md#persisting-hierarchical-data)
        * [Identity mapping](api-persistence.md#identity-mapping)
        * [JDBC session](api-persistence.md#jdbc-session)
        * [JPA Support](api-persistence.md#jpa-support)


    * [API: Contracts](api-contracts.md)
        * [Contract](api-contracts.md#contract)
        * [LedgerTransaction](api-contracts.md#ledgertransaction)
        * [requireThat](api-contracts.md#requirethat)
        * [Commands](api-contracts.md#commands)
            * [Branching verify with commands](api-contracts.md#branching-verify-with-commands)




    * [API: Contract Constraints](api-contract-constraints.md)
        * [Contract/State Agreement](api-contract-constraints.md#contract-state-agreement)
        * [App versioning with signature constraints](api-contract-constraints.md#app-versioning-with-signature-constraints)
        * [Issues when using the HashAttachmentConstraint](api-contract-constraints.md#issues-when-using-the-hashattachmentconstraint)
        * [Hash constrained states in private networks](api-contract-constraints.md#hash-constrained-states-in-private-networks)
        * [CorDapps as attachments](api-contract-constraints.md#cordapps-as-attachments)
        * [Constraints propagation](api-contract-constraints.md#constraints-propagation)
        * [Constraints migration to Corda 4](api-contract-constraints.md#constraints-migration-to-corda-4)
        * [Debugging](api-contract-constraints.md#debugging)
            * [Not setting CorDapp packages in tests](api-contract-constraints.md#not-setting-cordapp-packages-in-tests)
            * [Starting a node missing CorDapp(s)](api-contract-constraints.md#starting-a-node-missing-cordapp-s)
            * [Wrong fully-qualified contract name](api-contract-constraints.md#wrong-fully-qualified-contract-name)




    * [API: Vault Query](api-vault-query.md)
        * [Overview](api-vault-query.md#overview)
        * [Pagination](api-vault-query.md#pagination)
        * [Example usage](api-vault-query.md#example-usage)
            * [Kotlin](api-vault-query.md#kotlin)
            * [Java examples](api-vault-query.md#java-examples)


        * [Troubleshooting](api-vault-query.md#troubleshooting)
        * [Behavioural notes](api-vault-query.md#behavioural-notes)
        * [Other use case scenarios](api-vault-query.md#other-use-case-scenarios)
        * [Mapping owning keys to external IDs](api-vault-query.md#mapping-owning-keys-to-external-ids)


    * [API: Transactions](api-transactions.md)
        * [Transaction lifecycle](api-transactions.md#transaction-lifecycle)
        * [Transaction components](api-transactions.md#transaction-components)
            * [Input states](api-transactions.md#input-states)
                * [Reference input states](api-transactions.md#reference-input-states)


            * [Output states](api-transactions.md#output-states)
            * [Commands](api-transactions.md#commands)
            * [Attachments](api-transactions.md#attachments)
            * [Time-windows](api-transactions.md#time-windows)


        * [TransactionBuilder](api-transactions.md#transactionbuilder)
            * [Creating a builder](api-transactions.md#creating-a-builder)
            * [Adding items](api-transactions.md#adding-items)
            * [Signing the builder](api-transactions.md#signing-the-builder)


        * [SignedTransaction](api-transactions.md#signedtransaction)
            * [Verifying the transaction’s contents](api-transactions.md#verifying-the-transaction-s-contents)
            * [Verifying the transaction’s signatures](api-transactions.md#verifying-the-transaction-s-signatures)
            * [Signing the transaction](api-transactions.md#signing-the-transaction)
            * [Notarising and recording](api-transactions.md#notarising-and-recording)




    * [API: Flows](api-flows.md)
        * [An example flow](api-flows.md#an-example-flow)
            * [Initiator](api-flows.md#initiator)
            * [Responder](api-flows.md#responder)


        * [FlowLogic](api-flows.md#flowlogic)
        * [FlowLogic annotations](api-flows.md#flowlogic-annotations)
        * [Call](api-flows.md#call)
        * [ServiceHub](api-flows.md#servicehub)
        * [Common flow tasks](api-flows.md#common-flow-tasks)
            * [Transaction building](api-flows.md#transaction-building)
            * [Extracting states from the vault](api-flows.md#extracting-states-from-the-vault)
            * [Retrieving information about other nodes](api-flows.md#retrieving-information-about-other-nodes)
                * [Notaries](api-flows.md#notaries)
                * [Specific counterparties](api-flows.md#specific-counterparties)


            * [Communication between parties](api-flows.md#communication-between-parties)
                * [InitiateFlow](api-flows.md#initiateflow)
                * [Send](api-flows.md#send)
                * [Receive](api-flows.md#receive)
                * [SendAndReceive](api-flows.md#sendandreceive)
                * [Counterparty response](api-flows.md#counterparty-response)




        * [Subflows](api-flows.md#subflows)
            * [Inlined subflows](api-flows.md#inlined-subflows)
            * [Initiating subflows](api-flows.md#initiating-subflows)
                * [Core initiating subflows](api-flows.md#core-initiating-subflows)


            * [Library flows](api-flows.md#library-flows)
                * [FinalityFlow](api-flows.md#finalityflow)
                * [CollectSignaturesFlow/SignTransactionFlow](api-flows.md#collectsignaturesflow-signtransactionflow)
                * [SendTransactionFlow/ReceiveTransactionFlow](api-flows.md#sendtransactionflow-receivetransactionflow)


            * [Why inlined subflows?](api-flows.md#why-inlined-subflows)


        * [FlowException](api-flows.md#flowexception)
        * [ProgressTracker](api-flows.md#progresstracker)
        * [HTTP and database calls](api-flows.md#http-and-database-calls)
        * [Concurrency, Locking and Waiting](api-flows.md#concurrency-locking-and-waiting)
            * [Locking](api-flows.md#locking)
            * [Waiting](api-flows.md#waiting)




    * [API: Identity](api-identity.md)
        * [Party](api-identity.md#party)
        * [Confidential identities](api-identity.md#confidential-identities)
            * [SwapIdentitiesFlow](api-identity.md#swapidentitiesflow)
            * [IdentitySyncFlow](api-identity.md#identitysyncflow)




    * [API: ServiceHub](api-service-hub.md)
    * [API: RPC operations](api-rpc.md)
    * [API: Core types](api-core-types.md)
        * [SecureHash](api-core-types.md#securehash)
        * [CompositeKey](api-core-types.md#compositekey)


    * [API: Testing](api-testing.md)
        * [Flow testing](api-testing.md#flow-testing)
            * [MockNetwork](api-testing.md#mocknetwork)
            * [Adding nodes to the network](api-testing.md#adding-nodes-to-the-network)
            * [Running the network](api-testing.md#running-the-network)
            * [Running flows](api-testing.md#running-flows)
            * [Accessing `StartedMockNode` internals](api-testing.md#accessing-startedmocknode-internals)
                * [Querying a node’s vault](api-testing.md#querying-a-node-s-vault)
                * [Examining a node’s transaction storage](api-testing.md#examining-a-node-s-transaction-storage)


            * [Further examples](api-testing.md#further-examples)


        * [Contract testing](api-testing.md#contract-testing)
            * [Test identities](api-testing.md#test-identities)
            * [MockServices](api-testing.md#mockservices)
            * [Writing tests using a test ledger](api-testing.md#writing-tests-using-a-test-ledger)
                * [Checking for failure states](api-testing.md#checking-for-failure-states)
                * [Testing multiple scenarios at once](api-testing.md#testing-multiple-scenarios-at-once)
                * [Chaining transactions](api-testing.md#chaining-transactions)


            * [Further examples](api-testing.md#id1)




    * [API stability guarantees](corda-api.md#api-stability-guarantees)
    * [Public API](corda-api.md#public-api)
    * [Non-public API (experimental)](corda-api.md#non-public-api-experimental)
        * [Corda incubating modules](corda-api.md#corda-incubating-modules)
        * [Corda internal modules](corda-api.md#corda-internal-modules)


    * [The `@DoNotImplement` annotation](corda-api.md#the-donotimplement-annotation)


* [Corda and Corda Enterprise compatibility](version-compatibility.md)
* [Platform support matrix](platform-support-matrix.md)
    * [JDK support](platform-support-matrix.md#jdk-support)
    * [Operating systems supported in production](platform-support-matrix.md#operating-systems-supported-in-production)
    * [Operating systems supported in development](platform-support-matrix.md#operating-systems-supported-in-development)
    * [Databases](platform-support-matrix.md#databases)


* [Cheat sheet](cheat-sheet.md)




