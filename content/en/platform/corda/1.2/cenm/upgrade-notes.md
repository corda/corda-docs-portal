---
aliases:
- /releases/release-1.2/upgrade-notes.html
- /docs/cenm/head/upgrade-notes.html
- /docs/cenm/upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-upgrade-notes
    parent: cenm-1-2-cenm-releases
    weight: 180
    name: Upgrading CENM
tags:
- upgrade
- notes
title: Upgrading the Network Manager
---

# Upgrading Corda Enterprise Network Manager

This topic describes how to upgrade CENM from v1.1.x and v1.2.x to the latest version of v1.2, including the following services:

- Identity Manager Service (formerly Doorman)
- Network Map Service
- Signing Service
- Zone Service
- Auth Service
- Angel Service

The topic also includes legacy upgrade instructions for:

- v1.0 to v1.1 or v1.2
- v0.3 or greater to v1.0
- v0.2.x to v0.3
- v0.1 to v0.2.1
- v0.2(.0) to v0.2.1

Also see the relevant [CENM Release Notes]({{< relref "release-notes.md" >}}) of the release in question. If not specified, you may assume the versions you are currently using are still in force.

{{< warning >}}
Before you start the upgrade, you must consult the above release notes to confirm all changes between releases.
{{< /warning >}}

## 1.2 to 1.2.1

**Identity Manager Service**

The release includes changes to database schemas (see [Changelog]({{< relref "changelog.md" >}})) for Oracle databases;
new columns are created automatically upon each service start-up.
Ensure the Identity Manager Service is configured to perform this migration
by setting the `runMigration` property to `true`.

The upgrade process is otherwise just a drop-in replacement of the existing JAR files with `<service>-1.2.1.jar`.
Ensure you stop the service before replacing the JAR files.
Ensure that there are no orphan processes running after shout down.

## 1.1 to 1.2.1

 See the upgrade note for 1.1 to 1.2 below.

## 1.1 to 1.2

The release includes changes to database schemas (see [Changelog]({{< relref "changelog.md" >}})); new columns are created automatically
upon each service startup. Ensure the Identity Manager and Network Map are configured to perform this migration
by setting `runMigration` property to `true`.

The upgrade process is otherwise just a drop-in replacement of the existing JARs with `<service>-1.2.jar`.
Ensure you stop the services before replacing the JAR files.
Network Map and Signer services may not shut down properly when using shell command `shutdown`, ensure that there are no
orphan processes running after shout down. This may specifically impact the services using H2 database,
as an orphan process locks a H2 database file.

## 1.2.1 to 1.2.2

The upgrade process for 1.2.1 to 1.2.2 is a drop-in replacement of the existing JAR files with ``<service>-1.2.2.jar``.

## 1.2 to 1.2.1

 **Identity Manager**

  The release includes changes to database schemas (see [Changelog]({{< relref "../../1.2/cenm/changelog.md" >}}) for Oracle databases;
  new columns are created automatically upon each service start-up.
  Ensure the Identity Manager is configured to perform this migration
  by setting ``runMigration`` property to ``true``.

  The upgrade process is otherwise just a drop-in replacement of the existing JAR files with ``<service>-1.2.1.jar``.
  Ensure you stop the service before replacing the JAR files.
  Ensure that there are no orphan processes running after shout down.

## 1.1 to 1.2.1

 See the upgrade note for 1.1 to 1.2.

## 1.1 to 1.2

The release includes changes to database schemas (see [Changelog]({{< relref "../../1.2/cenm/changelog.md" >}}); new columns are created automatically
upon each service start-up. Ensure the Identity Manager and Network Map are configured to perform this migration
by setting `runMigration` property to `true`.

The upgrade process is otherwise just a drop-in replacement of the existing JAR files with `<service>-1.2.jar`.
Ensure you stop the services before replacing the JAR files.
Network Map and Signing Services may not shut down properly when using shell command `shutdown`, ensure that there are no
orphan processes running after shut down. This may specifically impact the services using H2 database,
as an orphan process locks a H2 database file.


## 1.0 to 1.2

See the upgrade note for 1.1 to 1.2.

## 1.0 to 1.1

{{< note >}}
Use latest patched version (1.1.1 or higher) of the services (JAR/ZIP files) instead of 1.1 version.
{{< /note >}}

### Identity Manager, Network Map and Signing Service

Ensure Identity Manager and Network Map Services will be configured to upgrade the databases upon start-up.
In the configuration files of the Identity Manager Service and the Network Map Service, set `runMigration` property to `true` - for example:

```guess
database {
    runMigration = true
    ...
 }
```

This step doesn’t relate to Signing Service as it doesn’t use a database. The upgrade process is just a drop-in replacement of the existing JAR files with `<service>-1.1.1.jar`.
Ensure the services are not running before replacing the JAR files.

### Dynamic loading of HSM JAR files

CENM 1.1 supports multiple HSMs, however due to to the proprietary nature of the HSM libraries, the release does
not work with these HSMs "out of the box". The user must provide the relevant libraries and reference them in the
configuration of the relevant component (Signing Service or PKI Tool). For more information, see [Signing services]({{< relref "signing-service.md" >}}).
and [Public key infrastructure (PKI) tool]({{< relref "pki-tool.md" >}}) for more information.

## 0.3+ to 1.0

CENM 1.0 introduces an overhauled Signing Service, official PostgreSQL support, and re-worked configuration files for
Identity Manager (formerly Doorman) and Network Map Services.


### Identity Manager service

The Doorman is now known as the Identity Manager Service. To upgrade, replace the Doorman JAR file with the Identity
Manager Service JAR file, and run the service, having migrated the configuration file to be CENM 1.0 compliant. The configuration file
has been re-worked - as a result, the service is no longer backward-compatible with pre-1.0 configuration files.
Currently, configuration file migrations must be performed manually. Refer to the Identity Manager Service documentation
for further guidance.

### Network Map service

The Network Map Service upgrade process is similar to that for the Identity Manager Service. Replace the existing Network Map Service JAR file
with its CENM 1.0 counterpart, and restart the service. The Network Map Service configuration file has also been re-worked.
Configurations predating CENM 1.0 must be migrated to be compatible with CENM 1.0. Refer to the Network Map Service documentation for further guidance.

### Signing Service

The Signing Service is now a long-running service in the same vein as the Identity Manager and Network Map,
as opposed to a command-line tool with one-shot execution. Signing tasks are configurable via the configuration file
supplied to the new Signing Service on start-up. Configure the Signing Service to perform any existing
signing tasks by referencing the Signing Service documentation.

### SQL Server

If you’re currently using Microsoft SQL server then, in previous versions of CENM, this worked out of the
box because the JDBC driver JAR was shipped as part of the CENM distributable. This is no longer the case
as CENM expands to support more databases it becomes impractical to do this, it also allows upgrading the
driver version to be done without shipping a new version of CENM.Using the new database configuration section, you should configure you persistence layer as follows:

```guess
database {
    ...
    jdbcDriver = "/path/to/sqljdbc_7.2/enu/mssql-jdbc-7.2.2.jre8.jar"
    driverClassName = "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    ...
}
```


### PostgreSQL

PostgreSQL is now officially supported as a tested and verified alternative.To use PostgreSQL, configure the persistence layer as follows:

```guess
database {
    ...
    jdbcDriver = "/path/to/postgresql-42.2.5.jar"
    driverClassName = "org.postgresql.Driver"
    ...
}
```


### Configuration files

CENM 1.0 Identity Manager and Network Map Services are not backward-compatible with configuration files for Doorman and Network Map Service versions 0.x.
Version 0.2.2 and 0.3 / 0.4 configuration files can be migrated to CENM 1.0 using the [configuration migration tool]({{< relref "tool-config-migration.md" >}}).
Using the generated 1.0 configurations, the services can be upgraded by stopping the services, swapping out the JAR file and configuration files, and restarting the services.


## 0.2.x to 0.3

The major change in 0.3 was the separation of the Network Map and Doorman database schemas. Prior to the schema
separation change, the Network Map heavily utilised the Doorman database tables. To upgrade a 0.2.X Doorman and Network Map,
the data should first be migrated.


### Migration Of Existing Data

To upgrade an existing Doorman or Network Map Service, a new database instance must first be created for the service to use.
Once this has been done the following steps should be followed to upgrade the service:


* Stop the current service to prevent new information being persisted to the old database.
* Use the 0.3 utility JAR to migrate the data from the old database to the new database.
* Swap out the old JAR for the new 0.3 CENM jar and updated the service configuration to point to the new database.
* Restart the service.

For example for the Doorman service:

![doorman migration](/en/images/doorman-migration.png "doorman migration")

These steps should be followed for both the Doorman and Network Map Services. This process is *non-destructive* - it
should leave the old database untouched, only copying the data across to the new databases. Once both services have been migrated
via the above process they will be fully functional:

![separated services](/en/images/separated-services.png "separated services")

### Other required changes

Separation of the schemas has also introduced some necessary modifications to existing processes and configuration
files. Most Notably:


#### Network Map to Doorman/Revocation communication configuration needs to be added for private networks and certificate revocation checking

If a node is a member of a private network, the current implementation of Corda only passes the node’s private network
id during its registration request to the Doorman (if configured on the node side). A consequence of this design and the
separation of Doorman and the Network Map Service is that when a node submits its node info to a Network Map Service,
the Network Map Service needs to communicate with the Doorman service as it can no longer do the direct lookup of a
node’s private network membership from within the Doorman database. This is facilitated via a new internal *CENM server* that
lives within each CENM service.

In case of a deployment scenario involving CENM upgrade from version prior to 0.3, the configuration file for the
The Network Map Service can be automatically upgraded using the configuration upgrade tool or the `--config-is-old` flag.
In the case of the Network Map Service, the configuration parameters `privateNetworkAutoEnrolment` and `checkRevocation`
are defaulted to false, therefore switching this behaviour off. This is because the exact endpoints for the Doorman
and Revocation services cannot be known by the upgrader.


{{< warning >}}
If you require private network functionality or node certificate revocation checking then the configuration
should be updated to include the appropriate settings. See the *Doorman & Revocation Communication* section
of the [Network Map service]({{< relref "network-map.md" >}}) document for more information.

{{< /warning >}}



#### The Network Map Signing Service requires a configuration update to specify communication with the Network Map Service

The release modifies the Network Map Signing Service to request data through the Network Map Service rather than going
directly to the database. Therefore the configuration needs to change to remove the redundant database configuration and
instead adding the service endpoint. As this information cannot be known by the configuration upgrader, this has to be added
manually. See [Signing services]({{< relref "signing-service.md" >}}) for more information on how to configure this.


#### The Certificate Revocation Request service requires a configuration update to specify communication the Revocation service

Similarly to above, the CRR Signing Service now pulls data through the Revocation service and therefore requires a
configuration modification. See [Signing services]({{< relref "signing-service.md" >}}) for more information on how to configure this.


#### Setting the network parameters requires passing the root certificate

When setting network parameters, the Network Map Service cannot validate the proposed notary certificates using the Doorman database.
Hence the trusted root certificate now needs to be passed during setting of parameters.
See the “Setting the Network Parameters” section of the [Network Map service]({{< relref "network-map.md" >}}) document for more information.


## 0.1 to 0.2.1

The major change from 0.1 to 0.2+ was the support of an arbitrary length PKI hierarchy. As a result, many of the
configuration parameters for the network management and Signing Service were changed. 0.2.1 is very similar to 0.2,
but comes with backward compatibility along with a configuration upgrade tool.

There are two ways to upgrade your old 0.1 network services environment:


### Without upgrading your configuration

The 0.2.1 Doorman/Network Map Service and Signing Service JAR files will work in place of their 0.1 counterparts, but
require an additional `--config-is-old` command-line flag to be passed upon start-up. This allows you to use you old
configuration files without any further steps. For example:

```bash
java -jar doorman-0.1.jar --config-file doorman-0.1.conf --config-is-old
```


### Upgrading your configuration file

You can also use the configuration file upgrade tool to create a new configuration file from your old 0.1 file.

The new JAR file can then be run with the new configuration file with no extra steps or command-line arguments.


## 0.2(.0) to 0.2.1


* **Auto Enrolment in Private Networks**To support automatic enrolment of nodes within a Private Network a new column has been added to the `private-networks` table
to facilitate indication as to whether that private network should allow for automatic registration. This task will handled
automatically via liquibase if “run_migration” is set when starting the 0.2.1 `doorman.jar`.
