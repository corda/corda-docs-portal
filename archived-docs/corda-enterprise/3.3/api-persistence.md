---
aliases:
- /releases/3.3/api-persistence.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    identifier: corda-enterprise-3-3-api-persistence
    parent: corda-enterprise-3-3-corda-api
    weight: 1020
tags:
- api
- persistence
title: 'API: Persistence'
---




# API: Persistence


Corda offers developers the option to expose all or some part of a contract state to an *Object Relational Mapping*
(ORM) tool to be persisted in a RDBMS.  The purpose of this is to assist *vault* development by effectively indexing
persisted contract states held in the vault for the purpose of running queries over them and to allow relational joins
between Corda data and private data local to the organisation owning a node.

The ORM mapping is specified using the [Java Persistence API](https://en.wikipedia.org/wiki/Java_Persistence_API)
(JPA) as annotations and is converted to database table rows by the node automatically every time a state is recorded
in the node’s local vault as part of a transaction.

{{< note >}}
Presently the node includes an instance of the H2 database. H2 database is supported for development purposes,
and we have certified Corda Enterprise to work against SQL Server 2017 and Azure SQL.
PostgreSQL 9.6 is supported preliminarily. Other databases will be officially supported very soon.
Much of the node internal state is also persisted there. You can access
the internal H2 database via JDBC, please see the info in “[Node administration](node-administration.md)” for details.

{{< /note >}}

## Schemas

Every `ContractState` can implement the `QueryableState` interface if it wishes to be inserted into the node’s local
database and accessible using SQL.

```kotlin
/**
 * A contract state that may be mapped to database schemas configured for this node to support querying for,
 * or filtering of, states.
 */
interface QueryableState : ContractState {
    /**
     * Enumerate the schemas this state can export representations of itself as.
     */
    fun supportedSchemas(): Iterable<MappedSchema>

    /**
     * Export a representation for the given schema.
     */
    fun generateMappedObject(schema: MappedSchema): PersistentState
}

```



The `QueryableState` interface requires the state to enumerate the different relational schemas it supports, for
instance in cases where the schema has evolved, with each one being represented by a `MappedSchema` object return
by the `supportedSchemas()` method.  Once a schema is selected it must generate that representation when requested
via the `generateMappedObject()` method which is then passed to the ORM.

Nodes have an internal `SchemaService` which decides what to persist and what not by selecting the `MappedSchema`
to use.

```kotlin
/**
 * A configuration and customisation point for Object Relational Mapping of contract state objects.
 */
interface SchemaService {
    /**
     * Represents any options configured on the node for a schema.
     */
    data class SchemaOptions(val databaseSchema: String? = null, val tablePrefix: String? = null)

    /**
     * Options configured for this node's schemas.  A missing entry for a schema implies all properties are null.
     */
    val schemaOptions: Map<MappedSchema, SchemaOptions>

    /**
     * Given a state, select schemas to map it to that are supported by [generateMappedObject] and that are configured
     * for this node.
     */
    fun selectSchemas(state: ContractState): Iterable<MappedSchema>

    /**
     * Map a state to a [PersistentState] for the given schema, either via direct support from the state
     * or via custom logic in this service.
     */
    fun generateMappedObject(state: ContractState, schema: MappedSchema): PersistentState
}

```



```kotlin
/**
 * A database schema that might be configured for this node.  As well as a name and version for identifying the schema,
 * also list the classes that may be used in the generated object graph in order to configure the ORM tool.
 *
 * @param schemaFamily A class to fully qualify the name of a schema family (i.e. excludes version)
 * @param version The version number of this instance within the family.
 * @param mappedTypes The JPA entity classes that the ORM layer needs to be configure with for this schema.
 */
open class MappedSchema(schemaFamily: Class<*>,
                        val version: Int,
                        val mappedTypes: Iterable<Class<*>>) {
    val name: String = schemaFamily.name

    /**
     * Points to a classpath resource containing the database changes for the [mappedTypes]
     */
    protected open val migrationResource: String? = null

    internal fun getMigrationResource(): String? = migrationResource

    override fun toString(): String = "${this.javaClass.simpleName}(name=$name, version=$version)"

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as MappedSchema

        if (version != other.version) return false
        if (mappedTypes != other.mappedTypes) return false
        if (name != other.name) return false

        return true
    }

    override fun hashCode(): Int {
        var result = version
        result = 31 * result + mappedTypes.hashCode()
        result = 31 * result + name.hashCode()
        return result
    }
}

```



The `SchemaService` can be configured by a node administrator to select the schemas used by each app. In this way the
relational view of ledger states can evolve in a controlled fashion in lock-step with internal systems or other
integration points and not necessarily with every upgrade to the contract code. It can select from the
`MappedSchema` offered by a `QueryableState`, automatically upgrade to a later version of a schema or even
provide a `MappedSchema` not originally offered by the `QueryableState`.

It is expected that multiple different contract state implementations might provide mappings within a single schema.
For example an Interest Rate Swap contract and an Equity OTC Option contract might both provide a mapping to
a Derivative contract within the same schema. The schemas should typically not be part of the contract itself and should exist independently
to encourage re-use of a common set within a particular business area or Cordapp.

{{< note >}}
It’s advisable to avoid cross-references between different schemas as this may cause issues when evolving `MappedSchema`
or migrating its data. At startup, nodes log such violations as warnings stating that there’s a cross-reference between `MappedSchema`’s.
The detailed messages incorporate information about what schemas, entities and fields are involved.

{{< /note >}}
`MappedSchema` offer a family name that is disambiguated using Java package style name-spacing derived from the
class name of a *schema family* class that is constant across versions, allowing the `SchemaService` to select a
preferred version of a schema.

The `SchemaService` is also responsible for the `SchemaOptions` that can be configured for a particular
`MappedSchema` which allow the configuration of a database schema or table name prefixes to avoid any clash with
other `MappedSchema`.

{{< note >}}
It is intended that there should be plugin support for the `SchemaService` to offer the version upgrading
and additional schemas as part of Cordapps, and that the active schemas be configurable.  However the present
implementation offers none of this and simply results in all versions of all schemas supported by a
`QueryableState` being persisted. This will change in due course. Similarly, it does not currently support
configuring `SchemaOptions` but will do so in the future.

{{< /note >}}

## Custom schema registration

Custom contract schemas are automatically registered at startup time for CorDapps. The node bootstrap process will scan
for schemas (any class that extends the `MappedSchema` interface) in the *plugins* configuration directory in your CorDapp jar.

For testing purposes it is necessary to manually register the packages containing custom schemas as follows:


* Tests using `MockNetwork` and `MockNode` must explicitly register packages using the *cordappPackages* parameter of `MockNetwork`
* Tests using `MockServices` must explicitly register packages using the *cordappPackages* parameter of the `MockServices` *makeTestDatabaseAndMockServices()* helper method.

{{< note >}}
Tests using the *DriverDSL* will automatically register your custom schemas if they are in the same project structure as the driver call.

{{< /note >}}

## Object relational mapping

The persisted representation of a `QueryableState` should be an instance of a `PersistentState` subclass,
constructed either by the state itself or a plugin to the `SchemaService`.  This allows the ORM layer to always
associate a `StateRef` with a persisted representation of a `ContractState` and allows joining with the set of
unconsumed states in the vault.

The `PersistentState` subclass should be marked up as a JPA 2.1 *Entity* with a defined table name and having
properties (in Kotlin, getters/setters in Java) annotated to map to the appropriate columns and SQL types.  Additional
entities can be included to model these properties where they are more complex, for example collections, so the mapping
does not have to be *flat*. The `MappedSchema` must provide a list of all of the JPA entity classes for that schema
in order to initialise the ORM layer.

Several examples of entities and mappings are provided in the codebase, including `Cash.State` and
`CommercialPaper.State`. For example, here’s the first version of the cash schema.

```kotlin
/*
 * R3 Proprietary and Confidential
 *
 * Copyright (c) 2018 R3 Limited.  All rights reserved.
 *
 * The intellectual and technical concepts contained herein are proprietary to R3 and its suppliers and are protected by trade secret law.
 *
 * Distribution of this file or any portion thereof via any medium without the express permission of R3 is strictly prohibited.
 */

package net.corda.finance.schemas

import net.corda.core.identity.AbstractParty
import net.corda.core.schemas.MappedSchema
import net.corda.core.schemas.PersistentState
import net.corda.core.serialization.CordaSerializable
import net.corda.core.utilities.MAX_HASH_HEX_SIZE
import net.corda.core.contracts.MAX_ISSUER_REF_SIZE
import org.hibernate.annotations.Type
import javax.persistence.*

/**
 * An object used to fully qualify the [CashSchema] family name (i.e. independent of version).
 */
object CashSchema

/**
 * First version of a cash contract ORM schema that maps all fields of the [Cash] contract state as it stood
 * at the time of writing.
 */
@CordaSerializable
object CashSchemaV1 : MappedSchema(
        schemaFamily = CashSchema.javaClass, version = 1, mappedTypes = listOf(PersistentCashState::class.java)) {

    override val migrationResource = "cash.changelog-master"

    @Entity
    @Table(name = "contract_cash_states", indexes = [Index(name = "ccy_code_idx", columnList = "ccy_code"), Index(name = "pennies_idx", columnList = "pennies")])
    class PersistentCashState(
            /** X500Name of owner party **/
            @Column(name = "owner_name", nullable = true)
            var owner: AbstractParty?,

            @Column(name = "pennies", nullable = false)
            var pennies: Long,

            @Column(name = "ccy_code", length = 3, nullable = false)
            var currency: String,

            @Column(name = "issuer_key_hash", length = MAX_HASH_HEX_SIZE, nullable = false)
            var issuerPartyHash: String,

            @Column(name = "issuer_ref", length = MAX_ISSUER_REF_SIZE, nullable = false)
            @Type(type = "corda-wrapper-binary")
            var issuerRef: ByteArray
    ) : PersistentState()
}

```



## Identity mapping

Schema entity attributes defined by identity types (`AbstractParty`, `Party`, `AnonymousParty`) are automatically
processed to ensure only the `X500Name` of the identity is persisted where an identity is well known, otherwise a null
value is stored in the associated column. To preserve privacy, identity keys are never persisted. Developers should use
the `IdentityService` to resolve keys from well know X500 identity names.



## JDBC session

Apps may also interact directly with the underlying Node’s database by using a standard
JDBC connection (session) as described by the [Java SQL Connection API](https://docs.oracle.com/javase/8/docs/api/java/sql/Connection.html)

Use the `ServiceHub` `jdbcSession` function to obtain a JDBC connection as illustrated in the following example:

```kotlin
        val nativeQuery = "SELECT v.transaction_id, v.output_index FROM vault_states v WHERE v.state_status = 0"

        database.transaction {
            val jdbcSession = services.jdbcSession()
            val prepStatement = jdbcSession.prepareStatement(nativeQuery)
            val rs = prepStatement.executeQuery()

```


JDBC sessions can be used in Flows and Service Plugins (see “[Writing flows](flow-state-machines.md)”)

The following example illustrates the creation of a custom corda service using a jdbcSession:

```kotlin
object CustomVaultQuery {

    @CordaService
    class Service(val services: AppServiceHub) : SingletonSerializeAsToken() {
        private companion object {
            private val log = contextLogger()
        }

        fun rebalanceCurrencyReserves(): List<Amount<Currency>> {
            val nativeQuery = """
                select
                    cashschema.ccy_code,
                    sum(cashschema.pennies)
                from
                    vault_states vaultschema
                join
                    contract_cash_states cashschema
                where
                    vaultschema.output_index=cashschema.output_index
                    and vaultschema.transaction_id=cashschema.transaction_id
                    and vaultschema.state_status=0
                group by
                    cashschema.ccy_code
                order by
                    sum(cashschema.pennies) desc
            """
            log.info("SQL to execute: $nativeQuery")
            val session = services.jdbcSession()
            return session.prepareStatement(nativeQuery).use { prepStatement ->
                prepStatement.executeQuery().use { rs ->
                    val topUpLimits: MutableList<Amount<Currency>> = mutableListOf()
                    while (rs.next()) {
                        val currencyStr = rs.getString(1)
                        val amount = rs.getLong(2)
                        log.info("$currencyStr : $amount")
                        topUpLimits.add(Amount(amount, Currency.getInstance(currencyStr)))
                    }
                    topUpLimits
                }
            }
        }
    }
}

```


which is then referenced within a custom flow:

```kotlin
        @Suspendable
        @Throws(CashException::class)
        override fun call(): List<SignedTransaction> {
            progressTracker.currentStep = AWAITING_REQUEST
            val topupRequest = otherPartySession.receive<TopupRequest>().unwrap {
                it
            }

            val customVaultQueryService = serviceHub.cordaService(CustomVaultQuery.Service::class.java)
            val reserveLimits = customVaultQueryService.rebalanceCurrencyReserves()

            val txns: List<SignedTransaction> = reserveLimits.map { amount ->
                // request asset issue
                logger.info("Requesting currency issue $amount")
                val txn = issueCashTo(amount, topupRequest.issueToParty, topupRequest.issuerPartyRef, topupRequest.notaryParty)
                progressTracker.currentStep = SENDING_TOP_UP_ISSUE_REQUEST
                return@map txn.stx
            }

            otherPartySession.send(txns)
            return txns
        }

```


For examples on testing `@CordaService` implementations, see the oracle example [here](oracles.md)
