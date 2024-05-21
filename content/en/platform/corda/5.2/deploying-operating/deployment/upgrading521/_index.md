---
description: "Learn how to upgrade your cluster from Corda 5.2 to Corda 5.2.1."
date: '2024-05-15'
title: "Upgrading from 5.2 to 5.2.1"
menu:
  corda52:
    parent: corda52-cluster-deploy
    identifier: corda52-cluster-upgrade521
    weight: 5000
---
# Upgrading from 5.2 to 5.2.1

This section describes how to upgrade a Corda cluster from version 5.2 to 5.2.1.

{{< note >}}
You cannot upgrade Corda 5.1 to 5.2.1. You must upgrade Corda to version 5.2 first. For information on how to do it, see [Upgrading from 5.1 to 5.2]({{< relref "../upgrading/_index.md" >}}).
{{< /note >}}

The examples provided in this section assume that you installed Corda 5.2 in a namespace called `corda`. This is different to other deployments.

To perform an upgrade, you must fulfill the required [prerequisites](#prerequisites) and go through the following steps:

1. [Back Up the Corda Database](#back-up-the-corda-database)
2. [Test the Migration](#test-the-migration)
3. [Migrate Data From Kafka Topics to the Cluster Database](#migrate-data-from-kafka-topics-to-the-cluster-database)
4. [Scale Down the Running Corda Worker Instances](#scale-down-the-running-corda-worker-instances)
5. [Migrate the Corda Cluster Database](#migrate-the-corda-cluster-database)
6. [Optional: Clear Down Key Rotation Stale Data](#optional-clear-down-key-rotation-stale-data)
7. [Update Kafka Topics](#update-kafka-topics)
8. [Launch the Corda 5.2.1 Workers](#launch-the-corda-521-workers)

For information about how to roll back an upgrade, see [Rolling Back]({{< relref "rolling-back521.md" >}}).

## Prerequisites

Corda 5 relies on certain underlying prerequisites, namely Kafka and PostgreSQL, administered by the Cluster Administrators.

{{< note >}}
This guide assumes that the Cluster Administrator assigned to upgrade Corda has full administrator access to these prerequisites.
{{< /note >}}

Developers, including customer CorDapp developers, or those trialing Corda, can use the R3-provided [Corda Helm chart]({{< relref "../deploying/_index.md#download-the-corda-helm-chart" >}}) which installs these prerequisites. The Corda Helm chart can also configure Corda, so it can reach these prerequisites, allowing a quick and convenient installation of Corda 5.

Customers in production are not expected to follow this path, and generally use managed services for these prerequisites. There are likely to be significant privilege restrictions in terms of who can administer these services. This guide cannot provide instructions on how to gain administrator access to customer-managed or self-hosted services.

### Downloads

Install PostgreSQL interface (`psql`) and Kubernetes command line tool (`kubectl`) on your local machine.

### Kafka Access

Some complications arise when trying to administer Kafka inside a Corda cluster from a host outside the cluster. Kafka connections are not created directly to the Kafka broker in the first instance, but via a bootstrap server which redirects requests to a broker based on its advertised listeners list. Advertised listeners are set up at Kafka deployment time and might not be accessible to the subnet of a host on a different subnet.

A simple port forward to Kafka is not sufficient as this only forwards traffic to the bootstrap server. The redirection from the bootstrap to a Kafka broker fails unless you are on the same subnet as the Kafka broker’s advertised listener name. Additionally, if SSL is enabled for your Kafka deployment, you cannot access it at a different host name from those covered by the certificate.

This guide cannot describe how to create a connection to any arbitrary Kafka deployment. It is up to the upgrader to ensure this is possible from their host.

You can test Kafka access using off-the-shelf Kafka tools. For example, if you can list Kafka topics using a command similar to this, you have the required access from your host:

```
kafka-topics --bootstrap-server=prereqs-kafka.test-namespace:9092 --list
```

### REST API Access

To get information about TLS certificate aliases, the data migration step requires access to the Corda REST API. This is required at the same stage when data is extracted from Kafka, which means access to Kafka and the Corda REST API must be available in the same environment at the same time. You must pass credentials and locations of both to the Corda CLI plugin when executed. You must have `GET` access to the `/key` and `/certificate` APIs.

### Corda CLI Tool and Corda 5 Plugins

Some upgrade steps use the {{< tooltip >}}Corda CLI{{< /tooltip >}} tool used also in Corda 5 [manual bootstrapping]({{< relref "../deploying/manual-bootstrapping.md" >}}). Users who entirely bootstrapped Corda 5 using the Corda Helm chart may not be familiar with this tool because the Corda Helm chart executes it for you. For instructions on how to install Corda CLI, go to [Installing the Corda CLI]({{< relref "../../../application-networks/tooling/installing-corda-cli.md" >}}).

{{< note >}}
The version of the Corda CLI tool and plugins must match the version of Corda 5 being upgraded to; that is, 5.2.1.
{{< /note >}}

The functionality of the tools, the database schemas and Kafka topics embedded in them pertain to the version of Corda they were built against.

## Back Up the Corda Database

You must create a backup of all schemas in your database:

* Cluster — name determined at bootstrap. For example, `CONFIG`.
* Crypto — name determined at bootstrap. For example, `CRYPTO`.
* RBAC — name determined at bootstrap. For example, `RBAC`.
* Virtual nodes schemas — multiple schemas per virtual node holding ID:
   * `vnode_crypto_<holding_id>`
   * `vnode_uniq_<holding_id>`
   * `vnode_vault_<holding_id>`

How these backups are performed, stored, and managed depends on their owner. It differs based on the database service supplier, and it is out of scope of this guide to detail that. Please refer to the database service provider’s documentation.

5.2.1 migration only makes changes in the cluster schema; backing up everything else is a precaution.

## Test the Migration

Follow the steps in [Scale Down the Running Corda Worker Instances]({{< relref "#scale-down-the-running-corda-worker-instances" >}}) on copies of your database backups to ensure the database migration stages are successful before proceeding with an upgrade of a production Corda.

This reveals any issues with migrating the data before incurring any downtime. It will also indicate the length of downtime required to perform a real upgrade, allowing you to schedule accordingly.

## Migrate Data From Kafka Topics to the Cluster Database

Disaster recovery additions require the migration of data previously only published to Kafka to the cluster database. Corda 5.2 deployments will already have published some of this data, so you must extract and copy it to the new database tables.

To extract this data from Kafka and generate SQL scripts to populate the new tables from it, you must call the Corda CLI tool with a specific 5.2.1 migration path plugin.

The Corda CLI tool needs access to the Kafka deployment, and the `/key` and `/certificate` part of the Corda REST API. For this reason, you must perform this step prior to scaling down Corda workers.

{{< note >}}
The Corda CLI tool migrates a snapshot of data at the point in time it is run. Performing administrative tasks on Corda after this stage of upgrade and before the next one results in potential data loss.
{{< /note >}}

For clusters that use the development prerequisites, Kafka login credentials and the SSL certificate can be obtained from the cluster's secret. If the cluster was deployed differently, it is assumed that the upgrader already knows these details. You can authenticate with Kafka by passing a standard Kafka properties file to the tool using the `-k` parameter. You can generate such a file in the following way:

```
KAFKA_PASSWORD=$(kubectl get secret -n corda prereqs-kafka -o go-template='{{ index .data "admin-password" | base64decode }}')
kubectl get secret -n corda prereqs-kafka -o go-template='{{ index .data "ca.crt" | base64decode }}' > ./kafka_config/ca.crt
cat > ./kafka_config/props.txt <<_EOF
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username=\"admin\" password=\"${KAFKA_PASSWORD}\";
ssl.truststore.location=/kafka_config/ca.crt
ssl.truststore.type=PEM
_EOF
```

To run the migration Corda CLI plugin, use the following command.

{{< note >}}
You must also provide REST API access here, including user name and password, and allow insecure connections. In this example, the REST API is port-mapped to the local machine. The provided credentials allow `GET` access to the `/key` APIs for each holding ID and to the `/certificate` APIs for `p2p-tls` and `p2p-session`.
{{< /note >}}

{{< tabs name="">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh upgrade migrate-data-5-2-1 -b <BOOTSTRAP-SERVERS> --kafka-config <CLIENT-PROPERTIES-FILE> -t <REST-URL> -u <USER> -p <PASSWORD>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd upgrade migrate-data-5-2-1 -b <BOOTSTRAP-SERVERS> --kafka-config <CLIENT-PROPERTIES-FILE> -t <REST-URL> -u <USER> -p <PASSWORD>
```
{{% /tab %}}
{{< /tabs >}}

Inspect the generated SQL files. You cannot apply them until database schema changes have been completed in step [Migrate the Corda Cluster Database]({{< relref "#migrate-the-corda-cluster-database" >}}). Keep these SQL files until then.

## Scale Down the Running Corda Worker Instances

{{< important >}}
After completing this step and until you finish the last step in these instructions, Corda 5.2 becomes unresponsive. To reduce Corda downtime, R3 recommends that you test the database migration and become fully familiar with the next set of steps before proceeding with this one.
{{< /important >}}

You can scale down the workers using any tool of your choice. For example, run the following commands if using `kubectl`:

```
kubectl scale --replicas=0 deployment/corda-crypto-worker -n corda
kubectl scale --replicas=0 deployment/corda-db-worker -n corda
kubectl scale --replicas=0 deployment/corda-flow-mapper-worker -n corda
kubectl scale --replicas=0 deployment/corda-flow-worker -n corda
kubectl scale --replicas=0 deployment/corda-membership-worker -n corda
kubectl scale --replicas=0 deployment/corda-p2p-gateway-worker -n corda
kubectl scale --replicas=0 deployment/corda-p2p-link-manager-worker -n corda
kubectl scale --replicas=0 deployment/corda-persistence-worker -n corda
kubectl scale --replicas=0 deployment/corda-rest-worker -n corda
kubectl scale --replicas=0 deployment/corda-token-selection-worker -n corda
kubectl scale --replicas=0 deployment/corda-uniqueness-worker -n corda
kubectl scale --replicas=0 deployment/corda-verification-worker -n corda
```

If you are scripting these commands, you can wait for the workers to be scaled down using something similar to the following:

```
while [ "$(kubectl get pods --field-selector=status.phase=Running -n corda | grep worker | wc -l | tr -d ' ')" != 0 ]
do
sleep 1
done
```

## Migrate the Corda Cluster Database

Migrating the database schema requires generating SQL scripts and applying them as separate steps.

To migrate the cluster database schemas, do the following:

1. Generate the required SQL scripts using the `spec` sub-command of the <a href = "../../reference/corda-cli/database.md"> Corda CLI `database` command</a>. For example:

   {{< tabs name="database">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh database spec -c -l ./sql_updates -g="" --jdbc-url=<DATABASE-URL> -u postgres
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd database spec -c -l ./sql_updates -g="" --jdbc-url=<DATABASE-URL> -u postgres
   ```
   {{% /tab %}}
   {{< /tabs >}}

   This example generates schemas into a directly called `sql_updates` but you can choose any output directory. The `database spec` command generates only cluster SQL as it is specified in the `-s="config"` parameter. The `-g="config:config"` instructs it to generate schema-aware SQL, so you do not need to apply the SQL to schemas explicitly in the next step.

2. Verify the generated SQL scripts and apply them to the PostgreSQL database. For example:

   ```shell
   psql -h localhost -p 5432 -f ./sql_updates/config.sql -d cordacluster -U postgres
   ```

3. Grant the necessary permissions. For example:

   ```shell
   psql -h localhost -c "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   psql -h localhost -c "GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA config TO corda" -p 5432 -d cordacluster -U postgres
   ```

   The `cluster` database user is the user set up by the Corda Helm chart when the configuration database was originally deployed.

4. Apply the SQL files generated in step [Migrate Data From Kafka Topics to the Cluster Database](#migrate-data-from-kafka-topics-to-the-cluster-database).

   {{< note >}}
   You must set the schema to the cluster configuration schema when using `psql`. By default, this is the configuration as used in this example. This is because the migration script is schema-agnostic.
   {{< /note >}}

   ```shell
   PGOPTIONS='-c search_path=config' psql -h localhost -p 5432 -f ./sql_updates/migrate_member_data.sql -d cordacluster -U postgres
   ```

## Optional: Clear Down Key Rotation Stale Data

Due to a fix in version 5.2.1, the transient flow status state has moved from the key rotation state manager schema to the flow state manager schema. As a result, the automatic cleanup of this data in the old key rotation status manager schema does not occur. Corda 5.2.1 cleans it only from the new location, potentially leaving stale data in the key rotation schema. To avoid unnecessary storage of stale data, R3 recommends that you delete all states from the key rotation state manager database.

The only functional consequence of deleting the key rotation state data is the loss of legacy key rotation status information. This does not affect the outcome of those key rotations but only affects any subsequent attempts to report their status. Using the key rotation API to check the status of past rotations will return a result as if they were never completed. Note that Corda only retains the most recent key rotation status for any tenant.

If you need legacy key rotation data, you can omit this step or perform it later. The upgrade process does not require it. If you choose to perform it later, ensure no key rotation operations are running at that time.

The name of the key rotation schema depends on the value `stateManager.keyRotation.partition` provided to the Corda Helm chart during bootstrapping. If not specified, it defaults to `sm_key_rotation`.

The following is an example `psql` used to delete the key rotation state, assuming the default schema name:

```
psql -h localhost -c "DELETE FROM sm_key_rotation.state" -p 5432 -d cordacluster -U postgres
```

## Update Kafka Topics

Corda 5.2.1 introduces new Kafka topic configurations, including changes to ACLs. While the Corda CLI tool can automatically apply these changes to a running Kafka deployment, customers may prefer not to manage Kafka indirectly through the Corda CLI. Instead, the Corda CLI tool provides parsable information about the required Kafka topic configurations, allowing users to manage their Kafka instances themselves. This section provides instructions for both alternatives.

### Self Managed Kafka Updates

There is no “SQL script” equivalent for Kafka for Corda Operators to review. Instead, the Corda CLI tool can generate a YAML file that describes how to set up the Kafka deployment.

The YAML file is self-explanatory and can be easily read by a human or imported into various third-party tools that automate Kafka topic changes. To generate the YAML file for importing into another tool or for manual administration, use the `preview` and `create` sub-commands of the Corda CLI `topic`command:

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

{{< note >}}
You do not need a connection to Kafka to perform this step. The YAML file represents the correct state for Kafka topics based on the platform version the tool was built against. It does not include information about the current state of any running Kafka instance. Any differences should be identified by the Kafka instance administrator or the automated tool that processes the YAML file.
{{< /note >}}

### Corda CLI Managed Kafka Updates

For clusters using the development prerequisites, you can obtain Kafka login credentials and the SSL certificate from the cluster secret. This is the same to what you did in section [Migrate Data From Kafka Topics to the Cluster Database](#migrate-data-from-kafka-topics-to-the-cluster-database), so if the file was already generated in that step, it can be reused here, allowing you to skip to running the plugin. If the cluster was deployed differently, it is assumed the upgrader already has this information. You can pass a standard Kafka properties file for authentication to the tool using the `-k` parameter. You can generate such a file as follows:

```
KAFKA_PASSWORD=$(kubectl get secret -n corda prereqs-kafka -o go-template='{{ index .data "admin-password" | base64decode }}')
kubectl get secret -n corda prereqs-kafka -o go-template='{{ index .data "ca.crt" | base64decode }}' > ./kafka_config/ca.crt
cat > ./kafka_config/props.txt <<_EOF
security.protocol=SASL_SSL
sasl.mechanism=PLAIN
sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required username=\"admin\" password=\"${KAFKA_PASSWORD}\";
ssl.truststore.location=/kafka_config/ca.crt
ssl.truststore.type=PEM
_EOF
```

To have the tool connect to the cluster and perform the necessary additions to ACLs, use the `preview` and `create` sub-commands of the Corda CLI `topic` command:

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

## Launch the Corda 5.2.1 Workers

If Corda 5.2 was deployed using Corda Helm chart, you can deploy Corda 5.2.1 the same way. This updates the deployments with the new image versions and scales them to the defined replica counts. Corda version is overridden at the command line and selecting the 5.2.1 Corda Helm chart defaults to the 5.2.1 worker images. If you provide your own values in a YAML file, ensure it does not refer to 5.2 images.

For more information, see the [Corda Helm chart]({{< relref "../deploying/_index.md#download-the-corda-helm-chart" >}}) instructions.
