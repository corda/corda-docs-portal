---
aliases:
- /docs/cenm/head/index.html
- /docs/cenm/index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: 950
project: cenm
section_menu: cenm-1-4
title: CENM 1.4
version: '1.4'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager (CENM) is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the user full control over all aspects of deployment, operation, and consensus rules.
This is provided as an alternative to using the service-level-managed production components
that are otherwise available from [Corda Network](https://corda.network), which is governed by the independent
[Corda Network Foundation](https://corda.network/).

{{< note >}}
**Release notes**

* For all Corda Enterprise Network Manager release notes, see the [Corda Enterprise Network Manager release notes](release-notes.md) page.
* For the latest Corda Enterprise release notes, see the [Corda Enterprise 4.6 release notes](../../corda-enterprise/4.6/release-notes-enterprise.md) page. You can view release notes for previous versions of Corda Enterprise in the relevant documentation section for each version, accessible from the left-hand side menu.
* For all Corda open source release notes, see the [Corda release notes](../../corda-os/4.6/release-notes.md) page.

{{< /note >}}

The Corda Enterprise Network Manager provides three main services:

* [Identity Manager Service](identity-manager.md) - enables nodes to join the network, and handles revocation of a node certificate.
* [Network Map Service](network-map.md) - provides a global view of the network.
* [Signing Service](signing-service.md) - provides a way to sign approved requests to join the network (Certificate Signing Requests - CSRs) or revoke a certificate (Certificate Revocation Requests - CRRs), as well as changes to the network map.

{{< note >}}
For instructions on deploying Corda Enterprise Network Manager with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts](deployment-kubernetes.md).

For a quick start guide on deploying Corda Enterprise Network Manager services as a test environment, see the [CENM test environment quick start guide](quick-start.md).
{{< /note >}}

Concepts and overview

* [Corda Networks](corda-networks.md)
* [Components of the Corda Enterprise Network Manager](enm-components.md)
* [The workflow](enm-components.md#the-workflow)
* [Databases](enm-components.md#databases)
* [Public Key Infrastructure (PKI)](enm-components.md#public-key-infrastructure-pki)
* [The node](enm-components.md#the-node)
* [Sub Zones](sub-zones.md)
* [Network Map overview](network-map-overview.md)
* [Certificate Revocation List](certificate-revocation.md)

CENM releases

* [Release notes](release-notes.md)
* [Upgrading Corda Enterprise Network Manager](upgrade-notes.md)

Operations

* [Deployment with Kubernetes](deployment-kubernetes.md)
  * [CENM Auth Service Helm Chart](deployment-kubernetes-auth.md)
  * [CENM Gateway Service Helm Chart](deployment-kubernetes-gateway.md)
  * [CENM Identity Manager Helm Chart](deployment-kubernetes-idman.md)
  * [CENM Network Map Helm Chart](deployment-kubernetes-nmap.md)
  * [CENM Notary Helm Chart](deployment-kubernetes-notary.md)
  * [CENM Signing Service Helm Chart](deployment-kubernetes-signer.md)
  * [CENM Zone Service Helm Chart](deployment-kubernetes-zone.md)
* [CENM test environment quick start guide](quick-start.md)
* [Zone Service](zone-service.md)
* [Angel Service](angel-service.md)
* [Identity Manager Service](identity-manager.md)
* [Network Map Service](network-map.md)
* [Signing Service](signing-service.md)
* [Auth Service](auth-service.md)
* [Gateway service](gateway-service.md)
* [CENM Command-line Interface (CLI) tool](cenm-cli-tool.md)
* [Updating the network parameters](updating-network-parameters.md)
* [Upgrading Corda Enterprise Network Manager](upgrade-notes.md)
* [CENM databases](database-set-up.md)
* [CENM User Admin tool](user-admin.md)
* [Troubleshooting common issues](troubleshooting-common-issues.md)
* [CENM support matrix](cenm-support-matrix.md)

Configuration

* [Identity Manager Service configuration parameters](config-identity-manager-parameters.md)
* [Network Map Service configuration parameters](config-network-map-parameters.md)
* [Network parameters](config-network-parameters.md)
* [Configuring the CENM services to use SSL](enm-with-ssl.md)
* [Workflow](workflow.md)

Tools and utilities

* [Tools and utilities](tools-index.md)
* [Embedded shell](shell.md)

Public Key Infrastructure

* [Certificate hierarchy guide](pki-guide.md)
* [Public Key Infrastructure (PKI) Tool](pki-tool.md)

Signing Plug-in Samples

* [EJBCA sample plug-in](ejbca-plugin.md)
