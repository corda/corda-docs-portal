---
aliases:
- /upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-upgrade-notes
    parent: cenm-1-4-operations
    weight: 170
tags:
- upgrade
- notes
title: Upgrading Corda Enterprise Network Manager
---


# Upgrading Corda Enterprise Network Manager

This document provides instructions for upgrading your network management suite - Identity Manager Service (formerly
Doorman), Network Map Service, Signing Service, Zone Service, Auth Service, Angel Service - from previous versions to the newest version. Please consult the relevant [release notes](release-notes.md) of the release in question. If not specified, you may assume the versions you are currently using are still in force.

{{< warning >}}
Before you start the upgrade, you must consult the [CENM Release Notes](release-notes.md) to confirm all changes between releases.
{{< /warning >}}

## 1.3.x to 1.4

CENM 1.4 includes a few changes and improvements that require some additional upgrade steps, as described below.

The general procedure for upgrading from CENM 1.3 to CENM 1.4 is as follows:

1. Stop all CENM 1.3 services.
2. To prevent picking up old Signing Service configurations by the Angel Service, remove or rename all configuration files that have to be updated (see the sections below).
3. Update Signing Service configuration files, as [described below](#manual-update-of-all-existing-signing-service-configurations). Note that there is a change in the way `subZoneID` is set in Signing Service configurations, as [described below](#change-in-setting-subzoneid-in-signing-service-configurations).
4. Replace the `.jar` files for all services with the latest CENM 1.4 `.jar` files. **ImportantL** In CENM 1.4, the FARM Service has been renamed to "Gateway Service", so the FARM Service `.jar` file used in CENM 1.3 should be replaced with the Gateway Service `.jar` file used in CENM 1.4.
5. Start the Auth Service, the Zone Service, and the Gateway Service. **Important:** The Zone Service requires the `--run-migration` option to be set to `true`, as [described below](#zone-service-database-migration).
6. Submit the updated configurations to the Zone Service.
7. Start the Identity Manager Service, the Signing Service, and the Network Map Service.

### Zone Service database migration

If you are upgrading to CENM 1.4 from CENM 1.3, you **must** set `runMigration = true` in the database configuration. This is required due to a change in the Zone Service database schema - a new column in the database tables `socket_config` and `signer_config` called `timeout` is used to record the new optional `timeout` parameter values used in `serviceLocations` configuration blocks (Signing Services) and `identityManager` and `revocation` configuration blocks (Network Map Service). This value can remain `null`,
in which case the default 30 seconds timeout will be used wherever applicable.

An example follows below:

```
database = {
  driverClassName = "org.h2.Driver"
  user = "testuser"
  password = "password"
  url = "jdbc:h2:file:/etc/corda/db;DB_CLOSE_ON_EXIT=FALSE;LOCK_TIMEOUT=10000;WRITE_DELAY=0;AUTO_SERVER_PORT=0"
  runMigration = true
}
```

### Signing Service configuration changes

In CENM 1.3 (and older versions), `subZoneID` was defined in Signing Service configurations as part of the service location alias (`serviceLocationAlias`), as shown below:

```
serviceLocations.network-map-<subzone ID>
```

And:

```
signers.NetworkMap.serviceLocationAlias = "network-map-<subzone ID>"
signers.NetworkParameters.serviceLocationAlias = "network-map-<subzone ID>"
```

In CENM 1.4, you must define `subZoneID` as new property value, as follows:

```
signers.NetworkMap.subZoneId = <subzone ID>
signers.NetworkParameters.subZoneId = <subzone ID>
```

### Manual update of all existing Signing Service configurations

The SMR (Signable Material Retriever) Service, which prior to CENM 1.4 was used to handle plug-ins for signing data, has been replaced by a plug-in loading logic inside the Signing Service. As a result, **all users must update their existing Signing Service configuration** when upgrading to CENM 1.4.

To update your Signing Service configuration:

1. Remove the `serviceLocationAlias` property from the signing task.
2. Remove the `serviceLocations` property and move the locations defined there to `serviceLocation` properties inside each signing task. Note that as a result Network Parameters signing tasks and Network Map signing tasks will have the same `serviceLocation` property.
3. Remove the `caSmrLocation` property.
4. Remove the `nonCaSmrLocation` property.
5. Configure the `pluginClass` and `pluginJar` properties inside each signing task to use the following structure:

```
plugin {
pluginClass =
pluginJar
}
```

## 1.2.x to 1.3

CENM 1.3 introduces a significant number of services. You should upgrade to CENM 1.2.2 before upgrading to 1.3.
The key steps for the upgrade are:

1. Generate new certificates for [FARM](gateway-service.md), [Auth](auth-service.md), and [Zone](zone-service.md) Services.
2. Generate a JWT token key pair for Auth Service.
3. Deploy FARM Service to provide a gateway between the CLI tool and the back-end services.
4. Deploy Auth Service to provide user authentication and authorisation to other services.
5. Deploy Zone Service to store configurations for the Identity Manager, Network Map, and Signing Services.
6. Create users in the Auth Service, for zone and subzone management.
7. Edit [Identity Manager Service](identity-manager.md), [Network Map Service](network-map.md), and [Signing Service](signing-service.md) configurations to remove shell access and add an admin listener configuration.
8. Edit the [Signing Service](signing-service.md) configuration so that signing tasks refer to [service aliases](signing-service.md#direct-cenm-service-locations) generated by the Zone Service.
9. Set Identity Manager Service configuration in the [Zone Service](zone-service.md).
10. Set Network Map Service configuration(s) in the Zone Service.
11. Set Signing Service configuation in the Zone Service.
12. Update existing service deployments.
13. Add [Angel Services](angel-service.md) to Identity Manager, Network Map, and Signing Services, to fetch configurations from the Zone
   Service.

### Generating certificates and JWT

You must generate SSL key pairs and certificates for the new services before deploying them.
You can do this using the PKI tool, and it is best to replace the
SSL certificates and keys for all services during this process. A draft PKI tool configuration
for generating the full SSL hierarchy is provided under [config-samples/upgrade-pki-tool-1.3.conf](config-samples/upgrade-pki-tool.conf/).

{{% important %}}
You must replace the `subject` and `crlDistributionUrl` entries in this configuration with values
appropriate to your deployment.
{{% /important %}}

To generate the JWT, refer to the [Auth Service](auth-service.md) documentation.

The generated keys and certificates will then need to be distributed to the service hosts,
replacing the existing SSL (but not network trust root or other signing key/certificates).

### Deploying Farm, Auth, and Zone Services

To deploy the new services, follow the guides in the service documentation:

* [FARM Service](gateway-service.md)
* [Auth Service](auth-service.md)
* [Zone Service](zone-service.md)

{{< note >}}
You should deploy two FARM Service instances - one for general access, accessible from user
systems, and a second one in the secure network alongside the Signing Service.
{{< /note >}}

### Create user(s)

The [Auth Service](auth-service.md) has an initial user who can manage users, however
for separation of responsibility this user cannot manage services. Therefore you
need to create user(s) for configuring the services, as well as potentially users
to operate the services once they are configured, such as signing certificates.

### Replace shell with Admin RPC

The legacy shell interface is not compatible with the new user authentication model,
and must be removed from the existing service configurations before adding them to
the Zone Service.

At this stage you should fetch service configurations from each host, as you'll be
setting them on the Zone Service after editing.

To replace the shell, configure an admin RPC listener on the Identity Manager,
Network Map, and Signing Services. Detailed instructions are provided in the documentation for each
service.

### Standardise service aliases

Service locations in the Signing Service configuration are provided automatically by the
Zone Service in CENM 1.3. However, to enable this, the service aliases have strictly defined
formats. You must update the task configurations to refer to service aliases matching
these names. The names are specified in [service aliases](signing-service.md#direct-cenm-service-locations).

### Push configurations to Zone Service

Once you finish updating the configurations, you must set them on the Zone Service. An example of
how to do this is shown below, but please see the CENM CLI tool documentation for details on what these
commands do, and adapt them to your deployment:

```bash
# Login
./cenm context login https://<Zone Service> -u <user> -p <password>
# Set the Identity Manager's external address
./cenm identity-manager config set-address -a=<Identity Manager Service>
# Set the Identity Manager config
./cenm identity-manager config set -f config/identitymanager.conf --zone-token
# Create a new subzone
./cenm zone create-subzone --config-file=config/networkmap.conf --label=Subzone --label-color="#000000" --network-map-address=<Network Map Service> --network-parameters=config/params.conf
# Set the Network Map configuration for a subzone (1 was taken from the response to the create-subzone command)
./cenm netmap config set -s 1 -f config/networkmap.conf --zone-token
# Set the Signer configuration last, as it depends on the first two service's locations for it to be complete
./cenm signer config set -f config/signer.conf --zone-token
```

### Update existing services

At this point you should shut down the previous services and replace their `.jar` files with `<service>-1.3.0.jar`.
Do not start them quite yet, as they should be managed by the Angel Service. Add the `angel-1.3.0.jar` file to
each managed service deployment (Identity Manager, Network Map, Zone), and configure the service start-up
to be via the Angel Service. Details on the arguments to the Angel Service are covered in the
[Angel Service documentation](angel-service.md).

## 1.2.1 to 1.2.2

The upgrade process for 1.2.1 to 1.2.2 is a drop-in replacement of the existing `.jar` files with ``<service>-1.2.2.jar``.

## 1.2 to 1.2.1

 **Identity Manager**

  The release includes changes to database schemas (see [Changelog](../1.2/changelog.md)) for Oracle databases;
  new columns are created automatically upon each service start-up.
  Ensure the Identity Manager is configured to perform this migration
  by setting ``runMigration`` property to ``true``.

  The upgrade process is otherwise just a drop-in replacement of the existing `.jar` files with ``<service>-1.2.1.jar``.
  Ensure you stop the service before replacing the `.jar` files.
  Ensure that there are no orphan processes running after shout down.

## 1.1 to 1.2.1

See the upgrade note for 1.1 to 1.2.

## 1.1 to 1.2

The release includes changes to database schemas (see [Changelog](../1.2/changelog.md)); new columns are created automatically
upon each service start-up. Ensure the Identity Manager and Network Map are configured to perform this migration
by setting `runMigration` property to `true`.

The upgrade process is otherwise just a drop-in replacement of the existing `.jar` files with `<service>-1.2.jar`.
Ensure you stop the services before replacing the `.jar` files.
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

This step doesn’t relate to Signing Service as it doesn’t use a database. The upgrade process is just a drop-in replacement of the existing `.jar` files with `<service>-1.1.1.jar`.
Ensure the services are not running before replacing the `.jar` files.

### Dynamic loading of HSM `.jar` files

CENM 1.1 supports multiple HSMs, however due to to the proprietary nature of the HSM libraries, the release does
not work with these HSMs "out of the box". The user must provide the relevant libraries and reference them in the
configuration of the relevant component (Signing Service or PKI Tool). For more information, see [Signing Services](signing-service.md).
and [Public Key Infrastructure (PKI) Tool](pki-tool.md) for more information.

## 0.3+ to 1.0

CENM 1.0 introduces an overhauled Signing Service, official PostgreSQL support, and re-worked configuration files for
Identity Manager (formerly Doorman) and Network Map Services.


### Identity Manager Service

The Doorman is now known as the Identity Manager Service. To upgrade, replace the Doorman `.jar` file with the Identity
Manager Service `.jar` file, and run the service, having migrated the configuration file to be CENM 1.0 compliant. The configuration file
has been re-worked - as a result, the service is no longer backward-compatible with pre-1.0 configuration files.
Currently, configuration file migrations must be performed manually. Refer to the Identity Manager Service documentation
for further guidance.

### Network Map Service

The Network Map Service upgrade process is similar to that for the Identity Manager Service. Replace the existing Network Map Service `.jar` file
with its CENM 1.0 counterpart, and restart the service. The Network Map Service configuration file has also been re-worked.
Configurations predating CENM 1.0 must be migrated to be compatible with CENM 1.0. Refer to the Network Map Service documentation for further guidance.

### Signing Service

The Signing Service is now a long-running service in the same vein as the Identity Manager and Network Map,
as opposed to a command-line tool with one-shot execution. Signing tasks are configurable via the configuration file
supplied to the new Signing Service on start-up. Configure the Signing Service to perform any existing
signing tasks by referencing the Signing Service documentation.

### SQL Server

If you’re currently using Microsoft SQL server then, in previous versions of CENM, this worked out of the
box because the JDBC driver `.jar` was shipped as part of the CENM distributable. This is no longer the case
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
Version 0.2.2 and 0.3 / 0.4 configuration files can be migrated to CENM 1.0 using the [configuration migration tool](tool-config-migration.md).
Using the generated 1.0 configurations, the services can be upgraded by stopping the services, swapping out the `.jar` file and configuration files, and restarting the services.


## 0.2.X to 0.3

The major change in 0.3 was the separation of the Network Map and Doorman database schemas. Prior to the schema
separation change, the Network Map heavily utilised the Doorman database tables. To upgrade a 0.2.X Doorman and Network Map,
the data should first be migrated.


### Migration Of Existing Data

To upgrade an existing Doorman or Network Map Service, a new database instance must first be created for the service to use.
Once this has been done the following steps should be followed to upgrade the service:


* Stop the current service to prevent new information being persisted to the old database.
* Use the 0.3 utility `.jar` to migrate the data from the old database to the new database.
* Swap out the old `.jar` for the new 0.3 CENM jar and updated the service configuration to point to the new database.
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
of the [Network Map Service](network-map.md) document for more information.

{{< /warning >}}



#### The Network Map signing service requires a configuration update to specify communication with the Network Map Service

The release modifies the Network Map Signing Service to request data through the Network Map Service rather than going
directly to the database. Therefore the configuration needs to change to remove the redundant database configuration and
instead adding the service endpoint. As this information cannot be known by the configuration upgrader, this has to be added
manually. See [Signing Services](signing-service.md) for more information on how to configure this.


#### The Certificate Revocation Request service requires a configuration update to specify communication the Revocation service

Similarly to above, the CRR Signing Service now pulls data through the Revocation service and therefore requires a
configuration modification. See [Signing Services](signing-service.md) for more information on how to configure this.


#### Setting the network parameters requires passing the root certificate

When setting network parameters, the Network Map Service cannot validate the proposed notary certificates using the Doorman database.
Hence the trusted root certificate now needs to be passed during setting of parameters.
See the “Setting the Network Parameters” section of the [Network Map Service](network-map.md) document for more information.


## 0.1 to 0.2.1

The major change from 0.1 to 0.2+ was the support of an arbitrary length PKI hierarchy. As a result, many of the
configuration parameters for the network management and signing service were changed. 0.2.1 is very similar to 0.2,
but comes with backward compatibility along with a configuration upgrade tool.

There are two ways to upgrade your old 0.1 network services environment:


### Without Upgrading Your Configuration

The 0.2.1 Doorman/Network Map Service and Signing Service `.jar` files will work in place of their 0.1 counterparts, but
require an additional `--config-is-old` command-line flag to be passed upon start-up. This allows you to use you old
configuration files without any further steps. For example:

```bash
java -jar doorman-0.1.jar --config-file doorman-0.1.conf --config-is-old
```


### Upgrading Your Configuration File

You can also use the configuration file upgrade tool to create a new configuration file from your old 0.1 file.

The new `.jar` file can then be run with the new configuration file with no extra steps or command-line arguments.


## 0.2(.0) to 0.2.1


* **Auto Enrolment in Private Networks**To support automatic enrolment of nodes within a Private Network a new column has been added to the `private-networks` table
to facilitate indication as to whether that private network should allow for automatic registration. This task will handled
automatically via liquibase if “run_migration” is set when starting the 0.2.1 `doorman.jar`.
