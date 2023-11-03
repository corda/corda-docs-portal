---
date: '2023-11-02'
version: 'Corda 5.1'
title: "Upgrading from 5.0"
menu:
  corda51:
    parent: corda51-cluster-deploy
    identifier: corda51-cluster-upgrade
    weight: 4000
section_menu: corda51
---
# Upgrading from 5.0

This section describes how to

## Prerequisites

This documentation assumes you have full administrator access to {{< tooltip >}}Corda CLI{{< /tooltip >}} {{< version-num >}} and Kafka. You must ensure that you can create a connection to your Kafka deployment. You can check this by confirming you can list Kafka topics by running a command similar to the following:

```shell
kafka-topics --bootstrap-server=prereqs-kafka.test-namespace:9092 --list
```

## 1. Back Up the Corda Database

You must create a backup of all schemas in your database:

* Cluster — name determined at bootstrap. For example, `CONFIG`.
* Crypto — name determined at bootstrap. For example, `CRYPTO`.
* RBAC — name determined at bootstrap. For example, `RBAC`.
* Virtual Nodes schemas:
  * `vnode_crypto_<holding_id>`
  * `vnode_uniq_<holding_id>`
  * `vnode_vault_<holding_id>`

## 2. Test the Migration

Follow the steps in [Migrate the Corda Cluster Database](#4-migrate-the-corda-cluster-database) and []() *** on copies of your database backups to ensure the database migration stages go smoothly before proceeding with an upgrade of a production Corda.

This reveal any issues with migrating the data before incurring any downtime. It will also indicate of the length of downtime required to perform a real upgrade, allowing you to scheduled accordingly.

## 3. Scale Down the Running Corda Worker Instances

{{< important >}}
Scaling down the Corda 5.0 workers results in Corda becoming unresponsive until you launch the Corda {{< version-num >}} workers. You must first test the database migration as described in [Test the Migration](#2-test-the-migration) and also ensure that you are familiar with the next set of steps to incur minimum Corda downtime.
{{< /important >}}

You can scale down the workers using any tool of your choice. For example, the run the following commands if using `kubectl`:

```shell
kubectl scale --replicas=0 deployment/corda-crypto-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-db-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-flow-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-membership-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-p2p-gateway-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-p2p-link-manager-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-rest-worker -n <corda_namespace>
```

If you are scripting these commands, you can wait for the workers to be scaled down using something similar to the following:
```shell
while [ "$(kubectl get pods --field-selector=status.phase=Running -n corda | grep worker | wc -l | tr -d ' ')" != 0 ]
do
  sleep 1
done
```

## 4. Migrate the Corda Cluster Database

To migrate the database schemas, do the following:

1. Generate the required SQL scripts using the `spec` sub-command of the <a href = "../../reference/corda-cli/database.md"> Corda CLI `database` command</a>. For example:

   {{< tabs name="database">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh database spec -c -l /sql_updates -s="config,rbac,crypto,statemanager" \
   -g="config:config,rbac:rbac,crypto:crypto,statemanager:state_manager" --jdbc-url=<DATABASE-URL> -u postgres
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd database spec -c -l /sql_updates -s="config,rbac,crypto,statemanager" `
   -g="config:config,rbac:rbac,crypto:crypto,statemanager:state_manager" --jdbc-url=<DATABASE-URL> -u postgres
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. Verify the generated SQL scripts and apply them to the Postgres database. For example:

   ```shell
   psql -h localhost -p 5432 -f ./sql_updates/config.sql -d cordacluster -U postgres
   psql -h localhost -p 5432 -f ./sql_updates/crypto.sql -d cordacluster -U postgres
   psql -h localhost -p 5432 -f ./sql_updates/rbac.sql -d cordacluster -U postgres
   psql -h localhost -p 5432 -f ./sql_updates/statemanager.sql -d cordacluster -U postgres
   ```

3. Grant the necessary permissions to the following new database tables:
   * Cluster database user — configured by the Helm chart by the property `db.cluster.username.value`. This is `corda` in the example below.
   * RBAC database user — configured by the Helm chart by the property `db.rbac.username.value`. This is `rbac_user` in the example below.
   * Crypto database user — configured by the Helm chart from the property `db.crypto.username.value`. This is `crypto_user` in the example below.

   For example:
   ```shell
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA rbac TO rbac_user" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA crypto TO crypto_user" -p 5432 -d cordacluster -U postgres
   ```
