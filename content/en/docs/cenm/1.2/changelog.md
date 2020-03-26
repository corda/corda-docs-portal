---
aliases:
- /changelog.html
- /releases/release-1.2/changelog.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-changelog
    parent: cenm-1-2-cenm-releases
    weight: 100
tags:
- changelog
title: Changelog
---


# Changelog

Here’s a summary of what’s changed in each Enterprise Network Manager release. For guidance on how to upgrade code from
the previous release, see [Upgrading Corda Enterprise Network Manager](upgrade-notes.md).

## CENM 1.2


* Remove core functionality for private network maps. This does not yet remove them from the database schema,
which will be in a future release. Related quarantined and staging node info tables are not maintained as of CENM 1.1.
* Added support for external PKI. This introduces new optional Signable Material Retriever Service (SMR) which fetches signable
and saves signed material. SMR invokes plugin which handles communication with Signing Service. Custom plugin should be
provided to handle external signing infrastructures.
* Oracle database needs to be configured with support for extended data types for VARCHAR2 and NVARCHAR2 column types.
Refer to CENM database setup page.
* Identity Manager service - new column `submission_token` added to database tables `certificate_signing_request`,
`certificate_revocation_request`, `workflow_csr`, `workflow_crr`.
* Network Map service - new column `platform_version` added to database tables `node_info` and `node_info_staging`.


## CENM 1.1


* Remove shell functionality for private network maps ahead of removing them entirely in a future release.
As part of this the *privateNetworkAutoEnrolment* configuration option has been removed.
* Changed CRaSH shell version to the patched version of the CRaSH shell used by Corda.
* Changed the way configuration parsing deals with missing imports to now treat this as an error
rather than just ignore the missing file.
* Added validation rule checking the availability and validity of sshd port specified in service config.
* Added support for additional database config properties.
* Added sql command to H2 db URL string such that exclusive locks are not acquired as with H2 db version <1.4.198 some sql commands
are not supported, which is rooted in the former. Previously an internal error occurred when using H2 and trying to issue
a CRR due to unsupported sql commands. Note that this issue has been fixed in later H2 db versions.
* Removed redundant check whether a workflow has been approved when Network Map requests private network mapping from
Identity Manager, as it suffices to check whether a valid (not revoked) CSR exists.
* Added `run purgeAllStagedNodeInfos` and `run purgeStagedNodeInfo nodeInfoHash: <node_info_hash>` commands to Network
Map interactive shell, allowing for the moving of nodes out of the staging table and into the main node info table of
the Network Map. This provides a solution to the scenario whereby a node gets stuck in the staging table (see
*Troubleshooting Common Issues* section).
* Added dynamic loading of HSM Jars. When using the Signing Service or PKI tool in conjunction with a HSM, the third
party Jars have to be provided by the user and referenced within the configuration file.
* Added logic for logging config files with the value “<{hidden}>” for password keys, preventing sensitive data
from ending up in the services’ logs.
* Added additional port availability checks for enmListener ports and address of services specified in the config file.
* Added Oracle DB support (versions 12cR2 and 11gR2).
* Added config migration tool (v0.2.2 / v0.3+ config files to v1.1 configs).
* Removed invalid mention of DSA keys within the package ownership documentation for Network Parameters. Corda does not
support DSA keys.


## CENM 1.0


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
* Moved private network management tools into the Network Map interactive shell.
* Added multi-phase config parsing.
* Separated Identity Manager, Network Map, Signing Service into stand-alone JARs.
* Renaming of Doorman to Identity Manager.
* Removed bundled mssql jdbc driver


## ENM 0.4


* Fixed Jira synchronisation issue for the rejected CSR/CRRs.
* Fixed the remark field length restriction in the CSR/CRR DB. In the past it was 256 characters causing some issues in JIRA.
* Added certificate signing request rejection reasons to the node’s rejection response.
* Added certificate signing request rejection reasons handling for the JIRA workflow.
* Signing Service -> Doorman socket based communication added.
* Added client and server health check tools to the utilities JAR
* Change of the naming convention Enterprise Zone Manager -> Enterprise Network Manager.
* Added packageOwnership map to the network parameters config

