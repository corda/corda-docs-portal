---
aliases:
- /releases/3.0/running-a-notary-cluster/installing-the-notary-service.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-installing-the-notary-service
    parent: corda-enterprise-3-0-introduction
    weight: 1020
tags:
- installing
- notary
- service
title: Setting up the Notary Service
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Setting up the Notary Service

In the previous section of this tutorial we set up a Percona cluster.

On top of the Percona cluster we’re deploying three Corda Enterprise Notary nodes `notary-{1,2,3}`.

If you’re deploying VMs in your environment you might need to adjust the host names accordingly.


## Configuration Files

Below is a template for the notary configuration. Notice the parameters
`rewriteBatchedStatements=true&useSSL=false&failOverReadOnly=false` of the
JDBC URL.  See [Node configuration](../corda-configuration-file.md) for a complete reference.

Put the IP address or host name of the nearest Percona server first in the JDBC
URL. When running a Percona and a Notary replica on a single machine, list the
local IP first.

{{< tabs name="tabs-1" >}}
node.conf

{{% tab name="kotlin" %}}
```kotlin
notary {
  mysql {
      connectionRetries={{ number of Percona nodes }}
      dataSource {
          autoCommit="false"
          jdbcUrl="jdbc:mysql://{{ your cluster IPs }}/{{ DB name, e.g. corda }}?rewriteBatchedStatements=true&useSSL=false&failOverReadOnly=false"
          username={{ DB username }}
          password={{ DB password }}
      }
  }
  validating=false
  serviceLegalName="O=HA Notary, C=GB, L=London"
}

devMode = true

rpcSettings {
      address : "localhost:18003"
      adminAddress : "localhost:18004"
}
keyStorePassword = ""
trustStorePassword = ""
p2pAddress : "{{ fully qualified domain name, e.g. host.example.com (or localhost in development) }}:{{ P2P port }}"

rpcUsers=[]
myLegalName : "O=Replica 1, C=GB, L=London"

// We recommend using Postgres for the node database, or an other supported
// database that you already have set up. Note that the notarised states
// are written to the MySQL database configured in `notary.mysql`.
dataSourceProperties = {
    dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
    dataSource.url = "jdbc:postgresql://[HOST]:[PORT]/postgres"
    dataSource.user = [USER]
    dataSource.password = [PASSWORD]
}
database = {
    transactionIsolationLevel = READ_COMMITTED
    schema = [SCHEMA]
}
jarDirs = [PATH_TO_JDBC_DRIVER_DIR]

```
{{% /tab %}}


{{< /tabs >}}

{{< note >}}
Omit `compatibilityZoneURL` and set `devMode = true` when using the bootstrapper.

{{< /note >}}

## Next Steps



* [Using the Bootstrapper](installing-the-notary-service-bootstrapper.md)
