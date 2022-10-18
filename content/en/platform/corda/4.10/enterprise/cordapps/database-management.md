---
date: '2021-07-2021'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-9-cordapps-states
tags:
- database
- management
title: Database management scripts
weight: 30
---

# Database management scripts

Corda and your installed CorDapps store their data in a relational database. When you install new CorDapp, the associated tables, indexes, foreign-keys, etc. must be created. If you install a new version of a CorDapp, its database schema may have changed,
but the existing data needs to be preserved or changed accordingly.

In Corda Enterprise, CorDapps’ custom tables are created or upgraded automatically based on
database management scripts written in [Liquibase](../../../../../../en/platform/corda/4.9/enterprise/node/operating/node-database.html#liquibase-ref) format and embedded in CorDapp `.jar`s.
Any CorDapp with custom tables (`MappedSchema`)  must contain a matching database management script.


## Script structure

The `MappedSchema` class requires a matching Liquibase script defining table creation. Liquibase scripts use a declarative set of XML tags and attributes to express DDL across database vendors.
Liquibase script code is grouped in a units called `changeSet`s. A single `changeSet` contains instructions to create/update/delete a single table.


### Database table creation

To create your initial tables, you can use tags such as `createTable` and `addPrimaryKey`.
See the [Liquibase documentation](https://www.liquibase.org/documentation/index.html) for examples and the complete Liquibase instruction list.

Below, you will find an example Liquibase script. It follows a simple `MappedSchema`, `MySchemaV1`.  The schema has a single JPA entity called `PersistentIOU` with the following fields:

```kotlin
import net.corda.core.identity.AbstractParty
import net.corda.core.schemas.MappedSchema
import net.corda.core.schemas.PersistentState
import java.util.*
import javax.persistence.*
import org.hibernate.annotations.Type

object MySchema

object MySchemaV1 : MappedSchema(schemaFamily = MySchema.javaClass,
    version = 1, mappedTypes = listOf(PersistentIOU::class.java)) {
    @Entity
    @Table(name = "iou_states")
    class PersistentIOU(
        @Column(name = "owner_name")
        var owner: AbstractParty?,
        @Column(name = "lender")
        var lenderName: String,
        @Column(name = "value", nullable = false)
        var value: Int,
        @Column(name = "linear_id", nullable = false)
        @Type(type = "uuid-char")
        var linearId: UUID
    ) : PersistentState() {
        // Default constructor required by hibernate.
        constructor(): this(null, "", 0, UUID.randomUUID())
    }
}
```

The corresponding Liquibase `changeSet` for the JPA entity is:

```xml
<changeSet author="My_Company" id="create-my_states">
<createTable tableName="iou_states">
    <column name="output_index" type="INT">
        <constraints nullable="false"/>
    </column>
    <column name="transaction_id" type="NVARCHAR(64)">
        <constraints nullable="false"/>
    </column>
    <column name="owner_name" type="NVARCHAR(255)"/>
    <column name="lender" type="NVARCHAR(255)">
        <constraints nullable="false"/>
    </column>
    <column name="value" type="INT">
        <constraints nullable="false"/>
    </column>
    <column name="linear_id" type="VARCHAR(255)">
        <constraints nullable="false"/>
    </column>
</createTable>
<addPrimaryKey columnNames="output_index, transaction_id"
      constraintName="PK_iou_states"
      tableName="iou_states"/>
</changeSet>
```

Each `changeSet` tag is uniquely identified by the combination of the `author` tag, the `id` tag, and the file classpath name.
The first entry `createTable` defines a new table. The table and the column names match the relevant names defined in JPA annotations of `PersistentIOU` class.
The columns `output_index` and `transaction_id` are mapped from the `PersistentState` superclass fields. The `addPrimaryKey` tag adds the compound primary key.
To achieve compatibility with supported databases, the mapping of `linearId` field is a custom `uuid-char` type. This type can be mapped to a `VARCHAR(255)` column.
Corda contains a built-in custom JPA converter for the `AbstractParty` type to a varchar column type, defined as `NVARCHAR(255)`.


### Database table modification

For any subsequent changes to a table, a create a new `changeSet`. The existing `changeSet` cannot be modified, as Liquibase needs to track what was created.

Building on the previous example, suppose that, for security reasons,
the `owner_name` column of the `PersistentIOU` entity needs to be stored as a hash instead of the X500 name of the owning party.

Replace the `PersistentIOU` field `owner`:

```kotlin
@Column(name = "owner_name")
var owner: AbstractParty?,
```

with:

```kotlin
@Column(name = "owner_name_hash", length = MAX_HASH_HEX_SIZE)
```

To change the database table:
1. Add a new column.
2. Populate the hash value of the old column to the new column for existing rows.
3. Remove the old column.

You can do this in a new `changeSet`:

```xml
<changeSet author="My_Company" id="replace owner_name with owner_name_hash">
    <addColumn tableName="iou_states">
        <column name="owner_name_hash" type="nvarchar(130)"/>
    </addColumn>
    <update tableName="iou_states">
        <column name="owner_name_hash" valueComputed="hash(owner_name)"/>
    </update>
    <dropColumn tableName="iou_states" columnName="owner_name"/>
</changeSet>
```

The column name change simplifies the migration steps, avoiding in-place column modification.


## Distributing scripts with CorDapps

By default, Corda expects a Liquibase script file name to be a hyphenated version of the `MappedSchema` name.
Change uppercase letters to lowercase, and be prefix the name with hyphen (except at the beginning of file).
For example, for a `MappedSchema` named `MySchema`, Corda searches for a `my-schema.changelog-master.xml` file.
You can use `.json` and `.sql` extensions under the `migration` package in CorDapp `.jar`s.

You can also set the name and the location in the `MappedSchema` code by overriding the field `val migration/migrationResource: String`.
Set the value as a `namespace` and a file name without an extension.

The files must be on classpath, so put them in the resources folder of your CorDapp source code. To follow Corda convention for structuring the change-logs, create one master changelog file per `MappedSchema` . Each will only include release changelogs.

Continuing the `MySchema` example, the initial CorDapp release contains two files. The first one is the master file `my-schema-v1.changelog-master.xml`:

```xml
<?xml version="1.1" encoding="UTF-8" standalone="no"?>
<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-3.5.xsd">
    <include file="migration/my-schema.changelog-init.xml"/>
</databaseChangeLog>
```

The master file contains one entry, which points to the second file. The `my-schema.changelog-init.xml` file contains an instruction to create a table and primary key.
For brevity, file encoding and XML schemas in the top-level entry are omitted from this example.

```xml
<databaseChangeLog>
<changeSet author="My_Company" id="create_my_states">
<createTable tableName="iou_states">
    <column name="output_index" type="INT">
        <constraints nullable="false"/>
    </column>
    <column name="transaction_id" type="NVARCHAR(64)">
        <constraints nullable="false"/>
    </column>
    <column name="owner_name" type="NVARCHAR(255)"/>
    <column name="lender" type="NVARCHAR(255)">
        <constraints nullable="false"/>
    </column>
    <column name="value" type="INT"/>
    <column name="linear_id" type="VARCHAR(255)"/>
</createTable>
<addPrimaryKey columnNames="output_index, transaction_id"
      constraintName="PK_iou_states"
      tableName="iou_states"/>
</changeSet>
</databaseChangeLog>
```

If the database schema changes with a subsequent CorDapp release, a new file is created and added to a “master” changelog file.
In the example below, the release changes a name and type of the *owner_name* column.

The master changelog file `my-schema-v1.changelog-master.xml` will have an additional entry:

```xml
<databaseChangeLog>
    <include file="migration/my-schema.changelog-init.xml"/>
    <include file="migration/my-schema.changelog-v2.xml"/>
</databaseChangeLog>
```

The actual column change is defined in a new `my-schema.changelog-v2.xml` file:

```xml
<databaseChangeLog>
   <changeSet author="My_Company" id="replace owner_name with owner_hash">
       <addColumn tableName="iou_states">
           <column name="owner_name_hash" type="nvarchar(130)"/>
       </addColumn>
       <update tableName="iou_states">
           <column name="owner_name_hash" valueComputed="hash(owner_name)"/>
       </update>
       <dropColumn tableName="iou_states" columnName="owner_name"/>
   </changeSet>
</databaseChangeLog>
```

The CorDapp retains the initial script `my-schema.changelog-init.xml` with unchanged content.


## Creating script for initial table creation using the Corda database management tool

The database management tool is a standalone .`jar` file named `tools-database-manager-${corda_release_version}.jar`.
Enterprise customers can use it to develop Liquibase scripts for CorDapps.

A generated script contains an instruction in SQL format (DDL statements), which may be not portable across different databases.
Only use the SQL format script development purposes, or when a CorDapp doesn’t need to be portable across
different databases (for example, if the CorDapp is deployed on nodes running against PostgreSQL),
You can use this script to create a portable Liquibase script in XML format. The tool only lets you create a Liquibase script for the initial database object. You cannot alter or delete tables.

You can use the `create-migration-sql-for-cordapp` sub-command to create initial database management scripts for each `MappedSchema` in a CorDapp:

```shell
java -jar tools-database-manager-|version|.jar \
            create-migration-sql-for-cordapp [-hvV]
                                             [--jar]
                                             [--logging-level=<loggingLevel>]
                                             -b=<baseDirectory>
                                             [-f=<configFile>]
                                             [<schemaClass>]
```

Optionally, you can set the `schemaClass` parameter to create migrations for a particular class. Otherwise, it creates migration
schemas for every class it finds.

Additional options:

* `--base-directory`, `-b`: (Required) The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the config file. Defaults to `node.conf`.
* `--jar`: Places generated migration scripts into a jar.
* `--verbose`, `--log-to-console`, `-v`: If set, this prints logging to the console and to a file.
* `--logging-level=<loggingLevel>`: Enables logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Shows a help message and exits.
* `--version`, `-V`: Prints version information and exits.


{{< warning >}}
The CorDapp must work on all supported Corda databases. It is the developer's responsibility to test the CorDapp and migration scripts against all databases.

{{< /warning >}}


Continuing the `MySchemaV1` class example, assume that you have a running MS SQL database. The *nodeA* directory contains Corda node configuration to connect to the database.
The *drivers* sub-directory contains a CorDapp with `MySchemaV1`.

To obtain Liquibase script in SQL format, run:

`java -jar tools-database-manager-${corda_release_version}.jar create-migration-sql-for-cordapp -b=my_cordapp/build/nodes/nodeA`

This will generate the `migration/my-schema-v1.changelog-master.sql` script with the content:

```sql
--liquibase formatted sql

--changeset R3.Corda.Generated:initial_schema_for_MySchemaV1

create table iou_states (
   output_index int not null,
    transaction_id nvarchar(64) not null,
    lender nvarchar(255),
    linear_id varchar(255) not null,
    owner_name nvarchar(255),
    value int not null,
    primary key (output_index, transaction_id)
);
```

The second comment has the format `--changeset author:change_set_id` with default values *R3.Corda.Generated* for the script author
and *initial_schema_for_<schema_class_name>* for the `changeSet` id.
For development purposes, the default values are sufficient. However, when you distribute the CorDapp, replace the generic
*R3.Corda.Generated* author name.

In most cases, the generated script in SQL format contains DDL that is only compatible with the database that created it.
In the above example, the script would fail on an Oracle database, due to the invalid *nvarchar* type. The correct Oracle database type is *nvarchar2*.



## Adding scripts retrospectively to an existing CorDapp

If a CorDapp does not include the required migration scripts for each `MappedSchema`, you can generate and inspect them before they are applied:


1. Deploy the CorDapp on your node (copy the `.jar` into the `cordapps` folder).
2. Locate the name of the `MappedSchema` object containing the new contract state entities.
3. Call the database management tool:
`java -jar corda-tools-database-manager-${corda_version}.jar --base-directory /path/to/node --create-migration-sql-for-cordapp com.example.MyMappedSchema`.
This generates a file called `my-mapped-schema.changelog-master.sql` in a folder called `migration` in the `base-directory`.
If no `MappedSchema` object is specified, the tool generates one SQL file for each schema defined in the CorDapp.
4. Inspect the file(s) to ensure correctness. This is a standard SQL file with some Liquibase metadata as comments.
5. Create a `.jar` containing the `migration` folder (`originalCorDappName-migration.jar`).
6. Deploy the `.jar` in the node’s `cordapps` folder with the CorDapp by running `jar cvf /path/to/node/cordapps/MyCordapp-migration.jar migration` in the node’s base directory.

Test the migration by running with the database management tool and inspecting the output file.


## Considerations for migrating open source CorDapps to Corda Enterprise

If you upgrade a node to Enterprise, then any CorDapps running on the node must contain Liquibase scripts.
Any custom tables (which are required by CorDapps) were created manually or by Hibernate upon node startup.
Therefore, the database doesn’t contain an entry in the *DATABASECHANGELOG* table, which is created by the Liquibase runner.
You need to create the entries and provide them to a node operator to run them manually.

See the  [Liquibase Sql Format](http://www.liquibase.org/documentation/sql_format.html) documents and Corda's [upgrade procedure](../../../../../../en/platform/corda/4.9/enterprise/node-operations-upgrading-os-to-ent.html#upgrade-from-corda-open-source-to-corda-enterprise) to learn how to obtain SQL statements.



## Liquibase specifics

When writing data migrations, certain databases may have particular limitations. These may require database-specific migration code. For example, in Oracle:

* 30 byte names - Prior to version 12c the maximum length of table/column names was around 30 bytes. After 12c, the limit is 128 bytes. There is no way to reconfigure the limit or make a Liquibase workaround without also specializing the CorDapp code.
* VARCHAR longer than 2000 bytes - Liquibase does not automatically resolve the issue, and will create a broken SQL statement. The solution is to migrate to LOB types (CLOB, BLOB, NCLOB) or extend the length limit. Versions after 12c can use [extended data types](https://oracle-base.com/articles/12c/extended-data-types-12cR1).


## Example Liquibase with specialised logic

When using Liquibase to work around the issue of VARCHAR length, you could create a changeset
specific to Oracle using the <changeset … dbms=”oracle”> with the supported Oracle value type. Liquibase
does not do the conversion automatically.

```xml
<!--This is only executed for Oracle-->
<changeSet author="author" dbms = "oracle">
    <createTable tableName="table">
        <column name="field" type="CLOB"/>
    </createTable>
</changeSet>

<!--This is only executed for H2, Postgres and SQL Server-->
<changeSet author="author" dbms="h2,postgresql,sqlserver">
    <createTable tableName="table">
        <column name="field" type="VARCHAR(4000)"/>
    </createTable>
</changeSet>
```

You will see one changeset for Oracle, and one for the other database types. The dbms check ensures the correct changeset is executed.
Test your scripts against each supported database.
