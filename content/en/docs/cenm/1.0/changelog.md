---
aliases:
- /releases/release-1.0/changelog.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-changelog
    parent: cenm-1-0-enm-releases
    weight: 100
tags:
- changelog
title: Changelog
---


# Changelog

Here’s a summary of what’s changed in each Enterprise Network Manager release. For guidance on how to upgrade code from
the previous release, see [Upgrading Corda Enterprise Network Manager](upgrade-notes.md).


## Unreleased


* CSR and CRR workflow logic rewritten according to the new design.
The new implementation removes DB queries over a large data sets and separates workflow-related logic from other parts of the system.
* Private network persistence layer refactored by encapsulating entity classes within the DAO.
* Removed redundant call between Signing Service and Revocation Service when signing a new CRL.
* Separated the Network Map REST protocol from the plain-text endpoints used for debugging to support
the future versioning of both independently.
* Added JSON plain text REST endpoints.
* Added support for dynamically loadable JDBC drivers.
* Added Postgresql as an officially supported database that the CENM is tested against.
* Added support for manually specifying the epoch value within a network parameter config file.
* Added contextual logging mechanism.
* Moved private network management tools into the Network Map interactive shell. See [Private Network Map](private-network-map.md) for
details.
* Added multi-phase config parsing.
* Separated Identity Manager, Network Map, Signing Service into stand-alone JARs.
* Renaming of Doorman to Identity Manager.
* Removed bundled mssql jdbc driver


## ENM 0.4


* Fixing the remark field length restriction in the CSR/CRR DB. In the past it was 256 characters causing some issues in JIRA.
* Added certificate signing request rejection reasons to the node’s rejection response.
* Added certificate signing request rejection reasons handling for the JIRA workflow.
* Signing Service -> Doorman socket based communication added.
* Added client and server health check tools to the utilities JAR
See [Inter-service Communication Health Checking Tool](tool-health-check.md) for more details
* Change of the naming convention Enterprise Zone Manager -> Enterprise Network Manager.
* Added packageOwnership map to the network parameters config


## EZM 0.3


* Added doorman and network map schema migration logic to the utilities JAR
as well as the migration status check to the Network Services JAR.
* Added support for the explicit whitelisted contracts specification in the network parameters configuration file.
See [Contract Whitelist Generation](contract-whitelisting.md) for more details.
* Certificate path validation is separated from the Doorman schema. It is based on the CertPath.validate method and
the certificate revocation list validation.
* Added the socket-based communication between Signing service and Network Map service.
See [Signing Service](signing-service.md) for more details.
* Added a timeout and backoff strategy to the local signer for Doorman, Revocation and Network Map
* Fixed the revocation service socket server to guarantee reads and writes will be completed
* Added embedded shell support for the Network Map & Doorman service. See [Embedded Shell](shell.md) for more details.
* Ensured consistent naming throughout DB schema
* Separated the Doorman/Revocation and Network Map DB schemas
* As a consequence of the schema separation added in verification to prevent a user from running both Network Map and
Doorman services simultaneously
* Modified private network management tool to run against the Network Map schema only
* Added requirement for network truststore to be passed when setting network parameters. This is a consequence of
separating the DB schemas, as the Network Map service no longer has access to the Doorman DB to check that the
Notaries within the network parameters have valid certificates. See the ‘Setting the Network Parameters’ section
within the [Network Map Service](network-map.md) for more details.
* Added SSL support for Zone Manager services. See [Configuring the ENM services to use SSL](enm-with-ssl.md) for more details.
* Added Doorman socket server with private network administration functionality.
* Integrate Doorman socket server with private network management tool, so that new private networks can be persisted
in both the Network Map and the Doorman DB.
* Added support for the certificate path validation (against the certificate revocation list) upon
the node info submission to the network map service.
* Integrate Doorman socket server with Network Map during node info publishing. This is for retrieval of the private
network mapping.
* Exposed SSL configuration for the ENM services
* Change of the naming convention Network Services -> Enterprise Zone Manager.
* Bug-Fix:
Certificate generation issue fix. [[ENT-2990](https://r3-cev.atlassian.net/browse/ENT-2990)]


## Network Services 0.2.2


* Patch version fixing the liquibase migration issue undetected in the 0.2.1 release.


## Network Services 0.2.1


* Added the Config Upgrade tool to the Network Services Tooling.
* Added the Certificate Hierarchy Verifier to the Network Services Tooling. See [Certificates Validator](tool-certificates-validator.md) for
details.
* Improved config validation with respect to the certificate set-up.
* Improved logging for the signing service.
* Support for backward compatibility for version 0.1.
* Support for auto enrolment of nodes at the time of submitting a CSR into a private network. See
[Private Network Map](private-network-map.md) for details.
* Initial tooling around management of private networks using a tool bundles in the utilities jar.
* Minor bugfix.


## Network Services 0.2


* The workflow engine for managing legal identity verification checks is no longer restricted to Jira or nothing.
Currently Jira is the only provided plugin, with more planned in the future. However, you can write your own
plugin for any workflow engine as per the example show in [Workflow](workflow.md)
* Adding new REST endpoints to the Network map to allow more human readable output to be generated as
JSON to facilitate debugging and inspection. See [Network Map Overview](network-map-overview.md) for details.
* Adding hidden command line options to disable parts of the configuration. Specifically, this is useful when
bootstrapping a Doorman / Network Map combined server where you wish to temporarily disable the configured
Network Map elements.These options are `--ignore-doorman` and `--ignore-network-map`
* Adding `minimumPlatformVersion` and `newPKIOnly` configuration options to the Doorman.
These can be used to validate a registration request from a node and reject if below the configured values.
See config-doorman-parameters for details
* Adding `minimumPlatformVersion` and `newPKIOnly` configuration options to the Network Map Service.
These can be used to validate a registration request from a node and reject if below the configured value.
See [Network Map Configuration Parameters](config-network-map-parameters.md) for details


## Network Services 0.1


* Separation of the Network services into their own repository

