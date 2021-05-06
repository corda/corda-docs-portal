---
aliases:
- /releases/release-1.1/index.html
- /index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: 330
project: cenm
section_menu: cenm-1-1
title: CENM 1.1
version: '1.1'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the operator full control over all aspects of deployment, operation, and the consensus rules.
This is provided as an alternative to taking advantage of utilising the service-level-managed production components
that are otherwise be available from [Corda Network](https://corda.network), governed by the independent
Corda Network Foundation.

The *Corda Enterprise Network Manager* encompasses three main services:


* [Identity Manager Service](identity-manager.md) - Enables nodes to join the network, as well as handles revocation of a nodes certificate
* [Network Map Service](network-map.md) - Provides a global view of the network
* [Signing Service](signing-service.md) - Provides a way to sign approved requests to join the network (CSRs) or revoke a certificate
(CRRs) as well as changes to the network map

For a quick start guide on running the ENM services see [Enterprise Network Manager Quick-Start Guide](quick-start.md).


Concepts and Overview

* [Corda Networks](corda-networks.md)
* [Components of the Corda Enterprise Network Manager](enm-components.md)
* [The Workflow](enm-components.md#the-workflow)
* [Databases](enm-components.md#databases)
* [Public Key Infrastructure](enm-components.md#public-key-infrastructure)
* [The Node](enm-components.md#the-node)
* [Sub Zones](sub-zones.md)
* [Network Map Overview](network-map-overview.md)
* [Certificate Revocation List (CRL)](certificate-revocation.md)




CENM Releases

* [Release notes](release-notes.md)
* [Upgrading Corda Enterprise Network Manager](upgrade-notes.md)
* [Changelog](changelog.md)




Operations

* [Enterprise Network Manager Quick-Start Guide](quick-start.md)
* [Identity Manager Service](identity-manager.md)
* [Network Map Service](network-map.md)
* [Signing Service](signing-service.md)
* [Updating the network parameters](updating-network-parameters.md)
* [Upgrading Corda Enterprise Network Manager](upgrade-notes.md)
* [CENM Databases](database-set-up.md)
* [Troubleshooting Common Issues](troubleshooting-common-issues.md)
* [CENM support matrix](cenm-support-matrix.md)




Configuration

* [Identity Manager Configuration Parameters](config-identity-manager-parameters.md)
* [Network Map Configuration Parameters](config-network-map-parameters.md)
* [Network Parameters](config-network-parameters.md)
* [Configuring the ENM services to use SSL](enm-with-ssl.md)
* [Workflow](workflow.md)




Tools & Utilities

* [Tools & Utilities](tools-index.md)
* [Embedded Shell](shell.md)




Public Key Infrastructure

* [Certificate Hierarchy Guide](pki-guide.md)
* [Public Key Infrastructure (PKI) Tool](pki-tool.md)
