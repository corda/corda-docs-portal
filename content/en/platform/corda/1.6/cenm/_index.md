---
date: '2020-01-08T09:59:25Z'
description: "Documentation for the 1.6 release of Corda Enterprise Network Manager (CENM)"
menu:
  versions:
    weight: 280
  cenm-1-6:
    weight: 1
    name: CENM 1.6
project: Corda
section_menu: cenm-1-6
title: CENM 1.6
version: 'CENM 1.6'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager (CENM) is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the user full control over all aspects of deployment, operation, and consensus rules.

{{< note >}}
**Release notes**

* For the latest CENM release notes, see the [CENM release notes]({{< relref "release-notes.md" >}}) page.
* For the latest Corda Enterprise release notes, see the Corda Enterprise Edition {{< latest-c4-version >}} {{< cordalatestrelref "enterprise/release-notes-enterprise.md" "release notes" >}} page. 
* For the latest Corda Open Source release notes, see the Corda Open Source {{< latest-c4-version >}} {{< cordalatestrelref "community/release-notes.md" "release notes" >}} page.
* For release notes of all versions, see [Corda]({{< relref "../../_index.md" >}}).
{{< /note >}}

The Corda Enterprise Network Manager provides the following services:

* [Identity Manager service]({{< relref "identity-manager.md" >}}) Enables nodes to join the network, and handles revocation of a node certificate.
* [Network Map service]({{< relref "network-map.md" >}}) Provides a global view of the network.
* [Signing Service]({{< relref "signing-service.md" >}}) Provides a way to sign approved requests to join the network (Certificate Signing Requests - CSRs) or revoke a certificate (Certificate Revocation Requests - CRRs), as well as changes to the network map.
* {{< cordalatestrelref "enterprise/node/auth-service.md" "Auth Service" >}} The user authentication and authorisation service. Stores and controls secure user-access to network services.
* {{< cordalatestrelref "enterprise/node/gateway-service.md" "Gateway Service" >}} Provides a transfer layer between front-end Corda Enterprise Network Manager (CENM) interfaces, and the Auth Service that underpins authentication and authorisation in CENM.
* [Zone Service]({{< relref "zone-service.md" >}}) A central store of configuration for other CENM services for one or more zones, and optionally for their subzones. Stores relevant configurations for the Identity Manager Service, the Network Map Service, and the Signing Service.
* [Angel Service]({{< relref "angel-service.md" >}}) An adapter, which manages the lifecycle of other services such as the Network Map Service or the Identity Manager Service, to make them more compatible with packaging tools such as Docker.

{{< note >}}
For instructions on deploying Corda Enterprise Network Manager with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts]({{< relref "deployment-kubernetes.md" >}}).

For instructions on deploying Corda Enterprise Network Manager with Amazon Web Services (AWS), see [CENM Deployment on AWS]({{< relref "aws-deployment-guide.md" >}}).

For a quick start guide on deploying Corda Enterprise Network Manager services as a test environment, see the [CENM test environment quick start guide]({{< relref "quick-start.md" >}}).
{{< /note >}}

## Concepts and overview

* [Corda Networks]({{< relref "corda-networks.md" >}})
* [Network Manager components]({{< relref "enm-components.md" >}})
* [The workflow]({{< relref "enm-components.md#the-workflow" >}})
* [Databases]({{< relref "enm-components.md#databases" >}})
* [Public Key Infrastructure (PKI)]({{< relref "enm-components.md#public-key-infrastructure-pki" >}})
* [The node]({{< relref "enm-components.md#the-node" >}})
* [Subzones]({{< relref "sub-zones.md" >}})
* [Network Map overview]({{< relref "network-map-overview.md" >}})
* [Certificate Revocation List]({{< relref "certificate-revocation.md" >}})

## CENM releases
* [Release notes]({{< relref "release-notes.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes.md" >}})

## Operations

* [Deployment with Kubernetes]({{< relref "deployment-kubernetes.md" >}})
  * [CENM Auth Service Helm Chart]({{< relref "deployment-kubernetes-auth.md" >}})
  * [CENM Gateway Service Helm Chart]({{< relref "deployment-kubernetes-gateway.md" >}})
  * [CENM Identity Manager Helm Chart]({{< relref "deployment-kubernetes-idman.md" >}})
  * [CENM Network Map Helm Chart]({{< relref "deployment-kubernetes-nmap.md" >}})
  * [CENM Notary Helm Chart]({{< relref "deployment-kubernetes-notary.md" >}})
  * [CENM Signing Service Helm Chart]({{< relref "deployment-kubernetes-signer.md" >}})
  * [CENM Zone Service Helm Chart]({{< relref "deployment-kubernetes-zone.md" >}})
* [CENM test environment quick start guide]({{< relref "quick-start.md" >}})
* [Zone Service]({{< relref "zone-service.md" >}})
* [Angel Service]({{< relref "angel-service.md" >}})
* [Identity Manager service]({{< relref "identity-manager.md" >}})
* [Network Map service]({{< relref "network-map.md" >}})
* [Signing Service]({{< relref "signing-service.md" >}})
* {{< cordalatestrelref "enterprise/node/auth-service.md" "Auth Service" >}}
* {{< cordalatestrelref "enterprise/node/gateway-service.md" "Gateway Service" >}}
* [CENM Command-line Interface (CLI) tool]({{< relref "cenm-cli-tool.md" >}})
* [Updating the network parameters]({{< relref "updating-network-parameters.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes.md" >}})
* [CENM databases]({{< relref "database-set-up.md" >}})
* [CENM User Admin tool]({{< relref "user-admin.md" >}})
* [Troubleshooting common issues]({{< relref "troubleshooting-common-issues.md" >}})
* [CENM support matrix]({{< relref "cenm-support-matrix.md" >}})

## Configuration

* [Identity Manager Service configuration parameters]({{< relref "config-identity-manager-parameters.md" >}})
* [Network Map Service configuration parameters]({{< relref "config-network-map-parameters.md" >}})
* [Network parameters]({{< relref "config-network-parameters.md" >}})
* [Configuring the CENM services to use SSL]({{< relref "enm-with-ssl.md" >}})
* [Workflow]({{< relref "workflow.md" >}})

## Tools and utilities

* [Index]({{< relref "tools-index.md" >}})
* [Public key infrastructure (PKI) tool]({{< relref "pki-tool.md" >}})
* [Certificate revocation request submission tool]({{< relref "tool-crr-submission.md" >}})
* Node Certificate Rotation Tool (contact your R3 account manager)
* [CENM Command-line Interface]({{< relref "cenm-cli-tool.md" >}})
* [CENM User Admin tool]({{< relref "user-admin.md" >}})
* [CENM management console]({{< relref "cenm-console.md" >}})
* {{< cordalatestrelref "enterprise/tools-config-obfuscator.md" "Config obfuscation tool" >}}
* [CRL Endpoint Check Tool]({{< relref "crl-endpoint-check-tool.md" >}})
* [Embedded shell]({{< relref "shell.md" >}})

## Public Key Infrastructure

* [Public Key Infrastructure (PKI) specifications]({{< relref "pki-specifications.md" >}})
* [Certificate hierarchy guide]({{< relref "pki-guide.md" >}})
* [Public key infrastructure (PKI) tool]({{< relref "pki-tool.md" >}})

## Signing Plug-in Samples

* [EJBCA sample plug-in]({{< relref "ejbca-plugin.md" >}})
