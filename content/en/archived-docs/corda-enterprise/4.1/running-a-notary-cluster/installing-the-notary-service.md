---
aliases:
- /releases/4.1/running-a-notary-cluster/installing-the-notary-service.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-installing-the-notary-service
    parent: corda-enterprise-4-1-introduction
    weight: 1020
tags:
- installing
- notary
- service
title: Setting up the Notary Service
---


# Setting up the Notary Service

In the previous section of this tutorial we set up a Percona cluster.

On top of the Percona XtraDB Cluster we’re deploying three notary worker nodes `notary-{1,2,3}` and
a single regular Corda node `node-1` that runs the notary health-check CorDapp.

If you’re deploying VMs in your environment you might need to adjust the host names accordingly.


## Configuration Files

Below is a template for the notary configuration. Notice the parameters
`rewriteBatchedStatements=true&useSSL=false&failOverReadOnly=false` of the
JDBC URL.  See [Node configuration](../corda-configuration-file.md) for a complete reference.

Put the IP address or host name of the nearest Percona server first in the JDBC
URL. When running a Percona and a Notary replica on a single machine, list the
local IP first.

In addition to the connection to the shared Percona DB holding the notary state,
each notary worker needs to have access to its own local node DB. See the
*dataSourceProperties* section in the configuration file.

{{< note >}}
Omit `compatibilityZoneURL` and set `devMode = true` when using the bootstrapper.

{{< /note >}}


## MySQL JDBC Driver

Each worker node requires a MySQL JDBC driver to be placed in the `drivers` directory to be able to communicate with the Percona XtraDB Cluster.
The official driver can be obtained from Maven or the [MySQL Connector/J download page](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-installing.html).


## Next Steps



* [Using the Bootstrapper](installing-the-notary-service-bootstrapper.md)



