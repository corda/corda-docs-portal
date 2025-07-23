---
aliases:
- /docs/cenm/head/index.html
- /docs/cenm/index.html
date: '2020-01-08T09:59:25Z'
description: "Documentation for the 1.4 release of Corda Enterprise Network Manager (CENM)"
menu:
  versions:
    weight: 300
  cenm-1-4:
    weight: 1
    name: CENM 1.4
project: Corda
section_menu: cenm-1-4
title: CENM 1.4
version: 'CENM 1.4'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager (CENM) is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the user full control over all aspects of deployment, operation, and consensus rules.

{{< note >}}
**Release notes**

* For all Corda Enterprise Network Manager release notes, see the [Corda Enterprise Network Manager release notes]({{< relref "release-notes.md" >}}) page.
* For the latest Corda Enterprise release notes, see the [Corda Enterprise Edition 4.6 release notes](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-enterprise/4.6/enterprise/release-notes-enterprise.md) page. You can view release notes for previous versions of Corda Enterprise in the relevant documentation section for each version, accessible from the left-hand side menu.
* For all Corda open source release notes, see the [Corda release notes](https://github.com/corda/corda-docs-portal/blob/main/content/en/archived-docs/corda-os/4.6/release-notes.md) page.

{{< /note >}}

The Corda Enterprise Network Manager provides three main services:

* [Identity Manager service]({{< relref "identity-manager.md" >}}) - enables nodes to join the network, and handles revocation of a node certificate.
* [Network Map service]({{< relref "network-map.md" >}}) - provides a global view of the network.
* [Signing Service]({{< relref "signing-service.md" >}}) - provides a way to sign approved requests to join the network (Certificate Signing Requests - CSRs) or revoke a certificate (Certificate Revocation Requests - CRRs), as well as changes to the network map.

{{< note >}}
For instructions on deploying Corda Enterprise Network Manager with Docker, Kubernetes, and Helm charts, see [CENM Deployment with Docker, Kubernetes, and Helm charts]({{< relref "deployment-kubernetes.md" >}}).

For a quick start guide on deploying Corda Enterprise Network Manager services as a test environment, see the [CENM test environment quick start guide]({{< relref "quick-start.md" >}}).
{{< /note >}}

Concepts and overview

* [Corda Networks]({{< relref "corda-networks.md" >}})
* [Network Manager components]({{< relref "enm-components.md" >}})
* [The workflow]({{< relref "workflow.md" >}})
* [Databases]({{< relref "database-set-up.md" >}})
* [Public Key Infrastructure (PKI)]({{< relref "pki-tool.md" >}})
* [The node]({{< relref "network-map.md#node-certificate-revocation-checking" >}})
* [Subzones]({{< relref "sub-zones.md" >}})
* [Network Map overview]({{< relref "network-map-overview.md" >}})
* [Certificate Revocation List]({{< relref "certificate-revocation.md" >}})

CENM releases

* [Release notes]({{< relref "release-notes.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes.md" >}})

Operations

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
* [Auth Service]({{< relref "auth-service.md" >}})
* [Gateway service]({{< relref "gateway-service.md" >}})
* [CENM Command-line Interface (CLI) tool]({{< relref "cenm-cli-tool.md" >}})
* [Updating the network parameters]({{< relref "updating-network-parameters.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes.md" >}})
* [CENM databases]({{< relref "database-set-up.md" >}})
* [CENM User Admin tool]({{< relref "user-admin.md" >}})
* [Troubleshooting common issues]({{< relref "troubleshooting-common-issues.md" >}})
* [CENM support matrix]({{< relref "cenm-support-matrix.md" >}})

Configuration

* [Identity Manager Service configuration parameters]({{< relref "config-identity-manager-parameters.md" >}})
* [Network Map Service configuration parameters]({{< relref "config-network-map-parameters.md" >}})
* [Network parameters]({{< relref "config-network-parameters.md" >}})
* [Configuring the CENM services to use SSL]({{< relref "enm-with-ssl.md" >}})
* [Workflow]({{< relref "workflow.md" >}})

Tools and utilities

* [Tools and utilities]({{< relref "tools-index.md" >}})
* [Embedded shell]({{< relref "shell.md" >}})

Public Key Infrastructure

* [Certificate hierarchy guide]({{< relref "pki-guide.md" >}})
* [Public key infrastructure (PKI) tool]({{< relref "pki-tool.md" >}})

Signing Plug-in Samples

* [EJBCA sample plug-in]({{< relref "ejbca-plugin.md" >}})
