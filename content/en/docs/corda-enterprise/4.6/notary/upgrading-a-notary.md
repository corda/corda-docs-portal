---
menu:
    corda-enterprise-4-6:
        identifier: corda-enterprise-4-6-upgrade-notary-database
        parent: corda-enterprise-4-6-notary-migration-overview
weight: 1
title: "Importing Percona notary data to CockroachDB"
---

# Importing Percona notary data to CockroachDB

Corda Enterprise supports two highly-available notary implementations: MySQL and JPA notaries. The MySQL notary requires
a Percona database, and is a **deprecated** implementation.

To migrate from a MySQL notary to a JPA notary you must change the backend database and database schema. After
notary data has been validated in the CockroachDB database, the [JPA Notary Setup](ha-notary-service-overview.md/)
and [Notary Worker Configuration](installing-the-notary-service.md/) processes can be followed.

## Before you begin

Before beginning you must have:

- An `ssh` accessible Percona cluster in **read-only mode**, or in **read/write** mode with no active connections.
- An `ssh` accessible CockroachDB cluster.
- A CockroachDB database cluster installed to `/opt/cockroachdb`.
- A `corda` user within the CockroachDB cluster.
- The required binaries are present in the PATH of the Percona and Cockroach machines.

Consider exchanging database `ssh` keys to avoid password requests when accessing the databases.

{{< note >}}
The use of read-only mode for the Percona database will require some database downtime.
{{</ note >}}

## Migrating Percona data to CockroachDB

1. The data in the Percona database must be extracted. To dump the `corda` database tables from the Percona database, use the following command, replacing `$PERCONA` with the address of your Percona database machine:

    ```bash
    ssh $PERCONA "bash -s -x -v" <<EOF
    mysqldump -u root --skip-lock-tables corda notary_committed_transactions notary_committed_states notary_request_log | gzip > dump.sql.gz
    EOF
    ```

    The dumped data will be stored locally in the `/home/mysql` directory.

2. The local data can now be copied to CockroachDB nodes. Replace the Cockroach node addresses before running the following command:

    ```bash
    #  REPLACE WITH YOUR COCKROACH NODES
    COCKROACH_NODES="cockroach@dbnode1.uksouth.cloudapp.azure.com \
    cockroach@dbnode2.uksouth.cloudapp.azure.com \
    cockroach@dbnode3.ukwest.cloudapp.azure.com"

    COCKROACH_DEST_PATH=/opt/cockroachdb/cockroach-data/extern/notary

    for NODE in $COCKROACH_NODES; do
      ssh $NODE "mkdir -p $COCKROACH_DEST_PATH"
      scp dump.sql.gz $NODE:$COCKROACH_DEST_PATH
    done
    ```

{{< warning >}}
The export file **must** be copied into a subdirectory of `/opt/cockroachdb/cockroach-data/extern/` for each node, as described in the [CockroachDB documentation](https://www.cockroachlabs.com/docs/v19.2/import.html#import-file-urls/)
{{</ warning >}}

3. After copying the data to CockroachDB, the data must be imported to the `corda_mysql` database. The `corda_mysql`
database is used to contain the MySQL data until it can be imported to the final `corda` database with the correct database
schema. The following command will import the Percona data in the `mysql` schema:

    ```bash
    # Get the first node from the previous variable.
    COCKROACH_FIRST_NODE=${COCKROACH_NODES%% *}

    ssh $COCKROACH_FIRST_NODE "bash -s -x -v" << EOF
    /opt/cockroachdb/bin/cockroach sql --certs-dir /opt/cockroachdb/certs/

    DROP DATABASE IF EXISTS corda_mysql;
    CREATE DATABASE IF NOT EXISTS corda_mysql;
    USE corda_mysql;

    # Note the location is the "data folder"/notary
    IMPORT MYSQLDUMP 'nodelocal:///notary/dump.sql.gz';
    EOF
    ```

    The Percona data has now been imported into a Cockroach database called `corda_mysql`.

### Importing Percona database data as a single script

The code blocks above can be combined into a single `bash` script. Take care to replace the Percona and CockroachDB addresses in the script before use:

```bash
#!/usr/bin/env bash

# REPLACE THESE WITH YOUR MACHINE(S)
PERCONA=mysql@mysql-dbnode1.uksouth.cloudapp.azure.com

COCKROACH_NODES="cockroach@jpa-dbnode1.uksouth.cloudapp.azure.com \
cockroach@jpa-dbnode2.uksouth.cloudapp.azure.com \
cockroach@jpa-dbnode3.ukwest.cloudapp.azure.com"
# END OF REPLACE

COCKROACH_FIRST_NODE=${COCKROACH_NODES%% *}
COCKROACH_ROOT=/opt/cockroachdb
COCKROACH_IMPORT_DIR=notary
COCKROACH_DEST_PATH=$COCKROACH_ROOT/cockroach-data/extern/$COCKROACH_IMPORT_DIR

echo --Dumping MySQL tables

time ssh $PERCONA "bash -s -x -v" <<EOF
rm dump.sql.gz
mysqldump -u root --skip-lock-tables corda notary_committed_transactions notary_committed_states notary_request_log | gzip > dump.sql.gz
ls -lh dump.sql.gz
EOF

echo --Copying export from mysql to local machine

scp $PERCONA:/home/mysql/dump.sql.gz .

echo --Making Cockroach data folders for import and copying export

for NODE in $COCKROACH_NODES; do
  ssh $NODE "mkdir -p $COCKROACH_DEST_PATH"
  scp dump.sql.gz $NODE:$COCKROACH_DEST_PATH
done

echo --Import dump into cockroach

time ssh $COCKROACH_FIRST_NODE "bash -s -x -v" << EOF
$COCKROACH_ROOT/bin/cockroach sql --certs-dir $COCKROACH_ROOT/certs/

DROP DATABASE IF EXISTS corda_mysql;
CREATE DATABASE IF NOT EXISTS corda_mysql;
USE corda_mysql;

IMPORT MYSQLDUMP 'nodelocal:///$COCKROACH_IMPORT_DIR/dump.sql.gz';
EOF

echo --Done
```

## Migrating the database schema

1. To migrate the database schema, run the following script, replacing the Cockroach node addresses:

    ```bash
    #!/usr/bin/env bash

    # REPLACE THESE
    COCKROACH_NODES="cockroach@jpa-dbnode1.uksouth.cloudapp.azure.com \
    cockroach@jpa-dbnode2.uksouth.cloudapp.azure.com \
    cockroach@jpa-dbnode3.ukwest.cloudapp.azure.com"

    #  We need a UUID to uniquely indentify the data - you should generate your own
    UUID="d12888c8-cd00-11ea-a5c9-77fe2bd43698"
    # END OF REPLACE

    COCKROACH_FIRST_NODE=${COCKROACH_NODES%% *}

    CORDA_SCHEMA=corda

    #  Begin...
    echo Converting Cockroach tables

    COCKROACH_ROOT=/opt/cockroachdb

    time ssh $COCKROACH_FIRST_NODE "bash -s -x -v" <<EOF
    $COCKROACH_ROOT/bin/cockroach sql --certs-dir $COCKROACH_ROOT/certs/

    drop database if exists $CORDA_SCHEMA cascade;

    create database if not exists $CORDA_SCHEMA;

    create table $CORDA_SCHEMA.notary_committed_states (
        state_ref varchar(73) not null,
        consuming_transaction_id varchar(64) not null,
        constraint id1 primary key (state_ref)
        );

    create table $CORDA_SCHEMA.notary_committed_transactions (
        transaction_id varchar(64) not null,
        constraint id2 primary key (transaction_id)
        );

    create table $CORDA_SCHEMA.notary_request_log (
        id varchar(76) not null,
        consuming_transaction_id varchar(64),
        requesting_party_name varchar(255),
        request_timestamp timestamp not null,
        request_signature bytes not null,
        worker_node_x500_name varchar(255),
        constraint id3 primary key (id),
        index (consuming_transaction_id)
        );

    create table $CORDA_SCHEMA.notary_double_spends (
        state_ref varchar(73) not null,
        request_timestamp timestamp not null,
        consuming_transaction_id varchar(64) not null,
        constraint id4 primary key (state_ref, consuming_transaction_id),
        index (state_ref, request_timestamp, consuming_transaction_id)
        );

    create user if not exists corda;

    grant select on database $CORDA_SCHEMA to corda;
    grant insert on database $CORDA_SCHEMA to corda;

    grant select on table $CORDA_SCHEMA.* to corda;
    grant insert on table $CORDA_SCHEMA.* to corda;

    select 'CONVERTING notary_committed_states' as status;

    insert into
        $CORDA_SCHEMA.notary_committed_states
    select
        UPPER(CONCAT(ENCODE(issue_transaction_id, 'hex'), ':', CAST(issue_transaction_output_id as string))) as state_ref,
        UPPER(ENCODE(consuming_transaction_id, 'hex')) as consuming_transaction_id
    from
        corda_mysql.notary_committed_states;


    --------------------------------------------------------------------------------

    select 'CONVERTING notary_committed_transactions' as status;

    insert into
        $CORDA_SCHEMA.notary_committed_transactions
    select
        UPPER(ENCODE(transaction_id, 'hex')) as transaction_id
    from
        corda_mysql.notary_committed_transactions;


    --------------------------------------------------------------------------------



    select 'CONVERTING notary_request_log' as status;

    insert into
        $CORDA_SCHEMA.notary_request_log
    select
        CONCAT('$UUID', TO_HEX(r.request_id)) as id,
        ENCODE(r.consuming_transaction_id, 'hex') as consuming_transaction_id,
        r.requesting_party_name as requesting_party_name,
        r.request_date::timestamp as request_date,
        r.request_signature as request_signature,
        r.worker_node_x500_name as worker_node_x500_name
    from
        corda_mysql.notary_request_log r;
    EOF
    ```

    The script has four distinct operations:

    - Creating a database named `corda`.
    - Creating a `corda` user and giving appropriate permissions.
    - Creating tables within the `corda` database.
    - Importing the notary data from the `corda_mysql` database into the `corda` database.

2. You can validate the notary data by checking the row counts in both databases. To run the row count, run the following script, replacing the Percona and Cockroach node addresses with your machine addresses:

    ```bash
    #!/usr/bin/env bash

    # REPLACE THESE WITH YOUR MACHINE(S)
    PERCONA=mysql@mysql-dbnode1.uksouth.cloudapp.azure.com

    COCKROACH_NODES="cockroach@jpa-dbnode1.uksouth.cloudapp.azure.com \
    cockroach@jpa-dbnode2.uksouth.cloudapp.azure.com \
    cockroach@jpa-dbnode3.ukwest.cloudapp.azure.com"
    # END OF REPLACE

    COCKROACH_FIRST_NODE=${COCKROACH_NODES%% *}
    CORDA_SCHEMA=corda
    COCKROACH_ROOT=/opt/cockroachdb

    echo PERCONA

    ssh $PERCONA "bash -s -x -v" <<EOF
    mysql -u root
    select count(*) as PERCONA_notary_committed_states from $CORDA_SCHEMA.notary_committed_states;
    select count(*) as PERCONA_notary_committed_transactions from $CORDA_SCHEMA.notary_committed_transactions;
    select count(*) as PERCONA_notary_request_log from $CORDA_SCHEMA.notary_request_log;
    EOF

    echo COCKROACH

    ssh $COCKROACH_FIRST_NODE "bash -s -x -v" <<EOF
    $COCKROACH_ROOT/bin/cockroach sql --certs-dir $COCKROACH_ROOT/certs/
    select count(*) as COCKROACH_notary_committed_states from $CORDA_SCHEMA.notary_committed_states;
    select count(*) as COCKROACH_notary_committed_transactions from $CORDA_SCHEMA.notary_committed_transactions;
    select count(*) as COCKROACH_notary_request_log from $CORDA_SCHEMA.notary_request_log;
    EOF
    ```

## Next steps

After the notary data migration is complete, at least one JPA notary node must be provisioned. To set up a JPA notary node,
see the [JPA Notary Setup](ha-notary-service-overview.md/) and [Notary Worker Configuration](installing-the-notary-service.md/) documentation.

After the JPA notary is operating, you should run the [Notary Health Check tool](../notary-healthcheck.md/) to ensure that the network is up and responsive.
