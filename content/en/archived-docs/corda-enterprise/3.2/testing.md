---
aliases:
- /releases/3.2/testing.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-testing
    parent: corda-enterprise-3-2-release-process-index
    weight: 1030
tags:
- testing
title: Testing Corda
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Testing Corda


## Automated Tests

Corda has a maintained suite of tests that any contributing developers must maintain and add to if new code has been added.

There are several distinct test suites each with a different purpose;

**Unit tests**: These are traditional unit tests that should only test a single code unit, typically a method or class.

**Integration tests**: These tests should test the integration of small numbers of units, preferably with mocked out services.

**Smoke tests**: These are full end to end tests which start a full set of Corda nodes and verify broader behaviour.

**Other**: These include tests such as performance tests, stress tests, etc, and may be in an external repo.

These tests are mostly written with JUnit and can be run via `gradle`. On windows run `gradlew test integrationTest
smokeTest` and on unix run `./gradlw test integrationTest smokeTest` or any combination of these three arguments.

Before creating a pull request please make sure these pass.


## Manual Testing

Manual testing would ideally be done for every set of changes merged into master, but practically you should manually test
anything that would be impacted by your changes. The areas that usually need to be manually tested and when are below;

**Node startup** - changes in the `node` or `node:capsule` project in both the Kotlin or gradle or the `cordformation` gradle plugin.

**Sample project** - changes in the `samples` project. eg; changing the IRS demo means you should manually test the IRS demo.

**Explorer** - changes to the `tools/explorer` project.

**Demobench** - changes to the `tools/demobench` project.

How to manually test each of these areas differs and is currently not fully specified. For now the best thing to do is
ensure the program starts, that you can interact with it, and that no exceptions are generated in normal operation.

TODO: Add instructions on manual testing


## External Database Testing

Running a node against a remote database requires several setup steps including a database setup/cleanup and adding a JDBC driver JAR to the node.
All required steps are described in [Standalone database](node-database.md#standalone-database-config-examples-ref).


### Integration Tests

Integration tests can be parameterised to run against any remote database (instead of the default embedded H2 instance).
When running Gradle task *integrationTest*, a combination of several system properties (passed as *-Dproperty=…*) can modify the node default JDBC setting and trigger a database setup before and after each test.

To run integration tests against a remote database provide these system properties:


* `custom.databaseProvider` -  the predefined configuration template for a node, the template is a name of the file under resources` folder and a switch to add JDBC driver runtime dependency, accepted values: *integration-azure-sql*, *integration-sql-server*, *integration-oracle-11*, *integration-oracle*, *integration-postgress*
* `test.db.script.dir` - the path to predefined set of SQL script templates for a given database, accepted values: *database-scripts/azure-sql*, *database-scripts/sql-server*, *database-scripts/oracle*, *database-scripts/postgress*
* `test.db.admin.user` - a database user to run SQL setup scripts, the user needs to have permissions to create other users and grant them permissions
* `test.db.admin.password` -  a password for the database user to run SQL scripts
* `corda.dataSourceProperties.dataSource.url` - specify full JDBC connection string use by a node to connect to database, JDBC URL provided by the predefined configuration file (by `databaseProvider`) doesn’t contain specific host names and port
* `corda.dataSourceProperties.dataSource.password` - optional parameter, defaults to a password set in the SQL scripts from `test.db.script.dir`

Example running Gradle integration tests task against Azure SQL database at *mycordadb.database.windows.net* host:

```bash
./gradlew integrationTest -Dcustom.databaseProvider=integration-sql-azure \
-Dcorda.dataSourceProperties.dataSource.url="jdbc:sqlserver://mycordadb.database.windows.net:1433;databaseName=mycordadb;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30" \
-Dtest.db.admin.user=dbuser@mycordadb \
-Dtest.db.admin.password='paSSword(!' \
-Dtest.db.script.dir=database-scripts/sql-azure
```

Several Gradle task parameters and additional setup code enable running against custom databases.
The property `custom.databaseProvider` is resolved at runtime to load a configuration file on the classpath with the
name `$custom.databaseProvider.conf` containing database configuration properties. These settings override the default H2 ones
defined in the node configuration file (see `reference.conf`).
Integration test run a predefined set of SQL setup scripts selected for a specific database provider by `test.db.script.dir`.
Integration tests run the script for all nodes involved in the test and replace *${schema}* with the appropriate value, derived from a node name. SQL templates files are executed at different stage of the integration test:



* `db-global-setup.sql`- before a test class (@BeforeClass), should create database users, schema and permissions
* `db-setup.sql` - before a test (@Before), should clean up/drop tables
* `db-cleanup.sql` - after a test (@After), may clean up/drop tables
* `db-global-cleanup.sql` - after a test class (@AfterClass), may drop user and schema


Not all stages need to be present e.g., when `db-setup.sql` deletes all tables before a test then `db-cleanup.sql` after the test is not needed.

The setup ensures that all nodes involved in a single integration test use different database users to achieve database separation.
The configuration file (denoted by the `custom.databaseProvider` property) defines a user and a schema based on the *${custom.nodeOrganizationName}* value.
The value is a placeholder which is resolved at runtime to a node organization name.



### Cordform Gradle task

Cordform task `deployNodes` can be modified to override default H2 database settings.
For each node element add `extraConfig` with all JDBC/database properties as described in [Node configuration](node-database.md#standalone-database-config-examples-ref).
The task copies JDBC driver JAR files to the `./drivers` subdirectory listed by the `drivers` property.
To avoid duplicated definitions of `extraConfig` or `drivers` properties, they can be defined at the top-level with an `ext.` prefix and reused for each node entry as shown in the example below.

```bash
task deployNodes(type: net.corda.plugins.Cordform, dependsOn: ['jar']) {

    ext.drivers = ['[JDBC_DRIVER_PATH]']
    ext.extraConfig = [
             'dataSourceProperties.dataSource.url' : 'jdbc:sqlserver://[DATABASE].database.windows.net:1433;databaseName=[DATABASE];encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30',
             'dataSourceProperties.dataSourceClassName' : 'com.microsoft.sqlserver.jdbc.SQLServerDataSource',
             'database.transactionIsolationLevel' : 'READ_COMMITTED',
             'database.runMigration' : 'true'
    ]
    ...
    node {
        ...
        extraConfig = ext.extraConfig + [
                 'dataSourceProperties.dataSource.user' : '[USER]',
                 'dataSourceProperties.dataSource.password' : '[PASSWORD]',
                 'database.schema' : '[SCHEMA]'
        ]

        drivers = ext.drivers
```

The Cordform task doesn’t create/cleanup the database and doesn’t download the required JDBC driver JAR, however it can copy already downloaded JDBC driver via the `drivers` property.
Manual database setup is described in [Node configuration](node-database.md#standalone-database-config-examples-ref).

{{< note >}}
To deploy nodes that are distributed with Capsule only, the Cordform task can use the `jarDirs` configuration entry instead of the `drivers` entry.

{{< /note >}}

### DriverDSL

A node started programmatically via the `DriverDSL` can be configured to use a remote database.
The JDBC driver JAR needs to be added as a Gradle runtime dependency for the `node` module in `build.gradle`.
The file already contains conditional addition of JDBC dependencies of supported databases.
For a given JDBC dependency, copy it outside of the conditional to ensure that it is always gets added to the node JAR.

For each node, pass JDBC/database properties described in [Node configuration](node-database.md#standalone-database-config-examples-ref) via the `customOverrides` parameter of the `startNode` method, e.g.:

```kotlin
startNode(providedName = ALICE_NAME, rpcUsers = listOf(demoUser), customOverrides = aliceDatabaseProperties)
```

`DriverDSL` doesn’t create/cleanup database. Manual database setup is described in [Node configuration](node-database.md#standalone-database-config-examples-ref).

