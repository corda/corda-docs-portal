---
date: '2020-01-08T09:59:25Z'
description: "Documentation for the 1.5 release of Corda Enterprise Network Manager (CENM)"
menu:
  versions:
    weight: 290
  cenm-1-5:
    weight: 1
    name: CENM 1.5
project: Corda
section_menu: cenm-1-5
title: CENM 1.5
version: 'CENM 1.5'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager (CENM) is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the user full control over all aspects of deployment, operation, and consensus rules.

{{< note >}}
**Release notes**

* For all Corda Enterprise Network Manager release notes, see the [Corda Enterprise Network Manager release notes]({{< relref "../../../../../en/platform/corda/1.6/cenm/release-notes.md" >}}) page.
* For all Corda 4 Enterprise Edition and Community/Open Source release notes, see [Welcome to Corda]({{< relref "../../../../../en/platform/corda/_index.md" >}}).

{{< /note >}}

The Corda Enterprise Network Manager provides the following services:

* [Identity Manager service]({{< relref "../../../../../en/platform/corda/1.5/cenm/identity-manager.md" >}}) Enables nodes to join the network, and handles revocation of a node certificate.
* [Network Map service]({{< relref "../../../../../en/platform/corda/1.5/cenm/network-map.md" >}}) Provides a global view of the network.
* [Signing Service]({{< relref "../../../../../en/platform/corda/1.5/cenm/signing-service.md" >}}) Provides a way to sign approved requests to join the network (Certificate Signing Requests - CSRs) or revoke a certificate (Certificate Revocation Requests - CRRs), as well as changes to the network map.
* [Auth Service]({{< relref "../../../../../en/platform/corda/4.8/enterprise/node/auth-service.md" >}}) The user authentication and authorisation service. Stores and controls secure user-access to network services.
* [Gateway Service]({{< relref "../../../../../en/platform/corda/4.8/enterprise/node/gateway-service.md" >}}) Provides a transfer layer between front-end Corda Enterprise Network Manager (CENM) interfaces, and the Auth Service that underpins authentication and authorisation in CENM.
* [Zone Service]({{< relref "../../../../../en/platform/corda/1.5/cenm/zone-service.md" >}}) A central store of configuration for other CENM services for one or more zones, and optionally for their subzones. Stores relevant configurations for the Identity Manager Service, the Network Map Service, and the Signing Service.
* [Angel Service]({{< relref "../../../../../en/platform/corda/1.5/cenm/angel-service.md" >}}) An adapter, which manages the lifecycle of other services such as the Network Map Service or the Identity Manager Service, to make them more compatible with packaging tools such as Docker.

{{< note >}}
For instructions on deploying Corda Enterprise Network Manager with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts]({{< relref "../../../../../en/platform/corda/1.5/cenm/deployment-kubernetes.md" >}}).

For instructions on deploying Corda Enterprise Network Manager with Amazon Web Services (AWS), see [CENM Deployment on AWS]({{< relref "../../../../../en/platform/corda/1.5/cenm/aws-deployment-guide.md" >}}).

For a quick start guide on deploying Corda Enterprise Network Manager services as a test environment, see the [CENM test environment quick start guide]({{< relref "../../../../../en/platform/corda/1.5/cenm/quick-start.md" >}}).
{{< /note >}}

## Concepts and overview

* [Corda Networks]({{< relref "../../../../../en/platform/corda/1.5/cenm/corda-networks.md" >}})
* [Network Manager components]({{< relref "../../../../../en/platform/corda/1.5/cenm/enm-components.md" >}})
* [The workflow]({{< relref "../../../../../en/platform/corda/1.5/cenm/enm-components.md#the-workflow" >}})
* [Databases]({{< relref "../../../../../en/platform/corda/1.5/cenm/enm-components.md#databases" >}})
* [Public Key Infrastructure (PKI)]({{< relref "../../../../../en/platform/corda/1.5/cenm/enm-components.md#public-key-infrastructure-pki" >}})
* [The node]({{< relref "../../../../../en/platform/corda/1.5/cenm/enm-components.md#the-node" >}})
* [Subzones]({{< relref "../../../../../en/platform/corda/1.5/cenm/sub-zones.md" >}})
* [Network Map overview]({{< relref "../../../../../en/platform/corda/1.5/cenm/network-map-overview.md" >}})
* [Certificate Revocation List]({{< relref "../../../../../en/platform/corda/1.5/cenm/certificate-revocation.md" >}})

## CENM releases
* [Release notes]({{< relref "release-notes.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "../../1.5/cenm/upgrade-notes.md" >}})

## Operations

* [Deployment with Kubernetes]({{< relref "../../1.5/cenm/deployment-kubernetes.md" >}})
  * [CENM Auth Service Helm Chart]({{< relref "../../1.5/cenm/deployment-kubernetes-auth.md" >}})
  * [CENM Gateway Service Helm Chart]({{< relref "../../1.5/cenm/deployment-kubernetes-gateway.md" >}})
  * [CENM Identity Manager Helm Chart]({{< relref "../../1.5/cenm/deployment-kubernetes-idman.md" >}})
  * [CENM Network Map Helm Chart]({{< relref "../../1.5/cenm/deployment-kubernetes-nmap.md" >}})
  * [CENM Notary Helm Chart]({{< relref "../../1.5/cenm/deployment-kubernetes-notary.md" >}})
  * [CENM Signing Service Helm Chart]({{< relref "../../1.5/cenm/deployment-kubernetes-signer.md" >}})
  * [CENM Zone Service Helm Chart]({{< relref "../../1.5/cenm/deployment-kubernetes-zone.md" >}})
* [CENM test environment quick start guide]({{< relref "../../1.5/cenm/quick-start.md" >}})
* [Zone Service]({{< relref "../../1.5/cenm/zone-service.md" >}})
* [Angel Service]({{< relref "../../1.5/cenm/angel-service.md" >}})
* [Identity Manager service]({{< relref "../../1.5/cenm/identity-manager.md" >}})
* [Network Map service]({{< relref "../../1.5/cenm/network-map.md" >}})
* [Signing Service]({{< relref "../../1.5/cenm/signing-service.md" >}})
* [Auth Service]({{< relref "../../4.8/enterprise/node/auth-service.md" >}})
* [Gateway Service]({{< relref "../../4.8/enterprise/node/gateway-service.md" >}})
* [CENM Command-line Interface (CLI) tool]({{< relref "../../1.5/cenm/cenm-cli-tool.md" >}})
* [Updating the network parameters]({{< relref "../../1.5/cenm/updating-network-parameters.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "../../1.5/cenm/upgrade-notes.md" >}})
* [CENM databases]({{< relref "../../1.5/cenm/database-set-up.md" >}})
* [CENM User Admin tool]({{< relref "../../1.5/cenm/user-admin.md" >}})
* [Troubleshooting common issues]({{< relref "../../1.5/cenm/troubleshooting-common-issues.md" >}})
* [CENM support matrix]({{< relref "../../1.5/cenm/cenm-support-matrix.md" >}})

## Configuration

* [Identity Manager Service configuration parameters]({{< relref "../../1.5/cenm/config-identity-manager-parameters.md" >}})
* [Network Map Service configuration parameters]({{< relref "../../1.5/cenm/config-network-map-parameters.md" >}})
* [Network parameters]({{< relref "../../1.5/cenm/config-network-parameters.md" >}})
* [Configuring the CENM services to use SSL]({{< relref "../../1.5/cenm/enm-with-ssl.md" >}})
* [Workflow]({{< relref "../../1.5/cenm/workflow.md" >}})

## Tools and utilities

* [Index]({{< relref "../../1.5/cenm/tools-index.md" >}})
* [Public key infrastructure (PKI) tool]({{< relref "../../1.5/cenm/pki-tool.md" >}})
* [Certificate revocation request submission tool]({{< relref "../../1.5/cenm/tool-crr-submission.md" >}})
* Node Certificate Rotation Tool (contact your R3 account manager)
* [CENM Command-line Interface]({{< relref "../../1.5/cenm/cenm-cli-tool.md" >}})
* [CENM User Admin tool]({{< relref "../../1.5/cenm/user-admin.md" >}})
* [CENM management console]({{< relref "../../1.5/cenm/cenm-console.md" >}})
* [Config obfuscation tool]({{< relref "../../4.8/enterprise/tools-config-obfuscator.md" >}})
* [CRL Endpoint Check Tool]({{< relref "../../1.5/cenm/crl-endpoint-check-tool.md" >}})
* [Embedded shell]({{< relref "../../1.5/cenm/shell.md" >}})

## Public Key Infrastructure

* [Public Key Infrastructure (PKI) specifications]({{< relref "../../1.5/cenm/pki-specifications.md" >}})
* [Certificate hierarchy guide]({{< relref "../../1.5/cenm/pki-guide.md" >}})
* [Public key infrastructure (PKI) tool]({{< relref "../../1.5/cenm/pki-tool.md" >}})

## Signing Plug-in Samples

* [EJBCA sample plug-in]({{< relref "../../1.5/cenm/ejbca-plugin.md" >}})
