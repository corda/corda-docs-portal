---
date: '2022-11-14'
title: "Manual Bootstrapping"
menu:
  corda-5-alpha:
    identifier: corda-5-alpha-deploy-manual
    parent: corda-5-alpha-tutorials-deploy
    weight: 3000
section-menu: corda-5-alpha
---
<!-- CLI https://r3-cev.atlassian.net/browse/DOC-4185-->
This section describes how to manually bootstrap Kafka, the database, and RBAC roles using the Corda CLI.
<!--do we need to add back in installation instructions??-->

By default, a Corda installation automatically performs various setup actions in Kafka and the database, and for Corda RBAC.
For customer's requiring additional control, this automatic setup can be disabled and the actions performed manually by an administrator with the assistance of the Corda CLI.

## Kafka

By default, a Corda installation automatically creates the Kafka topics it requires.
This behavior can be disabled by setting the following override in the deployment configuration:

```yaml
bootstrap:
  kafka:
    enabled: false
```

The Corda CLI can then be used to assist in creation of the topics prior to Corda installation in one of two ways.

In both cases, the first step is to create a [Kafka client properties](https://kafka.apache.org/documentation/#configuration) file.
An example properties file for a Kafka cluster using TLS and SASL authentication might look as follows:

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

Alternatively, the Corda CLI can be used to generate a shell script which may then be reviewed before executing against the broker.
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

The script `create.sh` would then be executed to created the topics.

## Database

By default, a Corda installation automatically creates and populates the database schema it requires.
This behavior can be disabled by setting the following override in the deployment configuration:

```yaml
bootstrap:
  db:
    enabled: false
```

The following steps can then be performed to manually set up the database prior to Corda installation.

### Create the Database Schemas

The following Corda CLI command generates DML files in the directory `/tmp/db` for creating the database schema:

```shell
corda-cli.sh database spec -c -l /tmp/db
```

The DML generated should be reviewed and then executed against the database.

### Create RBAC Database Connection Configuration

The following Corda CLI command generates DDL for populating the RBAC database connection configuration:

```shell
corda-cli.sh initial-config create-db-config -u <RBAC-USERNAME> -p <RBAC-PASSWORD> \
  --name corda-rbac --jdbcURL jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME> \
  --jdbcPoolMaxSize <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```

The `<SALT>` and `<PASSPHRASE>` are used to encrypt the credentials in the database.
These must match the values specified in the Corda deployment configuration for the DB worker:

```yaml
workers:
  db:
    salt: <SALT>
    passphrase: <PASSPHRASE>
```

An example usage might look as follows:

```shell
corda-cli.sh initial-config create-db-config -u rbac-user -p rc9VLHU3 \
  --name corda-rbac --jdbcURL jdbc:postgresql://postgres.example.com:5432/cordacluster \
  --jdbcPoolMaxSize 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
```

The DDL generated should be reviewed and then executed against the database.

### Create Crypto Database Connection Configuration

The following Corda CLI command generates DDL for populating the Crypto database connection configuration:

```shell
corda-cli.sh initial-config create-db-config -u <CRYPTO-USERNAME> -p <CRYPTO-PASSWORD> \
  --name corda-crypto --jdbcURL jdbc:postgresql://<DB-HOST>:<DB-PORT>/<DB=NAME>?currentSchema=CRYPTO \
  --jdbcPoolMaxSize <POOL-SIZE> --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```

The `<SALT>` and `<PASSPHRASE>` must match those used above and specified in the Corda deployment configuration.

An example usage might look as follows:

```shell
corda-cli.sh initial-config create-db-config -u crypto-user -p TqoCp4v2 \
  --name corda-crypto --jdbcURL jdbc:postgresql://postgres.example.com:5432/cordacluster?currentSchema=CRYPTO \
  --jdbcPoolMaxSize 5 --salt X3UaCpUH --passphrase UUWLhD8S -l /tmp/db
```

The DDL generated should be reviewed and then executed against the database.

### Create the Initial Admin User

The following Corda CLI command generates DDL for populating the initial admin user for Corda:

```shell
corda-cli.sh initial-config create-user-config -u <INITIAL-ADMIN-USERNAME> -p <INITIAL-ADMIN-PASSWORD> -l /tmp/db
```

The DDL generated should be reviewed and then executed against the database.

### Create the Database Users and Grant Access

Create the RBAC and Crypto users and grant access as follows:

```sql
CREATE USER <RBAC-USERNAME> WITH ENCRYPTED PASSWORD '<RBAC-PASSWORD>';
GRANT USAGE ON SCHEMA RPC_RBAC to <RBAC-USERNAME>;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA RPC_RBAC to <RBAC-USERNAME>;
CREATE USER <CRYPTO-USERNAME> WITH ENCRYPTED PASSWORD '<CRYPTO-PASSWORD>';
GRANT USAGE ON SCHEMA CRYPTO to <CRYPTO-USERNAME>;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA CRYPTO to <CRYPTO-USERNAME>;
```

### Create the Initial Crypto Configuration

The following Corda CLI command generates DDL for populating the initial crypto configuration:

```shell
corda-cli.sh initial-config create-crypto-config --salt <SALT> --passphrase <PASSPHRASE> -l /tmp/db
```

The `<SALT>` and `<PASSPHRASE>` must match those used above and specified in the Corda deployment configuration.

The DDL generated should be reviewed and then executed against the database.

## RBAC Roles

A post-install job normally creates three default RBAC roles for the Corda API.
Automatic creation of these RBAC roles can be disabled as follows:

```yaml
bootstrap:
  rbac:
    enabled: false
```

To manually create the three RBAC roles, execute the following three commands:

```shell
corda-cli.sh initial-rbac user-admin --yield 300 --user <INITIAL-ADMIN-USERNAME> \
  --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
corda-cli.sh initial-rbac vnode-creator --yield 300 --user <INITIAL-ADMIN-USERNAME> \
  --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
corda-cli.sh initial-rbac corda-developer --yield 300 --user <INITIAL-ADMIN-USERNAME> \
  --password <INITIAL-ADMIN-PASSWORD> --target <API-ENDPOINT>
```

`<API-ENDPOINT>` should be a URL where the Corda API is accessible, either via a load balancer or by forwading port 8888 from one of the RPC worker pods.
