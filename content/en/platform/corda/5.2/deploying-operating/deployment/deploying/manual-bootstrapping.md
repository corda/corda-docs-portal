---
description: "Learn how to disable automatic setup processes and manually configure Kafka, databases, and RBAC roles."
date: '2023-05-16'
title: "Manual Bootstrapping"
menu:
  corda52:
    parent: corda52-cluster-deploying
    identifier: corda52-cluster-bootstrapping
    weight: 2000
---
# Manual Bootstrapping

By default, the Corda installation process automatically performs various setup actions in {{< tooltip >}}Kafka{{< /tooltip >}}, the database, and for [Corda RBAC]({{< relref "../../config-users/_index.md">}}).
If you require additional control, you can disable these automatic setup processes and an administrator can manually perform the actions with the assistance of the [Corda CLI]({{< relref "../../tooling/installing-corda-cli.md" >}}).

This section describes how to configure the following:

* [Kafka]({{< relref "#kafka" >}})
* [Database]({{< relref "#database" >}})
* [RBAC Roles]({{< relref "#rbac-roles" >}})

When you have completed the manual configuration of the above, you can [Deploy Corda]({{< relref "./_index.md#deploying" >}}).

## Kafka

By default, a Corda installation automatically creates the Kafka topics it requires.
The following sections describe how to create the topics manually:

* [Disabling Automatic Creation](#disabling-automatic-creation)
* [Creating the Topics](#creating-the-topics)
* [Creating ACL Entries](#creating-acl-entries)

### Disabling Automatic Creation

To disable the automatic creation of topics, do the following:

1. Set the following override in the deployment configuration:

   ```yaml
   bootstrap:
     kafka:
       enabled: false
   ```

2. Create a [Kafka client properties](https://kafka.apache.org/documentation/#configuration) file.
The following is an example properties file for a Kafka cluster using {{< tooltip >}}TLS{{< /tooltip >}} and SASL authentication:

   ```properties
   security.protocol=SASL_SSL
   sasl.mechanism=SCRAM-SHA-256
   sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="<USERNAME>" password="<PASSWORD>" ;
   ssl.truststore.location=ca.crt
   ssl.truststore.type=PEM
   ```

   The examples that follow assume that this file is named `config.properties`.

### Creating the Topics

Use the {{< tooltip >}}Corda CLI{{< /tooltip >}} to assist in the creation of the topics prior to Corda installation in one of two ways:

* [Create the Default Topics](#create-the-default-topics)
* [Modify the Topic Configuration Before Creating](#modify-the-topic-configuration-before-creating)

For information about the Corda CLI `topic` command's arguments, see the [Corda CLI reference]({{< relref"../../../reference/corda-cli/topic.md">}}).

#### Create the Default Topics

Use the `connect` sub-command of the Corda CLI `create` sub-command to connect to the Kafka broker and create any required topics:

{{< tabs name="create-topics">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k <CLIENT-PROPERTIES-FILE> create -r <REPLICAS> -p <PARTITIONS> connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k <CLIENT-PROPERTIES-FILE> create -r <REPLICAS> -p <PARTITIONS> connect
```
{{% /tab %}}
{{< /tabs >}}

For example:

{{< tabs name="create-topics-example">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b kafka-1.example.com -k config.properties create -r 3 -p 10 connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b kafka-1.example.com -k config.properties create -r 3 -p 10 connect
```
{{% /tab %}}
{{< /tabs >}}

#### Modify the Topic Configuration Before Creating

Alternatively, the Corda CLI can generate a preview of the required Kafka topic configuration in YAML. You can save, and if required modify, this content before using the Corda CLI to execute it, as follows:

1. Use the `preview` sub-command of the Corda CLI `create` sub-command to generate a preview of the configuration:

   {{< tabs name="">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k <CLIENT-PROPERTIES-FILE> create -r <REPLICAS> -p <PARTITIONS> preview
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k <CLIENT-PROPERTIES-FILE> create -r <REPLICAS> -p <PARTITIONS> preview
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For example:

   {{< tabs name="">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh topic -b kafka-1.example.com -k config.properties create -p 1 -r 1 -u preview
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd topic -b kafka-1.example.com -k config.properties create -p 1 -r 1 -u preview
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. Review the output, make any necessary changes, and save the configuration to a file.

3. Use the `connect` sub-command with the `-f` argument to connect to the Kafka broker and execute the configuration:

   {{< tabs name="create-topics">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k <CLIENT-PROPERTIES-FILE> create -r <REPLICAS> -p <PARTITIONS> connect -f <YAML-TOPIC-FILE>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k <CLIENT-PROPERTIES-FILE> create -r <REPLICAS> -p <PARTITIONS> connect -f <YAML-TOPIC-FILE>
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For example:

   {{< tabs name="create-topics-example">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh topic -b kafka-1.example.com -k config.properties create -r 3 -p 10 connect -f topics.yaml
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd topic -b kafka-1.example.com -k config.properties create -r 3 -p 10 connect -f topics.yaml
   ```
   {{% /tab %}}
   {{< /tabs >}}

### Creating ACL Entries

If you are authenticating Kafka users, the Corda CLI can also create Access Control List (ACL) entries as appropriate for each Corda {{< tooltip >}}worker{{< /tooltip >}}.
Specify a set of name-value pairs giving the Kafka username that will be used for each Corda worker:

{{< tabs name="acl">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
create -r <REPLICAS> -p <PARTITIONS> \
-u crypto=<CRYPTO_USER> -u db=<DB_USER> -u flow=<FLOW_USER>  -u flowMapper=<FLOWMAPPER_USER> -u membership=<MEMBERSHIP_USER> \
-u p2pGateway=<P2P_GATEWAY_USER> -u p2pLinkManager=<P2P_LINK_MANAGER_USER> -u rest=<REST_USER> \
connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k config.properties `
create -r <REPLICAS> -p <PARTITIONS> `
-u crypto=<CRYPTO_USER> -u db=<DB_USER> -u flow=<FLOW_USER> -u flowMapper=<FLOWMAPPER_USER> -u membership=<MEMBERSHIP_USER> `
-u p2pGateway=<P2P_GATEWAY_USER> -u p2pLinkManager=<P2P_LINK_MANAGER_USER> -u rest=<REST_USER>
connect
```
{{% /tab %}}
{{< /tabs >}}

## Database

By default, a Corda installation automatically creates and populates the database schema it requires.

{{< note >}}
If you are deploying Corda Enterprise with HashiCorp Vault, you must disable automatic bootstrapping and manually configure the database, as described in this section.
{{< /note >}}

To create the schema manually, set the following override in the deployment configuration to disable the automatic creation:

```yaml
bootstrap:
  db:
    enabled: false
```

Create and populate the database schema, as follows:

1. [Create the database tables](#create-the-database-tables).
2. [Populate the RBAC database connection configuration](#populate-the-rbac-database-connection-configuration).
3. [Populate the crypto database connection configuration](#populate-the-crypto-database-connection-configuration).
4. [Populate the virtual nodes database connection configuration](#populate-the-virtual-nodes-database-connection-configuration).
5. [Populate the REST admin user](#populate-the-rest-admin-user).
6. [Create the RBAC and crypto users](#create-the-rbac-and-crypto-users).
7. [Populate the crypto configuration](#populate-the-crypto-configuration).

{{< note >}}

* If you are applying SQL to a schema using the `psql` command, you can specify which schema to apply it to using the `--dbname` parameter: `--dbname "dbname=cordacluster options=--search_path=<SCHEMA-NAME>"`.
* If you are targeting schemas, database and crypto-generated SQL should be applied to the `CONFIG` schema, and `create-user-config` generated SQL should be applied to the `RBAC` schema. If you do not specify the schema, the installation process creates the tables in the default schema, and you must update the next steps in this procedure to reflect this.
{{< /note >}}

### Create the Database Tables

1. Use the Corda CLI to generate DML files for creating the database tables to use for each of the crypto, config, and rbac components.

   The following command specifies that the `CONFIG`, `RBAC`, and `CRYPTO` schema should be used for the corresponding components and generates the files in the directory `/tmp/db`:

   {{< tabs name="DML">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh database spec -g config:CONFIG,rbac:RBAC,crypto:CRYPTO -c -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd database spec -g config:CONFIG,rbac:RBAC,crypto:CRYPTO -c -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For information about the Corda CLI `database` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/database.md">}}).

2. Review the DML files generated and then execute against the database.

3. For each state type and schema (see [State Manager Databases]({{< relref "./_index.md#state-manager-databases">}})), generate the DML file for creating the state manager database table. The following command specifies that the `STATE_MANAGER` schema should be used for the state manager and generates the file in the `/tmp/statemanager` directory:

   {{< tabs name="DML-state-manager">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh database spec -s "statemanager" -g "statemanager:state_manager" -c -l /tmp/state-manager
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd database spec -s "statemanager" -g "statemanager:state_manager" -c -l /tmp/state-manager
   ```
   {{% /tab %}}
   {{< /tabs >}}

4. Review the DML file generated and execute it against each of the State Manager databases.

### Populate the RBAC Database Connection Configuration

Depending on your installation, follow the steps in one of the following sections to generate DDL for populating the RBAC database connection configuration:

* [RBAC Database Connection Configuration for Corda](#rbac-database-connection-configuration-for-corda)
* [RBAC Database Connection Configuration for Corda Enterprise with HashiCorp Vault](#rbac-database-connection-configuration-for-corda-enterprise-with-hashicorp-vault) {{< enterprise-icon >}}

#### RBAC Database Connection Configuration for Corda

1. Execute the following Corda CLI command to generate DDL for populating the {{< tooltip >}}RBAC{{< /tooltip >}} database connection configuration:

   {{< tabs name="RBAC">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> \
     --name corda-rbac --jdbc-url 'jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=RBAC' \
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> \
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> `
     --name corda-rbac --jdbc-url jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=RBAC `
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> `
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   The `<SALT>` and `<PASSPHRASE>` are used to encrypt the credentials in the database. These must match the values specified in the [Corda deployment configuration]({{< relref "./_index.md#encryption" >}}).

   For example:

   {{< tabs name="RBAC-example">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u rbacuser -p rc9VLHU3 \
     --name corda-rbac --jdbc-url 'jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=RBAC' \
     --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 \
     --validation-timeout 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u rbacuser -p rc9VLHU3 `
      --name corda-rbac --jdbc-url jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=RBAC `
      --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 `
      --validation-timeout 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For information about the Corda CLI `create-db-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-db-config" >}}).

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `CONFIG` schema.

#### RBAC Database Connection Configuration for Corda Enterprise with HashiCorp Vault {{< enterprise-icon >}}

1. Execute the following Corda CLI command to generate DDL for populating the RBAC database connection configuration:

   {{< tabs name="RBAC-ent">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <RBAC-USERNAME> \
      --name corda-rbac --jdbc-url 'jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=RBAC' \
      --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> \
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> -t VAULT --vault-path <path-to-corda-created-secrets> --key rbac -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <RBAC-USERNAME> `
     --name corda-rbac --jdbc-url jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=RBAC `
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> `
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> -t VAULT --vault-path <path-to-corda-created-secrets> --key rbac -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   The Vault parameters are used to retrieve encrypted values from the external secrets service. These must match the values specified in the [Corda deployment configuration]({{< relref "./_index.md#encryption" >}}).

   For example:

   {{< tabs name="RBAC-example-ent">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u rbacuser \
      --name corda-rbac --jdbc-url 'jdbc:postgresql://prereqs-postgres:5432/cordacluster?currentSchema=RBAC' \
      --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 \
     --validation-timeout 5 -t VAULT --vault-path dbsecrets --key rbac -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u rbacuser `
     --name corda-rbac --jdbc-url jdbc:postgresql://prereqs-postgres:5432/cordacluster?currentSchema=RBAC `
     --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 `
     --validation-timeout 5 -t VAULT --vault-path dbsecrets --key rbac -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For information about the Corda CLI `create-db-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-db-config" >}}).

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `CONFIG` schema.

### Populate the Crypto Database Connection Configuration

Depending on your installation, follow the steps in one of the following sections to generate DDL for populating the CRYPTO database connection configuration:

* [Crypto Database Connection Configuration for Corda](#crypto-database-connection-configuration-for-corda)
* [Crypto Database Connection Configuration for Corda Enterprise with HashiCorp Vault](#crypto-database-connection-configuration-for-corda-enterprise-with-hashicorp-vault) {{< enterprise-icon >}}

#### Crypto Database Connection Configuration for Corda

1. Execute the following Corda CLI command to generate DDL for populating the Crypto database connection configuration:

   {{< tabs name="DDL-crypto">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <CRYPTO-USERNAME> -p <CRYPTO-PASSWORD> \
     --name corda-crypto --jdbc-url `jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=CRYPTO` \
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> \
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <CRYPTO-USERNAME> -p <CRYPTO-PASSWORD> `
     --name corda-crypto --jdbc-url jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=CRYPTO `
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> `
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   The `<SALT>` and `<PASSPHRASE>` must match those used above and specified in the [Corda deployment configuration]({{< relref "./_index.md#encryption" >}}).

   For example:

   {{< tabs name="DDL-crypto-example">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u cryptouser -p TqoCp4v2 \
     --name corda-crypto --jdbc-url 'jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=CRYPTO' \
     --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 \
     --validation-timeout 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u cryptouser -p TqoCp4v2 `
     --name corda-crypto --jdbc-url jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=CRYPTO `
     --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 `
     --validation-timeout 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For information about the Corda CLI `create-db-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-db-config" >}}).

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `CONFIG` schema.

#### Crypto Database Connection Configuration for Corda Enterprise with HashiCorp Vault {{< enterprise-icon >}}

1. Execute the following Corda CLI command to generate DDL for populating the Crypto database connection configuration:

   {{< tabs name="DDL-crypto-ent">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <CRYPTO-USERNAME> \
     --name corda-crypto --jdbc-url `jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=CRYPTO` \
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> \
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> -t VAULT --vault-path <path-to-corda-created-secrets> --key crypto -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <CRYPTO-USERNAME> `
     --name corda-crypto --jdbc-url jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=CRYPTO `
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> `
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> -t VAULT --vault-path <path-to-corda-created-secrets> --key crypto -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   The Vault parameters are used to retrieve encrypted values from the external secrets service. These must match the values specified in the [Corda deployment configuration]({{< relref "./_index.md#encryption" >}}).

   For example:

   {{< tabs name="DDL-crypto-example-ent">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u cryptouser \
     --name corda-crypto --jdbc-url 'jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=CRYPTO' \
     --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 \
     --validation-timeout 5 -t VAULT --vault-path dbsecrets --key crypto -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u cryptouser `
     --name corda-crypto --jdbc-url jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=CRYPTO `
     --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 `
     --validation-timeout 5 -t VAULT --vault-path dbsecrets --key crypto -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For information about the Corda CLI `create-db-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-db-config" >}}).

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `CONFIG` schema.

### Populate the Virtual Nodes Database Connection Configuration

Depending on your installation, follow the steps in one of the following sections to generate DDL for populating the VIRTUAL_NODE database connection configuration:

* [Virtual Nodes Database Connection Configuration for Corda](#virtual-nodes-database-connection-configuration-for-corda)
* [Virtual Nodes Database Connection Configuration for Corda Enterprise with HashiCorp Vault](#virtual-nodes-database-connection-configuration-for-corda-enterprise-with-hashicorp-vault) {{< enterprise-icon >}}

#### Virtual Nodes Database Connection Configuration for Corda

1. Execute the following Corda CLI command to generate DDL for populating the virtual nodes database connection configuration:

   {{< tabs name="vNode">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <VNODE-USERNAME> -p <VNODE-PASSWORD> \
     --name corda-virtual-nodes --jdbc-url 'jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>' \
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> \
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db \
     --is-admin
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <VNODE-USERNAME> -p <VNODE-PASSWORD> `
     --name corda-virtual-nodes --jdbc-url jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> `
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> `
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db `
     --is-admin
   ```
   {{% /tab %}}
   {{< /tabs >}}

   {{< note >}}
   There is no schema in `--jdbc-url` as virtual nodes create their own schemas. However, `--is-admin` is required as this is a DDL configuration not DML.
   For more information about the Corda CLI `create-db-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-db-config">}}).
   {{< /note >}}

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `CONFIG` schema.

#### Virtual Nodes Database Connection Configuration for Corda Enterprise with HashiCorp Vault {{< enterprise-icon >}}

1. Execute the following Corda CLI command to generate DDL for populating the virtual nodes database connection configuration:

   {{< tabs name="vNode-ent">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <VNODE-USERNAME> \
     --name corda-virtual-nodes --jdbc-url 'jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>' \
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> \
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> -t VAULT --vault-path <path-to-corda-created-secrets> --key vnodes -l /tmp/db \
     --is-admin
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <VNODE-USERNAME> `
     --name corda-virtual-nodes --jdbc-url jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> `
     --jdbc-pool-max-size <MAX-POOL-SIZE> --jdbc-pool-min-size <MIN-POOL-SIZE> --idle-timeout <TIMEOUT> `
     --max-lifetime <LIFETIME> --keepalive-time <LIVENESS> --validation-timeout <TIMEOUT> -t VAULT --vault-path <path-to-corda-created-secrets> --key vnodes -l /tmp/db `
     --is-admin
   ```
   {{% /tab %}}
   {{< /tabs >}}

   {{< note >}}
   There is no schema in `--jdbc-url` as virtual nodes create their own schemas. However, `--is-admin` is required as this is a DDL configuration, not DML.

   For more information about the Corda CLI `create-db-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-db-config">}}).
   {{< /note >}}

   For example:
   {{< tabs name="vNode-ent-example">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <VNODE-USERNAME> \
     --name corda-virtual-nodes --jdbc-url 'jdbc:postgresql://prereqs-postgres:5432/cordacluster' \
     --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 \
     --validation-timeout 5 -t VAULT --vault-path dbsecrets --key vnodes -l /tmp/db \
     --is-admin
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <VNODE-USERNAME> `
     --name corda-virtual-nodes --jdbc-url jdbc:postgresql://prereqs-postgres:5432/cordacluster `
     --jdbc-pool-max-size 5 --jdbc-pool-min-size 1 --idle-timeout 100 --max-lifetime 1000 --keepalive-time 60 `
     --validation-timeout 5 -t VAULT --vault-path dbsecrets --key vnodes -l /tmp/db `
     --is-admin
   ```
   {{% /tab %}}
   {{< /tabs >}}

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `CONFIG` schema.

### Populate the REST Admin User

1. Execute the following Corda CLI command to generate DDL for populating the initial REST admin user for Corda:

   {{< tabs name="DDL-user">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-user-config -u <INITIAL-ADMIN-USERNAME> -p <INITIAL-ADMIN-PASSWORD> -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-user-config -u <INITIAL-ADMIN-USERNAME> -p <INITIAL-ADMIN-PASSWORD> -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For more information about the Corda CLI `create-user-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-user-config">}}).

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `RBAC` schema.

### Grant Access to the Cluster Database

The cluster database user is the user set in the `config.username` field under each Corda worker that interacts with the cluster database (see [deployment configuration]({{< relref "./_index.md#cluster-database" >}})).
For each Corda Worker that interacts with the cluster database, grant access to the user as follows:

```sql
GRANT USAGE ON SCHEMA "CONFIG" TO "<CONFIG-DB-USERNAME>";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA "CONFIG" TO "<CONFIG-DB-USERNAME>";
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA "CONFIG" TO "<CONFIG-DB-USERNAME>";
ALTER ROLE <CONFIG-DB-USERNAME> SET search_path TO "CONFIG";
```

### Create RBAC, Crypto and Virtual Node Users

Using the values defined for `RBAC-USERNAME` and `RBAC-PASSWORD` in [Populate the RBAC database connection configuration](#populate-the-rbac-database-connection-configuration), create the RBAC user and grant access as follows:

```sql
CREATE USER "<RBAC-USERNAME>" WITH ENCRYPTED PASSWORD '<RBAC-PASSWORD>';
GRANT USAGE ON SCHEMA "RBAC" to "<RBAC-USERNAME>";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA "RBAC" to "<RBAC-USERNAME>";
ALTER ROLE "<RBAC-USERNAME>" SET search_path TO "RBAC";
```

Using the values defined for `CRYPTO-USERNAME` and `CRYPTO-PASSWORD` in [Populate the crypto database connection configuration](#populate-the-crypto-database-connection-configuration), create the Crypto user and grant access as follows:

```sql
CREATE USER "<CRYPTO-USERNAME>" WITH ENCRYPTED PASSWORD '<CRYPTO-PASSWORD>';
GRANT USAGE ON SCHEMA "CRYPTO" to "<CRYPTO-USERNAME>";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA "CRYPTO" to "<CRYPTO-USERNAME>";
ALTER ROLE "<CRYPTO-USERNAME>" SET search_path TO "CRYPTO";
```

Using the values defined for `VNODE-USERNAME` and `VNODE-PASSWORD` in [[Populate the virtual nodes database connection configuration](#populate-the-virtual-nodes-database-connection-configuration), create the virtual node user and grant access as follows:

```sql
CREATE USER "<VNODE-USERNAME>" WITH ENCRYPTED PASSWORD '<VNODE-PASSWORD>';
GRANT USAGE ON SCHEMA "VIRTUAL_NODE" to "<VNODE-USERNAME>";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA "VIRTUAL_NODE" to "<VNODE-USERNAME>";
ALTER ROLE "<VNODE-USERNAME>" SET search_path TO "VIRTUAL_NODE";
```

### Grant Access to the State Manager Databases

As mentioned in [State Manager Databases]({{< relref "./_index.md#state-manager-databases">}}), Corda workers use individual sets of credentials for accessing any particular state type.
These credentials are configured at the Corda worker level, under `stateManager.<STATE_TYPE>.username` and `stateManager.<STATE_TYPE>.password`.
By default, different state types are assigned to different database schemas and so you must grant access carefully.

| <div style="width:100px">STATE-MANAGER-USERNAME </div> | <div style="width:100px">STATE-MANAGER-PERMISSIONS </div> | <div style="width:100px">STATE-MANAGER-SCHEMA </div> |
|--------------------------------------------------------|-----------------------------------------------------------|------------------------------------------------------|
| `flow.stateManager.flowCheckpoint.username`            | SELECT, INSERT, UPDATE, DELETE                            | `sm_flow_checkpoint`                                 |
| `flowMapper.stateManager.flowMapping.username`         | SELECT, INSERT, UPDATE, DELETE                            | `sm_flow_mapping`                                    |
| `rest.stateManager.flowStatus.username`                | SELECT, INSERT, UPDATE, DELETE                            | `sm_flow_status`                                     |
| `rest.stateManager.keyRotation.username`               | SELECT                                                    | `sm_key_rotation`                                    |
| `crypto.stateManager.keyRotation.username`             | SELECT, INSERT, UPDATE, DELETE                            | `sm_key_rotation`                                    |
| `p2pLinkManager.stateManager.p2pSession.username`     | SELECT, INSERT, UPDATE, DELETE                            | `sm_p2p_session`                                     |
| `tokenSelection.stateManager.tokenPoolCache.username`  | SELECT, INSERT, UPDATE, DELETE                            | `sm_token_pool_cache`                                |

Using the table above as reference, and going from top to bottom, grant access to the user as follows:

```sql
GRANT USAGE ON SCHEMA "<STATE-MANAGER-SCHEMA>" TO "<STATE-MANAGER-USERNAME>";
GRANT <STATE-MANAGER-PERMISSIONS> ON ALL TABLES IN SCHEMA "<STATE-MANAGER-SCHEMA>" TO "<STATE-MANAGER-USERNAME>";
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA "<STATE-MANAGER-SCHEMA>" TO "<STATE-MANAGER-USERNAME>";
ALTER ROLE "<STATE-MANAGER-USERNAME>" SET search_path TO "<STATE-MANAGER-SCHEMA>";
```

### Populate the Crypto Configuration

Depending on your installation, follow the steps in one of the following sections to generate DDL for populating the initial crypto configuration:

* [Initial Crypto Configuration for Corda](#initial-crypto-configuration-for-corda)
* [Initial Crypto Configuration for Corda Enterprise with HashiCorp Vault](#initial-crypto-configuration-for-corda-enterprise-with-hashicorp-vault) {{< enterprise-icon >}}

#### Initial Crypto Configuration for Corda

1. Execute the following Corda CLI command to generate DDL for populating the initial crypto configuration:

   {{< tabs name="DDL-crypto-config">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{< /tab >}}
   {{% tab name="PowerShell" %}}
   ```sh
   corda-cli.cmd initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{< /tab >}}
   {{< /tabs >}}

   The `<SALT>` and `<PASSPHRASE>` must match those used above and specified in the Corda deployment configuration. For more information about the Corda CLI `create-crypto-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-crypto-config">}}).

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `CONFIG` schema.

#### Initial Crypto Configuration for Corda Enterprise with HashiCorp Vault {{< enterprise-icon >}}

1. Execute the following Corda CLI command to generate DDL for populating the initial crypto configuration:

   {{< tabs name="DDL-crypto-config-ent">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-crypto-config -t VAULT -v cryptosecrets -ks salt -kp passphrase -l /tmp/db
   ```
   {{< /tab >}}
   {{% tab name="PowerShell" %}}
   ```sh
   corda-cli.cmd initial-config create-crypto-config -t VAULT -v cryptosecrets -ks salt -kp passphrase -l /tmp/db
   ```
   {{< /tab >}}
   {{< /tabs >}}

   `salt` and `passphrase` are the names of Vault keys and should be entered as shown: they are not to be substituted for any actual salt or passphrase. For more information about the Corda CLI `create-crypto-config` command's arguments, see the [Corda CLI reference]({{< relref "../../../reference/corda-cli/initial-config.md#create-crypto-config">}}).

2. Review the DDL files generated and then execute against the database, ensuring that you apply them to the `CONFIG` schema.

## RBAC Roles

By default, a post-install job creates three default [RBAC roles]({{< relref "../../config-users/_index.md">}}) for the REST API.
To create the roles manually, perform the steps described in this section.

{{< note >}}
You can create RBAC roles manually only after the Corda cluster setup has been completed as an RBAC role requires the REST API URL as a parameter. That value should be a URL where the API is [accessible]({{< relref "../../../reference/rest-api/accessing.md" >}}), either via a load balancer or by forwarding port 8888 from one of the REST worker pods.
{{</ note >}}

1. Set the following override in the deployment configuration to disable the automatic creation:

   ```yaml
   bootstrap:
     rbac:
       enabled: false
   ```

2. Execute the following command:

   {{< tabs name="rbac">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-rbac all-cluster-roles --yield 300 --user <INITIAL-ADMIN-USERNAME> --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-rbac all-cluster-roles --yield 300 --user <INITIAL-ADMIN-USERNAME> --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   ```
   {{% /tab %}}
   {{< /tabs >}}

   For information about the Corda CLI `initial-rbac` command's arguments, see the [Corda CLI reference]({{< relref"../../../reference/corda-cli/initial-rbac.md">}}).
