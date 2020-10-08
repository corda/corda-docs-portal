---
aliases:
- /releases/4.3/running-a-notary-cluster/installing-percona.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-installing-percona
    parent: corda-enterprise-4-3-corda-enterprise
    weight: 1040
tags:
- installing
- percona
title: Configuring the notary backend - MySQL notary
---


# Configuring the notary backend - MySQL notary

The MySQL notary service is tested against Percona XtraDB Cluster 5.7. Percona’s
[documentation page](https://www.percona.com/doc/percona-xtradb-cluster/LATEST/index.html) explains the installation
in detail.


{{< warning >}}
The MySQL notary service is deprecated and will be removed in the future. A [JPA notary service](installing-jpa.md)
should be used instead.

{{< /warning >}}


{{< note >}}
When setting up on Red Hat Enterprise Linux and CentOS make sure SELinux is *disabled* (we found issues even with the *permissive* mode).
Otherwise you might get state transfer errors when starting up the second node, such as:
`[Warning] WSREP: 0.0 (pxc-cluster-node-1): State transfer to 1.0 (pxc-cluster-node-2) failed: -2 (No such file or directory)`

Note also that **each** Percona XtraDB Cluster node requires multiple ports to be opened, the defaults are: 3306, 4444, 4567 and 4568.

{{< /note >}}

## MySQL driver

If Percona is used as the database, each worker node requires a MySQL JDBC driver to be placed in
the `drivers` directory to be able to communicate with the Percona XtraDB Cluster. The official
driver can be obtained from Maven or the
[MySQL Connector/J download page](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-installing.html).


## Networking

The Percona nodes communicate with each other via group communication (GComm). The Percona
replicas should only be reachable from each other and from the worker nodes.

We recommend running the worker nodes and the Percona service in a joined private subnet, opening
up the P2P ports of the workers for external traffic.


## Setup

In this section we’re setting up a three-node Percona cluster.  A three-node cluster can tolerate one crash
fault. In production, you probably want to run five nodes, to be able to tolerate up to two faults.

Host names and IP addresses used in the example are listed in the table below.


{{< table >}}

|Host|IP|
|---------|--------|
|percona-1|10.1.0.1|
|percona-2|10.1.0.2|
|percona-3|10.1.0.3|

{{< /table >}}


## Installation

Percona provides repositories for the YUM and APT package managers.
Alternatively you can install from source. For simplicity, we are going to
install Percona using the default data directory `/var/lib/mysql`.

{{< note >}}
The steps below should be run on all your Percona nodes, unless otherwise
mentioned. You should write down the host names or IP addresses of all your
Percona nodes before starting the installation, to configure the data
replication and later to configure the JDBC connection of your notary
cluster.

{{< /note >}}
Run the commands below on all nodes of your Percona cluster to configure the
Percona repositories and install the service.

```sh
wget https://repo.percona.com/apt/percona-release_0.1-4.$(lsb_release -sc)_all.deb
sudo dpkg -i percona-release_0.1-4.$(lsb_release -sc)_all.deb
sudo apt-get update
sudo apt-get install percona-xtradb-cluster-57
```

The service will start up automatically after the installation, you can confirm that the service is
running with `service mysql status`, start the service with `sudo service mysql start` and stop with
`sudo service mysql stop`.


## Configuration


### Configure the MySQL Root Password (if necessary)

Some distributions allow root access to the database through a Unix domain socket, others
require you to find the temporary password in the log file and change it upon
first login.


### Stop the Service

```sh
sudo service mysql stop
```


### Setup replication

Variables you need to change from the defaults are listed in the table below.


{{< table >}}

|Variable Name|Example|Description|
|----------------------|-----------------------------------------------------------|----------------------------------------------------------|
|wsrep_cluster_address|gcomm://10.1.0.1,10.1.0.2,10.1.0.3|The addresses of all the cluster nodes (host and port)|
|wsrep_node_address|10.1.0.1|The address of the Percona node|
|wsrep_cluster_name|notary-cluster-1|The name of the Percona cluster|
|wsrep_sst_auth|username:password|The credentials for SST|
|wsrep_provider_options|“gcache.size=8G”|Replication options|

{{< /table >}}

Configure all replicas via
`/etc/mysql/percona-xtradb-cluster.conf.d/wsrep.cnf` as shown in the template
below.

{{< tabs name="tabs-1" >}}
wsrep.cnf

{{% tab name="kotlin" %}}
```kotlin
[mysqld]
# Path to Galera library
wsrep_provider=/usr/lib/galera3/libgalera_smm.so
wsrep_provider_options="gcache.size=8G"
# TODO set options related to the timeouts for WAN:
# evs.keepalive_period=PT3s
# evs.inactive_check_period=PT10S
# evs.suspect_timeout=PT30S
# evs.install_timeout=PT1M
# evs.send_window=1024
# evs.user_send_window=512

# Cluster connection URL contains IPs of nodes
#If no IP is found, this implies that a new cluster needs to be created,
#in order to do that you need to bootstrap this node
wsrep_cluster_address="gcomm://{{ your_cluster_IPs }}"

# In order for Galera to work correctly binlog format should be ROW
binlog_format=ROW

# MyISAM storage engine has only experimental support
default_storage_engine=InnoDB

# Slave thread to use
wsrep_slave_threads= 8

wsrep_log_conflicts

# This changes how InnoDB autoincrement locks are managed and is a requirement for Galera
innodb_autoinc_lock_mode=2

# Node IP address
wsrep_node_address={{ node_address }}

# Cluster name
wsrep_cluster_name={{ cluster_name }}

#If wsrep_node_name is not specified,  then system hostname will be used
#wsrep_node_name=

#pxc_strict_mode allowed values: DISABLED,PERMISSIVE,ENFORCING,MASTER
pxc_strict_mode=ENFORCING

# SST method
wsrep_sst_method=xtrabackup-v2

#Authentication for SST method
wsrep_sst_auth={{ sst_user }}:{{ sst_pass }}

```
{{% /tab %}}




[wsrep.cnf](../resources/wsrep.cnf) | ![github](/images/svg/github.svg "github")

{{< /tabs >}}

The file `/etc/mysql/percona-xtradb-cluster.conf.d/mysqld.cnf` contains additional settings like the data directory. We’re assuming
you keep the default `/var/lib/mysql`.


### Configure AppArmor, SELinux or other Kernel Security Module

If you’re changing the location of the database data directory, you might need to
configure your security module accordingly.


### On the first Percona node


#### Start the Database

```sh
sudo /etc/init.d/mysql bootstrap-pxc
```

Watch the logs using `tail -f /var/log/mysqld.log`. Look for a log entry like
`WSREP: Setting wsrep_ready to true`.

You can now connect to the database using a standard tool (e.g. the `mysql` command line tool).


#### Create the Corda User

```sql
CREATE USER corda IDENTIFIED BY '{{ password }}';
```


#### Create the Database and Tables

We need to create three tables in our database:


* `notary_committed_states`
* `notary_request_log`
* `notary_committed_transactions`

We can do this using the following commands:

{{< note >}}
The below schema is intended to be used with the MySQL notary implementation and not the JPA notary implementation. See the note in
introduction for more details on the difference between the MySQL and JPA notary implementations.

{{< /note >}}
```sql
CREATE DATABASE corda;

CREATE TABLE IF NOT EXISTS corda.notary_committed_states(
  issue_transaction_id BINARY(32) NOT NULL,
  issue_transaction_output_id INT UNSIGNED NOT NULL,
  consuming_transaction_id BINARY(32) NOT NULL,
  CONSTRAINT id PRIMARY KEY (issue_transaction_id, issue_transaction_output_id)
);

GRANT SELECT, INSERT ON corda.notary_committed_states TO 'corda';

CREATE TABLE IF NOT EXISTS corda.notary_request_log(
  consuming_transaction_id BINARY(32) NOT NULL,
  requesting_party_name TEXT NOT NULL,
  request_signature BLOB NOT NULL,
  request_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  request_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  CONSTRAINT rid PRIMARY KEY (request_id)
);

GRANT INSERT ON corda.notary_request_log TO 'corda';

CREATE TABLE IF NOT EXISTS corda.notary_committed_transactions(
  transaction_id BINARY(32) NOT NULL,
  CONSTRAINT tid PRIMARY KEY (transaction_id)
);

GRANT SELECT, INSERT ON corda.notary_committed_transactions TO 'corda';
```


#### Create the SST User

```sql
CREATE USER ‘{{ sst_user }}’@’localhost’ IDENTIFIED BY ‘{{ sst_pass }}‘;
GRANT RELOAD, LOCK TABLES, PROCESS, REPLICATION CLIENT ON *.* TO ‘{{ sst_user }}’@’localhost’;
FLUSH PRIVILEGES;
```


### On all other Nodes

Once you have updated the `wsrep.cnf` on all nodes, start MySQL on all the
remaining nodes of your cluster. Run this command on all nodes of your cluster,
except the first one.

```sh
service mysql start
```

Watch the logs using `tail -f /var/log/mysqld.log`. Make sure you can start
the MySQL client on the command line and access the `corda` database on all
nodes.

```sh
mysql
mysql> use corda;
# The output should be `Database changed`.
```

In the next section, we’re [Configuring the notary worker nodes](installing-the-notary-service.md).
