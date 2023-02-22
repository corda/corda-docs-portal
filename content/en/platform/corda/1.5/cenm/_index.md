---
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: 290
  cenm-1-5:
    weight: 1
    name: CENM 1.5
project: corda
section_menu: cenm-1-5
title: CENM 1.5
version: 'CENM 1.5'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager (CENM) is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the user full control over all aspects of deployment, operation, and consensus rules.
This is provided as an alternative to using the service-level-managed production components
that are otherwise available from [Corda Network](https://corda.network), which is governed by the independent
[Corda Network Foundation](https://corda.network/).

{{< note >}}
**Release notes**

* For all Corda Enterprise Network Manager release notes, see the [Corda Enterprise Network Manager release notes](../../../../../en/platform/corda/1.5/cenm/release-notes.md) page.
* For all Corda 4 Enterprise Edition release notes, see [Welcome to Corda - Corda 4 Enterprise](../../../../../en/platform/corda.html#corda-4-enterprise).
* For all Corda 4 Community Edition release notes, see [Welcome to Corda - Corda 4 Community Edition (Formerly Open Source)](../../../../../en/platform/corda.html#corda-4-community-edition-formerly-open-source).

{{< /note >}}

The Corda Enterprise Network Manager provides the following services:

* [Identity Manager Service](../../../../../en/platform/corda/1.5/cenm/identity-manager.md) Enables nodes to join the network, and handles revocation of a node certificate.
* [Network Map Service](../../../../../en/platform/corda/1.5/cenm/network-map.md) Provides a global view of the network.
* [Signing Service](../../../../../en/platform/corda/1.5/cenm/signing-service.md) Provides a way to sign approved requests to join the network (Certificate Signing Requests - CSRs) or revoke a certificate (Certificate Revocation Requests - CRRs), as well as changes to the network map.
* [Auth Service](../../../../../en/platform/corda/4.8/enterprise/node/auth-service.md) The user authentication and authorisation service. Stores and controls secure user-access to network services.
* [Gateway Service](../../../../../en/platform/corda/4.8/enterprise/node/gateway-service.md) Provides a transfer layer between front-end Corda Enterprise Network Manager (CENM) interfaces, and the Auth Service that underpins authentication and authorisation in CENM.
* [Zone Service](../../../../../en/platform/corda/1.5/cenm/zone-service.md) A central store of configuration for other CENM services for one or more zones, and optionally for their Sub Zones. Stores relevant configurations for the Identity Manager Service, the Network Map Service, and the Signing Service.
* [Angel Service](../../../../../en/platform/corda/1.5/cenm/angel-service.md) An adapter, which manages the lifecycle of other services such as the Network Map Service or the Identity Manager Service, to make them more compatible with packaging tools such as Docker.

{{< note >}}
For instructions on deploying Corda Enterprise Network Manager with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes.md).

For instructions on deploying Corda Enterprise Network Manager with Amazon Web Services (AWS), see [CENM Deployment on AWS](../../../../../en/platform/corda/1.5/cenm/aws-deployment-guide.md).

For a quick start guide on deploying Corda Enterprise Network Manager services as a test environment, see the [CENM test environment quick start guide](../../../../../en/platform/corda/1.5/cenm/quick-start.md).
{{< /note >}}

## Concepts and overview

* [Corda Networks](../../../../../en/platform/corda/1.5/cenm/corda-networks.md)
* [Components of the Corda Enterprise Network Manager](../../../../../en/platform/corda/1.5/cenm/enm-components.md)
* [The workflow](../../../../../en/platform/corda/1.5/cenm/enm-components.html#the-workflow)
* [Databases](../../../../../en/platform/corda/1.5/cenm/enm-components.html#databases)
* [Public Key Infrastructure (PKI)](../../../../../en/platform/corda/1.5/cenm/enm-components.html#public-key-infrastructure-pki)
* [The node](../../../../../en/platform/corda/1.5/cenm/enm-components.html#the-node)
* [Sub Zones](../../../../../en/platform/corda/1.5/cenm/sub-zones.md)
* [Network Map overview](../../../../../en/platform/corda/1.5/cenm/network-map-overview.md)
* [Certificate Revocation List](../../../../../en/platform/corda/1.5/cenm/certificate-revocation.md)

## CENM releases

* [Release notes](../../../../../en/platform/corda/1.5/cenm/release-notes.md)
* [Release notes (Japanese)](../../../../../en/platform/corda/1.5/cenm/release-notes-ja.md)
* [Upgrading Corda Enterprise Network Manager](../../../../../en/platform/corda/1.5/cenm/upgrade-notes.md)

## Operations

* [Deployment with Kubernetes](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes.md)
  * [CENM Auth Service Helm Chart](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes-auth.md)
  * [CENM Gateway Service Helm Chart](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes-gateway.md)
  * [CENM Identity Manager Helm Chart](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes-idman.md)
  * [CENM Network Map Helm Chart](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes-nmap.md)
  * [CENM Notary Helm Chart](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes-notary.md)
  * [CENM Signing Service Helm Chart](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes-signer.md)
  * [CENM Zone Service Helm Chart](../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes-zone.md)
* [CENM test environment quick start guide](../../../../../en/platform/corda/1.5/cenm/quick-start.md)
* [Zone Service](../../../../../en/platform/corda/1.5/cenm/zone-service.md)
* [Angel Service](../../../../../en/platform/corda/1.5/cenm/angel-service.md)
* [Identity Manager Service](../../../../../en/platform/corda/1.5/cenm/identity-manager.md)
* [Network Map Service](../../../../../en/platform/corda/1.5/cenm/network-map.md)
* [Signing Service](../../../../../en/platform/corda/1.5/cenm/signing-service.md)
* [Auth Service](../../../../../en/platform/corda/4.8/enterprise/node/auth-service.md)
* [Gateway Service](../../../../../en/platform/corda/4.8/enterprise/node/gateway-service.md)
* [CENM Command-line Interface (CLI) tool](../../../../../en/platform/corda/1.5/cenm/cenm-cli-tool.md)
* [Updating the network parameters](../../../../../en/platform/corda/1.5/cenm/updating-network-parameters.md)
* [Upgrading Corda Enterprise Network Manager](../../../../../en/platform/corda/1.5/cenm/upgrade-notes.md)
* [CENM databases](../../../../../en/platform/corda/1.5/cenm/database-set-up.md)
* [CENM User Admin tool](../../../../../en/platform/corda/1.5/cenm/user-admin.md)
* [Troubleshooting common issues](../../../../../en/platform/corda/1.5/cenm/troubleshooting-common-issues.md)
* [CENM support matrix](../../../../../en/platform/corda/1.5/cenm/cenm-support-matrix.md)

## Configuration

* [Identity Manager Service configuration parameters](../../../../../en/platform/corda/1.5/cenm/config-identity-manager-parameters.md)
* [Network Map Service configuration parameters](../../../../../en/platform/corda/1.5/cenm/config-network-map-parameters.md)
* [Network parameters](../../../../../en/platform/corda/1.5/cenm/config-network-parameters.md)
* [Configuring the CENM services to use SSL](../../../../../en/platform/corda/1.5/cenm/enm-with-ssl.md)
* [Workflow](../../../../../en/platform/corda/1.5/cenm/workflow.md)

## Tools and utilities

* [Index](../../../../../en/platform/corda/1.5/cenm/tools-index.md)
* [Public Key Infrastructure (PKI) Tool](../../../../../en/platform/corda/1.5/cenm/pki-tool.md)
* [Certificate Revocation Request Submission Tool](../../../../../en/platform/corda/1.5/cenm/tool-crr-submission.md)
* Node Certificate Rotation Tool (contact your R3 account manager)
* [CENM Command-line Interface Tool](../../../../../en/platform/corda/1.5/cenm/cenm-cli-tool.md)
* [CENM User Admin tool](../../../../../en/platform/corda/1.5/cenm/user-admin.md)
* [CENM Management Console](../../../../../en/platform/corda/1.5/cenm/cenm-console.md)
* [Config Obfuscation Tool](../../../../../en/platform/corda/4.7/enterprise/tools-config-obfuscator.md)
* [CRL Endpoint Check Tool](../../../../../en/platform/corda/1.5/cenm/crl-endpoint-check-tool.md)
* [Embedded shell](../../../../../en/platform/corda/1.5/cenm/shell.md)

## Public Key Infrastructure

* [Public Key Infrastructure (PKI) specifications](../../../../../en/platform/corda/1.5/cenm/pki-specifications.md)
* [Certificate hierarchy guide](../../../../../en/platform/corda/1.5/cenm/pki-guide.md)
* [Public Key Infrastructure (PKI) Tool](../../../../../en/platform/corda/1.5/cenm/pki-tool.md)

## Signing Plug-in Samples

* [EJBCA sample plug-in](../../../../../en/platform/corda/1.5/cenm/ejbca-plugin.md)
