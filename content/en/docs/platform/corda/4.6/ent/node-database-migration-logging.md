---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-operating-db
tags:
- node
- database
- migration
- logging
title: Database schema migration logging
weight: 40
---



# Database schema migration logging

Database migrations for the Corda node’s internal database objects are recorded in the node’s default log file.

The detailed, unstructured logs produced by Liquibase can be enabled by providing additional log4j2 configuration.

The setup of CorDapps’ custom tables (which only happens automatically when using H2) are not recorded in the node’s logs
by default. Enabling the Hibernate logger will produce these logs (see node-administration-logging).


## Log format

The migration logs are in a fixed format, prefixed with *DatabaseInitialisation*.
The log consists of two parts, the sequence of the change sets to be run and the progress of change sets execution.
A change set is a single database schema change, defined in a Liquibase script, which may contain one or more DDL statements.

The log sequence:

```none
<START>
[<COUNT>
<LIST>
<PROGRESS>]
<SUCCESSFUL> | <ERROR>
```

where:


* START := a log line denoting the start of a database initialisation
* COUNT := the number of change sets to be applied to the database
* LIST := the list od all change sets to be run, each change set on a separate line
* PROGRESS := log lines before and after running each change set
* SUCCESSFUL := a line denoting end of the database initialisation with status success.
* ERROR := a log line denoting that the migration has failed, depending where the failure occurs
COUNT, LIST or PROGRESS may be not present

The log line format:

```none
DatabaseInitialisation(id="<RANDOM_ID>";[changeset="<ID>"| file="<FILE_NAME>"][source="<CORDAPP>"|"node";]status="<STATUS>"[;error_code="<CODE>";message="<ERROR>"])
```

where:


* RANDOM_ID := a random generated value identifying the set of migrations, to aid with log parsing
* ID := Liquibase [change set ID](https://www.liquibase.org/documentation/changeset.html)
* FILE_NAME := the Liquibase file which couldn’t be found or parsed, occurs with STATUS=”error”
* CORDAPP := the CorDapp JAR file name containing the Database Management Script or “node” value for Corda node core tables
* STATUS := the status for the entire database schema initialisation process and a specific change sets:
|        “start” - start of the whole database migration process,
|        “to be run” - the list of change sets before migration run,
|        “start” - the start of the current change set,
|        “successful” - the successful completion of a change set,
|        “error” - an error for the whole process or an error while running a specific change set
* CODE := a predefined error code (see [Error codes](#node-database-migration-logging-error-codes))
* ERROR := a detailed message, for change set error it will be error produced by Liquibase

An example database initialisation log:


```none
DatabaseInitialisation(id="FrSzFgm2";status="start")
DatabaseInitialisation(id="FrSzFgm2";changeset_count="2")
DatabaseInitialisation(id="FrSzFgm2";changeset="migration/common.changelog-init.xml::1511451595465-1.1::R3.Corda";source="node";status="to be run")
DatabaseInitialisation(id="FrSzFgm2";changeset="migration/vault-schema.changelog-init.xml::1511451595465-22::R3.Corda";source="node";status="to be run")
DatabaseInitialisation(id="FrSzFgm2";changeset="migration/common.changelog-init.xml::1511451595465-1.1::R3.Corda";source="node";status="start")
DatabaseInitialisation(id="FrSzFgm2";changeset="migration/common.changelog-init.xml::1511451595465-1.1::R3.Corda";source="node";status="successful")
DatabaseInitialisation(id="FrSzFgm2";changeset="migration/vault-schema.changelog-init.xml::1511451595465-22::R3.Corda";source="node";status="start")
DatabaseInitialisation(id="FrSzFgm2";changeset="migration/vault-schema.changelog-init.xml::1511451595465-22::R3.Corda";source="node";status="successful")
DatabaseInitialisation(id="FrSzFgm2";status="successful")
```



An example unsuccessful database initialisation log:


```log
...
DatabaseInitialisation(id="FrSzFgm2";changeset="migration/common.changelog-init.xml::1511451595465-1.1::R3.Corda";source="node";status="start")
DatabaseInitialisation(id="FrSzFgm2";changeset="migration/common.changelog-init.xml::1511451595465-1.1::R3.Corda";source="node";status="error";error_code="9";message="Migration failed for change set migration/node-services.changelog-init.xml::1511451595465-39::R3.Corda:      Reason: liquibase.exception.DatabaseException: Table "NODE_MESSAGE_RETRY" not found; SQL statement: ALTER TABLE PUBLIC.node_message_retry ADD CONSTRAINT node_message_retry_pkey PRIMARY KEY (message_id) [42102-197] [Failed SQL: ALTER TABLE PUBLIC.node_message_retry ADD CONSTRAINT node_message_retry_pkey PRIMARY KEY (message_id)]")
DatabaseInitialisation(id="FrSzFgm2";status="error";error_code="9";message="Migration failed for change set migration/node-services.changelog-init.xml::1511451595465-39::R3.Corda:      Reason: liquibase.exception.DatabaseException: Table "NODE_MESSAGE_RETRY" not found; SQL statement: ALTER TABLE PUBLIC.node_message_retry ADD CONSTRAINT node_message_retry_pkey PRIMARY KEY (message_id) [42102-197] [Failed SQL: ALTER TABLE PUBLIC.node_message_retry ADD CONSTRAINT node_message_retry_pkey PRIMARY KEY (message_id)]")
```





## Error codes

As mentioned above, an error log entry includes a numeric `<CODE>` preceded by the `error_code=` label. These error codes serve
as predefined categories grouping potentially many specific errors.  The following codes are currently in use:


* 1 - error not belonging to any other category;
* 2 - missing database driver or an invalid value for the dataSourceClassName property, for example:

```none
DatabaseInitialisation(id="bMmdUxxZ";status="error";error_code="2";message="Could not find the database driver class. Please add it to the 'drivers' folder. See: https://docs.corda.net/corda-configuration-file.html")
```


* 3 - invalid data source property, for example:

```none
DatabaseInitialisation(id="jcaavDAO";status="error";error_code="3";message="Could not create the DataSource: Property invalid_property does not exist on target class org.postgresql.ds.PGSimpleDataSource")
```


* 4 - initialization error, for example:

```none
DatabaseInitialisation(id="r52KsERT";status="error";error_code="4";message="Could not connect to the database. Please check your JDBC connection URL, or the connectivity to the database.")
```


* 5 - missing database migration script, for example:

```none
DatabaseInitialisation(id="nCTRAxNg";file="migration/my-schema.changelog-master";source="my-cordapp.jar";status="error";error_code="5";message="Missing migration script migration/my-schema.changelog-master.[xml/sql/yml/json] required by mapped schema com.mycompany.mycordapp.MySchema v1.") {}
DatabaseInitialisation(id="nCTRAxNg";status="error";error_code="5";message="Missing migration script migration/my-schema.changelog-master.[xml/sql/yml/json] required by mapped schema com.mycompany.mycordapp.MySchema v1.") {}
```


* 6 - error while parsing database migration script, for example:

```none
DatabaseInitialisation(id="EojbAXaT";file="migration/my-schema.changelog-master.xml";source="my-cordapp.jar";status="error";error_code="6";message="Error parsing master.changelog.json") {}
DatabaseInitialisation(id="EojbAXaT";status="error";error_code="6";message="Error parsing master.changelog.json") {}
```


* 7 - invalid SQL statement in database migration script, for example:

```none
DatabaseInitialisation(id="Klvw19Cp";source="node";status="error";error_code="7";message="Could not create the DataSource: Migration failed for change set migration/vault-schema.changelog-v8.xml::create-external-id-to-state-party-view::R3.Corda:      Reason: liquibase.exception.DatabaseException: ERROR: syntax error at or near \"choose\"   Position: 48 [Failed SQL: CREATE VIEW my_schema.v_pkey_hash_ex_id_map AS choose                 state_party.public_key_hash,                 state_party.transaction_id,                 state_party.output_index,                 pk_hash_to_ext_id_map.external_id             from state_party             join pk_hash_to_ext_id_map             on state_party.public_key_hash = pk_hash_to_ext_id_map.public_key_hash]")
```


* 8 - invalid SQL type in database migration script, for example:

```none
DatabaseInitialisation(id="Xlrw5seg";changeset="migration/my-schema.changelog-master.xml::1512743551377-1::R3.Corda";source="my-cordapp.jar";status="error";error_code="8";message="Migration failed for change set migration/my-schema.changelog-master.xml::1512743551377-1::R3.Corda:      Reason: liquibase.exception.DatabaseException: ERROR: type \"biginteger\" does not exist   Position: 82 [Failed SQL: CREATE TABLE \"AliceCorp\".messages (output_index INTEGER NOT NULL, transaction_id BIGINTEGER(100) NOT NULL, dummy VARCHAR(255))]")
DatabaseInitialisation(id="Xlrw5seg";status="error";error_code="8";message="Migration failed for change set migration/my-schema.changelog-master.xml::1512743551377-1::R3.Corda:      Reason: liquibase.exception.DatabaseException: ERROR: type \"biginteger\" does not exist   Position: 82 [Failed SQL: CREATE TABLE \"AliceCorp\".messages (output_index INTEGER NOT NULL, transaction_id BIGINTEGER(100) NOT NULL, dummy VARCHAR(255))]")
```


* 9 - unable to apply a change set due to its incompatibility with the current database state, for example:

```none
DatabaseInitialisation(id="9HBhcBgl";changeset="migration/my-schema.changelog-master.xml::1512743551377-1::R3.Corda";source="my-cordapp.jar";status="error";error_code="9";message="Migration failed for change set migration/my-schema.changelog-master.xml::1512743551377-1::R3.Corda:      Reason: liquibase.exception.DatabaseException: ERROR: relation \"messages\" already exists [Failed SQL: CREATE TABLE \"AliceCorp\".messages (output_index INTEGER NOT NULL, transaction_id VARCHAR(64) NOT NULL, dummy VARCHAR(255))]")
DatabaseInitialisation(id="9HBhcBgl";status="error";error_code="9";message="Migration failed for change set migration/my-schema.changelog-master.xml::1512743551377-1::R3.Corda:      Reason: liquibase.exception.DatabaseException: ERROR: relation \"messages\" already exists [Failed SQL: CREATE TABLE \"AliceCorp\".messages (output_index INTEGER NOT NULL, transaction_id VARCHAR(64) NOT NULL, dummy VARCHAR(255))]")
```


* 10 - outstanding database migration change sets, for example:

```none
DatabaseInitialisation(id="oT6igoGJ";status="error";error_code="10";message="Incompatible database schema version detected. Node is configured with option database.runMigration=false or the most recent Database Management Tool has not been run. Reason: There are 109 outstanding database changes that need to be run.") {}
```


* 11 - no outstanding database migration change sets however mapped schema code (JPA entity) is incompatible with a database object (e.g. table) created by database management script, for example:

```none
DatabaseInitialisation(id="e6KAmx6O";status="error";error_code="11";message="Incompatible database schema version detected. Reason: All database changes are up-to-date however JPA Entity is incompatible with database schema. Reason: Schema-validation: missing column [dummy] in table [`AliceCorp`.messages]")
```


* 999 - uncategorised exception when applying a change set;


## Native Liquibase logs

The native Liquibase logs are disabled by default.
They can be enabled by adding an extra log4j2 file with ‘INFO’ log level for the ‘liquibase’ logger:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="INFO">
    <Loggers>
        <Logger name="liquibase" additivity="false" level="INFO"/>
    </Loggers>
</Configuration>
```

When starting the Corda node the extra config file need to be provided:

```bash
java -jar -Dlog4j.configurationFile=log4j2.xml,path_to_custom_file.xml corda.jar
```

Enabling custom logging is also described in node-administration-logging.
