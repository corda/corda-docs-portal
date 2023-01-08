---
aliases:
- /releases/4.0/running-a-notary-cluster/operating-percona.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-0:
    identifier: corda-enterprise-4-0-operating-percona
    parent: corda-enterprise-4-0-introduction
    weight: 1030
tags:
- operating
- percona
title: Percona Monitoring, Backup and Restore (Advanced)
---


# Percona Monitoring, Backup and Restore (Advanced)


## Monitoring

Percona Monitoring and Management (PMM) is a platform for managing and
monitoring your Percona cluster.  See the [PMM documentation](https://www.percona.com/doc/percona-monitoring-and-management/index.html).


### Running PMM Server

Install PMM Server on a single machine of your cluster.

```sh
docker create \
  -v /opt/prometheus/data \
  -v /opt/consul-data \
  -v /var/lib/mysql \
  -v /var/lib/grafana \
  --name pmm-data \
  percona/pmm-server:latest /bin/true

docker run -d \
  -p 80:80 \
  --volumes-from pmm-data \
  --name pmm-server \
  percona/pmm-server:latest
```


### Installing PMM  Client

You need to configure the Percona repositories first, as described above.
Install and configure PMM Client on all the machines that are running Percona.

```sh
sudo apt-get install pmm-client
sudo pmm-admin config --server ${PMM_HOST}:${PMM_PORT}
```


## Backup

You can take backups with the `XtraBackup` tool. The command below creates a
backup in `/data/backups`.

```sh
xtrabackup --backup --target-dir=/data/backups/
```


## Restore


### Stop the Cluster

Stop the Percona cluster by shutting down nodes one by one. Prepare the backup to restore using

```sh
xtrabackup --prepare --target-dir=/data/backups/
```


### Restore from a Backup

```sh
mv '{{ data-directory }}' '{{ data-directory-backup }}'
xtrabackup --copy-back --target-dir=/data/backups/
sudo chown -R mysql:mysql '{{ data-directory }}'
```

Note that you might need the data in `{{ data-direcotry-backup }}` in case you
need to repair and replay from the binlog, as described below.


### Start the first Node

```sh
/etc/init.d/mysql bootstrap-pxc
```


## Repair

You can recover from some accidents, e.g. a table drop, by restoring the last
backup and then applying the binlog up to the offending statement.


### Replay the Binary Log

XtraBackup records the binlog position of the backup in
`xtrabackup_binlog_info`. Use this positon to start replaying the binlog from
your data directory (e.g. `/var/lib/mysql`, or the target directory of the move command
used in the backup step above).

```sh
mysqlbinlog '{{ binlog-file }}' --start-position=<start-position> > binlog.sql
```

In case there are offending statements, such as
accidental table drops, you can open `binlog.sql` for examination.

Optionally can also pass `--base64-output=decode-rows` to decode every statement into a human readable format.

```sh
mysqlbinlog $BINLOG_FILE --start-position=$START_POS --stop-position=$STOP_POS > binlog.sql
# Replay the binlog
mysql -u root -p < binlog.sql
```


### Start remaining Nodes

Finally, start the remaining nodes of the cluster.


## Restarting a Cluster

When all nodes of the cluster are down, manual intervention is needed to bring
the cluster back up. On the node with the most advanced replication index,
`set safe_to_bootstrap: 1` in the file `grastate.dat` in the data directory.
You can use `SHOW GLOBAL STATUS LIKE 'wsrep_last_committed';` to find out the
sequence number of the last committed transaction. Or, if MySQL is down, use
`mysqld_safe --wsrep-recover`. This command prints the recovered position.
Once you have found the most advanced node, start that node using
`/etc/init.d/mysql bootstrap-pxc`. Bring back one node at a time and watch
the logs. If a SST is required, the first node can only serve as a donor for
one node a time.

See the documentation of the safe to bootstrap feature. Similar to restoring
from backup, restarting the entire cluster is an operation that deserves
practice. See the [documentation](http://galeracluster.com/2016/11/introducing-the-safe-to-bootstrap-feature-in-galera-cluster/)
of this feature.

