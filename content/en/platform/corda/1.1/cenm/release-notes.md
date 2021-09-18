---
aliases:
- /releases/release-1.1/release-notes.html
- /release-notes.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-1:
    identifier: cenm-1-1-release-notes
    parent: cenm-1-1-cenm-releases
    weight: 80
tags:
- release
- notes
title: Release notes
---


# Release notes

## Release 1.1.3

CENM 1.1.3 introduces fixes to known issues in CENM 1.1.

Fixed issues
* Identity Manager upgrade from CENM 0.4:
  * causes JIRA Workflow Plugin to stop existing tickets in 'New' or 'In Progress' status from being progressed
  * prevents rejected records from being cleared by `workflow_*`.
* When multiple users are configured to use the Signing Service, the service authenticates all the credentials before checking whether the threshold is reached, which would result in multiple authentications for every user.
* The process of creating and signing the CRL fails when upgrading from CENM 0.4 if the existing revoked certificates lacked a revocation reason.

## Release 1.1.1

CENM 1.1.1 introduces a fix to a known issue in CENM 1.1.

Fixed issues

Identity Manager upgrade from CENM 0.4 causes JIRA Workflow Plugin to lose all pending tickets.

## Release 1.1

The R3 Network Services team is excited to announce the release of CENM 1.1,
introducing support for a number of additional HSMs as well as adding support for Oracle DB.
For deployments of pre-1.0 CENM a migration tool has been added to rewrite legacy
configurations to be compatible with 1.1.

### Major New Features

**Oracle Database Support**

Support has been added for Oracle DB versions 12cR2 and 11gR2 as a backend data store.
For full setup instructions see [CENM Databases](database-set-up.md).

**Configuration Migration Tool**

To simplify the upgrade process from early versions of CENM a configuration migration tool has been
added. This is intended to upgrade v0.2.2/v0.3+ configurations to v1.1, including both restructuring
changes to the configuration file and updating the value of fields (such as database driver class).
See [Config migration tool](tool-config-migration.md) for details on this tool.

**Hardware Security Module Support**

Support for HSMs has been significantly extended, and as part of this work the HSM Jar files are
now dynamically loaded and should be provided by the user. Support has been added for Azure Key Vault,
as well as for Gemalto and Securosys HSMs in both the PKI Tool and Signing Service.

### Other Improvements

* CENM now supports encryption of passwords in configuration files, using encryption keys derived from
hardware attributes. An obfuscation tool ships with CENM, to process configuration files and encrypt
marked fields. For more details on usage see [Config Obfuscation Tool](config-obfuscation-tool.md).
* Fixed an internal error which occurred when using H2 versions below 1.4.198 due to use of unsupported
lock types.
* Added `run purgeAllStagedNodeInfos` and `run purgeStagedNodeInfo nodeInfoHash: <node_info_hash>` commands
to the Network Map interactive shell, allowing for the moving of nodes out of the staging table and into the
main node info table of the Network Map. This provides a solution to the scenario whereby a node gets stuck
in the staging table (see *Troubleshooting Common Issues* section).
* Simplified configuration by removing configuration options for private network maps. This feature is being
removed in preference of using subzones, and therefore these configuration options merely add complexity.

### Known Issues

* The PKI tool fails if the password for a key store and key are different. This only applies to local key
stores. Please ensure key passwords match the key store password to avoid this issue.
* Logging in case of Gemalto HSM call failures is limited, which complicates diagnosis. This is to be improved in a future version.
* Config migration tool displays configuration output version as 1.0, actual target
is 1.1.
* Config migration tool does not generate a `shell` configuration section, and therefore the generated configurations may not be usable as-is.
This is intentional in order as the operator needs to make decisions on this configuration, for example password.
* PKI tool reports “Error whilst attempt to read config lines.” if it cannot find a configuration file, rather than a more specific error message.

## Release 1.0

R3 and The Network Services team are proud to deliver the inaugural release of the Corda Enterprise
Network Manager version 1.0. The CENM can be used to operate a bespoke Corda network when the requirement
for an entity to be in complete control of the consensus rules, identity, and deployment topology exists.

This is the same software used to operate the global Corda Network on behalf of the Corda
Network Foundation since its launch in 2018.

Please note, whilst this is the first public release of the Corda Enterprise Network Manager, these
release notes and any associated documentation should be read from the perspective of those coming
fresh to the product but also those who are upgrading from pre-release versions.

### Major New Features

**The Signing Service**

The Signing Service is a new addition to the suite of CENM services, sitting alongside the Identity Manager and Network
Map. It provides a network operator with full control over the signing of node identity data (CSRs and CRRs) and global
network data (Network Map and Network Parameters) and includes features such as HSM integration, signing scheduling and
support for multiple Network Map services. See [Signing Service](signing-service.md) to learn more about this service.

**Brand new PKI tooling**

The PKI Tool enables a network operator to easily generate Corda-compliant certificate hierarchy (keys and
certificates) as well as certificate revocation lists. The tool supports both local and HSM key stores and can be
customized with the configuration file. See [Public Key Infrastructure (PKI) Tool](pki-tool.md) to learn about all the features of the PKI Tool.

**Full End to End SSL communication**

All CENM components now communicate over SSL with one another, this completes the removal of the “database as message
queue” of older versions. See [Configuring the ENM services to use SSL](enm-with-ssl.md) for more information.

**Security And Performance Fixes**

### Minor Features

**Postgresql Support**

As well as SQLServer, the CENM suite now supports postgresql as a backend data store.

**Protocol Separation**

In pre release versions of CENM the user information REST endpoints shared a namespace with the core
Corda Network Map protocol. This was done to better draw distinction between the protocol itself as
required by Corda nodes, and the more free-form functionality offered to users. This will allow for future
versioned changes to the protocol without changing that which the Corda nodes depend upon.

### Major New Features

* `/network-map`
* `/network-map-user`

The Signing Service is a new addition to the suite of CENM services, sitting alongside the Identity Manager and Network
Map. It provides a network operator with full control over the signing of node identity data (CSRs and CRRs) and global
network data (Network Map and Network Parameters) and includes features such as HSM integration, signing scheduling and
support for multiple Network Map services. See [Signing Service](signing-service.md) to learn more about this service.

**Epoch Control**

The PKI Tool enables a network operator to easily generate Corda-compliant certificate hierarchy (keys and
certificates) as well as certificate revocation lists. The tool supports both local and HSM key stores and can be
customized with the configuration file. See [Public Key Infrastructure (PKI) Tool](pki-tool.md) to learn about all the features of the PKI Tool.

**Shell**

Migrated the private network management utility tool into the Network Map interactive shell. The new command within the
shell is an interactive command, allowing a user to run the same management tools without having to worry about passing
in a configuration file or remembering the correct start up flag.

**Config Debugability**

Added multi-phase parsing of config files. Parsing and validation errors are now batched before being presented to
the user, eliminating the frustration from having to address errors one by one.

**Security And Performance Fixes**

### Minor Features

**Postgresql Support**

Due to the database schema separation outlined below, the 0.3 release now supports segregated sub zones. That is,
sub-zones of nodes that operate in what appear to the nodes to be isolated networks, with their own notary(ies) and
network parameters. Critically, however, their certificate governance remains under the jurisdiction of a global
Doorman. This way, temporary benefits such as higher privacy, differential network parameters upgrade schedules or use
of temporary private notaries can be delivered. Note that the ability to merge one sub-zone into another is not
currently supported. See the [Sub Zones](sub-zones.md) documentation for more information.

**Protocol Separation**

In pre release versions of CENM the user information REST endpoints shared a namespace with the core
Corda Network Map protocol. This was done to better draw distinction between the protocol itself as
required by Corda nodes, and the more free-form functionality offered to users. This will allow for future
versioned changes to the protocol without changing that which the Corda nodes depend upon.

The two top-level endpoints are now

* `/network-map`
* `/network-map-user`

see [Network Map Overview](network-map-overview.md) for more information.

Another change that is introduced in the newest release is the ability to interact with the Doorman and Network Map
services via a shell. The commands available currently mainly allow an operator to inspect the state of the service,
for example by viewing the current set of nodes within the public network, or viewing the list of Certificate Signing
Requests that are awaiting approval. See the [Embedded Shell](shell.md) documentation for more information.

Added support for overriding the default “increment previous value by 1” behaviour for epoch values during network
parameter updates/initialisation. This allows a user to specify the epoch within the parameter config file and it
facilitates arbitrary jumps in epoch values. This is necessary for the day-to-day management of multiple sub-zones as
well as the merging of one sub-zone into another.

**Shell**

Migrated the private network management utility tool into the Network Map interactive shell. The new command within the
shell is an interactive command, allowing a user to run the same management tools without having to worry about passing
in a configuration file or remembering the correct start up flag.

**Config Debugability**

Added multi-phase parsing of config files. Parsing and validation errors are now batched before being presented to
the user, eliminating the frustration from having to address errors one by one.

The service-based architecture requires tooling around service state monitoring. Currently (i.e. with the 0.3 release),
there is no dedicated utility that would address that issue. As for now, the network operator needs to rely only on service logs and manual service endpoint pinging in order to
assess in what state the service is.

* Identity Manager: `http://<<IDENTITY_MANAGER_ADDRESS>>/status`
* Network Map: `http://<<NETWORK_MAP_SERVICE_ADDRESS>>/network-map/my-hostname`
* Revocation Service (currently part of the Identity Manager): `http://<<REVOCATION_SERVICE_ADDRESS>>/status`
