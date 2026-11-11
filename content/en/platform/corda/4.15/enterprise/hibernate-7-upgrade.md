---
date: '2026-11-10'
menu:
  corda-enterprise-4-15:
    identifier: "corda-enterprise-4-15-hibernate-7-upgrade"
    parent: corda-enterprise-4-15-upgrading-menu
tags:
- upgrading
- hibernate
- jakarta
- persistence
- cordapp
title: Hibernate 7 and Jakarta Persistence in Corda Enterprise Edition 4.15
weight: 25
---

# Hibernate 7 and Jakarta Persistence in Corda Enterprise Edition 4.15

Corda Enterprise Edition 4.15 upgrades its object-relational mapper from Hibernate ORM 5.6, which is end of life, to **Hibernate ORM 7.4.12**.
Hibernate 6 and later implement *Jakarta Persistence* rather than *Java EE Persistence*, so the persistence annotations that CorDapps use for
their vault schemas, and the `EntityManager` that `ServiceHub.withEntityManager` hands to a flow, move from the `javax.persistence` package to
the `jakarta.persistence` package.

This page describes what the change means for node operators and for CorDapp developers: what you have to do to run the CorDapps you have
on a 4.15 node, and how to update a CorDapp for 4.15. It is the "Upgrading to Hibernate 7" documentation that the node's error messages
refer to.

## Who needs to do what

| You are...                                        | What you need to do |
|---------------------------------------------------|---------------------|
| **A node or notary operator**                     | Check that your database version is supported. Nothing else for this upgrade: the move to Hibernate 7 needs no database change and no configuration change. Corda 4.15 does add database migrations for other features, so the usual [database update]({{< relref "node-upgrade-notes.md#step-3-update-the-database" >}}) is still part of the node upgrade. CorDapps built for Corda 4.14 or earlier load without a rebuild. The node converts their `javax.persistence` classes to `jakarta.persistence` as it loads them, and refuses to start if a CorDapp uses something Hibernate 7 no longer has. See [Running CorDapps built for Corda 4.14 or earlier](#running-cordapps-built-for-corda-414-or-earlier). Hibernate 7's behaviour changes apply to converted CorDapps as they do to rebuilt ones, so test your CorDapps on a 4.15 node before you upgrade production. |
| **A CorDapp developer** with a custom schema      | Nothing to run on 4.15. When you next rebuild, port your schema classes to `jakarta.persistence`. A script does most of it. See [Updating a CorDapp for Corda 4.15](#updating-a-cordapp-for-corda-415). A CorDapp that uses a Hibernate `@Type` other than the ones the node substitutes must be ported before it can run on 4.15. |
| **A CorDapp developer** without a custom schema   | Nothing. Code that calls `ServiceHub.withEntityManager` or uses JPA classes directly is converted like the schemas. Port it when you next rebuild. Code that uses Hibernate classes directly is not converted: if it uses a class or member that Hibernate 7 no longer has, such as `Session.save`, the node refuses the CorDapp at start-up and the CorDapp must be ported. |

**The Hibernate 7 upgrade itself needs no database migration.** No table, column, index or sequence is added, changed or removed because
of it, and Liquibase has no changesets for it: Hibernate 7 is configured to read and write the formats that existing databases already use.
See [What stays the same in the database](#what-stays-the-same-in-the-database). Corda 4.15 does, however, add new tables for other
features, so the node's database still has to be migrated to 4.15 as for any release, with the database management tool or
`run-migration-scripts`. See [Step 3: Update the database]({{< relref "node-upgrade-notes.md#step-3-update-the-database" >}}) in the node
upgrade notes.

## For node operators

### Check your database version

Hibernate 7 raised the minimum database versions it supports. Every node database in the [platform support matrix]({{< relref "platform-support-matrix.md" >}})
for 4.15 is at or above the minimum. If you run a database version that is not in the matrix, Hibernate may generate SQL that it does not
support, so upgrade the database before you upgrade the node. Use a current JDBC driver for your database.

| Database                                  | Minimum version supported by Hibernate 7 |
|-------------------------------------------|------------------------------------------|
| PostgreSQL                                | 14                                       |
| Oracle                                    | 19c                                      |
| Microsoft SQL Server / Azure SQL          | 2014 (12.0)                              |
| CockroachDB (standalone JPA notary only)  | 23.2                                     |
| H2 (development only)                     | 2.1.214                                  |

Hibernate does not refuse an older database. It logs a warning at start-up, for example `HHH000511: The 13.0 version for [PostgreSQL] is no
longer supported, hence certain features may not work properly.`, and carries on. If you see this message, plan a database upgrade.

### Check the `database.hibernateDialect` setting

Hibernate 7 removed the dialects that were specific to one version of a database, such as `SQLServer2012Dialect`, `Oracle12cDialect`,
`PostgreSQL95Dialect` and `CockroachDB201Dialect`. If one of these is set as `database.hibernateDialect` in `node.conf`, or in the
configuration of a standalone JPA notary, the node maps it to the dialect that replaces it (`SQLServerDialect`, `OracleDialect`,
`PostgreSQLDialect` or `CockroachDialect`) and logs a warning:

```
The Hibernate dialect org.hibernate.dialect.SQLServer2012Dialect no longer exists. Using org.hibernate.dialect.SQLServerDialect instead. Please update the database configuration, or remove the dialect as it is detected automatically.
```

Nothing needs to change for the node to start. Remove the setting when convenient: Hibernate detects the database and its version itself,
and no supported database needs the setting. A custom dialect class is used as it is, and must have been built for Hibernate 7.

### Oracle

* **Oracle 23ai and later.** From Oracle 23, Hibernate 7 would map `Boolean` attributes to Oracle's native `boolean` type, and the node would
  refuse to start because the existing columns are `NUMBER(1)`. Corda configures Hibernate so that booleans stay `NUMBER(1)` on every Oracle
  version, for the node's own tables and for CorDapp tables, and makes Liquibase create new boolean columns as `NUMBER(1)` as before. New and
  upgraded databases therefore have the same column types.
* **`LONG RAW` columns, all Oracle versions.** Hibernate 7 reads the columns of a result row in a different order from Hibernate 5, which the
  Oracle JDBC driver does not allow for `LONG` and `LONG RAW` columns (the vault's `constraint_data` column is one). The node therefore sets the
  Oracle JDBC system property `oracle.jdbc.useFetchSizeWithLongColumn=true` when its database is Oracle, unless it is already set. You do not
  need to do anything. If you set it to `false` yourself, vault queries fail with `ORA-17027: Stream has already been closed`.

### Standalone JPA notary

The standalone JPA notary bootstraps Hibernate itself. It uses the same compatibility settings as the node, so an existing notary database does
not need to change. On CockroachDB, Hibernate 7 detects the database and uses its CockroachDB dialect when `hibernateDialect` is not set,
where Hibernate 5 used a PostgreSQL dialect. The visible effect is that a CockroachDB serialisation conflict in the middle of a transaction
(error 40001, `WriteTooOldError`) is now reported as a rollback, which the notary retries, where 4.14 failed the whole batch. To keep the old
behaviour, set `hibernateDialect` to `org.hibernate.dialect.PostgreSQLDialect`.

Hibernate 7's minimum CockroachDB version is 23.2. A notary on CockroachDB 23.1.x, which the platform support matrix still lists, starts
with the `HHH000511` warning described under [Check your database version](#check-your-database-version).

### Running CorDapps built for Corda 4.14 or earlier

A CorDapp built for Corda 4.14 or earlier refers to `javax.persistence`, which Hibernate 7 does not read. The node's CorDapp class loader
therefore converts such classes as it loads them: every reference to `javax.persistence` in the class bytes is renamed to `jakarta.persistence`.
This is what application servers did for Java EE applications when they moved to Jakarta EE. The rename covers:

* The schema annotations (`@Entity`, `@Table`, `@Column`, and so on).
* `AttributeConverter` implementations.
* Code that uses `EntityManager`, and the query and criteria types, in `ServiceHub.withEntityManager` blocks.
* `catch` clauses of the JPA exception types.
* The Kotlin metadata of Kotlin classes, so Kotlin reflection on a converted class sees the renamed types.

The jar on disk is not touched, so its hash, its signature and the contract constraints that depend on them are unaffected. A CorDapp that
bundles the `javax.persistence` API jar inside its own jar is loaded as well: the API classes are left as they are and only the CorDapp's
classes are converted. A CorDapp built for Corda 4.15 (`jakarta.persistence`) is loaded as it is. The log shows, once per converted CorDapp:

```
CorDapp /opt/corda/cordapps/my-cordapp-1.0.jar was built for Corda 4.14 or earlier (javax.persistence); its classes are converted to jakarta.persistence for Hibernate 7 as they are loaded
```

The Database Management Tool and the Transaction Validator Utility load CorDapps through the same class loader, so a CorDapp built for 4.14
or earlier is converted there too.

#### Hibernate annotations the node substitutes

Hibernate's own annotations are not renamed, and several of them changed between Hibernate 5 and 7, so on a class it converts the node
rewrites or checks each one.

`@Type(type = "...")`, whose members changed in Hibernate 6, is replaced by the `@JdbcTypeCode` that Corda's own schemas use, or by a
`@Convert` to a converter that stores the same format, for the following names. Each name is also recognised by the name of its Hibernate 5
type class, which `@Type` accepted too. The stored formats are unchanged.

| `@Type(type = "...")` on 4.14                                       | Replaced by |
|---------------------------------------------------------------------|-------------|
| `uuid-char`                                                         | `@JdbcTypeCode(SqlTypes.VARCHAR)` |
| `corda-wrapper-binary`                                              | `@JdbcTypeCode(SqlTypes.VARBINARY)` |
| `corda-blob`                                                        | `@JdbcTypeCode(CordaSqlTypes.CORDA_BLOB)`: a BLOB, `bytea` on PostgreSQL |
| `materialized_blob`                                                 | `@JdbcTypeCode(SqlTypes.BLOB)` |
| `materialized_clob`                                                 | `@JdbcTypeCode(SqlTypes.CLOB)` |
| `uuid-binary`                                                       | `@JdbcTypeCode(SqlTypes.BINARY)` |
| `binary`                                                            | `@JdbcTypeCode(SqlTypes.VARBINARY)` |
| `text`                                                              | `@JdbcTypeCode(SqlTypes.LONGVARCHAR)` |
| `pg-uuid`                                                           | `@JdbcTypeCode(SqlTypes.UUID)`: PostgreSQL's native `uuid` |
| `yes_no`, `true_false`                                              | `@Convert` to Corda's `YesNoBooleanConverter` or `TrueFalseBooleanConverter`, with `@JdbcTypeCode(SqlTypes.CHAR)`. They store `Y`/`N` and `T`/`F` in a `CHAR` column and read it as Hibernate 5 did, padded or not, so the column a 4.14 node used passes validation on every database, including the `char(1)` column a 4.14 node created on SQL Server under the nationalised character data setting. |
| `numeric_boolean`                                                   | `@Convert` to Hibernate 7's `NumericBooleanConverter`: 1/0 |
| `string`, on a `String`                                             | `@JdbcTypeCode(SqlTypes.VARCHAR)`. On SQL Server the explicit Hibernate 5 type opted the column out of nationalised character data (`varchar`, not `nvarchar`), and the explicit JDBC type keeps it so. |
| `character`, on a `Character` or `char`                             | `@Convert` to Corda's `SingleCharacterConverter` with `@JdbcTypeCode(SqlTypes.CHAR)`: a `CHAR` column as before, read by its first character, so a `CHAR(255)` column that Hibernate 5's DDL created on H2 reads as it did. |
| `long`, `integer`, `short`, `byte`, `boolean`, `double`, `float`, `big_decimal`, `big_integer`, `timestamp`, `date`, `time`, `instant` | Nothing, on a member of the Java type the name was the default mapping for (for example `@Type(type = "long")` on a `Long`): Hibernate 7's default mapping is the same. A `@Type` of these names on a member of another type was a choice, and the class is refused. |

Other Hibernate annotations are rewritten to what they meant:

* `@Where`, `@WhereJoinTable` and `@OrderBy`, which Hibernate 7 renamed, become `@SQLRestriction`, `@SQLJoinTableRestriction` and `@SQLOrder`.
* `@DynamicInsert(true)` and `@DynamicUpdate(true)` lose the member that Hibernate 7 no longer has; `@DynamicInsert(false)` and
  `@DynamicUpdate(false)` are dropped, as they only said what the absence of the annotation says.
* `@Generated(GenerationTime.INSERT)` becomes `@Generated(event = INSERT)`, `ALWAYS` becomes `{INSERT, UPDATE}`, and `NEVER` drops the annotation.
* The `@Cascade` constants Hibernate 7 removed are mapped: `DELETE` to `REMOVE`, `EVICT` to `DETACH` and `SAVE_UPDATE` to `PERSIST`. Like
  Hibernate 5's save-update cascade, `PERSIST` saves new children reachable from a managed parent when the session flushes and does not
  cascade `merge`. One difference remains: a *detached* child reachable from a managed parent at flush was re-attached and updated by
  Hibernate 5, but Hibernate 7 treats it as new and inserts it, so the flush fails with a duplicate-key error and the transaction rolls back.
  Code that relied on this must `merge` the child and add the managed copy the merge returns instead.
* `@ParamDef(type = "boolean")` and the other basic type names become the Java class Hibernate 7 expects, `@Cache(include = "non-lazy")`
  becomes `includeLazy = false`, and `CacheModeType` in `@NamedQuery` and `@NamedNativeQuery` becomes `CacheMode`.
* `@Index` and `@ForeignKey` only affected the DDL that Hibernate generated, which a node does not use (Liquibase creates its tables). They are
  dropped with a warning in the log that names the class and member, and so is a `@Table` (or each `@Table` of a `@Tables`) that sets only
  `appliesTo`, `indexes`, `comment` or `foreignKey`.
* Every other Hibernate annotation is checked against Hibernate 7, member by member. The JVM would silently drop an annotation that
  Hibernate 7 no longer has, or a member that it no longer has or declares differently, and the mapping would change without a trace. The
  node refuses to start instead, with a message naming the class, the annotation and the member.

#### What makes the node refuse a CorDapp

Check the schema classes of each CorDapp built for 4.14 or earlier for the following before you upgrade, or start a 4.15 test node with the
CorDapps in its `cordapps` directory. The start-up check goes through every class of every jar and reports all problems at once, so a test
node is the pre-upgrade check.

* `@TypeDef` and `@TypeDefs`, and a `@Type` other than the names in the table above (a custom type, or a basic type on a member of another type).
* `@Table` with `fetch`, `inverse`, `optional`, `sqlInsert`, `sqlUpdate` or `sqlDelete`, which changed how Hibernate read and wrote the
  secondary table. Hibernate 7 expresses these through `@SecondaryRow` and the `table` member of `@SQLInsert`, `@SQLUpdate` and `@SQLDelete`.
* Annotations that Hibernate 7 removed without an equivalent: `@Loader`, `@Polymorphism`, `@LazyCollection`, `@Proxy`, `@SelectBeforeUpdate`,
  `@Columns`, `@AccessType`, `@GeneratorType`, `@Target`, `@Persister`, `@Tuplizer`, `@IndexColumn` and `@Sort`.
* Members that Hibernate 7 removed or declares differently, without an equivalent the node can write: `@Any` and `@ManyToAny` with `metaColumn`
  or `metaDef`, `@CollectionId` with `columns` or `type`, `@CollectionType(type = "...")`, `@ParamDef(type = "...")` naming anything but the
  basic types above, and `@Cache(include = ...)` with a value other than `all` or `non-lazy`.
* Code that references a Hibernate class or member that Hibernate 7 no longer has. The conversion leaves Hibernate classes other than
  annotations alone, for example the `Session` API reached through `EntityManager.unwrap`. When it starts, the node resolves every Hibernate
  class and member that each converted class refers to (supertypes, field and method types, calls, field accesses, casts and `catch` clauses)
  against its Hibernate 7. A reference to something that no longer exists, such as `Session.save`, `Session.update`, `Session.delete` or the
  Hibernate 5 type classes, would fail with a `NoSuchMethodError` or `NoClassDefFoundError` when that code ran. References to classes and
  members that still exist, such as the exception types, `Session.flush` and `createQuery`, pass, and that code runs against Hibernate 7 unchanged.

In every case the node stops at start-up with a `CordappConversionException` that lists every class that cannot be converted and what is
wrong with it. Nothing is changed in the database when this happens. For example:

```
2 class(es) of the CorDapps built for Corda 4.14 or earlier cannot be converted for Hibernate 7 (Corda 4.15):
  - /opt/corda/cordapps/my-cordapp-1.0.jar: The class com.example.Repo uses Hibernate classes or members that do not exist in Hibernate 7
    (Corda 4.15), so that code would fail when it runs: method org.hibernate.Session.save(java.lang.Object).
  - /opt/corda/cordapps/my-cordapp-1.0.jar: The class com.example.MyState$PersistentMyState uses the Hibernate 5 annotation @Type(type = "my-type")
    on amount, which has no equivalent in Hibernate 7 that the node can substitute ...
The CorDapps that contain them need to be rebuilt for Corda 4.15 ...
```

Obtain an updated CorDapp from its vendor, or update it yourself as described in [Updating a CorDapp for Corda 4.15](#updating-a-cordapp-for-corda-415),
before you start the node on 4.15.

The code-reference check is stricter than the JVM, which links lazily: a class is refused for a reference in a method that may never run,
whether in the CorDapp's own code or in a library it bundles. If you cannot get a rebuilt CorDapp and accept that such code fails only when it
runs, start the node with the JVM option `-Dnet.corda.cordapp.missingHibernateReferences=warn`, on the `java` command line or through
`custom.jvmArgs` in `node.conf`. The references are then logged as warnings at start-up and the classes are loaded anyway. The node reads the
setting once, when it starts. The annotation checks are not affected by it, because those failures would be silent.

The check only looks at classes that refer to `javax.persistence`, because those are the ones the node converts. A class that uses a removed
Hibernate class without touching JPA, such as a Hibernate 5 custom type, is loaded as it is and fails when it runs, as after any other library
upgrade. A Hibernate library that the CorDapp bundles itself and the node does not ship, such as Hibernate Validator, is not checked against
the node's Hibernate.

#### Hibernate 7 behaviour changes apply to converted CorDapps

What the conversion does not change is Hibernate itself. A converted CorDapp runs on Hibernate 7 with Corda's compatibility settings, exactly
as a CorDapp rebuilt for 4.15 does, so every behaviour change listed under [Changes you have to make by hand](#changes-you-have-to-make-by-hand)
applies to it too: HQL and JPQL are validated strictly, `persist` of a duplicate marks the transaction for rollback, native queries return
`Long` where they returned `BigInteger`, `LIKE` patterns no longer treat a backslash as an escape on H2, PostgreSQL and CockroachDB, `NOT IN` an empty list
matches every row, and an entity attribute of an array type is refused when the node starts. A 4.14 CorDapp that relies on any of these needs
the same change a rebuilt one would, so run its flows on a 4.15 test node before relying on the conversion in production.

### Things you may notice

* The first database update after the upgrade, with the Database Management Tool or `run-migration-scripts`, logs
  `Upgrading checksum for Changeset ...` once for every changeset the database already has, before the 4.15 changesets run. Corda 4.15 moves
  Liquibase from 4.20.0 to 4.33.0, which stores changeset checksums in a new format, so Liquibase rewrites the checksum column of its
  changelog table. These lines are not migrations. A 4.14 node still accepts the checksums after a rollback.
* Hibernate logs messages such as `HHH90006001: Setting 'hibernate.id.db_structure_naming_strategy' is still incubating` once per session
  factory at start-up. They are informational.
* If the database does not match what Corda expects, start-up fails with `HibernateSchemaChangeException` and the reason, as before. The reason
  now starts with `Schema validation:` rather than `Schema-validation:`. Update any log alert that matches the old text.
* If a flow ends up in the flow hospital with `Attempted to commit database transaction marked for rollback` shortly after an
  `EntityExistsException` for the same entity, see [Recognising a failure caused by the `save` to `persist` change](#recognising-a-failure-caused-by-the-save-to-persist-change).
* With `exportHibernateJMXStatistics` enabled, the `org.hibernate:type=statistics` MBean has the same attributes as before and some new ones,
  such as `QueryPlanCacheHitCount` and `SlowQueries`. Its `getSecondLevelCacheStatistics` and `getNaturalIdCacheStatistics` operations are gone.
  Corda does not use Hibernate's second-level cache, so they had nothing to report.
* The `--allow-hibernate-to-manage-app-schema` option (development only) still creates *missing* tables and columns, and still does not alter
  existing ones. Hibernate 7's own `update` mode would alter existing columns; Corda turns that off.
* With a converted CorDapp, Quasar may print a line such as
  `[quasar] WARNING: Method not found in class - assuming suspendable: com/example/Repo#find(Ljakarta/persistence/EntityManager;...)` on the
  console at start-up. It is harmless. Quasar instruments the converted classes as the node loads them, but for a class that has not been
  loaded yet it reads the method list from the jar, where the method still has its `javax.persistence` signature. A call through the
  converted signature is then not found, and Quasar treats the method as possibly suspending, which is the safe assumption.

### Rolling back

The Hibernate 7 upgrade changes no database structure, so it does not by itself stop the database from being used with the previous version
of the node. Other changes in Corda 4.15 do add tables, so follow the usual rollback procedure: restore the backup you took before the
upgrade, and roll CorDapps back with it.

## Updating a CorDapp for Corda 4.15

### What changes

| Hibernate 5 / Corda 4.14                                               | Hibernate 7 / Corda 4.15 |
|------------------------------------------------------------------------|--------------------------|
| `import javax.persistence.*`                                            | `import jakarta.persistence.*` |
| `javax.persistence:javax.persistence-api:2.2`                           | `jakarta.persistence:jakarta.persistence-api:3.2.0` |
| `org.hibernate:hibernate-core:5.x`                                      | `org.hibernate.orm:hibernate-core:7.4.12.Final` |
| `@Type(type = "uuid-char")`                                             | `@JdbcTypeCode(SqlTypes.VARCHAR)` |
| `@Type(type = "corda-wrapper-binary")`                                  | `@JdbcTypeCode(SqlTypes.VARBINARY)` |
| `@Type(type = "corda-blob")`                                            | `@JdbcTypeCode(CordaSqlTypes.CORDA_BLOB)` |
| `@Type(type = "materialized_blob")`                                     | `@JdbcTypeCode(SqlTypes.BLOB)` |
| `session.save(x)`                                                       | `session.persist(x)` |
| `session.update(x)`, `session.saveOrUpdate(x)`                          | `session.merge(x)` |
| `session.delete(x)`                                                     | `session.remove(x)` |
| `javax.persistence.EntityManager` in `serviceHub.withEntityManager {}` | `jakarta.persistence.EntityManager` |

Declare Hibernate and the Jakarta Persistence API as `cordaProvided` (compile-only) dependencies, as you did for Hibernate 5. The node
provides them, and a CorDapp must not bundle them.

### Use the migration script

The script [migrate-cordapp-to-hibernate7.sh](https://github.com/corda/corda/blob/release/os/4.15/tools/scripts/migrate-cordapp-to-hibernate7.sh)
in the Corda repository applies the package, dependency, `uuid-char` and `corda-wrapper-binary` changes above to your source tree (Kotlin,
Java and Gradle files), and then lists everything else for you to change by hand: the other `@Type` names, the `Session` calls, HQL and
JPQL queries, `@OrderColumn`, and dependencies that bring in Hibernate 5.

```bash
migrate-cordapp-to-hibernate7.sh --dry-run path/to/your/cordapp   # show what would change
```

```bash
migrate-cordapp-to-hibernate7.sh path/to/your/cordapp             # apply, then review the report
```

It is safe to run twice. Always review the diff and run your tests.

The script changes the Hibernate dependencies that your build files declare, and lists the entries in your build files that are likely to
bring in Hibernate 5 through another dependency: Corda 4.14 or earlier, and Spring Data JPA. Gradle cannot put Hibernate 5 on the same
classpath as Corda 4.15. See [Gradle reports a capability conflict on `hibernate-core`](#gradle-reports-a-capability-conflict-on-hibernate-core).

### Changes you have to make by hand

**HQL and JPQL are validated strictly.** Hibernate 5 passed anything it did not recognise straight through to the database. Hibernate 7
rejects it with `SemanticException`.

```kotlin
// Before: tx_id is a column name. Rejected by Hibernate 7.
"from MyEntity where tx_id = :id"
// After: use the attribute name.
"from MyEntity where txId = :id"

// Before: compared an association to the id of the target entity. Rejected by Hibernate 7.
"... join Blob blob on checkpoint.blob = blob.id"
// After: compare the association to the entity.
"... join Blob blob on checkpoint.blob = blob"
```

**Custom Hibernate types.** `@Type(type = "...")`, `@TypeDef` and the `org.hibernate.type.*TypeDescriptor` classes no longer exist. Use
`@JdbcTypeCode`, `@JdbcType` and `@JavaType`, or a JPA `AttributeConverter`.

**Stricter mappings.** For example, `@OrderColumn` is only allowed on a `java.util.List`, not on a `Set`. An association to an entity that was
never persisted, for example a `@OneToOne` with `@PrimaryKeyJoinColumn`, is reported when the session is flushed. Persist the associated
entity as well.

**Result order.** A query with no `ORDER BY` has no defined order. Hibernate 7 renders some queries differently, for example an `IN` over a
composite key, so a database may now return rows in a different order. Add an explicit sort.

**Duplicate `persist`.** If the session already holds a different instance with the same id, `persist` fails immediately with
`EntityExistsException` and marks the transaction for rollback, so the transaction cannot be committed even if you catch the exception.
`EntityManager.persist` already behaved like this with Hibernate 5, so code that uses `withEntityManager` is unaffected. Code that used
Hibernate's `Session.save`, for example in a service through `AppServiceHub.database.transaction { session.save(...) }`, has to change to
`persist` and is affected: `save` threw `NonUniqueObjectException` and did not mark the transaction for rollback, so code that caught it and
carried on now fails when the transaction commits. Check for the existing entity first instead, for example with `session.find`.

**Constraint violations.** A duplicate-key violation that was reported as a `PersistenceException` wrapping a `ConstraintViolationException`
is now reported as the `ConstraintViolationException` itself, which is itself a `PersistenceException`. The same applies to Hibernate's other
JDBC exceptions, such as `SQLGrammarException` and `DataException`. Code that catches `PersistenceException` is unaffected. Code that tests
`e.cause is ConstraintViolationException` has to test the exception itself as well, for example by walking the cause chain.

**Native SQL result types.** A native query (`createNativeQuery`) returns a `BIGINT` column, or `count(*)`, as a `Long` where Hibernate 5
returned a `BigInteger`. Code that casts the result to `BigInteger` now fails with a `ClassCastException`. Use `(result as Number).toLong()`.
Date and time columns still come back as `java.sql.Timestamp`, `Date` and `Time`.

**`LIKE` patterns on H2, PostgreSQL and CockroachDB.** Hibernate 7 adds `escape ''` to a `LIKE` with no escape character on these databases, so
a backslash in a pattern is now an ordinary character. For example, the pattern `a\_b` used to match only the value `a_b`; it now matches
values such as `a\xb` and no longer matches `a_b`. Oracle and SQL Server never treated the backslash specially and are unchanged. If you
escape `_` or `%`, give the escape character explicitly, for example with the JPA criteria API's `like(path, pattern, '\\')`. Vault
`Builder.like` and `notLike` patterns behave in the same new way.

**Tables generated from your entities get `CHECK` constraints.** When Hibernate generates the DDL for a CorDapp table (the Database Management
Tool's `create-migration-sql-for-cordapp` sub-command, or `--allow-hibernate-to-manage-app-schema` in development), an enum column gets
`check (col between 0 and N)` (ordinal) or `check (col in (...))` (string), and on Oracle a boolean gets `check (col in (0,1))`. Ordinal enum
columns also get a narrower type (`tinyint`, `smallint`, `number(3,0)`). Tables that already exist are not changed. If you later add a
constant to the enum, inserting it fails with a check-constraint violation. Review generated scripts and remove the `CHECK` clauses you do not
want before you apply them.

**A `Character` in a `CHAR` column wider than one character.** Hibernate 5's own DDL made a `Character` (or `yes_no` / `true_false`) column
`CHAR(255)` on H2, and Hibernate 5 read the space-padded value it got back. Hibernate 7 rejects it with
`CoercionException: value contains more than one character`. This affects H2 schemas that Hibernate generated, for example on development
nodes and in scripts from the 4.14 migration exporter. A hand-written `CHAR(1)` column is fine. A rebuilt CorDapp should either change the
column to `CHAR(1)` or map the attribute through its own `AttributeConverter<Character, String>` that takes the first character of what it
reads (not one that trims it, which would turn a stored space into null), declared with `@JdbcTypeCode(SqlTypes.CHAR)`. The node does the
latter for a converted CorDapp.

**Arrays.** An `IntArray`, `LongArray`, `Array<String>` or similar attribute was stored as a serialised binary value with Hibernate 5.
Hibernate 7 maps it to the database's array type (or XML on SQL Server), so a table created before 4.15 fails validation with
`wrong column type ... expecting [... array ...]`. An `Array<Byte>` (`Byte[]`) or `Array<Char>` (`Character[]`) attribute, which Hibernate 5
stored as binary or character data, is refused when the node starts (`MappingException`). Use `ByteArray` or `String` instead, or an
`AttributeConverter` that stores the value as before.

**Smaller differences.**

* `NOT IN` an empty list now matches every row on every database. With Hibernate 5 it matched no rows on PostgreSQL and SQL Server, every row
  on H2, and failed on Oracle.
* On SQL Server, `avg` of an integer column is no longer truncated to an integer, so it now returns the same value as on the other databases.
* On SQL Server, an `IN` list of more than 2,100 numeric values fails with `The incoming request has too many parameters`, because Hibernate 7
  binds each value as a parameter where Hibernate 5 inlined numbers. Split such lists.
* `persist` and `merge` mark the transaction for rollback on any failure, not only a duplicate id, for example a `null` in a non-nullable
  property. Hibernate 5's `save` and `update` did not.

**`withEntityManager` receives a `jakarta.persistence.EntityManager`.** The block passed to `serviceHub.withEntityManager` receives a
`jakarta.persistence.EntityManager` in 4.15, so a CorDapp rebuilt for 4.15 has to bind to that type. The script renames the import. The API
checker records the method without its type parameter, so it shows no change. Run the tests of every flow that uses `withEntityManager` after
the rebuild.

#### Gradle reports a capability conflict on `hibernate-core`

Hibernate 5 was published as `org.hibernate:hibernate-core`, and Hibernate 6 and later as `org.hibernate.orm:hibernate-core`. Hibernate 7's
Gradle metadata says that it provides both, so that Gradle never puts two versions of Hibernate on one classpath. Corda 4.15 brings in
Hibernate 7 through `corda-core`. If anything else in the same configuration depends on Hibernate 5, Gradle refuses to resolve it:

```
> Could not resolve all files for configuration ':compileClasspath'.
   > Could not resolve org.hibernate.orm:hibernate-core:7.4.12.Final.
      > Module 'org.hibernate.orm:hibernate-core' has been rejected:
           Cannot select module with conflict on capability 'org.hibernate:hibernate-core:7.4.12.Final' also provided by [org.hibernate:hibernate-core:7.4.12.Final(compile)]
```

To find the dependency that brings in Hibernate 5, run `dependencyInsight` for the module and configuration that failed:

```bash
./gradlew <module>:dependencyInsight --dependency org.hibernate:hibernate-core --configuration compileClasspath
```

The usual causes are a module that still depends on a Corda 4.14 or earlier artifact (for example, a test CorDapp deliberately built against an
older Corda) in the same configuration as Corda 4.15, and a library that depends on Hibernate 5, such as Spring Data JPA in a Spring Boot 2 web
server that is in the same Gradle module as `corda-rpc`. Different versions of the *same* Corda artifact are not a problem, because Gradle picks
the newest one.

To fix it, in order of preference:

1. Upgrade or remove the dependency that brings in Hibernate 5.
2. If that dependency does not use Hibernate itself, exclude Hibernate 5 from it:

   ```groovy
   cordaProvided("net.corda:corda-core:4.11") {
       exclude group: 'org.hibernate', module: 'hibernate-core'
   }
   ```

3. To fix every path at once, replace the old coordinate with Hibernate 7 throughout the build:

   ```groovy
   configurations.configureEach {
       resolutionStrategy.dependencySubstitution {
           substitute module('org.hibernate:hibernate-core') using module('org.hibernate.orm:hibernate-core:7.4.12.Final') because 'Corda 4.15 uses Hibernate 7'
       }
   }
   ```

A capability rule with `selectHighestVersion()` does not help, because both candidates have the same version. Only exclude or replace
Hibernate 5 for code that does not use it. A library that calls Hibernate 5 is likely to fail at run time against Hibernate 7.

#### Recognising a failure caused by the `save` to `persist` change

Code that relied on catching a duplicate and carrying on in the same transaction fails in two steps:

1. The duplicate is reported where it happens:
   `jakarta.persistence.EntityExistsException: A different object with the same identifier value was already associated with this persistence context for entity [<entity class>#<id>]`,
   caused by `org.hibernate.NonUniqueObjectException` with the same message. With Corda 4.14 the same situation logged
   `org.hibernate.NonUniqueObjectException: A different object with the same identifier value was already associated with the session : [<entity class>#<id>]`.
2. If the code catches that exception and carries on, the transaction can no longer commit, and none of its changes are saved:
   `net.corda.nodeapi.internal.persistence.RolledBackDatabaseSessionException: Attempted to commit database transaction marked for rollback`.
   * **In a flow**, the commit happens at the flow's next checkpoint: its next suspension (`send`, `receive`, `sleep` or a subflow that
     suspends) or the end of the flow. The node log shows `Flow [<flow id>] admitted to hospital`, then
     `StateTransitionException: Attempted to commit database transaction marked for rollback`, then
     `Flow error discharged from hospital`. The flow is retried from its last checkpoint. If the duplicate happens every time, the flow is
     retried three times and then kept for overnight observation.
   * **Outside a flow**, for example in a service using `AppServiceHub.database.transaction { ... }`, the `transaction` call itself throws
     `RolledBackDatabaseSessionException`.

With Corda 4.14 the same code logged only the `NonUniqueObjectException`, and the rest of the transaction was committed. The fix is to check
for the existing entity before persisting it, or to use `merge` if updating it is what was meant, rather than catching the exception.

### Rebuilding, signing and versioning

The persistence annotations are part of your state classes' bytecode, so the CorDapp jar that contains them changes. Treat the result as a new
CorDapp version:

* Increase the CorDapp version number.
* Sign it with the **same key** as before. States using a signature constraint continue to verify.
* States using a **hash constraint** are pinned to the old jar and need the usual
  [constraint migration]({{< relref "cordapps/cordapp-constraint-migration.md" >}}) process.
* If you keep contracts and states in a jar separate from your flows, only the jar containing the schema classes needs to change.

See [Upgrading deployed CorDapps]({{< relref "node-operations-upgrade-cordapps.md" >}}) for how to roll the new version out.

### Testing

`MockNetwork`, `MockServices` and the driver run against H2 and let Hibernate create the tables of your own schemas, as before. Test your
CorDapp against every database you support. Hibernate's mapping of some Java types differs between databases, so run your integration tests
against PostgreSQL, SQL Server and Oracle if you can.

The conversion of `javax.persistence` classes only happens in the node's CorDapp class loader, which loads CorDapps from jars in the node's
`cordapps` directory. Classes that reach the node through its own classpath are loaded unchanged, and a node that finds such a class still
built against `javax.persistence` in a schema fails fast with a message that says so. That is the case for:

* `MockNetwork` and `MockServices`, and an **in-process** driver node (`startInProcess = true`): the CorDapp's classes are on the test's classpath.
* Your own CorDapp under test, supplied from its class directory (`cordappsForPackages`, or `TestCordapp.findCordapp` on a project's own
  classes), on any kind of node.

An **out-of-process** driver node (the default) does convert a CorDapp supplied as a jar, for example a third-party CorDapp built for 4.14
that your tests depend on: the driver removes jars that carry a CorDapp manifest from the node's classpath and the node loads them from its
`cordapps` directory, as a real node does. So, to test on 4.15, port your own CorDapp to `jakarta.persistence`, and run tests that need an
unported third-party jar on out-of-process driver nodes or a real node until its vendor ships a 4.15 build.

### A CorDapp you cannot rebuild

Nothing needs to be done: the node converts it as described in [Running CorDapps built for Corda 4.14 or earlier](#running-cordapps-built-for-corda-414-or-earlier).
Treat the conversion as a compatibility bridge for a CorDapp you cannot rebuild yet, not as a build target: on 4.15 it cannot use a Hibernate
annotation, `@Type` name, class or member that Hibernate 7 no longer has, and the Hibernate 7 behaviour changes above apply to it without the
rebuild that would have made them visible at compile time. If the node refuses it, ask the vendor for a 4.15 build.

## What stays the same in the database

Hibernate 6 and 7 changed several defaults. Corda sets the following properties so that the data formats used by existing databases and
CorDapps do not change, for the node database and for the standalone JPA notary. You do not need to set or change any of them.

| Behaviour that changed in Hibernate 6 and later                                          | How Corda keeps the Hibernate 5 behaviour |
|------------------------------------------------------------------------------------------|-------------------------------------------|
| `@GeneratedValue` uses a sequence per entity (`foo_SEQ`), incrementing by 50             | The single `hibernate_sequence`, with an increment of 1, is still used |
| `Instant` is stored as `TIMESTAMP WITH TIME ZONE` and read using the database session's time zone | Stored as a UTC `TIMESTAMP`, independent of the database server's time zone |
| `UUID` is stored in the database's native type (`uuid`, `uniqueidentifier`, `raw(16)`)   | `BINARY(16)`, or the native `uuid` on PostgreSQL, as in Hibernate 5 |
| Oracle `double` and `float` are `BINARY_DOUBLE` and `BINARY_FLOAT`                       | `FLOAT`, as in Hibernate 5 |
| From Oracle 23, `Boolean` is the native `boolean` type                                   | `NUMBER(1)` on every Oracle version, as in Hibernate 5 |
| `Duration` is stored as `NUMERIC(21)` or an interval                                     | A `BIGINT` number of nanoseconds, as in Hibernate 5 |
| `OffsetDateTime` and `ZonedDateTime` keep their offset                                   | A plain `TIMESTAMP`, normalised to UTC, as in Hibernate 5 |
| Native SQL queries return `java.time` types for date and time columns                    | `java.sql.Timestamp`, `Date` and `Time`, as in Hibernate 5 |
| A bulk HQL `update` of an `@Immutable` entity throws an exception                        | Allowed, with a warning, as in Hibernate 5 |
| `hbm2ddl=update` also alters existing columns                                            | Only missing tables and columns are created |

Corda's own `@Type` mappings are preserved: `uuid-char` is still stored as 36 characters, `corda-wrapper-binary` as `VARBINARY`,
`corda-blob` as a BLOB (`bytea` on PostgreSQL) and `materialized_blob` as a BLOB.

## Frequently asked questions

**Do I have to run any database scripts?** Not for the Hibernate 7 upgrade: it does not change the database. Corda 4.15 does add
migrations for other features, so the node's database still has to be migrated to 4.15 as described in
[Upgrading a node to Corda Enterprise Edition 4.15]({{< relref "node-upgrade-notes.md#step-3-update-the-database" >}}).

**Is a converted CorDapp still the same CorDapp?** Yes. The conversion happens in memory as classes are loaded. The jar, its hash and its
signature are unchanged, so contract constraints, attachments and the CorDapp's identity on the network are unaffected.

**Will my vault data still be readable?** Yes. The vault tables, and the formats of their columns, are unchanged.

**Does my CorDapp need Hibernate 7 on its classpath?** Only if it uses Hibernate classes directly, for example `@JdbcTypeCode`. The node provides
Hibernate. Declare it `cordaProvided` (compile-only) in your build, as you did for Hibernate 5.

**Can I build one CorDapp that runs on 4.14 and 4.15?** A CorDapp built for 4.14 (`javax.persistence`) runs on both: natively on 4.14 and
converted on 4.15, within the limits described above. A CorDapp built for 4.15 (`jakarta.persistence`) does not run on 4.14.
