---
aliases:
- /docs/cenm/head/index.html
- /docs/cenm/index.html
date: '2020-01-08T09:59:25Z'
menu:
  versions:
    weight: -265
project: cenm
section_menu: cenm-1-5
title: CENM 1.5
version: '1.5'
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
* For the latest Corda Enterprise release notes, see the [Corda Enterprise 4.7 release notes](../../corda-enterprise/4.7/release-notes-enterprise.md) page. You can view release notes for previous versions of Corda Enterprise in the relevant documentation section for each version, accessible from the left-hand side menu.
* For all Corda open source release notes, see the [Corda release notes](../../corda-os/4.7/release-notes.md) page.

{{< /note >}}

The Corda Enterprise Network Manager provides the following services:

* [Identity Manager Service](identity-manager.md) Enables nodes to join the network, and handles revocation of a node certificate.
* [Network Map Service](network-map.md) Provides a global view of the network.
* [Signing Service](signing-service.md) Provides a way to sign approved requests to join the network (Certificate Signing Requests - CSRs) or revoke a certificate (Certificate Revocation Requests - CRRs), as well as changes to the network map.
* [Auth Service](auth-service.md) The user authentication and authorization service for CENM. Stores and controls secure user-access to network services.
* [Gateway Service](gateway-service.md) Provides a transfer layer between front-end Corda Enterprise Network Manager (CENM) interfaces, and the Auth Service that underpins authentication and authorisation in CENM.
* [Zone Service](zone-service.md) A central store of configuration for other CENM services for one or more zones, and optionally for their Sub Zones. Stores relevant configurations for the Identity Manager Service, the Network Map Service, and the Signing Service.
* [Angel Service](angel-service.md) An adapter, which manages the lifecycle of other services such as the Network Map Service or the Identity Manager Service, to make them more compatible with packaging tools such as Docker.

{{< note >}}
For instructions on deploying Corda Enterprise Network Manager with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts](deployment-kubernetes.md).

For instructions on deploying Corda Enterprise Network Manager with Amazon Web Services (AWS), see [CENM Deployment on AWS](aws-deployment-guide.md).

For a quick start guide on deploying Corda Enterprise Network Manager services as a test environment, see the [CENM test environment quick start guide](quick-start.md).
{{< /note >}}

## Concepts and overview

* [Corda Networks](corda-networks.md)
* [Components of the Corda Enterprise Network Manager](enm-components.md)
* [The workflow](enm-components.md#the-workflow)
* [Databases](enm-components.md#databases)
* [Public Key Infrastructure (PKI)](enm-components.md#public-key-infrastructure-pki)
* [The node](enm-components.md#the-node)
* [Sub Zones](sub-zones.md)
* [Network Map overview](network-map-overview.md)
* [Certificate Revocation List](certificate-revocation.md)

## CENM releases

* [Release notes](release-notes.md)
* [Release notes (Japanese)](release-notes-ja.md)
* [Upgrading Corda Enterprise Network Manager](upgrade-notes.md)

## Operations

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

## Configuration

* [Identity Manager Service configuration parameters](config-identity-manager-parameters.md)
* [Network Map Service configuration parameters](config-network-map-parameters.md)
* [Network parameters](config-network-parameters.md)
* [Configuring the CENM services to use SSL](enm-with-ssl.md)
* [Workflow](workflow.md)

## Tools and utilities

* [Index](tools-index.md)
* [Public Key Infrastructure (PKI) Tool](pki-tool.md)
* [Certificate Revocation Request Submission Tool](tool-crr-submission.md)
* Node Certificate Rotation Tool (contact [R3 support](https://www.r3.com/support/))
* [CENM Command-line Interface Tool](cenm-cli-tool.md)
* [CENM User Admin tool](user-admin.md)
* [CENM Management Console](cenm-console.md)
* [Config Obfuscation Tool](../../corda-enterprise/4.5/tools-config-obfuscator.md)
* [CRL Endpoint Check Tool](crl-endpoint-check-tool.md)
* [Embedded shell](shell.md)

## Public Key Infrastructure

* [Public Key Infrastructure (PKI) specifications](pki-specifications.md)
* [Certificate hierarchy guide](pki-guide.md)
* [Public Key Infrastructure (PKI) Tool](pki-tool.md)

## Signing Plug-in Samples

* [EJBCA sample plug-in](ejbca-plugin.md)
