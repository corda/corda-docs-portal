---
aliases:
- /releases/release-1.0/upgrade-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-upgrade-notes
    parent: cenm-1-0-operations
    weight: 170
tags:
- upgrade
- notes
title: Upgrading Corda Enterprise Network Manager
---


# Upgrading Corda Enterprise Network Manager

These notes provide instructions for upgrading your network management (Doorman, Network Map or Revocation) service or
signing service from previous versions to the newest version. Please consult the relevant release notes of the release
in question. If not specified, you may assume the versions you are currently using are still in force.

We also strongly recommend cross referencing with the [Changelog](changelog.md) to confirm changes.



## 0.3+ to 1.0


* **SQL Server**If you’re currently using Microsoft SQL server then, in previous versions of CENM, this worked out of the
box because the JDBC driver jar was shipped as part of the CENM distributable. This is no longer the case
as CENM expands to support more databases it becomes impractical to do this, it also allows upgrading the
driver version to be done without shipping a new version of CENM.Using the new database configuration section, you should configure you persistence layer as follows:


## 0.2.X to 0.3

The major change in 0.3 was the separation of the Network Map and Doorman database schemas. Prior to the schema
separation change, the Network Map heavily utilised the Doorman DB tables. To upgrade a 0.2.X Doorman and Network Map,
the data should first be migrated.


### Migration Of Existing Data

To upgrade an existing Doorman or Network Map instance, a new DB instance must first be created for the service to use.
Once this has been done the following steps should be followed to upgrade the service:


* Stop the current service to prevent new information being persisted to the old DB.
* Use the 0.3 utility jar to migrate the data from the old DB to the new DB.
* Swap out the old jar for the new 0.3 ENM jar and updated the service configuration to point to the new DB.
* Restart the service.

For example for the Doorman service:

![doorman migration](/en/images/doorman-migration.png "doorman migration")
These steps should be followed for both the Doorman and Network Map services. This step is *non-destructive* - it
should leave the old DB untouched, only copying the data across to the new DBs. Once both services have been migrated
via the above steps they should be fully functional:

![separated services](/en/images/separated-services.png "separated services")

### Other Required Changes

Separation of the schemas has also introduced some necessary modifications to existing processes and configuration
files. Most Notably:


#### Network Map to Doorman/Revocation communication configuration needs to be added for private networks and certificate revocation checking

If a node is a member of a private network, the current implementation of Corda only passes the node’s private network
id during its registration request to the Doorman (if configured on the node side). A consequence of this design and the
separation of Doorman and the Network Map service is that when a node submits its NodeInfo to a network map instance,
the network map instance needs to communicate with the Doorman service as it can no longer do the direct lookup of a
node’s private network membership from within the Doorman DB. This is facilitated via a new internal *ENM server* that
lives within each ENM service.

In case of a deployment scenario involving ENM upgrade from version prior to 0.3, the configuration file for the
Network Map service can be automatically upgraded using the config upgrader tool or the `--config-is-old` flag.
In the case of the Network Map service, the config parameters `privateNetworkAutoEnrolment` and `checkRevocation`
are defaulted to false, therefore switching this behaviour off. This is because the exact endpoints for the Doorman
and Revocation services cannot be known by the upgrader.


{{< warning >}}
If you require private network functionality or node certificate revocation checking then the configuration
should be updated to include the appropriate settings. See the *Doorman & Revocation Communication* section
of the [Network Map Service](network-map.md) doc for more information.

{{< /warning >}}



#### The Network Map signing service requires a configuration update to specify communication the Network Map service

The release modifies the Network Map Signing Service to request data through the Network Map service rather than going
directly to the database. Therefore the configuration needs to change to remove the redundant DB configuration and
instead adding the service endpoint. As this information cannot be known by the config upgrader, this has to be added
manually. See [Signing Service](signing-service.md) for more information on how to configure this.


#### The Certificate Revocation Request service requires a configuration update to specify communication the Revocation service

Similarly to above, the CRR Signing Service now pulls data through the Revocation service and therefore requires a
configuration modification. See [Signing Service](signing-service.md) for more information on how to configure this.


#### Setting the network parameters requires passing the root certificate

When setting network parameters, the Network Map service cannot validate the proposed notary certificates using the Doorman DB.
Hence the trusted root certificate now needs to be passed during setting of parameters.
See the “Setting the Network Parameters” section of the [Network Map Service](network-map.md) doc for more information.


## 0.1 to 0.2.1

The major change from 0.1 to 0.2+ was the support of an arbitrary length PKI hierarchy. As a result, many of the
configuration parameters for the network management and signing service were changed. 0.2.1 is very similar to 0.2,
but comes with backward compatibility along with a configuration upgrade tool.

There are two ways to upgrade your old 0.1 network services environment:


### Without Upgrading Your Configuration

The 0.2.1 Doorman/Network Map Service and Signing Service JARs will work in place of their 0.1 counterparts, but
require an additional `--config-is-old` command line flag to be passed upon startup. This allows you to use you old
configuration files without and further steps. For example:

```bash
java -jar doorman-0.1.jar --config-file doorman-0.1.conf --config-is-old
```


### Upgrading Your Configuration File

You can also use the configuration file upgrade tool to create a new config file from your old 0.1 file.

The new JAR can then be run with the new configuration file with no extra steps or command line arguments.


## 0.2(.0) to 0.2.1


* **Auto Enrolment in Private Networks**To support automatic enrolment of nodes within a Private Network a new column has been added to the `private-networks` table
to facilitate indication as to whether that private network should allow for automatic registration. This task will handled
automatically via liquibase if “run_migration” is set when starting the 0.2.1 `doorman.jar`.

