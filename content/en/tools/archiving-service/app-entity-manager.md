---
date: '2026-06-03T12:00:00Z'
menu:
  tools:
    parent: tools-archiving
tags:
- archive
- backup schema
- archive install
- archive transactions
- app entity manager
- off-ledger database
- off-ledger db

title: App Entity Manager
weight: 720
---

# App Entity Manager

The `AppEntityManager` library can be used by CorDapps to access off-ledger databases using JPA APIs.

You can configure the service by recording JPA properties in a CorDapp conf file in the `cordapps/config` directory, or programmatically by using the `AppEntityServiceHub` class.

The service can be used by multiple CorDapps concurrently, with the library maintaining a map of Corda application context to JPA entity manager factories.

If no JPA configuration is supplied then the service reverts to the standard `ServiceHub.withEntityManager` API calls.

## Entity example

Let `Student` be an entity class:

 ```kotlin
package com.entity

import javax.persistence.*

@Entity
@Table(name = "student")
class Student {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    var id = 0
...
}
```

## Methods for initialising an entity manager factory

A CorDapp can initialise an entity manager factory using the following methods:

* Record JPA properties in the CorDapp's configuration file.
* Provide JPA properties programmatically through `AppEntityServiceHub`.

## Using CorDapp configuration

A CorDapp can initialise an entity manager factory by using the following properties in the CorDapp conf file in the `cordapps/config` directory:

* `hibernate.show_sql` - default false.
* `hibernate.format_sql` - default false.
* `hibernate.hbm2ddl.auto` - default update.
* `hibernate.dialect` - database dialect, no default.
* `hibernate.ejb.loaded.classes` - comma separated list of entity classes, default empty.
* `javax.persistence.jdbc.driver` - no default.
* `javax.persistence.jdbc.url` - no default.
* `javax.persistence.jdbc.user` - no default.
* `javax.persistence.jdbc.password` - no default.

The CorDapp configuration should contain the following properties.

```text
javax.persistence.jdbc.driver="org.h2.Driver"
javax.persistence.jdbc.url="jdbc:h2:mem:test2"
javax.persistence.jdbc.user="sa"
javax.persistence.jdbc.password=""
hibernate.ejb.loaded.classes="com.entity.Student"
```

The persistence entity factory will be initialised on the first call to the manager.

```kotlin
@Suspendable
override fun call(): Boolean {
    val student = Student("John", "Doe", "john.doe@rrr.com")

    // Execute an insert
    serviceHub.withAppEntityManager(){
        this.persist(student)
    }

    // Execute a query
    val result = serviceHub.withAppEntityManager(){
        this.createQuery(
            "SELECT email FROM Student st WHERE st.firstName LIKE :name")
            .setParameter("name", "John")
            .setMaxResults(10)
            .resultList
    }
...
}
```

## Using programmatic configuration

An entity manager factory can also be created programmatically by constructing an `AppEntityServiceHub` with a name, the JPA properties, and the entity classes. This can also be used outside of the context of a running Corda node.

```kotlin
import com.r3.libs.appentitymanager.AppEntityManager.PERSISTENCE_JDBC_DRIVER
import com.r3.libs.appentitymanager.AppEntityManager.PERSISTENCE_JDBC_PASSWORD
import com.r3.libs.appentitymanager.AppEntityManager.PERSISTENCE_JDBC_URL
import com.r3.libs.appentitymanager.AppEntityManager.PERSISTENCE_JDBC_USER
import com.r3.libs.appentitymanager.AppEntityServiceHub

val properties = mapOf<String, String>(
    PERSISTENCE_JDBC_DRIVER to "org.h2.Driver",
    PERSISTENCE_JDBC_URL to "jdbc:h2:mem:hub",
    PERSISTENCE_JDBC_USER to "sa",
    PERSISTENCE_JDBC_PASSWORD to ""
)

val appEntityServiceHub = AppEntityServiceHub("student-db", properties, listOf(Student::class.java))

val student = Student("John", "Doe", "john.doe@rrr.com")

// Execute an insert
appEntityServiceHub.withEntityManager {
    this.persist(student)
}

// Execute a query
val result = appEntityServiceHub.withEntityManager {
    this.createQuery(
        "SELECT email FROM Student st WHERE st.firstName LIKE :name")
        .setParameter("name", "John")
        .setMaxResults(10)
        .resultList
}

// Close the entity manager factory when it is no longer needed
appEntityServiceHub.closeEntityManager()
```

`AppEntityServiceHub` also provides a constructor that accepts a Typesafe `Config` object instead of a map.

## Missing configuration

If the `javax.persistence.jdbc.driver` and `javax.persistence.jdbc.url` properties are not set in the configuration then the standard `ServiceHub` entity manager will be used.

## ServiceHub extension functions

The following extension functions have been added to ServiceHub.

```kotlin
fun <T : Any?> ServiceHub.withAppEntityManager(block: EntityManager.() -> T): T

fun ServiceHub.withAppEntityManager(block: Consumer<EntityManager>)

fun ServiceHub.closeAppEntityManager()
```

## CorDapp configuration file
JPA configuration properties can be recorded in the CorDapp's
configuration file in the `cordapps/config` directory. The configuration file
must have the same name as the CorDapp's jar file but with the suffix `conf`.

## Development H2 default database
Since the default node H2 database cannot be shared it is not possible to use this
service to create an alternative schema on the default vault H2 database.
