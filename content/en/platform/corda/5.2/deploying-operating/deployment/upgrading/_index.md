---
description: "Learn how to upgrade your cluster from Corda 5.1 to Corda 5.2."
date: '2023-11-02'
title: "Upgrading from 5.1"
menu:
  corda52:
    parent: corda52-cluster-deploy
    identifier: corda52-cluster-upgrade
    weight: 4000
---
# Upgrading from 5.1

This section describes how to upgrade a Corda cluster from 5.1 to {{< version-num >}}. It lists the required [prerequisites](#prerequisites) and describes the following steps required to perform an upgrade:

1. [Back Up the Corda Database](#back-up-the-corda-database)
1. [Test the Migration](#test-the-migration)
1. [Scale Down the Running Corda Worker Instances](#scale-down-the-running-corda-worker-instances)
1. [Migrate the Corda Cluster Database](#migrate-the-corda-cluster-database)
1. [Migrate State Manager Databases](#migrate-state-manager-databases)
1. [Managing 5.2 Multi-Database Support](#managing-52-multi-database-support)
1. [Setting Search Paths](#setting-search-paths)
1. [Migrate the Virtual Node Databases](#migrate-the-virtual-node-databases)
1. [Update Kafka Topics](#update-kafka-topics)
1. [Launch the Corda {{< version-num >}} Workers](#launch-the-corda-workers)

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

Follow the steps in [Migrate the Corda Cluster Database](#migrate-the-corda-cluster-database) and [Migrate State Manager Databases](#migrate-state-manager-databases) on copies of your database backups to ensure that the database migration stages are successful before proceeding with an upgrade of a production instance of Corda.

This reveals any issues with migrating the data before incurring any downtime. It will also indicate the length of downtime required to perform a real upgrade, allowing you to schedule accordingly.

For information about rolling back the Corda 5.0 to Corda {{< version-num >}} upgrade process, see [Rolling Back]({{< relref "rolling-back.md" >}}).

## Scale Down the Running Corda Worker Instances

{{< important >}}
Scaling down the Corda 5.1 workers results in Corda becoming unresponsive until you launch the Corda {{< version-num >}} workers. You must first test the database migration as described in [Test the Migration](#test-the-migration) and also ensure that you are familiar with the rest of the upgrade process to incur minimum Corda downtime.
{{< /important >}}

You can scale down the workers using any tool of your choice. For example, the run the following commands if using `kubectl`:

```shell
kubectl scale --replicas=0 deployment/corda-crypto-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-db-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-flow-mapper-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-flow-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-membership-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-p2p-gateway-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-p2p-link-manager-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-persistence-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-rest-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-token-selection-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-uniqueness-worker -n <corda_namespace>
kubectl scale --replicas=0 deployment/corda-verification-worker -n <corda_namespace>
```

If you are scripting these commands, you can wait for the workers to be scaled down using something similar to the following:
```shell
while [ "$(kubectl get pods --field-selector=status.phase=Running -n <corda_namespace> | grep worker | wc -l | tr -d ' ')" != 0 ]
do
  sleep 1
done
```

## Migrate the Corda Cluster Database

To migrate the cluster database schemas, do the following:

1. Generate the required SQL scripts using the `spec` sub-command of the <a href = "../../reference/corda-cli/database.md"> Corda CLI `database` command</a>. For example:

   {{< tabs name="database">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh database spec -c -l /sql_updates -g="" --jdbc-url=<DATABASE-URL> -u postgres
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd database spec -c -l /sql_updates -g="" --jdbc-url=<DATABASE-URL> -u postgres
   ```
   {{% /tab %}}
   {{< /tabs >}}
   This example generates the schemas into a directory named `sql_updates` but you can choose any output directory. The `database spec` command generates all but state manager SQL by default. This example does not specify any overrides so the default schema names are used. `-g=""` generates schema-aware SQL.

2. Verify the generated SQL scripts and apply them to the Postgres database. For example:

   ```shell
   psql -h localhost -p 5432 -f ./sql_updates/config.sql -d cordacluster -U postgres
   psql -h localhost -p 5432 -f ./sql_updates/crypto.sql -d cordacluster -U postgres
   psql -h localhost -p 5432 -f ./sql_updates/rbac.sql -d cordacluster -U postgres
   ```

3. Grant the necessary permissions:
   * `cluster` user - set up by the Helm chart, in Corda 5.1 from the property `db.cluster.username.value`. `corda` in this example. In Corda 5.2 this property does not exist and is set elsewhere in the config. More information about this is provided later in this document.****
   * `rbac` user - set up by the Helm chart from the property `db.rbac.username.value`. `rbac_user` in this example.
   * `crypto` user - set up by the Helm chart from the property `db.crypto.username.value`. `crypto_user` this example.

   For example:
   ```shell
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA rbac TO rbac_user" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA crypto TO crypto_user" -p 5432 -d cordacluster -U postgres
   ```

## Migrate State Manager Databases

To migrate the state manager database schemas, do the following:

1. Generate the required SQL scripts using the `spec` sub-command of the <a href = "../../reference/corda-cli/database.md"> Corda CLI `database` command</a>. For example:

   {{< tabs name="state-manager">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh database spec -c -l /sql_updates -s="statemanager" -g="statemanager:state_manager" --jdbc-url=<DATABASE-URL> -u postgres
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd database spec -c -l /sql_updates -s="statemanager" -g="statemanager:state_manager" --jdbc-url=<DATABASE-URL> -u postgres
   ```
   {{% /tab %}}
   {{< /tabs >}}
   The name `state_manager` is always used for the state manager schema in every 5.1 deployment.

2. Verify the generated SQL scripts and apply them to the Postgres database. For example:

   ```shell
   psql -h localhost -p 5432 -f ./sql_updates/statemanager.sql -d cordacluster -U postgres
   ```

3. Grant the necessary permissions. The database role username for the state manager in Corda 5.2 is the property specified by `workers.<worker_type>.stateManager.db.username` in the helm chart. However, if you set a value, Corda uses the `db.cluster.username.value` value is used. This is the same behavior as Corda 5.1.

   For example:
   ```shell
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -p 5432 -f ./sql_updates/statemanager.sql -d cordacluster -U postgres
   ```   

## Managing 5.2 Multi-Database Support

Corda 5.2 introduced support for multiple state manager databases, based on type of state. Corda 5.1 supported only one state manager database where all states were stored. There is no migration path that splits existing states between new databases and Corda deployments that were running 5.1 must continue to use a single database for all states.

However, to keep cluster and state manager database configuration aligned, cluster database configuration was modified slightly.
As a result, as part of the migration to 5.2, you must add new values in the YAML provided to the Helm chart. The 5.1 YAML schema also contains values that are no longer compatible and must be removed. To update your Helm chart YAML, do the following:

1. Remove the following sections, including the top-level label:

   ```yaml
   db: <-- remove including this line
   ...
   ```

   ```yaml
   bootstrap:
      db:
         cluster: <-- remove including this line
      ...
   ```

1. Add the following sections, updating the examples with the equivalent values from the Corda 5.1 deployment being upgraded:

   ```yaml
   databases:
    - id: "default"
      name: "cordacluster"
      port: 5432
      type: "postgresql"
      host: "prereqs-postgres"
    - id: "state-manager"
      name: "cordacluster"
      port: 5432
      type: "postgresql"
      host: "prereqs-postgres"
   ```

   ```
   bootstrap:
   ...
   db:
      databases: <-- this is new, it references the db in the snippet above
       - id: "default"
         username:
         value: "postgres"
   ```

1. Add the following lines to map the multi-database support back to the 5.1 mono-database. 5.1 used a fixed schema name of `state_manager` for the state manager database which is hardcoded below in the partition field.

   ```
   stateManager:
   flowCheckpoint:
      type: Database
      storageId: "state-manager" <-- this references the db in snippet above
      partition: "state_manager"
   flowMapping:
      type: Database
      storageId: "state-manager"
      partition: "state_manager"
   flowStatus:
      type: Database
      storageId: "state-manager"
      partition: "state_manager"
   keyRotation:
      type: Database
      storageId: "state-manager"
      partition: "state_manager"
   p2pSession:
      type: Database
      storageId: "state-manager"
      partition: "state_manager"
   tokenPoolCache:
      type: Database
      storageId: "state-manager"
      partition: "state_manager"
   ```

1. Configure each worker with individual user access to the state manager database. Corda only reads this from a secret, so you must create that secret with the 5.1 username in it, as the field `corda-username`. For example:

   ```shell
   kubectl create secret generic -n corda prereqs-postgres-user --from-literal=corda-username=corda
   ```

1. Add the accompanying YAML additions that pull the username out of the secret, which existed in 5.1:

   ```
   workers:
      crypto:
         config:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
         stateManager:
            keyRotation:
               username:
                  valueFrom:
                     secretKeyRef:
                        name: "prereqs-postgres-user"
                        key: "corda-username"
               password:
                  valueFrom:
                     secretKeyRef:
                        name: "prereqs-postgres"
                        key: "corda-password"
      db:
         config:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
      persistence:
         config:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
      tokenSelection:
         config:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
      stateManager:
         tokenPoolCache:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
   uniqueness:
      config:
         username:
            valueFrom:
               secretKeyRef:
                  name: "prereqs-postgres-user"
                  key: "corda-username"
         password:
            valueFrom:
               secretKeyRef:
                  name: "prereqs-postgres"
                  key: "corda-password"
   flow:
      stateManager:
         flowCheckpoint:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
         password:
            valueFrom:
               secretKeyRef:
                  name: "prereqs-postgres"
                  key: "corda-password"
   flowMapper:
      stateManager:
         flowMapping:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
   p2pLinkManager:
      stateManager:
         p2pSession:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
   rest:
      stateManager:
         keyRotation:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
         flowStatus:
            username:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres-user"
                     key: "corda-username"
            password:
               valueFrom:
                  secretKeyRef:
                     name: "prereqs-postgres"
                     key: "corda-password"
   ```

## Setting Search Paths

In Corda 5.1, schema names were injected everywhere as part of JDBC URLs. As of Corda 5.2, to support databases behind proxies, `search_path` was removed from JDBC URLs. As a result, as part of the migration process, you must set the `search_path` of the cluster database at SQL level. For example:

```shell
psql -h localhost -c "ALTER ROLE "corda" SET search_path TO config, state_manager" -p 5432 -d cordacluster -U postgres
psql -h localhost -c "ALTER ROLE "rbac_user" SET search_path TO rbac" -p 5432 -d cordacluster -U postgres
psql -h localhost -c "ALTER ROLE "crypto_user" SET search_path TO crypto" -p 5432 -d cordacluster -U postgres
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

   ```shell
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
helm upgrade corda -n <corda_namespace> oci://corda-os-docker.software.r3.com/helm-charts/release/os/{{<version-num>}}/corda --version {{<version-num>}}.0 -f values.yaml
```
For more information about the values in the deployment YAML file, see [Configure the Deployment]({{< relref "../../deployment/deploying/_index.md#configure-the-deployment" >}}).
