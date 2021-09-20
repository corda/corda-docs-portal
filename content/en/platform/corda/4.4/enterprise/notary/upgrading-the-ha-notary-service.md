---
aliases:
- /releases/4.4/notary/upgrading-the-ha-notary-service.html
- /docs/corda-enterprise/head/notary/upgrading-the-ha-notary-service.html
- /docs/corda-enterprise/notary/upgrading-the-ha-notary-service.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-corda-nodes-notary-operate
tags:
- upgrading
- ha
- notary
- service
title: Upgrading the notary to a new version of Corda Enterprise
weight: 9
---


# Upgrading the notary to a new version of Corda Enterprise

## Version 4.4.6

{{< warning >}}
This release addresses a security issue in the JPA notary if the Corda database management tool was used during notary backing database setup. Corda implementations that do not use the Corda database management tool during notary setup are unaffected and no action is required. After applying the 4.4.6 patch, you must re-run the Corda Database Management Tool to apply the security fix.
{{< /warning >}}


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
