---
aliases:
- /docs/cenm/head/index.html
- /docs/cenm/index.html
date: '2020-01-08T09:59:25Z'
project: corda
section_menu: cenm-1-3
version: 'CENM 1.3'
description: "Documentation for the 1.3 release of Corda Enterprise Network Manager (CENM)"
menu:
  versions:
    weight: 310
  cenm-1-3:
    weight: 1
    name: CENM 1.3
project: corda
section_menu: cenm-1-3
title: CENM 1.3
version: 'CENM 1.3'
---

# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager (CENM) is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the user full control over all aspects of deployment, operation, and consensus rules.
This is provided as an alternative to using the service-level-managed production components
that are otherwise available from [Corda Network](https://corda.network), which is governed by the independent
[Corda Network Foundation](https://corda.network/).

The Corda Enterprise Network Manager provides three main services:

* [Identity Manager Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/identity-manager.md" >}}) - enables nodes to join the network, and handles revocation of a node certificate.
* [Network Map Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/network-map.md" >}}) - provides a global view of the network.
* [Signing Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/signing-service.md" >}}) - provides a way to sign approved requests to join the network (Certificate Signing Requests - CSRs) or revoke a certificate (Certificate Revocation Requests - CRRs), as well as changes to the network map.

{{< note >}}
For instructions on deploying Corda Enterprise Network Manager with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes.md" >}}).

For a quick start guide on deploying Corda Enterprise Network Manager services as a test environment, see the [CENM test environment quick start guide]({{< relref "../../../../../en/platform/corda/1.3/cenm/quick-start.md" >}}).
{{< /note >}}

Concepts and overview

* [Corda Networks]({{< relref "../../../../../en/platform/corda/1.3/cenm/corda-networks.md" >}})
* [Components of the Corda Enterprise Network Manager]({{< relref "../../../../../en/platform/corda/1.3/cenm/enm-components.md" >}})
* [The workflow]({{< relref "../../../../../en/platform/corda/1.3/cenm/workflow.md" >}})
* [Databases]({{< relref "../../../../../en/platform/corda/1.3/cenm/database-set-up.md" >}})
* [Public Key Infrastructure (PKI)]({{< relref "../../../../../en/platform/corda/1.3/cenm/pki-tool.md" >}})
* [The node](../../../../../en/platform/corda/1.3/cenm/network-map.html#node-certificate-revocation-checking)
* [Sub Zones]({{< relref "../../../../../en/platform/corda/1.3/cenm/sub-zones.md" >}})
* [Network Map overview]({{< relref "../../../../../en/platform/corda/1.3/cenm/network-map-overview.md" >}})
* [Certificate Revocation List]({{< relref "../../../../../en/platform/corda/1.3/cenm/certificate-revocation.md" >}})

CENM releases

* [Release notes]({{< relref "../../../../../en/platform/corda/1.3/cenm/release-notes.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "../../../../../en/platform/corda/1.3/cenm/upgrade-notes.md" >}})

Operations

* [Deployment with Kubernetes]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes.md" >}})
  * [CENM Auth Service Helm Chart]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes-auth.md" >}})
  * [CENM FARM Service Helm Chart]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes-farm.md" >}})
  * [CENM Identity Manager Helm Chart]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes-idman.md" >}})
  * [CENM Network Map Helm Chart]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes-nmap.md" >}})
  * [CENM Notary Helm Chart]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes-notary.md" >}})
  * [CENM Signing Service Helm Chart]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes-signer.md" >}})
  * [CENM Zone Service Helm Chart]({{< relref "../../../../../en/platform/corda/1.3/cenm/deployment-kubernetes-zone.md" >}})
* [CENM test environment quick start guide]({{< relref "../../../../../en/platform/corda/1.3/cenm/quick-start.md" >}})
* [Zone Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/zone-service.md" >}})
* [Angel Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/angel-service.md" >}})
* [Identity Manager Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/identity-manager.md" >}})
* [Network Map Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/network-map.md" >}})
* [Signing Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/signing-service.md" >}})
* [Auth Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/auth-service.md" >}})
* [FARM Service]({{< relref "../../../../../en/platform/corda/1.3/cenm/gateway-service.md" >}})
* [CENM Command-line Interface (CLI) tool]({{< relref "../../../../../en/platform/corda/1.3/cenm/cenm-cli-tool.md" >}})
* [Updating the network parameters]({{< relref "../../../../../en/platform/corda/1.3/cenm/updating-network-parameters.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "../../../../../en/platform/corda/1.3/cenm/upgrade-notes.md" >}})
* [CENM databases]({{< relref "../../../../../en/platform/corda/1.3/cenm/database-set-up.md" >}})
* [CENM User Admin tool]({{< relref "../../../../../en/platform/corda/1.3/cenm/user-admin.md" >}})
* [Troubleshooting common issues]({{< relref "../../../../../en/platform/corda/1.3/cenm/troubleshooting-common-issues.md" >}})
* [CENM support matrix]({{< relref "../../../../../en/platform/corda/1.3/cenm/cenm-support-matrix.md" >}})

Configuration

* [Identity Manager Service configuration parameters]({{< relref "../../../../../en/platform/corda/1.3/cenm/config-identity-manager-parameters.md" >}})
* [Network Map Service configuration parameters]({{< relref "../../../../../en/platform/corda/1.3/cenm/config-network-map-parameters.md" >}})
* [Network parameters]({{< relref "../../../../../en/platform/corda/1.3/cenm/config-network-parameters.md" >}})
* [Configuring the CENM services to use SSL]({{< relref "../../../../../en/platform/corda/1.3/cenm/enm-with-ssl.md" >}})
* [Workflow]({{< relref "../../../../../en/platform/corda/1.3/cenm/workflow.md" >}})

Tools and utilities

* [Tools and utilities]({{< relref "../../../../../en/platform/corda/1.3/cenm/tools-index.md" >}})
* [Embedded shell]({{< relref "../../../../../en/platform/corda/1.3/cenm/shell.md" >}})

Public Key Infrastructure

* [Certificate hierarchy guide]({{< relref "../../../../../en/platform/corda/1.3/cenm/pki-guide.md" >}})
* [Public Key Infrastructure (PKI) Tool]({{< relref "../../../../../en/platform/corda/1.3/cenm/pki-tool.md" >}})

Signing Plug-in Samples

* [EJBCA sample plug-in]({{< relref "../../../../../en/platform/corda/1.3/cenm/ejbca-plugin.md" >}})
