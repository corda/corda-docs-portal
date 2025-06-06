---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-12:
    parent: corda-enterprise-4-12-corda-nodes-notary-config
tags:
- installing
- notary
- service
title: Configuring the notary worker nodes
weight: 2
---

# Configuring the notary worker nodes

In configuring the notary worker nodes, please note the following:

* The X500 name of the notary service is configured in `notary.serviceLegalName`.
* Put the IP address or host name of the nearest shared DB server first in the JDBC
URL. When running a DB node and a notary worker node on a single machine, list the
local IP first
* In addition to the connection to the shared DB holding the notary state,
each notary worker needs to have access to its own local node DB. See the
*dataSourceProperties* section in the configuration file
* Omit `compatibilityZoneURL` and set `devMode = true` when using the bootstrapper
* When using CockroachDB, set `generateNativeSql = true` in the JPA block. This guarantees the best performance.
* If using load balancers in front of Cockroach DB nodes, set `maxLifetime` in the `jpa/dataSourceProperties` block. Use a sensible value in milliseconds. A value of `maxLifetime=600000` is equivalent to 10 minutes.
  * The value should be less than the load balancer idle timeout. This avoids false Hibernate warnings about closed connections.

The configuration below will result in the JPA notary implementation being used:

{{< tabs name="tabs-1" >}}
node.conf

{{% tab name="kotlin" %}}
```kotlin
notary {
  jpa {
    connectionRetries={{ number of database replicas }}
    // Only required if using CockroachDB.
    generateNativeSql = true

    // Only required if the schema isn't the default schema of the user.
    database.schema = {{ schema name, e.g. corda_adm }}

    dataSourceProperties {
      autoCommit="false"
      jdbcUrl="jdbc:dbidentifier://{{ [IP1]:[Port1],[IP2]:[Port2],[IP3]:[Port3] }}/{{ DB name, e.g. corda }}"
      username={{ DB username }}
      password={{ DB password }}
      // Only required if using CockroachDB.
      maxLifetime=600000
    }
    database {
      validateSchema = true
    }
  }
  validating=false
  // Only required for an HA notary.
  serviceLegalName="O=HA Notary, C=GB, L=London"
}

compatibilityZoneURL = "https://example.com:1300"
devMode = false

rpcSettings {
  address : "localhost:18003"
  adminAddress : "localhost:18004"
}
keyStorePassword = ""
trustStorePassword = ""
p2pAddress : "{{ fully qualified domain name, e.g. host.example.com (or localhost in development) }}:{{ P2P port }}"

rpcUsers=[]
myLegalName : "O=Worker 1, C=GB, L=London"

// R3 recommends using Postgres for the node database, or an other supported
// database that you already have set up. Note that the notarised states
// are written to the shared notary database configured in `notary.jpa`.
dataSourceProperties = {
  dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
  dataSource.url = "jdbc:postgresql://[HOST]:[PORT]/postgres"
  dataSource.user = [USER]
  dataSource.password = [PASSWORD]
}
database = {
  schema = [SCHEMA]
}
jarDirs = [PATH_TO_JDBC_DRIVER_DIR]

```
{{% /tab %}}




[node.conf](../resources/node.conf) | ![github](/images/svg/github.svg "github")


{{< /tabs >}}

See [Node configuration]({{< relref "../node/setup/corda-configuration-file.md" >}}) for a complete reference.


## MySQL notary (deprecated)

The configuration below will result in the MySQL notary being used. Note the lack of
the `jpa` configuration tag and the presence of the `mysql` configuration tag. Only the
`notary` tag is included in this excerpt - the remainder of the configuration file does not
change.

{{< tabs name="tabs-2" >}}
percona.conf

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
```
{{% /tab %}}




[percona.conf](../resources/percona.conf) | ![github](/images/svg/github.svg "github")



{{< /tabs >}}


## Configuration obfuscation

Corda Enterprise comes with a tool for obfuscating secret values in configuration files, which is strongly recommended for production deployments.
For a notary worker node, the database IP addresses, database user credentials, `keyStore` and `trustStore` password fields in
the configuration file should be obfuscated. Usage instructions can be found on the [Configuration obfuscator]({{< relref "../tools-config-obfuscator.md" >}}) page.

Note that configuration obfuscation can be used with any notary.

Your configuration should look something like this:

```kotlin
notary {
  [jpa or mysql] {
      connectionRetries=[NUMBER_OF_REPLICAS]
      dataSource {
          autoCommit="false"
          jdbcUrl="<encrypt{jdbc connection string}>"
          username=[USER_NAME]
          password="<encrypt{your-data-source-password}>"
      }
  }
  validating=false
  serviceLegalName="O=HA Notary, C=GB, L=London"
}

...

keyStorePassword = "<encrypt{your-key-store-password}>"
trustStorePassword = "<encrypt{your-trust-store-password}>"

...

dataSourceProperties = {
    dataSourceClassName = "org.postgresql.ds.PGSimpleDataSource"
    dataSource.url = "jdbc:postgresql://[HOST]:[PORT]/postgres"
    dataSource.user = [USER_NAME]
    dataSource.password = "<encrypt{your-data-source-password}>"
}
```


## Obtaining the notary service identity

The notary service is registered with the CENM identity service using the registration tool as documented in [notary registration]({{< relref "../ha-utilities.md#notary-registration" >}}).
Once the service is registered, each worker node is registered using the `initial-registration` process. See [joining a compatibility zone]({{< relref "../network/joining-a-compatibility-zone.md" >}}).
