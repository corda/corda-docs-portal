---
date: '2022-11-14'
title: "Manual Bootstrapping"
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-deploy-manual
    parent: corda-5-alpha-tutorials-deploy
    weight: 3000
section_menu: corda-5-alpha
---

By default, the Corda installation process automatically performs various setup actions in Kafka and the database, and for Corda RBAC.
If you require additional control, you can disable these automatic setup processes and an administrator can manually perform the actions with the assistance of the [Corda CLI](../installing-corda-cli.html).

## Kafka

By default, a Corda installation automatically creates the Kafka topics it requires.
To create the topics manually, do the following:
1. Set the following override in the deployment configuration to disable the automatic creation:

   ```yaml
   bootstrap:
     kafka:
       enabled: false
   ```

2. Use the Corda CLI to assist in the creation of the topics prior to Corda installation in one of two ways:
   * [Topic Creation by Direct Connection](#topic-creation-by-direct-connection)
   * [Topic Creation by Scripting](#topic-creation-by-scripting)

   In both cases, the first step is to create a [Kafka client properties](https://kafka.apache.org/documentation/#configuration) file. The following is an example properties file for a Kafka cluster using TLS and SASL authentication:

   ```properties
   security.protocol=SASL-SSL
   sasl.mechanism=SCRAM-SHA-256
   sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required username=<USERNAME> password=<PASSWORD> ;
   ssl.truststore.location=ca.crt
   ssl.truststore.type=PEM
   ```

The examples that follow assume that this file is called `config.properties`.

### Topic Creation by Direct Connection

In the first option, the Corda CLI connects directly to the Kafka broker to create the topics.
The Corda CLI command to create the topics looks as follows:

```shell
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <RELICAS> -p <PARTITIONS> connect
```

For example:

```shell
corda-cli.sh topic -b kafka-1.example.com -k config.properties create -r 3 -p 10 connect
```

### Topic Creation by Scripting

Alternatively, the Corda CLI can generate a shell script which you should review before executing against the broker.
The shell script makes use of the `kafka-topic.sh` script provided with a Kafka installation.

The Corda CLI command looks as follows:

```shell
corda-cli.sh topic -b <BOOTSTRAP-SERVERS> -k config.properties \
  create -r <RELICAS> -p <PARTITIONS> script -f <FILE> -c <CONCURRENCY>
```

Where `<FILE>` is the name of the file in which to save the script and `<CONCURRENCY>` is the number of topics to create in parallel to speed execution.

For example:

```shell
corda-cli.sh topic -b kafka-1.example.com -k config.properties \
  create -r 3 -p 10 script -f create.sh -c 6
```

You can then execute the `create.sh` script to create the topics.

## Database

By default, a Corda installation automatically creates and populates the database schema it requires.
To create the schema manually, do the following:
1. Set the following override in the deployment configuration to disable the automatic creation:

   ```yaml
   bootstrap:
     db:
       enabled: false
   ```



2. Use the Corda CLI to generate DML files for creating the database schema. For example, the following command generates the files in the directory `/tmp/db`:

   ```shell
   corda-cli.sh database spec -c -l /tmp/db
   ```

3. Review the DML files generated and then execute against the database.


4. Execute the following Corda CLI command to generate DDL for populating the RBAC database connection configuration:

   ```shell
   corda-cli.sh initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> \
     --name corda-rbac --jdbcURL jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> \
     --jdbcPoolMaxSize <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```

   The `<SALT>` and `<PASSPHRASE>` are used to encrypt the credentials in the database. These must match the values specified in the Corda deployment configuration for the DB worker:

   ```yaml
   workers:
     db:
       salt: <SALT>
       passphrase: <PASSPHRASE>
   ```

   For example:

   ```shell
   corda-cli.sh initial-config create-db-config -u rbac-user -p rc9VLHU3 \
     --name corda-rbac --jdbcURL jdbc:postgresql://postgres.example.com:5432/cordacluster \
     --jdbcPoolMaxSize 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```

5. Review the DDL files generated and then execute against the database.


6. Execute the following Corda CLI command to generate DDL for populating the Crypto database connection configuration:

   ```shell
   corda-cli.sh initial-config create-db-config -u <CRYPTO-USERNAME> -p <CRYPTO-PASSWORD> \
     --name corda-crypto --jdbcURL jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=CRYPTO \
     --jdbcPoolMaxSize <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
   ```

   The `<SALT>` and `<PASSPHRASE>` must match those used above and specified in the Corda deployment configuration.

   For example:

   ```shell
   corda-cli.sh initial-config create-db-config -u crypto-user -p TqoCp4v2 \
     --name corda-crypto --jdbcURL jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=CRYPTO \
     --jdbcPoolMaxSize 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
   ```

7. Review the DDL files generated and then execute against the database.


8. Execute the following Corda CLI command to generate DDL for populating the initial admin user for Corda:

   ```shell
   corda-cli.sh initial-config create-user-config -u <INITIAL-ADMIN-USERNAME> -p <INITIAL-ADMIN-PASSWORD> -l /tmp/db
   ```

9. Review the DDL files generated and then execute against the database.

10. Create the RBAC and Crypto users and grant access as follows:

    ```sql
    CREATE USER <RBAC-USERNAME> WITH ENCRYPTED PASSWORD '<RBAC-PASSWORD>';
    GRANT USAGE ON SCHEMA RPC_RBAC to <RBAC-USERNAME>;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA RPC_RBAC to <RBAC-USERNAME>;
    CREATE USER <CRYPTO-USERNAME> WITH ENCRYPTED PASSWORD '<CRYPTO-PASSWORD>';
    GRANT USAGE ON SCHEMA CRYPTO to <CRYPTO-USERNAME>;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA CRYPTO to <CRYPTO-USERNAME>;
    ```

11. Execute the following Corda CLI command to generate DDL for populating the initial crypto configuration:

    ```shell
    corda-cli.sh initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
    ```

    The `<SALT>` and `<PASSPHRASE>` must match those used above and specified in the Corda deployment configuration.

12. Review the DDL files generated and then execute against the database.

## RBAC Roles

By default, a post-install job normally creates three default RBAC roles for the Corda API.
To create the roles manually, do the following:
1. Set the following override in the deployment configuration to disable the automatic creation:

   ```yaml
   bootstrap:
     rbac:
       enabled: false
   ```

2. Execute the following three commands:

   ```shell
   corda-cli.sh initial-rbac user-admin --yield 300 --user <INITIAL-ADMIN-USERNAME> \
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   corda-cli.sh initial-rbac vnode-creator --yield 300 --user <INITIAL-ADMIN-USERNAME> \
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   corda-cli.sh initial-rbac corda-developer --yield 300 --user <INITIAL-ADMIN-USERNAME> \
     --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
   ```

   `<API-ENDPOINT>` should be a URL where the Corda API is accessible, either via a load balancer or by forwarding port 8888 from one of the RPC worker pods.
