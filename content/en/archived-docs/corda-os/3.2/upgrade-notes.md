---
aliases:
- /releases/release-V3.2/upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-3-2:
    identifier: corda-os-3-2-upgrade-notes
    parent: corda-os-3-2-building-a-cordapp-index
    weight: 1040
tags:
- upgrade
- notes
title: Upgrading a CorDapp to a new platform version
---


# Upgrading a CorDapp to a new platform version

These notes provide instructions for upgrading your CorDapps from previous versions, starting with the upgrade from our
first public Beta ([Milestone 12](changelog.md#changelog-m12)), to [V1.0](changelog.md#changelog-v1).



## General rules

Always remember to update the version identifiers in your project gradle file:

```shell
ext.corda_release_version = '1.0.0'
ext.corda_gradle_plugins_version = '1.0.0'
```

It may be necessary to update the version of major dependencies:

```shell
ext.kotlin_version = '1.1.4'
ext.quasar_version = '0.7.9'
```

Please consult the relevant release notes of the release in question. If not specified, you may assume the
versions you are currently using are still in force.

We also strongly recommend cross referencing with the [Changelog](changelog.md) to confirm changes.


## v3.1 to v3.2


### Gradle Plugin Version

You will need to update the `corda_release_version` identifier in your project gradle file.

```shell
ext.corda_release_version = '3.2-corda'
```


### Database schema changes


* Database upgrade - a typo has been corrected in the `NODE_ATTACHMENTS_CONTRACTS` table name.

When upgrading from versions 3.0 or 3.1, run the following command:

```sql
ALTER TABLE [schema].NODE_ATTCHMENTS_CONTRACTS RENAME TO NODE_ATTACHMENTS_CONTRACTS;
```

Schema name is optional, run SQL when the node is not running.


* Postgres database upgrade - Change the type of the `checkpoint_value` column to `bytea`.

This will address the issue that the *vacuum* function is unable to clean up deleted checkpoints as they are still referenced from the `pg_shdepend` table.


```sql
ALTER TABLE node_checkpoints ALTER COLUMN checkpoint_value set data type bytea using null;
```


{{< note >}}
This change will also need to be run when migrating from version 3.0.

{{< /note >}}

{{< note >}}
The Corda node will fail on startup if the database was not updated with the above commands.

{{< /note >}}

## v3.0 to v3.1


### Gradle Plugin Version

Corda 3.1 uses version 3.1.0 of the gradle plugins and your `build.gradle` file should be updated to reflect this.

```shell
ext.corda_gradle_plugins_version = '3.1.0'
```

You will also need to update the `corda_release_version` identifier in your project gradle file.

```shell
ext.corda_release_version = '3.1-corda'
```


## V2.0 to V3.0


### Gradle Plugin Version

Corda 3.0 uses version 3.0.9 of the gradle plugins and your `build.gradle` file should be updated to reflect this.

```shell
ext.corda_gradle_plugins_version = '3.0.9'
```

You will also need to update the `corda_release_version` identifier in your project gradle file.

```shell
ext.corda_release_version = 'corda-3.0'
```


### Network Map Service

With the re-designed network map service the following changes need to be made:


* The network map is no longer provided by a node and thus the `networkMapService` config is ignored. Instead the
network map is either provided by the compatibility zone (CZ) operator (who operates the doorman) and available
using the `compatibilityZoneURL` config, or is provided using signed node info files which are copied locally.
See [Network Map](network-map.md) for more details, and setting-up-a-corda-network.rst on how to use the network
bootstrapper for deploying a local network.
* Configuration for a notary has been simplified. `extraAdvertisedServiceIds`, `notaryNodeAddress`, `notaryClusterAddresses`
and `bftSMaRt` configs have been replaced by a single `notary` config object. See [Node configuration](corda-configuration-file.md)
for more details.
* The advertisement of the notary to the rest of the network, and its validation type, is no longer determined by the
`extraAdvertisedServiceIds` config. Instead it has been moved to the control of the network operator via
the introduction of network parameters. The network bootstrapper automatically includes the configured notaries
when generating the network parameters file for a local deployment.
* Any nodes defined in a `deployNodes` gradle task performing the function of the network map can be removed, or the
`NetworkMap` parameter can be removed for any “controller” node which is both the network map and a notary.
* For registering a node with the doorman the `certificateSigningService` config has been replaced by `compatibilityZoneURL`.


### Corda Plugins


* Corda plugins have been modularised further so the following additional gradle entries are necessary:
For example:> 



The plugin needs to be applied in all gradle build files where there is a dependency on Corda using any of:
cordaCompile, cordaRuntime, cordapp


* For existing contract ORM schemas that extend from `CommonSchemaV1.LinearState` or `CommonSchemaV1.FungibleState`,
you will need to explicitly map the `participants` collection to a database table. Previously this mapping was done
in the superclass, but that makes it impossible to properly configure the table name. The required changes are to:
    * Add the `override var participants: MutableSet<AbstractParty>? = null` field to your class, and
    * Add JPA mappings

For example:> 
```kotlin
@Entity
@Table(name = "cash_states_v2",
        indexes = arrayOf(Index(name = "ccy_code_idx2", columnList = "ccy_code")))
class PersistentCashState(

        @ElementCollection
        @Column(name = "participants")
        @CollectionTable(name="cash_states_v2_participants", joinColumns = arrayOf(
                JoinColumn(name = "output_index", referencedColumnName = "output_index"),
                JoinColumn(name = "transaction_id", referencedColumnName = "transaction_id")))
        override var participants: MutableSet<AbstractParty>? = null,
```






### AMQP

Whilst the enablement of AMQP is a transparent change, as noted in the [Object serialization](serialization.md) documentation
the way classes, and states in particular, should be written to work with this new library may require some
alteration to your current implementation.



* With AMQP enabled Java classes must be compiled with the -parameter flag.
    * If they aren’t, then the error message will complain about `arg<N>` being an unknown parameter.
    * If recompilation is not viable, a custom serializer can be written as per [Pluggable Serializers for CorDapps](cordapp-custom-serializers.md)
    * It is important to bear in mind that with AMQP there must be an implicit mapping between constructor
parameters and properties you wish included in the serialized form of a class.
        * See [Object serialization](serialization.md) for more information




* Error messages of the form`Constructor parameter - "<some parameter of a constructor>" - doesn't refer to a property of "class <some.class.being.serialized>"`indicate that a class, in the above example `some.class.being.serialized`, has a parameter on its primary constructor that
doesn’t correlate to a property of the class. This is a problem because the Corda AMQP serialization library uses a class’s
constructor (default, primary, or annotated) as the means by which instances of the serialized form are reconstituted.See the section “Mismatched Class Properties / Constructor Parameters” in the [Object serialization](serialization.md) documentation



### Database schema changes

An H2 database instance (represented on the filesystem as a file called *persistence.mv.db*) used in Corda 1.0 or 2.0
cannot be directly reused with Corda 3.0 due to minor improvements and additions to stabilise the underlying schemas.


### Configuration

Nodes that do not require SSL to be enabled for RPC clients now need an additional port to be specified as part of their configuration.
To do this, add a block as follows to the nodes configuraiton:


```script
rpcSettings {
    adminAddress "localhost:10007"
}
```



to *node.conf* files.

Also, the property *rpcPort* is now deprecated, so it would be preferable to substitute properties specified that way e.g., *rpcPort=10006* with a block as follows:


```script
rpcSettings {
    address "localhost:10006"
    adminAddress "localhost:10007"
}
```



Equivalent changes should be performed on classes extending *CordformDefinition*.


### Testing


* The registration mechanism for CorDapps in `MockNetwork` unit tests has changed:
    * CorDapp registration is now done via the `cordappPackages` constructor parameter of MockNetwork. This parameter
is a list of `String` values which should be the package names of the CorDapps containing the contract
verification code you wish to load
    * The `unsetCordappPackages` method is now redundant and has been removed


* Many classes have been moved between packages, so you will need to update your imports
{{< attention >}}

We have provided a several scripts (depending upon your operating system of choice) to smooth the upgrade
process for existing projects. This can be found at `tools\scripts\update-test-packages.sh` for the Bash shell and
`tools/scripts/upgrade-test-packages.ps1` for Windows Power Shell users in the source tree
{{< /attention >}}


* setCordappPackages and unsetCordappPackages have been removed from the ledger/transaction DSL and the flow test framework,
and are now set via a constructor parameter or automatically when constructing the MockServices or MockNetwork object
* Key constants e.g. `ALICE_KEY` have been removed; you can now use TestIdentity to make your own
* The ledger/transaction DSL must now be provided with MockServices as it no longer makes its own
* In transaction blocks, input and output take their arguments as ContractStates rather than lambdas
* Also in transaction blocks, command takes its arguments as CommandDatas rather than lambdas
* The MockServices API has changed; please refer to its API documentation
* TestDependencyInjectionBase has been retired in favour of a JUnit Rule called SerializationEnvironmentRule
* This replaces the initialiseSerialization parameter of ledger/transaction and verifierDriver
* The withTestSerialization method is obsoleted by SerializationEnvironmentRule and has been retired
* 
    * Similarly, the MockNetwork.createNode methods now take a MockNodeParameters builder


* MockNode constructor parameters are now aggregated in MockNodeArgs for easier subclassing
* MockNetwork.Factory has been retired as you can simply use a lambda
* testNodeConfiguration has been retired, please use a mock object framework of your choice instead
* MockNetwork.createSomeNodes and IntegrationTestCategory have been retired with no replacement
* Starting a flow can now be done directly from a node object. Change calls of the form `node.getServices().startFlow(...)`
to `node.startFlow(...)`
* Similarly a tranaction can be executed directly from a node object. Change calls of the form `node.getDatabase().transaction({ it -> ... })`
to `node.transaction({() -> ... })`
* `startFlow` now returns a `CordaFuture`, there is no need to call `startFlow(...).getResultantFuture()`


## V1.0 to V2.0


* You need to update the `corda_release_version` identifier in your project gradle file. The
corda_gradle_plugins_version should remain at 1.0.0:> 
```shell
ext.corda_release_version = '2.0.0'
ext.corda_gradle_plugins_version = '1.0.0'
```






## Public Beta (M12) to V1.0


### Build


* MockNetwork has moved. To continue using `MockNetwork` for testing, you must add the following dependency to your
`build.gradle` file:> 
```shell
testCompile "net.corda:corda-node-driver:$corda_release_version"
```


{{< note >}}
You may only need `testCompile "net.corda:corda-test-utils:$corda_release_version"` if not using the Driver
DSL{{< /note >}}




### Configuration


* `CordaPluginRegistry` has been removed:
    * The one remaining configuration item `customizeSerialisation`, which defined a optional whitelist of types for
use in object serialization, has been replaced with the `SerializationWhitelist` interface which should be
implemented to define a list of equivalent whitelisted classes
    * You will need to rename your services resource file. ‘resources/META-INF/services/net.corda.core.node.CordaPluginRegistry’
becomes ‘resources/META-INF/services/net.corda.core.serialization.SerializationWhitelist’
    * `MockNode.testPluginRegistries` was renamed to `MockNode.testSerializationWhitelists`
    * In general, the `@CordaSerializable` annotation is the preferred method for whitelisting, as described in
[Object serialization](serialization.md)




### Missing imports

Use IntelliJ’s automatic imports feature to intelligently resolve the new imports:


* Missing imports for contract types:
    * CommercialPaper and Cash are now contained within the `finance` module, as are associated helpers functions. For
example:
        * `import net.corda.contracts.ICommercialPaperState` becomes `import net.corda.finance.contracts.ICommercialPaperState`
        * `import net.corda.contracts.asset.sumCashBy` becomes `import net.corda.finance.utils.sumCashBy`
        * `import net.corda.core.contracts.DOLLARS` becomes `import net.corda.finance.DOLLARS`
        * `import net.corda.core.contracts.issued by` becomes `import net.corda.finance.issued by`
        * `import net.corda.contracts.asset.Cash` becomes `import net.corda.finance.contracts.asset.Cash`




* Missing imports for utility functions:
    * Many common types and helper methods have been consolidated into `net.corda.core.utilities` package. For example:
        * `import net.corda.core.crypto.commonName` becomes `import net.corda.core.utilities.commonName`
        * `import net.corda.core.crypto.toBase58String` becomes `import net.corda.core.utilities.toBase58String`
        * `import net.corda.core.getOrThrow` becomes `import net.corda.core.utilities.getOrThrow`




* Missing flow imports:
    * In general, all reusable library flows are contained within the **core** API `net.corda.core.flows` package
    * Financial domain library flows are contained within the **finance** module `net.corda.finance.flows` package
    * Other flows that have moved include `import net.corda.core.flows.ResolveTransactionsFlow`, which becomes
`import net.corda.core.internal.ResolveTransactionsFlow`




### Core data structures


* Missing `Contract` override:
    * `Contract.legalContractReference` has been removed, and replaced by the optional annotation
`@LegalProseReference(uri = "<URI>")`


* Unresolved reference:
    * `AuthenticatedObject` was renamed to `CommandWithParties`


* Overrides nothing:
    * `LinearState.isRelevant` was removed. Whether a node stores a `LinearState` in its vault depends on whether the
node is one of the state’s `participants`
    * `txBuilder.toLedgerTransaction` now requires a `ServiceHub` parameter. This is used by the new Contract
Constraints functionality to validate and resolve attachments




### Flow framework


* `FlowLogic` communication has been upgraded to use explicit `FlowSession` instances to communicate between nodes:
    * `FlowLogic.send`/`FlowLogic.receive`/`FlowLogic.sendAndReceive` has been replaced by `FlowSession.send`/
`FlowSession.receive`/`FlowSession.sendAndReceive`. The replacement functions do not take a destination
parameter, as this is defined implictly by the session used
    * Initiated flows now take in a `FlowSession` instead of `Party` in their constructor. If you need to access the
counterparty identity, it is in the `counterparty` property of the flow session


* `FinalityFlow` now returns a single `SignedTransaction`, instead of a `List<SignedTransaction>`
* `TransactionKeyFlow` was renamed to `SwapIdentitiesFlow`
* `SwapIdentitiesFlow` must be imported from the *confidential-identities* package `net.corda.confidential`


### Node services (ServiceHub)


* Unresolved reference to `vaultQueryService`:
    * Replace all references to `<services>.vaultQueryService` with `<services>.vaultService`
    * Previously there were two vault APIs. Now there is a single unified API with the same functions: `VaultService`.


* `FlowLogic.ourIdentity` has been introduced as a shortcut for retrieving our identity in a flow
* `serviceHub.myInfo.legalIdentity` no longer exists
* `getAnyNotary` has been removed. Use `serviceHub.networkMapCache.notaryIdentities[0]` instead
* `ServiceHub.networkMapUpdates` is replaced by `ServiceHub.networkMapFeed`
* `ServiceHub.partyFromX500Name` is replaced by `ServiceHub.wellKnownPartyFromX500Name`
    * A “well known” party is one that isn’t anonymous. This change was motivated by the confidential identities work




### RPC Client


* Missing API methods on the `CordaRPCOps` interface:
    * `verifiedTransactionsFeed` has been replaced by `internalVerifiedTransactionsFeed`
    * `verifiedTransactions` has been replaced by `internalVerifiedTransactionsSnapshot`
    * These changes are in preparation for the planned integration of Intel SGX™, which will encrypt the transactions
feed. Apps that use this API will not work on encrypted ledgers. They should generally be modified to use the vault
query API instead
    * Accessing the `networkMapCache` via `services.nodeInfo().legalIdentities` returns a list of identities
        * This change is in preparation for allowing a node to host multiple separate identities in the future






### Testing

Please note that `Clauses` have been removed completely as of V1.0. We will be revisiting this capability in a future
release.


* CorDapps must be explicitly registered in `MockNetwork` unit tests:
    * This is done by calling `setCordappPackages`, an extension helper function in the `net.corda.testing` package,
on the first line of your `@Before` method. This takes a variable number of `String` arguments which should be
the package names of the CorDapps containing the contract verification code you wish to load
    * You should unset CorDapp packages in your `@After` method by using `unsetCordappPackages` after
`stopNodes`


* CorDapps must be explicitly registered in `DriverDSL` and `RPCDriverDSL` integration tests:
    * You must register package names of the CorDapps containing the contract verification code you wish to load using
the `extraCordappPackagesToScan: List<String>` constructor parameter of the driver DSL




### Finance


* `FungibleAsset` interface simplification:
    * The `Commands` grouping interface that included the `Move`, `Issue` and `Exit` interfaces has been removed
    * The `move` function has been renamed to `withNewOwnerAndAmount`
* This is for consistency with `OwnableState.withNewOwner`




### Miscellaneous


* `args[0].parseNetworkHostAndPort()` becomes `NetworkHostAndPort.parse(args[0])`
* There is no longer a `NodeInfo.advertisedServices` property
    * The concept of advertised services has been removed from Corda. This is because it was vaguely defined and
real-world apps would not typically select random, unknown counterparties from the network map based on
self-declared capabilities
    * We will introduce a replacement for this functionality, business networks, in a future release
    * For now, services should be retrieved by legal name using `NetworkMapCache.getNodeByLegalName`




### Gotchas


* Be sure to use the correct identity when issuing cash:
    * The third parameter to `CashIssueFlow` should be the *notary* (and not the *node identity*)




#### [From Milestone 13](changelog.md#changelog-m13)


### Core data structures


* `TransactionBuilder` changes:
    * Use convenience class `StateAndContract` instead of `TransactionBuilder.withItems` for passing
around a state and its contract.


* Transaction builder DSL changes:
    * When adding inputs and outputs to a transaction builder, you must also specify `ContractClassName`
        * `ContractClassName` is the name of the `Contract` subclass used to verify the transaction




* Contract verify method signature change:
    * `override fun verify(tx: TransactionForContract)` becomes `override fun verify(tx: LedgerTransaction)`


* You no longer need to override `ContractState.contract` function


### Node services (ServiceHub)


* ServiceHub API method changes:
    * `services.networkMapUpdates().justSnapshot` becomes `services.networkMapSnapshot()`




### Configuration


* No longer need to define `CordaPluginRegistry` and configure `requiredSchemas`:
    * Custom contract schemas are automatically detected at startup time by class path scanning
    * For testing purposes, use the `SchemaService` method to register new custom schemas (e.g.
`services.schemaService.registerCustomSchemas(setOf(YoSchemaV1))`)




### Identity


* Party names are now `CordaX500Name`, not `X500Name`:
    * `CordaX500Name` specifies a predefined set of mandatory (organisation, locality, country) and optional fields
(common name, organisation unit, state) with validation checking
    * Use new builder `CordaX500Name.build(X500Name(target))` or explicitly define the X500Name parameters using the
`CordaX500Name` constructors




### Testing


* MockNetwork testing:
    * Mock nodes in node tests are now of type `StartedNode<MockNode>`, rather than `MockNode`
    * `MockNetwork` now returns a `BasketOf(<StartedNode<MockNode>>)`
    * You must call internals on `StartedNode` to get `MockNode` (e.g. `a = nodes.partyNodes[0].internals`)


* Host and port changes:
    * Use string helper function `parseNetworkHostAndPort` to parse a URL on startup (e.g.
`val hostAndPort = args[0].parseNetworkHostAndPort()`)


* Node driver parameter changes:
    * The node driver parameters for starting a node have been reordered
    * The node’s name needs to be given as an `CordaX500Name`, instead of using `getX509Name`




#### [From Milestone 12 (First Public Beta)](changelog.md#changelog-m12)


### Core data structures


* Transaction building:
    * You no longer need to specify the type of a `TransactionBuilder` as `TransactionType.General`
    * `TransactionType.General.Builder(notary)` becomes `TransactionBuilder(notary)`




### Build


* Gradle dependency reference changes:
    * Module names have changed to include `corda` in the artifacts’ JAR names:



```shell
compile "net.corda:core:$corda_release_version" -> compile "net.corda:corda-core:$corda_release_version"
compile "net.corda:finance:$corda_release_version" -> compile "net.corda:corda-finance:$corda_release_version"
compile "net.corda:jackson:$corda_release_version" -> compile "net.corda:corda-jackson:$corda_release_version"
compile "net.corda:node:$corda_release_version" -> compile "net.corda:corda-node:$corda_release_version"
compile "net.corda:rpc:$corda_release_version" -> compile "net.corda:corda-rpc:$corda_release_version"
```


### Node services (ServiceHub)


* `ServiceHub` API changes:
    * `services.networkMapUpdates` becomes `services.networkMapFeed`
    * `services.getCashBalances` becomes a helper method in the *finance* module contracts package
(`net.corda.finance.contracts.getCashBalances`)




### Finance


* Financial asset contracts (`Cash`, `CommercialPaper`, `Obligations`) are now a standalone CorDapp within the
`finance` module:
    * You need to import them from their respective packages within the `finance` module (e.g.
`net.corda.finance.contracts.asset.Cash`)
    * You need to import the associated asset flows from their respective packages within `finance` module. For
example:
        * `net.corda.finance.flows.CashIssueFlow`
        * `net.corda.finance.flows.CashIssueAndPaymentFlow`
        * `net.corda.finance.flows.CashExitFlow`




* The `finance` gradle project files have been moved into a `net.corda.finance` package namespace:
    * Adjust imports of Cash flow references
    * Adjust the `StartFlow` permission in `gradle.build` files
    * Adjust imports of the associated flows (`Cash*Flow`, `TwoPartyTradeFlow`, `TwoPartyDealFlow`)



