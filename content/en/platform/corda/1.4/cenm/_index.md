---
aliases:
- /docs/cenm/head/index.html
- /docs/cenm/index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: 300
  cenm-1-4:
    weight: 1
    name: CENM 1.4
project: corda
section_menu: cenm-1-4
title: CENM 1.4
version: 'CENM 1.4'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager (CENM) is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the user full control over all aspects of deployment, operation, and consensus rules.
This is provided as an alternative to using the service-level-managed production components
that are otherwise available from [Corda Network](https://corda.network), which is governed by the independent
[Corda Network Foundation](https://corda.network/).

{{< note >}}
**Release notes**

* For all Corda Enterprise Network Manager release notes, see the [Corda Enterprise Network Manager release notes](../../../../../en/platform/corda/1.4/cenm/release-notes.md) page.
* For the latest Corda Enterprise release notes, see the [Corda Enterprise Edition 4.6 release notes](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-enterprise/4.6/enterprise/release-notes-enterprise.md) page. You can view release notes for previous versions of Corda Enterprise in the relevant documentation section for each version, accessible from the left-hand side menu.
* For all Corda open source release notes, see the [Corda release notes](../../../../../en/platform/corda/4.6/open-source/release-notes.md) page.

{{< /note >}}

The Corda Enterprise Network Manager provides three main services:

* [Identity Manager Service](../../../../../en/platform/corda/1.4/cenm/identity-manager.md) - enables nodes to join the network, and handles revocation of a node certificate.
* [Network Map Service](../../../../../en/platform/corda/1.4/cenm/network-map.md) - provides a global view of the network.
* [Signing Service](../../../../../en/platform/corda/1.4/cenm/signing-service.md) - provides a way to sign approved requests to join the network (Certificate Signing Requests - CSRs) or revoke a certificate (Certificate Revocation Requests - CRRs), as well as changes to the network map.

{{< note >}}
For instructions on deploying Corda Enterprise Network Manager with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes.md).

For a quick start guide on deploying Corda Enterprise Network Manager services as a test environment, see the [CENM test environment quick start guide](../../../../../en/platform/corda/1.4/cenm/quick-start.md).
{{< /note >}}

Concepts and overview

* [Corda Networks](../../../../../en/platform/corda/1.4/cenm/corda-networks.md)
* [Components of the Corda Enterprise Network Manager](../../../../../en/platform/corda/1.4/cenm/enm-components.md)
* [The workflow](../../../../../en/platform/corda/1.4/cenm/workflow.md)
* [Databases](../../../../../en/platform/corda/1.4/cenm/database-set-up.md)
* [Public Key Infrastructure (PKI)](../../../../../en/platform/corda/1.4/cenm/pki-tool.md)
* [The node](../../../../../en/platform/corda/1.4/cenm/network-map.html#node-certificate-revocation-checking)
* [Sub Zones](../../../../../en/platform/corda/1.4/cenm/sub-zones.html)
* [Network Map overview](../../../../../en/platform/corda/1.4/cenm/network-map-overview.md)
* [Certificate Revocation List](../../../../../en/platform/corda/1.4/cenm/certificate-revocation.md)

CENM releases

* [Release notes](../../../../../en/platform/corda/1.4/cenm/release-notes.md)
* [Upgrading Corda Enterprise Network Manager](../../../../../en/platform/corda/1.4/cenm/upgrade-notes.md)

Operations

* [Deployment with Kubernetes](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes.md)
  * [CENM Auth Service Helm Chart](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes-auth.md)
  * [CENM Gateway Service Helm Chart](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes-gateway.md)
  * [CENM Identity Manager Helm Chart](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes-idman.md)
  * [CENM Network Map Helm Chart](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes-nmap.md)
  * [CENM Notary Helm Chart](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes-notary.md)
  * [CENM Signing Service Helm Chart](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes-signer.md)
  * [CENM Zone Service Helm Chart](../../../../../en/platform/corda/1.4/cenm/deployment-kubernetes-zone.md)
* [CENM test environment quick start guide](../../../../../en/platform/corda/1.4/cenm/quick-start.md)
* [Zone Service](../../../../../en/platform/corda/1.4/cenm/zone-service.md)
* [Angel Service](../../../../../en/platform/corda/1.4/cenm/angel-service.md)
* [Identity Manager Service](../../../../../en/platform/corda/1.4/cenm/identity-manager.md)
* [Network Map Service](../../../../../en/platform/corda/1.4/cenm/network-map.md)
* [Signing Service](../../../../../en/platform/corda/1.4/cenm/signing-service.md)
* [Auth Service](../../../../../en/platform/corda/1.4/cenm/auth-service.md)
* [Gateway service](../../../../../en/platform/corda/1.4/cenm/gateway-service.md)
* [CENM Command-line Interface (CLI) tool](../../../../../en/platform/corda/1.4/cenm/cenm-cli-tool.md)
* [Updating the network parameters](../../../../../en/platform/corda/1.4/cenm/updating-network-parameters.md)
* [Upgrading Corda Enterprise Network Manager](../../../../../en/platform/corda/1.4/cenm/upgrade-notes.md)
* [CENM databases](../../../../../en/platform/corda/1.4/cenm/database-set-up.md)
* [CENM User Admin tool](../../../../../en/platform/corda/1.4/cenm/user-admin.md)
* [Troubleshooting common issues](../../../../../en/platform/corda/1.4/cenm/troubleshooting-common-issues.md)
* [CENM support matrix](../../../../../en/platform/corda/1.4/cenm/cenm-support-matrix.md)

Configuration

* [Identity Manager Service configuration parameters](../../../../../en/platform/corda/1.4/cenm/config-identity-manager-parameters.md)
* [Network Map Service configuration parameters](../../../../../en/platform/corda/1.4/cenm/config-network-map-parameters.md)
* [Network parameters](../../../../../en/platform/corda/1.4/cenm/config-network-parameters.md)
* [Configuring the CENM services to use SSL](../../../../../en/platform/corda/1.4/cenm/enm-with-ssl.md)
* [Workflow](../../../../../en/platform/corda/1.4/cenm/workflow.md)

Tools and utilities

* [Tools and utilities](../../../../../en/platform/corda/1.4/cenm/tools-index.md)
* [Embedded shell](../../../../../en/platform/corda/1.4/cenm/shell.md)

Public Key Infrastructure

* [Certificate hierarchy guide](../../../../../en/platform/corda/1.4/cenm/pki-guide.md)
* [Public Key Infrastructure (PKI) Tool](../../../../../en/platform/corda/1.4/cenm/pki-tool.md)

Signing Plug-in Samples

* [EJBCA sample plug-in](../../../../../en/platform/corda/1.4/cenm/ejbca-plugin.md)
