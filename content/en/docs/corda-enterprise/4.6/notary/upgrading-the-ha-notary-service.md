---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-notary-operate
tags:
- upgrading
- ha
- notary
- service
title: Upgrading the notary to a new version of Corda Enterprise
weight: 9
---


# Upgrading the notary to a new version of Corda Enterprise

## Version 4.6

No additional steps are needed to upgrade from version 4.5 to 4.6.

{{% note %}}
In 4.6, when starting a new driver using the driver DSL, the notary node will start by default as a thread in the same JVM process that runs the driver regardless to the `startNodesInProcess` driver properties (and not as a new process if the `startNodesInProcess` is `false`). This setting can be overridden. Please note that if the test interacts with the notary and expects the notary to run as a new process, you must set `startInProcess` to `false`.
{{% /note %}}

## Version 4.5

We've introduced the `notary_double_spends` table and added an index to the `notary_request_log` table. The `notary_double_spend` table contains information about attempted double-spend transactions.

Upgrade steps:

1. Back up your DB cluster.
2. Test to ensure that you can restore from backup.
3. Add the new table and indexes to a database in your cluster. It will be replicated to all other databases in the cluster. If you experience problems when the notary worker is restarted, perform a rolling upgrade on the notary worker nodes as detailed in the [node upgrade guide](../node-upgrade-notes.md).

### JPA notary using a CockroachDB database

To upgrade a CockroachDB database, run the following command:

```
create index on notary_request_log (consuming_transaction_id)

create table notary_double_spends (
    state_ref varchar(73) not null,
    request_timestamp timestamp not null,
    consuming_transaction_id varchar(64) not null,
    constraint id4 primary key (state_ref, consuming_transaction_id),
    index (state_ref, request_timestamp, consuming_transaction_id)
    );
```

### JPA notary using an Oracle RAC database

To upgrade an Oracle RAC database, run the following commands:

1. Create the new notary table using the following command:

    ```
    create table corda_adm.notary_double_spends (
      state_ref varchar(73) not null,
      request_timestamp timestamp not null,
      consuming_transaction_id varchar(64) not null,
      constraint id4 primary key (state_ref)
      );
    ```

2. Once the table has been created, add indexes using the following commands:

    ```sql
    create index tx_idx on corda_adm.notary_request_log(consuming_transaction_id)

    create index state_ts_tx_idx on corda_adm.notary_double_spends (state_ref,request_timestamp,consuming_transaction_id)
    ```

3. Lastly, grant access rights to the table:

    ```sql
    GRANT SELECT, INSERT ON corda_adm.notary_double_spends TO corda_pdb_user;
    ```

## Version 4.4

The `notary_request_log` table was extended to include the X500 name of the worker node that processed the request.

Upgrade steps:

* Backup your DB Cluster.
* Test you can restore from backup.
* Log in to any database server of your cluster and add the new column to the `notary_request_log` table, see SQL statements below. It will be replicated to all other database servers.
* In the unlikely event that the database gets corrupted, take all the notary worker nodes down and restore the database.
* Perform a rolling upgrade on the notary worker nodes. Follow the [node upgrade guide](../node-upgrade-notes.md) for each node, and make sure the node is running and is no longer in flow draining mode before moving on to the next one.


### JPA Notary

#### CockroachDB

```sql
ALTER TABLE notary_request_log ADD COLUMN worker_node_x500_name VARCHAR(255);
```

#### Oracle RAC

```sql
ALTER TABLE notary_request_log ADD worker_node_x500_name VARCHAR(255);
```

### Percona XtraDB


```sql
ALTER TABLE notary_request_log ADD COLUMN worker_node_x500_name TEXT;
```

## Version 4.2

Since Corda Enterprise 4.2 the MySQL JDBC driver now needs to be installed manually for every worker node, otherwise nodes will fail to start.
See [notary installation page](installing-the-notary-service.md#mysql-driver) for more information.


## Version 4.0

In Corda Enterprise 4.0 an additional table `notary_committed_transactions` is being used by the HA notary to support the new reference state functionality.

{{< note >}}
In order to enable reference state usage, the minimum platform version of the whole network has to be updated to version 4, which means
both the client nodes and the notary service have to be upgraded to version 4.

{{< /note >}}
Upgrade steps:


* Backup your Percona XtraDB Cluster.
* Test you can restore from backup.
* Log in to any Percona XtraDB Cluster database server and create the `notary_committed_transactions` table. It will be replicated to all other database servers.>
```sql
CREATE TABLE IF NOT EXISTS notary_committed_transactions (
    transaction_id BINARY(32) NOT NULL,
    CONSTRAINT tid PRIMARY KEY (transaction_id)
);
```




* In the unlikely event that the database gets corrupted, take all the notary worker nodes down and restore the database.
* Perform a rolling upgrade on the notary worker nodes. Follow the [node upgrade guide](../node-upgrade-notes.md) for each node, and make sure the node is running and is no longer in flow draining mode before moving on to the next one.
