---
date: '2023-05-11'
version: 'Corda 5.0'
title: "Manual Bootstrapping"
version: 'Corda 5.0'
menu:
  corda5:
    parent: corda5-cluster-deploying
    identifier: corda5-cluster-bootstrapping
    weight: 2000
section_menu: corda5
---
# Manual Bootstrapping

By default, the Corda installation process automatically performs various setup actions in Kafka, the database, and for [Corda RBAC]({{< relref "../../config-users/_index.md">}}).
If you require additional control, you can disable these automatic setup processes and an administrator can manually perform the actions with the assistance of the [Corda CLI]({{< relref "../../tooling/installing-corda-cli.md" >}}).

This section describes how to configure the following:
* [Kafka]({{< relref "#kafka" >}})
* [Database]({{< relref "#database" >}})
* [RBAC Roles]({{< relref "#rbac-roles" >}})

When you have completed the manual configuration of the above, you can [Deploy Corda]({{< relref "./_index.md#deployment" >}}).

## Kafka 

By default, a Corda installation automatically creates the Kafka topics it requires.
To create the topics manually, do the following:
1. Set the following override in the deployment configuration to disable the automatic creation:

   ```yaml
   bootstrap:
     kafka:
       enabled: false
   ```
2. Create a [Kafka client properties](https://kafka.apache.org/documentation/#configuration) file.
The following is an example properties file for a Kafka cluster using TLS and SASL authentication:

   ```properties
   security.protocol=SASL_SSL
   sasl.mechanism=SCRAM-SHA-256
   sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username="<USERNAME>" password="<PASSWORD>" ;
   ssl.truststore.location=ca.crt
   ssl.truststore.type=PEM
   ```
   The examples that follow assume that this file is called `config.properties`.

3. Use the Corda CLI to assist in the creation of the topics prior to Corda installation in one of two ways:
    * [Topic Creation by Direct Connection](#topic-creation-by-direct-connection)
    * [Topic Creation by Scripting](#topic-creation-by-scripting)

### Topic Creation by Direct Connection

In the first option, the Corda CLI connects directly to the Kafka broker to create the topics.
The Corda CLI command to create the topics looks as follows:

{{< tabs name="create-topics">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <REPLICAS> -p <PARTITIONS> connect
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k config.properties create -r <REPLICAS> -p <PARTITIONS> connect
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

If you are authenticating Kafka users, the Corda CLI can also create Access Control List (ACL) entries as appropriate for each Corda worker.
Specify a set of name-value pairs giving the Kafka username that will be used for each Corda worker:

{{< tabs name="acl">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <REPLICAS> -p <PARTITIONS> \
  -u crypto=<CRYPTO_USER> -u db=<DB_USER> -u flow=<FLOW_USER> -u membership=<MEMBERSHIP_USER> \
  -u p2pGateway=<P2P_GATEWAY_USER> -u p2pLinkManager=<P2P_LINK_MANAGER_USER> -u rest=<REST_USER> \
  connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k config.properties `
  create -r <REPLICAS> -p <PARTITIONS> `
  -u crypto=<CRYPTO_USER> -u db=<DB_USER> -u flow=<FLOW_USER> -u membership=<MEMBERSHIP_USER> `
  -u p2pGateway=<P2P_GATEWAY_USER> -u p2pLinkManager=<P2P_LINK_MANAGER_USER> -u rest=<REST_USER> `
  connect
```
{{% /tab %}}
{{< /tabs >}}

### Topic Creation by Scripting

Alternatively, the Corda CLI can generate a script which you should review before executing against the broker.
The script makes use of the `kafka-topic.sh` script provided with a Kafka installation.

Run the following Corda CLI command to generate the script:

{{< tabs name="cli-script">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <REPLICAS> -p <PARTITIONS> script -f <FILE> -c <CONCURRENCY>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k config.properties create -r <REPLICAS> -p <PARTITIONS> script -f <FILE> -c <CONCURRENCY>
```
{{% /tab %}}
{{< /tabs >}}

Where `<FILE>` is the name of the file in which to save the script and `<CONCURRENCY>` is the number of topics to create in parallel to speed execution.

For example:

{{< tabs name="cli-script-example">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b kafka-1.example.com -k config.properties \
  create -r 3 -p 10 script -f create.sh -c 6
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b kafka-1.example.com -k config.properties create -r 3 -p 10 script -f create.sh -c 6
```
{{% /tab %}}
{{< /tabs >}}

If you are authenticating Kafka users, the Corda CLI can also create Access Control List (ACL) entries as appropriate for each Corda worker.
Specify a set of name-value pairs giving the Kafka username that will be used for each Corda worker:

{{< tabs name="acl2">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <REPLICAS> -p <PARTITIONS> \
  -u crypto=<CRYPTO_USER> -u db=<DB_USER> -u flow=<FLOW_USER> -u membership=<MEMBERSHIP_USER> \
  -u p2pGateway=<P2P_GATEWAY_USER> -u p2pLinkManager=<P2P_LINK_MANAGER_USER> -u rest=<REST_USER> \
  connect
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd topic -b <BOOTSTRAP-SERVERS> -k config.properties `
  create -r <REPLICAS> -p <PARTITIONS> `
  -u crypto=<CRYPTO_USER> -u db=<DB_USER> -u flow=<FLOW_USER> -u membership=<MEMBERSHIP_USER> `
  -u p2pGateway=<P2P_GATEWAY_USER> -u p2pLinkManager=<P2P_LINK_MANAGER_USER> -u rest=<REST_USER> `
  connect
```
{{% /tab %}}
{{< /tabs >}}

You can then execute the `create` script to create the topics.

## Database

By default, a Corda installation automatically creates and populates the database schema it requires.
To create the schema manually, do the following:
1. Set the following override in the deployment configuration to disable the automatic creation:

   ```yaml
   bootstrap:
     db:
       enabled: false
   ```

{{< note >}}

* If you are applying SQL to a schema using the `psql` command you can specify which schema to apply it to using the `--dbname` parameter like so: `--dbname "dbname=cordacluster options=--search_path=<SCHEMA-NAME>"`

* If you are targeting schemas, database and crypto generated SQL should be applied to the CONFIG schema, and create-user-config generated SQL should be applied to the RBAC schema. If the schemas are not specified, then the tables will be created in the default schema and the next steps in this procedure will need updating to reflect this.
{{< /note >}}

2. Use the Corda CLI to generate DML files for creating the database tables to use for each of the `crypto`, `config`, and `rbac` components.

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

3. Review the DML files generated and then execute against the database.

4. Execute the following Corda CLI command to generate DDL for populating the RBAC database connection configuration, in this case use CONFIG:

   {{< tabs name="RBAC">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> \
     --name corda-rbac --jdbc-url 'jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=RBAC' \
     --jdbc-pool-max-size <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> `
     --name corda-rbac --jdbc-url jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=RBAC `
     --jdbc-pool-max-size <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   The `<SALT>` and `<PASSPHRASE>` are used to encrypt the credentials in the database. These must match the values specified in the [Corda deployment configuration]({{< relref "#encryption" >}}).

For example:

{{< tabs name="RBAC-example">}}
{{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u rbacuser -p rc9VLHU3 \
     --name corda-rbac --jdbc-url 'jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=RBAC' \
     --jdbc-pool-max-size 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u rbacuser -p rc9VLHU3 `
     --name corda-rbac --jdbc-url jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=RBAC `
     --jdbc-pool-max-size 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```
{{% /tab %}}
{{< /tabs >}}

5. Review the DDL files generated and then execute against the database.

6. Execute the following Corda CLI command to generate DDL for populating the Crypto database connection configuration,in this case use CONFIG:

   {{< tabs name="DDL-crypto">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u <CRYPTO-USERNAME> -p <CRYPTO-PASSWORD> \
     --name corda-crypto --jdbc-url `jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=CRYPTO` \
     --jdbc-pool-max-size <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <CRYPTO-USERNAME> -p <CRYPTO-PASSWORD> `
     --name corda-crypto --jdbc-url jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=CRYPTO `
     --jdbc-pool-max-size <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```
   {{% /tab %}}
   {{< /tabs >}}

   The `<SALT>` and `<PASSPHRASE>` must match those used above and specified in the [Corda deployment configuration]({{< relref "#encryption" >}}).

For example:

{{< tabs name="DDL-crypto-example">}}
{{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-config create-db-config -u cryptouser -p TqoCp4v2 \
     --name corda-crypto --jdbc-url 'jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=CRYPTO' \
     --jdbc-pool-max-size 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u cryptouser -p TqoCp4v2 `
     --name corda-crypto --jdbc-url jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=CRYPTO `
     --jdbc-pool-max-size 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```
{{% /tab %}}
{{< /tabs >}}

7. Review the DDL files generated and then execute against the database.

8. Execute the following Corda CLI command to configure vNodes, in this case use CONFIG:


{{< tabs name="vNode-example">}}
{{% tab name="Bash" %}}
   ```sh
  corda-cli.sh initial-config create-db-config -u <VNODE-USERNAME> -p <VNODE-PASSWORD> \
    --name orda-virtual-nodes --jdbc-url 'jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> \ --jdbc-pool-max-size <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db \ --is-admin'
   ```
{{% /tab %}}
{{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-config create-db-config -u <VNODE-USERNAME> -p <VNODE-PASSWORD> \
    --name orda-virtual-nodes --jdbc-url `jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> \ --jdbc-pool-max-size <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db \ --is-admin`
   ```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
There is no schema in `--jdbc-url` as vNodes create their own schemas. However, `--is-admin` is required as this is a DDL configuration not DML.
{{< /note >}}

9. Execute the following Corda CLI command to generate DDL for populating the initial admin user for Corda, in this case use RBAC:

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

10. Review the DDL files generated and then execute against the database.

11. Create the RBAC and Crypto users and grant access as follows:

    ```sql
    CREATE USER <RBAC-USERNAME> WITH ENCRYPTED PASSWORD '<RBAC-PASSWORD>';
    GRANT USAGE ON SCHEMA RBAC to <RBAC-USERNAME>;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA RBAC to <RBAC-USERNAME>;
    CREATE USER <CRYPTO-USERNAME> WITH ENCRYPTED PASSWORD '<CRYPTO-PASSWORD>';
    GRANT USAGE ON SCHEMA CRYPTO to <CRYPTO-USERNAME>;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA CRYPTO to <CRYPTO-USERNAME>;
    ```

12. Execute the following Corda CLI command to generate DDL for populating the initial crypto configuration, in this case use CONFIG:

{{< tabs name="DDL-crypto-config">}}
{{% tab name="Bash" %}}
```sh
 corda-cli.sh initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
 corda-cli.cmd initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```
{{% /tab %}}
{{< /tabs >}}
The `<SALT>` and `<PASSPHRASE>` must match those used above and specified in the Corda deployment configuration.

13. Review the DDL files generated and then execute against the database.

## RBAC Roles

By default, a post-install job normally creates three default [RBAC roles]({{< relref "../../config-users/_index.md">}}) for the Corda API.
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

2. Execute the following three commands:

   {{< tabs name="rbac">}}
   {{% tab name="Bash" %}}
   ```sh
   corda-cli.sh initial-rbac user-admin --yield 300 --user <INITIAL-ADMIN-USERNAME> \
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   corda-cli.sh initial-rbac vnode-creator --yield 300 --user <INITIAL-ADMIN-USERNAME> \
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   corda-cli.sh initial-rbac corda-developer --yield 300 --user <INITIAL-ADMIN-USERNAME> \
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   corda-cli.cmd initial-rbac user-admin --yield 300 --user <INITIAL-ADMIN-USERNAME> `
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   corda-cli.cmd initial-rbac vnode-creator --yield 300 --user <INITIAL-ADMIN-USERNAME> `
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   corda-cli.cmd initial-rbac corda-developer --yield 300 --user <INITIAL-ADMIN-USERNAME> `
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   ```
   {{% /tab %}}
   {{< /tabs >}}