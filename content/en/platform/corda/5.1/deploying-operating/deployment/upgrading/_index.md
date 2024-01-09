---
description: "Learn how to upgrade your cluster from Corda 5.0 to Corda 5.1."
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

This section describes how to upgrade a Corda cluster from 5.0 to {{< version-num >}}. It lists the required [prerequisites](#prerequisites) and describes the following steps required to perform an upgrade:

1. [Back Up the Corda Database](#back-up-the-corda-database)
2. [Test the Migration](#test-the-migration)
3. [Scale Down the Running Corda Worker Instances](#scale-down-the-running-corda-worker-instances)
4. [Migrate the Corda Cluster Database](#migrate-the-corda-cluster-database)
5. [Update the Database Connection Configuration Table](#update-the-database-connection-configuration-table)
6. [Migrate the Virtual Node Databases](#migrate-the-virtual-node-databases)
7. [Update Kafka Topics](#update-kafka-topics)
8. [Launch the Corda {{< version-num >}} Workers](#launch-the-corda-workers)

For information about how to roll back an upgrade, see [Rolling Back]({{< relref "rolling-back.md" >}}).

Following a platform upgrade, Network Operators should upgrade their networks. For more information, see [Upgrading an Application Network]({{< relref "../../../application-networks/upgrading/_index.md" >}}).

## Prerequisites

This documentation assumes you have full administrator access to the {{< tooltip >}}Corda CLI{{< /tooltip >}} {{< version-num >}} and Kafka. You must ensure that you can create a connection to your Kafka deployment. You can check this by confirming you can list Kafka topics by running a command such as the following:

```shell
kafka-topics --bootstrap-server=prereqs-kafka.test-namespace:9092 --list
```

## Back Up the Corda Database

You must create a backup of all schemas in your database:

* Cluster — name determined at bootstrap. For example, `CONFIG`.
* Crypto — name determined at bootstrap. For example, `CRYPTO`.
* RBAC — name determined at bootstrap. For example, `RBAC`.
* Virtual Nodes schemas:
  * `vnode_crypto_<holding_id>`
  * `vnode_uniq_<holding_id>`
  * `vnode_vault_<holding_id>`

## Test the Migration

Follow the steps in [Migrate the Corda Cluster Database](#migrate-the-corda-cluster-database) and [Update the Database Connection Configuration Table](#update-the-database-connection-configuration-table) on copies of your database backups to ensure that the database migration stages are successful before proceeding with an upgrade of a production instance of Corda.

This reveals any issues with migrating the data before incurring any downtime. It will also indicate the length of downtime required to perform a real upgrade, allowing you to schedule accordingly.

For information about rolling back the Corda 5.0 to Corda {{< version-num >}} upgrade process, see [Rolling Back]({{< relref "rolling-back.md" >}}).

## Scale Down the Running Corda Worker Instances

{{< important >}}
Scaling down the Corda 5.0 workers results in Corda becoming unresponsive until you launch the Corda {{< version-num >}} workers. You must first test the database migration as described in [Test the Migration](#test-the-migration) and also ensure that you are familiar with the rest of the upgrade process to incur minimum Corda downtime.
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

## Migrate the Corda Cluster Database

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
   * Cluster database — configured by the Helm chart by the property `db.cluster.username.value`; `corda` in the example below.
   * RBAC database — configured by the Helm chart by the property `db.rbac.username.value`; `rbac_user` in the example below.
   * Crypto database — configured by the Helm chart from the property `db.crypto.username.value`; `crypto_user` in the example below.
   * State manager database — configured by the Helm chart from the property `db.cluster.username.value`; `corda` in the example below.

   For example:
   ```shell
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA rbac TO rbac_user" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA crypto TO crypto_user" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT USAGE ON SCHEMA state_manager TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA state_manager TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA state_manager TO corda" -p 5432 -d cordacluster -U postgres
   ```

## Update the Database Connection Configuration Table

Corda 5.0 only used one concurrent connection for each virtual node. As of 5.1, this is configurable in [corda.db]({{< relref "../../config/fields/db.md" >}}). As part of the upgrade process, you must remove the 5.0 setting to enable the new Corda {{< version-num >}} default of 10 maximum virtual node connections.

To remove the 5.0 setting, issue a SQL statement that removes `"pool":{"max_size":1}`, from the JSON config in each row in the cluster `db_connections` table. In the following example, `CONFIG` in `CONFIG.db_connection` is the name of the cluster schema, while `config` is a column name that you must specify in lowercase:
```shell
psql -h localhost -c "UPDATE CONFIG.db_connection SET config = REPLACE(config,'\"pool\":{\"max_size\":1},','')" -p 5432 -d cordacluster -U postgres
```

## Migrate the Virtual Node Databases

Migrating virtual node databases requires the short hash holding ID of each virtual node. For more information, see [Retrieving Virtual Nodes]({{< relref "../../vnodes/retrieving.md" >}}).

To migrate the virtual node databases, do the following:

1. Create a file containing the short hash holding IDs of the virtual nodes to migrate.

2. Generate the required SQL scripts using the `platform-migration` sub-command of the <a href = "../../reference/corda-cli/vnode.md"> Corda CLI `vnode` command</a>. For example, if you save the holding IDs in `/sql_updates/holdingIds`:

   {{< tabs name="">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh vnode platform-migration --jdbc-url=jdbc:postgresql://host.docker.internal:5432/cordacluster -u postgres -i /sql_updates/holdingIds -o /sql_updates/vnodes.sql
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd vnode platform-migration --jdbc-url=jdbc:postgresql://host.docker.internal:5432/cordacluster -u postgres -i /sql_updates/holdingIds -o /sql_updates/vnodes.sql
   ```
   {{% /tab %}}
   {{< /tabs >}}

3. Review the generated SQL and apply it as follows:
   ```
   psql -h localhost -p 5432 -f ./sql_updates/vnodes.sql -d cordacluster -U postgres
   ```

4. Grant the required permissions for the user for each virtual node for the three database schemas. Corda creates these users when it creates the schemas and so you must extract the credentials from the database using the previously created file of holding IDs. R3 recommends that you script this stage, as follows:
   ```sh
   while read HOLDING_ID; do
      # In Corda 5.0 all virtual node schemas and users are created by Corda, so we need to extract their names from the db
    
      # Grab the schema names for this holding Id
      VAULT_SCHEMA=$(psql -h localhost -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'vnode_vault%'" -p 5432 -d cordacluster -U postgres | tr -d ' ' | grep -i $HOLDING_ID | grep vault )
      CRYPTO_SCHEMA=$(psql -h localhost -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'vnode_crypto%'" -p 5432 -d cordacluster -U postgres | tr -d ' ' | grep -i $HOLDING_ID | grep crypto )
      UNIQ_SCHEMA=$(psql -h localhost -c "SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE 'vnode_uniq%'" -p 5432 -d cordacluster -U postgres | tr -d ' ' | grep -i $HOLDING_ID | grep uniq)

      # Get the vault users associated with this holding id
      VAULT_DDL_USER=$(psql -h localhost -c "select usename from pg_catalog.pg_user" -p 5432 -d cordacluster -U postgres | grep -i $HOLDING_ID | tr -d ' ' | grep vault | grep ddl)
      VAULT_DML_USER=$(psql -h localhost -c "select usename from pg_catalog.pg_user" -p 5432 -d cordacluster -U postgres | grep -i $HOLDING_ID | tr -d ' ' | grep vault | grep dml)

      # Get the crypto users associated with this holding id
      CRYPTO_DDL_USER=$(psql -h localhost -c "select usename from pg_catalog.pg_user" -p 5432 -d cordacluster -U postgres | grep -i $HOLDING_ID | tr -d ' ' | grep crypto | grep ddl)
      CRYPTO_DML_USER=$(psql -h localhost -c "select usename from pg_catalog.pg_user" -p 5432 -d cordacluster -U postgres | grep -i $HOLDING_ID | tr -d ' ' | grep crypto | grep dml)

      # Get the uniqueness users associated with this holding id
      UNIQ_DDL_USER=$(psql -h localhost -c "select usename from pg_catalog.pg_user" -p 5432 -d cordacluster -U postgres | grep -i $HOLDING_ID | tr -d ' ' | grep uniq | grep ddl)
      UNIQ_DML_USER=$(psql -h localhost -c "select usename from pg_catalog.pg_user" -p 5432 -d cordacluster -U postgres | grep -i $HOLDING_ID | tr -d ' ' | grep uniq | grep dml)

      # Update priviledges for any new tables in the crypto schema with the crypto users
      psql -h localhost -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA $CRYPTO_SCHEMA TO $CRYPTO_DDL_USER" -p 5432 -d cordacluster -U postgres
      psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA $CRYPTO_SCHEMA TO $CRYPTO_DML_USER" -p 5432 -d cordacluster -U postgres

      # Update priviledges for any new tables in the vault schema with the vault users
      psql -h localhost -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA $VAULT_SCHEMA TO $VAULT_DDL_USER" -p 5432 -d cordacluster -U postgres
      psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA $VAULT_SCHEMA TO $VAULT_DML_USER" -p 5432 -d cordacluster -U postgres

      # Update priviledges for any new tables in the uniqueness schema with the uniqueness users
      psql -h localhost -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA $UNIQ_SCHEMA TO $UNIQ_DDL_USER" -p 5432 -d cordacluster -U postgres
      psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA $UNIQ_SCHEMA TO $UNIQ_DML_USER" -p 5432 -d cordacluster -U postgres
   done <./sql_updates/holdingIds
   ```

## Update Kafka Topics

Corda {{< version-num >}} contains new Kafka topics and also revised Kafka ACLs. You can apply these changes in one of the following ways:

* [Automatically to a running Kafka deployment using the Corda CLI](#corda-cli-kafka-updates).
* [Manually by reviewing a preview of the required Kafka topic configuration](#manual-kafka-updates).

### Corda CLI Kafka Updates

Use the `connect` and `create` sub-commands of the Corda CLI `topic` command to connect to the Kafka broker and create any required topics. For example:

{{< tabs name="create-topics-example">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b=prereqs-kafka:9092 -k=/kafka_config/props.txt create connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b=prereqs-kafka:9092 -k=/kafka_config/props.txt create connect
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
The Corda CLI does not delete topics or ACLs. R3 recommends that you do not clean up any old topics or ACLs until the upgrade to Corda 5.1 is complete. While these old topics, remain you can still perform an [upgrade rollback]({{< relref "rolling-back.md" >}}).
{{< /note >}}

### Manual Kafka Updates

Alternatively, the `preview` and `create` sub-commands of the Corda CLI `topic` command can generate a preview of the required Kafka configuration in YAML. You can save, and if required modify, this content before using the Corda CLI to execute it, as follows:

1. Use the `preview` sub-command of the Corda CLI `create` sub-command to generate a preview of the configuration. For example:

   {{< tabs name="">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh topic create -u crypto=CRYPTO_USER -u db=DB_USER -u flow=FLOW_USER -u membership=MEMBERSHIP_USER \
   -u p2pGateway=P2P_GATEWAY_USER -u p2pLinkManager=P2P_LINK_MANAGER_USER -u rest=REST_USER \
   -u uniqueness=UNIQUENESS_WORKER -u flowMapper=FLOW_MAPPER_USER -u persistence=PERSISTENCE_USER \
   -u verification=VERIFICATION_WORKER preview
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd topic create -u crypto=CRYPTO_USER -u db=DB_USER -u flow=FLOW_USER -u membership=MEMBERSHIP_USER `
   -u p2pGateway=P2P_GATEWAY_USER -u p2pLinkManager=P2P_LINK_MANAGER_USER -u rest=REST_USER `
   -u uniqueness=UNIQUENESS_WORKER -u flowMapper=FLOW_MAPPER_USER -u persistence=PERSISTENCE_USER `
   -u verification=VERIFICATION_WORKER preview
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. Review the output and make any necessary changes.

   The YAML generated by the Corda CLI represents the required state of Kafka topics for Corda {{< version-num >}}. The Corda CLI does not connect to any running Kafka instance and so the Kafka instance administrator must use the preview to decide the required changes for your cluster.
   {{< note >}}
   R3 recommends that you do not delete old topics or ACLs until the upgrade to Corda {{< version-num >}} is complete. While these old topics, remain you can still perform an [upgrade rollback]({{< relref "rolling-back.md" >}}).
  {{< /note >}}

## Launch the Corda {{< version-num >}} Workers

To complete the upgrade to {{< version-num >}} and launch the Corda {{< version-num >}} workers, upgrade the Helm chart:

```shell
helm upgrade corda -n corda oci://corda-os-docker.software.r3.com/helm-charts/release/os/{{<version-num>}}/corda --version {{<version-num>}}.0 -f values.yaml
```
For more information about the values in the deployment YAML file, see [Configure the Deployment]({{< relref "../../deployment/deploying/_index.md#configure-the-deployment" >}}).
