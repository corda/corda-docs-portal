---
title: "Corda Enterprise 4.1"
date: 2020-01-08T09:59:25Z
---


# Corda Enterprise 4.1
Welcome to the documentation website for Corda Enterprise 4.1, based on the Corda 4.0 open source release.

Corda Enterprise 4.1 builds on the performance, scalability, high-availability, enhanced DMZ security, and multiple database vendor support
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


Corda Enterprise 4.1 also includes the new features of Corda 4, notably:


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


You can learn more about all new features in the [Enterprise]({{< relref "release-notes-enterprise" >}}) and [Open Source]({{< relref "release-notes" >}}) release notes.


{{< note >}}
You can read this site offline by [downloading the PDF](_static/corda-developer-site.pdf).


{{< /note >}}
Corda Enterprise is binary compatible with apps developed for the open source node. This docsite is intended for
            administrators and advanced users who wish to learn how to install and configure an enterprise deployment. For
            application development please continue to refer to [the main project documentation website](https://docs.corda.net/).


{{< note >}}
Corda Enterprise provides platform API version 4, which matches the API available in open source Corda 4.x releases.


{{< /note >}}

* [Release notes]({{< relref "release-notes-enterprise" >}})
    * [Corda Enterprise 4.1]({{< relref "release-notes-enterprise#release" >}})
        * [Key new features and components]({{< relref "release-notes-enterprise#key-new-features-and-components" >}})

        * [Further improvements, additions and changes]({{< relref "release-notes-enterprise#further-improvements-additions-and-changes" >}})

        * [Known issues]({{< relref "release-notes-enterprise#known-issues" >}})

        * [Upgrade notes]({{< relref "release-notes-enterprise#upgrade-notes" >}})



* [Upgrading CorDapps to Corda Enterprise 4.1]({{< relref "app-upgrade-notes-enterprise" >}})
    * [Upgrading from Open Source]({{< relref "app-upgrade-notes-enterprise#upgrading-from-open-source" >}})
        * [Running on Corda Enterprise 4.1]({{< relref "app-upgrade-notes-enterprise#running-on-release" >}})

        * [Re-compiling for Corda Enterprise 4.1]({{< relref "app-upgrade-notes-enterprise#re-compiling-for-release" >}})


    * [Upgrading from Enterprise 4.0]({{< relref "app-upgrade-notes-enterprise#upgrading-from-enterprise-4-0" >}})

    * [Upgrading from Enterprise 3.x]({{< relref "app-upgrade-notes-enterprise#upgrading-from-enterprise-3-x" >}})
        * [Example]({{< relref "app-upgrade-notes-enterprise#example" >}})



* [Upgrading your node to Corda Enterprise 4.1]({{< relref "node-upgrade-notes" >}})
    * [Step 1. Drain the node]({{< relref "node-upgrade-notes#step-1-drain-the-node" >}})

    * [Step 2. Make a backup of your node directories and database]({{< relref "node-upgrade-notes#step-2-make-a-backup-of-your-node-directories-and-database" >}})

    * [Step 3. Update database]({{< relref "node-upgrade-notes#step-3-update-database" >}})
        * [3.1. Configure the Database Management Tool]({{< relref "node-upgrade-notes#configure-the-database-management-tool" >}})
            * [Azure SQL]({{< relref "node-upgrade-notes#azure-sql" >}})

            * [SQL Server]({{< relref "node-upgrade-notes#sql-server" >}})

            * [Oracle]({{< relref "node-upgrade-notes#oracle" >}})

            * [PostgreSQL]({{< relref "node-upgrade-notes#postgresql" >}})


        * [3.2. Extract DDL script using Database Management Tool]({{< relref "node-upgrade-notes#extract-ddl-script-using-database-management-tool" >}})

        * [3.3. Apply DDL scripts on a database]({{< relref "node-upgrade-notes#apply-ddl-scripts-on-a-database" >}})

        * [3.4. Apply data updates on a database]({{< relref "node-upgrade-notes#apply-data-updates-on-a-database" >}})


    * [Step 4. Replace `corda.jar` with the new version]({{< relref "node-upgrade-notes#step-4-replace-corda-jar-with-the-new-version" >}})

    * [Step 5. Start up the node]({{< relref "node-upgrade-notes#step-5-start-up-the-node" >}})

    * [Step 6. Undrain the node]({{< relref "node-upgrade-notes#step-6-undrain-the-node" >}})


* [Corda API]({{< relref "corda-api" >}})
    * [API: States]({{< relref "api-states" >}})
        * [ContractState]({{< relref "api-states#contractstate" >}})

        * [ContractState sub-interfaces]({{< relref "api-states#contractstate-sub-interfaces" >}})
            * [LinearState]({{< relref "api-states#linearstate" >}})

            * [OwnableState]({{< relref "api-states#ownablestate" >}})
                * [FungibleState]({{< relref "api-states#fungiblestate" >}})


            * [Other interfaces]({{< relref "api-states#other-interfaces" >}})


        * [User-defined fields]({{< relref "api-states#user-defined-fields" >}})

        * [The vault]({{< relref "api-states#the-vault" >}})

        * [TransactionState]({{< relref "api-states#transactionstate" >}})

        * [Reference States]({{< relref "api-states#reference-states" >}})

        * [State Pointers]({{< relref "api-states#state-pointers" >}})


    * [API: Persistence]({{< relref "api-persistence" >}})
        * [Schemas]({{< relref "api-persistence#schemas" >}})

        * [Custom schema registration]({{< relref "api-persistence#custom-schema-registration" >}})

        * [Object relational mapping]({{< relref "api-persistence#object-relational-mapping" >}})

        * [Persisting Hierarchical Data]({{< relref "api-persistence#persisting-hierarchical-data" >}})

        * [Identity mapping]({{< relref "api-persistence#identity-mapping" >}})

        * [JDBC session]({{< relref "api-persistence#jdbc-session" >}})

        * [JPA Support]({{< relref "api-persistence#jpa-support" >}})


    * [API: Contracts]({{< relref "api-contracts" >}})
        * [Contract]({{< relref "api-contracts#contract" >}})

        * [LedgerTransaction]({{< relref "api-contracts#ledgertransaction" >}})

        * [requireThat]({{< relref "api-contracts#requirethat" >}})

        * [Commands]({{< relref "api-contracts#commands" >}})
            * [Branching verify with commands]({{< relref "api-contracts#branching-verify-with-commands" >}})



    * [API: Contract Constraints]({{< relref "api-contract-constraints" >}})
        * [Reasons for Contract Constraints]({{< relref "api-contract-constraints#reasons-for-contract-constraints" >}})
            * [Implicit vs Explicit Contract upgrades]({{< relref "api-contract-constraints#implicit-vs-explicit-contract-upgrades" >}})


        * [Types of Contract Constraints]({{< relref "api-contract-constraints#types-of-contract-constraints" >}})

        * [Signature Constraints]({{< relref "api-contract-constraints#signature-constraints" >}})
            * [Signing CorDapps for use with Signature Constraints]({{< relref "api-contract-constraints#signing-cordapps-for-use-with-signature-constraints" >}})

            * [Using Signature Constraints in transactions]({{< relref "api-contract-constraints#using-signature-constraints-in-transactions" >}})

            * [App versioning with Signature Constraints]({{< relref "api-contract-constraints#app-versioning-with-signature-constraints" >}})


        * [Hash Constraints]({{< relref "api-contract-constraints#hash-constraints" >}})
            * [Issues when using the HashAttachmentConstraint]({{< relref "api-contract-constraints#issues-when-using-the-hashattachmentconstraint" >}})

            * [Hash constrained states in private networks]({{< relref "api-contract-constraints#hash-constrained-states-in-private-networks" >}})


        * [Contract/State Agreement]({{< relref "api-contract-constraints#contract-state-agreement" >}})

        * [Using Contract Constraints in Transactions]({{< relref "api-contract-constraints#using-contract-constraints-in-transactions" >}})

        * [CorDapps as attachments]({{< relref "api-contract-constraints#cordapps-as-attachments" >}})

        * [Constraints propagation]({{< relref "api-contract-constraints#constraints-propagation" >}})

        * [Constraints migration to Corda 4]({{< relref "api-contract-constraints#constraints-migration-to-corda-4" >}})

        * [Debugging]({{< relref "api-contract-constraints#debugging" >}})


    * [API: Vault Query]({{< relref "api-vault-query" >}})
        * [Overview]({{< relref "api-vault-query#overview" >}})

        * [Pagination]({{< relref "api-vault-query#pagination" >}})

        * [Example usage]({{< relref "api-vault-query#example-usage" >}})
            * [Kotlin]({{< relref "api-vault-query#kotlin" >}})

            * [Java examples]({{< relref "api-vault-query#java-examples" >}})


        * [Troubleshooting]({{< relref "api-vault-query#troubleshooting" >}})

        * [Behavioural notes]({{< relref "api-vault-query#behavioural-notes" >}})

        * [Other use case scenarios]({{< relref "api-vault-query#other-use-case-scenarios" >}})

        * [Mapping owning keys to external IDs]({{< relref "api-vault-query#mapping-owning-keys-to-external-ids" >}})


    * [API: Transactions]({{< relref "api-transactions" >}})
        * [Transaction lifecycle]({{< relref "api-transactions#transaction-lifecycle" >}})

        * [Transaction components]({{< relref "api-transactions#transaction-components" >}})
            * [Input states]({{< relref "api-transactions#input-states" >}})
                * [Reference input states]({{< relref "api-transactions#reference-input-states" >}})


            * [Output states]({{< relref "api-transactions#output-states" >}})

            * [Commands]({{< relref "api-transactions#commands" >}})

            * [Attachments]({{< relref "api-transactions#attachments" >}})

            * [Time-windows]({{< relref "api-transactions#time-windows" >}})


        * [TransactionBuilder]({{< relref "api-transactions#transactionbuilder" >}})
            * [Creating a builder]({{< relref "api-transactions#creating-a-builder" >}})

            * [Adding items]({{< relref "api-transactions#adding-items" >}})

            * [Signing the builder]({{< relref "api-transactions#signing-the-builder" >}})


        * [SignedTransaction]({{< relref "api-transactions#signedtransaction" >}})
            * [Verifying the transaction’s contents]({{< relref "api-transactions#verifying-the-transaction-s-contents" >}})

            * [Verifying the transaction’s signatures]({{< relref "api-transactions#verifying-the-transaction-s-signatures" >}})

            * [Signing the transaction]({{< relref "api-transactions#signing-the-transaction" >}})

            * [Notarising and recording]({{< relref "api-transactions#notarising-and-recording" >}})



    * [API: Flows]({{< relref "api-flows" >}})
        * [An example flow]({{< relref "api-flows#an-example-flow" >}})
            * [Initiator]({{< relref "api-flows#initiator" >}})

            * [Responder]({{< relref "api-flows#responder" >}})


        * [FlowLogic]({{< relref "api-flows#flowlogic" >}})

        * [FlowLogic annotations]({{< relref "api-flows#flowlogic-annotations" >}})

        * [Call]({{< relref "api-flows#call" >}})

        * [ServiceHub]({{< relref "api-flows#servicehub" >}})

        * [Common flow tasks]({{< relref "api-flows#common-flow-tasks" >}})
            * [Transaction building]({{< relref "api-flows#transaction-building" >}})

            * [Extracting states from the vault]({{< relref "api-flows#extracting-states-from-the-vault" >}})

            * [Retrieving information about other nodes]({{< relref "api-flows#retrieving-information-about-other-nodes" >}})
                * [Notaries]({{< relref "api-flows#notaries" >}})

                * [Specific counterparties]({{< relref "api-flows#specific-counterparties" >}})


            * [Communication between parties]({{< relref "api-flows#communication-between-parties" >}})
                * [InitiateFlow]({{< relref "api-flows#initiateflow" >}})

                * [Send]({{< relref "api-flows#send" >}})

                * [Receive]({{< relref "api-flows#receive" >}})

                * [SendAndReceive]({{< relref "api-flows#sendandreceive" >}})

                * [Counterparty response]({{< relref "api-flows#counterparty-response" >}})



        * [Subflows]({{< relref "api-flows#subflows" >}})
            * [Inlined subflows]({{< relref "api-flows#inlined-subflows" >}})

            * [Initiating subflows]({{< relref "api-flows#initiating-subflows" >}})
                * [Core initiating subflows]({{< relref "api-flows#core-initiating-subflows" >}})


            * [Library flows]({{< relref "api-flows#library-flows" >}})
                * [FinalityFlow]({{< relref "api-flows#finalityflow" >}})

                * [CollectSignaturesFlow/SignTransactionFlow]({{< relref "api-flows#collectsignaturesflow-signtransactionflow" >}})

                * [SendTransactionFlow/ReceiveTransactionFlow]({{< relref "api-flows#sendtransactionflow-receivetransactionflow" >}})


            * [Why inlined subflows?]({{< relref "api-flows#why-inlined-subflows" >}})


        * [FlowException]({{< relref "api-flows#flowexception" >}})

        * [ProgressTracker]({{< relref "api-flows#progresstracker" >}})

        * [HTTP and database calls]({{< relref "api-flows#http-and-database-calls" >}})

        * [Concurrency, Locking and Waiting]({{< relref "api-flows#concurrency-locking-and-waiting" >}})
            * [Locking]({{< relref "api-flows#locking" >}})

            * [Waiting]({{< relref "api-flows#waiting" >}})



    * [API: Identity]({{< relref "api-identity" >}})
        * [Party]({{< relref "api-identity#party" >}})

        * [Confidential identities]({{< relref "api-identity#confidential-identities" >}})
            * [SwapIdentitiesFlow]({{< relref "api-identity#swapidentitiesflow" >}})

            * [IdentitySyncFlow]({{< relref "api-identity#identitysyncflow" >}})



    * [API: ServiceHub]({{< relref "api-service-hub" >}})

    * [API: RPC operations]({{< relref "api-rpc" >}})

    * [API: Core types]({{< relref "api-core-types" >}})
        * [SecureHash]({{< relref "api-core-types#securehash" >}})

        * [CompositeKey]({{< relref "api-core-types#compositekey" >}})


    * [API: Testing]({{< relref "api-testing" >}})
        * [Flow testing]({{< relref "api-testing#flow-testing" >}})
            * [MockNetwork]({{< relref "api-testing#mocknetwork" >}})

            * [Adding nodes to the network]({{< relref "api-testing#adding-nodes-to-the-network" >}})

            * [Running the network]({{< relref "api-testing#running-the-network" >}})

            * [Running flows]({{< relref "api-testing#running-flows" >}})

            * [Accessing `StartedMockNode` internals]({{< relref "api-testing#accessing-startedmocknode-internals" >}})
                * [Querying a node’s vault]({{< relref "api-testing#querying-a-node-s-vault" >}})

                * [Examining a node’s transaction storage]({{< relref "api-testing#examining-a-node-s-transaction-storage" >}})


            * [Further examples]({{< relref "api-testing#further-examples" >}})


        * [Contract testing]({{< relref "api-testing#contract-testing" >}})
            * [Test identities]({{< relref "api-testing#test-identities" >}})

            * [MockServices]({{< relref "api-testing#mockservices" >}})

            * [Writing tests using a test ledger]({{< relref "api-testing#writing-tests-using-a-test-ledger" >}})
                * [Checking for failure states]({{< relref "api-testing#checking-for-failure-states" >}})

                * [Testing multiple scenarios at once]({{< relref "api-testing#testing-multiple-scenarios-at-once" >}})

                * [Chaining transactions]({{< relref "api-testing#chaining-transactions" >}})


            * [Further examples]({{< relref "api-testing#id1" >}})



    * [API stability guarantees]({{< relref "corda-api#api-stability-guarantees" >}})

    * [Public API]({{< relref "corda-api#public-api" >}})

    * [Non-public API (experimental)]({{< relref "corda-api#non-public-api-experimental" >}})
        * [Corda incubating modules]({{< relref "corda-api#corda-incubating-modules" >}})

        * [Corda internal modules]({{< relref "corda-api#corda-internal-modules" >}})


    * [The `@DoNotImplement` annotation]({{< relref "corda-api#the-donotimplement-annotation" >}})


* [Corda and Corda Enterprise compatibility]({{< relref "version-compatibility" >}})

* [Platform support matrix]({{< relref "platform-support-matrix" >}})
    * [JDK support]({{< relref "platform-support-matrix#jdk-support" >}})

    * [Operating systems supported in production]({{< relref "platform-support-matrix#operating-systems-supported-in-production" >}})

    * [Operating systems supported in development]({{< relref "platform-support-matrix#operating-systems-supported-in-development" >}})

    * [Databases]({{< relref "platform-support-matrix#databases" >}})


* [Cheat sheet]({{< relref "cheat-sheet" >}})



