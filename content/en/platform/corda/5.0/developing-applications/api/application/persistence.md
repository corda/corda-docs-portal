---
date: '2023-02-10'
version: 'Corda 5.0'
title: "net.corda.v5.application.persistence"
menu:
  corda5:
    identifier: corda5-api-app-persistence
    parent: corda5-api-application
    weight: 6000
section_menu: corda5
---
# net.corda.v5.application.persistence
The `persistence` package provides services for performing persistence operations; mainly reading and writing data to and from the database. The `PersistenceService` is the main service for providing this functionality.

Corda 5 supports CRUD (Create, Read, Update, Delete) operations for user-defined types. This is achieved using JPA-annotated entities and, to manage database migrations, Liquibase.

## Defining Custom Tables Using Liquibase Migrations

[CorDapps](../../../introduction/key-concepts.html#cordapps) store data in a relational database.
When Corda creates a [virtual node](../../../introduction/key-concepts.html#virtual-nodes) for a CorDapp (as part of a [CPI](../../../introduction/key-concepts.html#corda-package-installer-cpi)), it requires associated tables, indexes, foreign-keys, and so on.
To create these, you must embed Liquibase files into the CorDapp [CPK](../../../introduction/key-concepts.html#corda-packages-cpks).

Liquibase manages database changes in a “Change Log” which references one or more change sets.
You must specify the top-level `databaseChangeLog` in a resource file in the CPK called `migration/db.changelog-master.xml`.
This file can reference one or more files including `changeSet`.

You should organise these change sets with future changes in mind.
For example, we recommend a single `include` per version of the table.
Once a `changeSet` is deployed, it cannot be changed and any change must be provided as a `changeSet` with a new `id`.
We suggest adding a version in the `id`; for example, `<table-name>-v1`.

Example of `src/resources/migration/db.changelog-master.xml`:
```xml
<?xml version="1.1" encoding="UTF-8" standalone="no"?>
<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.3.xsd">
    <include file="migration/dogs-migration-v1.0.xml"/>
</databaseChangeLog>
```
The referenced `include` file should also be a resource file in `src/resources/migration` and define the table itself. For example, `src/resources/migration/dogs-migration-v1.0.xml`:
```xml
<?xml version="1.1" encoding="UTF-8" standalone="no"?>
<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog http://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-4.3.xsd">

    <changeSet author="R3.Corda" id="dogs-migrations-v1.0">
        <createTable tableName="dog">
            <column name="id" type="uuid">
                <constraints nullable="false"/>
            </column>
            <column name="name" type="VARCHAR(255)"/>
            <column name="birthdate" type="DATETIME"/>
            <column name="owner" type="VARCHAR(255)"/>
        </createTable>
        <addPrimaryKey columnNames="id" constraintName="dog_id" tableName="dog"/>
    </changeSet>
</databaseChangeLog>
```
{{< note >}}
The `include` file reference is resolved relative to the resources path in the CPK and not relative to the current directory.
{{< /note >}}

## Running the Migrations

To run the migrations:
1. Upload the CPI.
2. Create a virtual node using the [Corda 5 REST API](../../../operating/operating-tutorials/rest-api.html).

  The migrations run when the virtual node is created and logging shows the migrations executing.
  If you have direct database access, you should see the tables being created.
  If you are using Postgres, make sure to look under the correct schema, since each virtual node creates a new schema, unless an external VNode database was provided during VNode creation.

## Mapping Your New Tables to JPA Entities

CorDapps should use JPA annotated POJOs for data access objects.
Each class requires `@CordaSerializable` and `@Entity` annotations.
The following is an example that also defines some named JPQL queries:

```kotlin
@CordaSerializable
@Entity(name = "dog")
@NamedQueries(
    NamedQuery(name = "Dog.summon", query = "SELECT d FROM Dog d WHERE d.name = :name"),    
    NamedQuery(name = "Dog.independent", query = "SELECT d FROM Dog d WHERE d.owner IS NULL"),    
    NamedQuery(name = "Dog.summonLike", query = "SELECT d FROM Dog d WHERE d.name LIKE :name ORDER BY d.name"),    
    NamedQuery(name = "Dog.all", query = "SELECT d FROM Dog d ORDER BY d.name"),    
    NamedQuery(name = "Dog.release", query = "UPDATE Dog SET owner=null")
)
class Dog(
    @Id    
    @Column(name = "id", nullable = false)    
    val id: UUID,    
    @Column(name = "name")    
    val name: String,    
    @Column(name = "birthdate")    
    val birthdate: Instant,
    @Column(name = "owner")
    val owner: String?
) {
    constructor() : this(id = UUID.randomUUID(), name = "", birthdate = Instant.now(), owner = "")

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false

        other as Dog

        if (id != other.id) return false
        if (name != other.name) return false
        if (birthdate != other.birthdate) return false
        if (owner != other.owner) return false

        return true
    }

    override fun hashCode(): Int {
        var result = id.hashCode()
        result = 31 * result + name.hashCode()
        result = 31 * result + birthdate.hashCode()
        result = 31 * result + owner.hashCode()
        return result
    }
}
```

{{< note >}}
This example specifies the table and column names.
If they are not specified, JPA uses defaults.
{{< /note >}}


## Using the Persistence API From a CorDapp Flow

To use the Persistence API from a flow:

1. Define a reference to the persistence service. This should be supplied via the Corda dependency injection system:
   ```kotlin
   import net.corda.v5.application.flows.CordaInject
   import net.corda.v5.application.flows.ClientStartableFlow
   import net.corda.v5.application.persistence.PersistenceService

   class MyExampleFlow : ClientStartableFlow {
       @CordaInject
       lateinit var persistenceService: PersistenceService

       // your code goes here
   ```

2. To create a `Dog` entity that writes a row to the database, use the following code:
   ```kotlin
     val dog = Dog(dogId, "dog", Instant.now(), "none")
     persistenceService.persist(dog)
    ```   

   {{< note >}}
  All persistence operations are processed over the message bus.
   {{< /note >}}

3. To load a row from the database by ID, use the following code:
   ```kotlin
     val dog = persistenceService.find(Dog::class.java, dogId)
     return if (dog == null) {
         "no dog found"
     } else {
         "found dog id='${dog.id}' name='${dog.name}"
     }
   ```

     Alternatively, to load all entities and create `Dog` instances for every record in the `Dog` table in the database, use the following code:
     ```kotlin
     val dogs = persistenceService.findAll(Dog::class.java).execute()
     ```

4. To update a record, use the merge operation. For example, to change the name of a `Dog` and set the owner to null:
   ```kotlin
   val newDogName = input.getValue("name")
   persistenceService.merge(Dog(dogId, newDogName, Instant.now(), "none"))
   ```
   All of the operations available are defined in the public interface: <a href="../../../../../../api-ref/corda/5.0/net/corda/v5/application/persistence/PersistenceService.html" target="_blank">`PersistenceService`</a>.


{{< note >}}
Currently, inputs and outputs to `PersistenceService` must fit in a ~1MB (972,800 bytes) Kafka message. This size limit will be removed in future versions.
{{< /note >}}
