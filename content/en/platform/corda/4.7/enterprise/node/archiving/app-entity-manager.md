---
date: '2020-04-24T12:00:00Z'
menu:
  corda-enterprise-4-7:
    parent: corda-enterprise-4-7-corda-nodes-archive-service
tags:
- archive
- backup schema
- archive install
- archive transactions
- app entity manager
- off-ledger database
- off-ledger db

title: App Entity Manager
weight: 500
---

# App Entity Manager

The `AppEntityManager` library can be used by CorDapps to access off-ledger databases using JPA APIs.

You can initialise the service using a JPA persistence XML or through configuration properties. The properties can be set explicitly in a call to `ServiceHub.initAppEntityManager` or implicitly by using a CorDapp conf file in the `cordapps/config` directory.

The service can be used by multiple CorDapps concurrently, with the library maintaining a map of Corda application context to JPA entity manager factories.

If no JPA configuration is supplied then the Database Service will revert to the standard `ServiceHub.withEntityManager` API calls.

## Entity example

Let `Student` be an entity class:

 ```aidl
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

* Provide a JPA persistence XML file and persistence unit name.
* Provide JPA properties in a map.
* Record JPA properties in the CorDapp's configuration file.

## Using a persistence XML file

The library will search for a persistence XML file in the `META-INF` directory named after the CorDapp's short name in lower case appended with `-persistence.xml`. For example, if the CorDapp was called 'Archive Tool' then the default persistence XML file will be 'archive-tool-persistence.xml'.

```aidl
?xml version="1.0" encoding="UTF-8"?>
<persistence version="2.1"
             xmlns="http://xmlns.jcp.org/xml/ns/persistence"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence
    http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
    <persistence-unit name="app-entity-manager">
        <class>com.entity.Student</class>
        <properties>
            <property name="javax.persistence.jdbc.driver" value="org.h2.Driver" />
            <property name="javax.persistence.jdbc.url" value="jdbc:h2:mem:test" />
            <property name="javax.persistence.jdbc.user" value="sa" />
            <property name="javax.persistence.jdbc.password" value="" />
            <property name="hibernate.hbm2ddl.auto" value="update" />
            <property name="hibernate.c3p0.min_size" value="5" />
            <property name="hibernate.c3p0.max_size" value="20" />
            <property name="hibernate.c3p0.timeout" value="300" />
            <property name="hibernate.c3p0.max_statements" value="50" />
            <property name="hibernate.c3p0.idle_test_period" value="120" />
        </properties>
    </persistence-unit>
</persistence>
```

The default persistence unit name is `app-entity-manager`. This can be changed using the `persistence.unit.name` property.

An alternative persistence XML file name can be given by using the `persistence.xml` property.`

The persistence entity factory is initialised on the first call to the manager.

```aidl
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

## Using CorDapp configuration

A CorDapp can initialise an entity manager factory by using the following properties in the CorDapp conf file in the `cordapps/config` directory:

* `persistence.unit.name` - persistence unit name within the persistence XML, default 'app-entity-manager'.
* `persistence.xml` - path to a persistence xml, defaults to the built-in file.
* `hibernate.show_sql` - default false.
* `hibernate.format_sql` - default false.
* `hibernate.hbm2ddl.auto` - default update.
* `hibernate.ejb.loaded.classes` - comma separated list of entity classes, default empty.
* `javax.persistence.jdbc.driver` - no default.
* `javax.persistence.jdbc.url` - no default.
* `javax.persistence.jdbc.user` - no default.
* `javax.persistence.jdbc.password` - no default.

The CorDapp configuration should contain the following properties.

```aidl
javax.persistence.jdbc.driver="org.h2.Driver"
javax.persistence.jdbc.url="jdbc:h2:mem:test2"
javax.persistence.jdbc.user="sa"
javax.persistence.jdbc.password=""
hibernate.ejb.loaded.classes="com.entity.Student"
```

The persistence entity factory will be initialised on the first call to the manager.

```aidl
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

The AppEntityManager can also be initialised within a flow by giving a JPA configuration and entity classes to the library `initAppEntityManager` method.

```aidl
import com.r3.libs.appentitymanager.AppEntityManager.PERSISTENCE_JDBC_DRIVER
import com.r3.libs.appentitymanager.AppEntityManager.PERSISTENCE_JDBC_PASSWORD
import com.r3.libs.appentitymanager.AppEntityManager.PERSISTENCE_JDBC_URL
import com.r3.libs.appentitymanager.AppEntityManager.PERSISTENCE_JDBC_USER

@Suspendable
override fun call(): Boolean {
    val properties = mapOf<Any, Any>(
        PERSISTENCE_JDBC_DRIVER to "org.h2.Driver",
        PERSISTENCE_JDBC_URL to "jdbc:h2:mem:hub",
        PERSISTENCE_JDBC_USER to "sa",
        PERSISTENCE_JDBC_PASSWORD to ""
    )

    serviceHub.initAppEntityManager(properties, listOf(Student::class.java))

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

## Missing configuration

If neither a persistence XML file nor a JDBC URL is set in the configuration
properties then the standard `ServiceHub` entity manager will be used.

## ServiceHub extension functions

The following extension functions have been added to ServiceHub.

```aidl
fun ServiceHub.initAppEntityManager(properties: Map<Any, Any>, entities: List<Class<*>>)

fun <T : Any?> ServiceHub.withAppEntityManager(block: EntityManager.() -> T): T

fun ServiceHub.withAppEntityManager(block: Consumer<EntityManager>)
```

## Built-in persistence XML file

The built-in persistence XML file is given below. This file is used if none is provided.

```aidl
<?xml version="1.0" encoding="UTF-8"?>
<persistence version="2.1"
             xmlns="http://xmlns.jcp.org/xml/ns/persistence"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence
    http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">

    <persistence-unit name="app-entity-manager">
        <properties>
            <property name="hibernate.c3p0.min_size" value="5" />
            <property name="hibernate.c3p0.max_size" value="20" />
            <property name="hibernate.c3p0.timeout" value="300" />
            <property name="hibernate.c3p0.max_statements" value="50" />
            <property name="hibernate.c3p0.idle_test_period" value="120" />
        </properties>
    </persistence-unit>
</persistence>
```

## CorDapp configuration file
JPA configuration properties can be recorded in the CorDapp's
configuration file in the `cordapps/config` directory. The configuration file
must have the same name as the CorDapp's jar file but with the suffix `conf`.

## Development H2 default database
Since the default node H2 database cannot be shared it is not possible to use this
service to create an alternative schema on the default vault H2 database.
