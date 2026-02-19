---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-14:
    identifier: corda-enterprise-4-14-notary-migration-overview
    parent: corda-enterprise-4-14-corda-nodes-notary-operate
tags:
- notary
- db
- migration
title: Migrating notary databases
weight: 3
---


# Migrating notary databases

With the MySQL notary being deprecated, Corda Enterprise notary operators should consider moving to a database supported by the JPA notary
instead.


## When to migrate

Migrating from one notary implementation to another is a complex procedure and should not be attempted unless there is
significant benefit from the migration. Possible reasons for migration include:

* Higher performance is required than a simple notary solution, but the user wishes to use their existing database.
* A highly available solution is required and the current database is not highly available.
* Greater scalability or performance is required than a highly available MySQL notary installation.

{{< note >}}
Simple notary refers to running the notary using the built-in database connection of the Corda node. This notary
implementation can connect to any database supported by Corda, however, the JPA notary implementation is more
performant. Note that the simple notary and JPA notary use different database schemas and thus data migration is
still required if switching between the two.

{{< /note >}}

{{< warning >}}
Any data lost during the migration process could lead to a loss of ledger integrity.

{{< /warning >}}


The recommended migration path would be to migrate the data stored in the source database to the target database. The data
would then be restored to a new database and the notary’s configuration changed to reflect the new database. Thus, the identity of
the notary would not change and transactions would still target it. However, the notary will have to be shutdown for a short
period of time during the migration.


## Considerations


* The JPA notary uses a different database schema to the Simple or MySQL notaries, and thus a transformation must be applied.
* The notary must be shut down during the final phase of migration.
* Depending on the number of states notarized by the notary, the amount of time taken to transfer the data could be significant.


## Schema differences: simple notary to JPA notary


{{< table >}}

|Table|Source Column(s)|Target Column(s)|Expression|
|--------------------------|-----------------------------|-------------------|------------------------------------------|
|notary_committed_states|transaction_id
output_index|state_ref|state_ref = transaction_id + ‘:’ +
output_index|

{{< /table >}}


## Schema differences: MySQL notary to JPA notary


{{< table >}}

|Table|Source Column(s)|Target Column(s)|Expression|
|--------------------------|-----------------------------|-------------------|------------------------------------------|
|notary_committed_states|issue_transaction_id
issue_transaction_output_id|state_ref|state_ref = issue_transaction_id + ‘:’ +
issue_transaction_output_id|
|notary_request_log|request_date|request_timestamp|request_timestamp = request_date|

{{< /table >}}


## Migration procedure


1. Use the [Corda database management tool]({{< relref "../node/operating/node-database.md#database-management-tool" >}}) to prepare the schema in the target database.
2. Obtain the latest backup of the source database.
3. Extract the data from the source database, transform it and load the data into the target database.
4. Loading this older copy of the data from the source database into the target database reduces the time taken for the final step.
5. Shutdown the notary, and when the notarisation request queue is drained, disconnect the source database to prevent any new data being written to it.
6. Perform a diff backup in order to retrieve the data that has been written to the database since the backup restored in Step 3.
7. Use the same transformation in order to load the diff backup into the target database.
8. Verify that the target database contains all of the data present in the source database.
9. Reconfigure the notary to use the JPA notary connected to the target database.
10. Restart the notary.
11. Verify that the notary operates normally.

