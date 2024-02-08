---
aliases:
- /releases/release-1.2/index.html
date: '2020-01-08T09:59:25Z'
project: corda
section_menu: cenm-1-2
version: 'CENM 1.2'
description: "Documentation for the 1.2 release of Corda Enterprise Network Manager (CENM)"
menu:
  versions:
    weight: 320
  cenm-1-2:
    weight: 1
    name: CENM 1.2
project: corda
section_menu: cenm-1-2
title: CENM 1.2
version: 'CENM 1.2'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the operator full control over all aspects of deployment, operation, and the consensus rules.
This is provided as an alternative to taking advantage of utilising the service-level-managed production components
that are otherwise be available from [Corda Network](https://corda.network), governed by the independent
Corda Network Foundation.

The *Corda Enterprise Network Manager* encompasses three main services:


* [Identity Manager Service]({{< relref "../../../../../en/platform/corda/1.2/cenm/identity-manager.md" >}}) - Enables nodes to join the network, as well as handles revocation of a nodes certificate
* [Network Map Service]({{< relref "../../../../../en/platform/corda/1.2/cenm/network-map.md" >}}) - Provides a global view of the network
* [Signing Services]({{< relref "../../../../../en/platform/corda/1.2/cenm/signing-service.md" >}}) - Provides a way to sign approved requests to join the network (CSRs) or revoke a certificate
(CRRs) as well as changes to the network map

For a quick start guide on running the ENM services see [Enterprise Network Manager Quick-Start Guide]({{< relref "../../../../../en/platform/corda/1.2/cenm/quick-start.md" >}}).


Concepts and Overview

* [Corda Networks]({{< relref "../../../../../en/platform/corda/1.2/cenm/corda-networks.md" >}})
* [Components of the Corda Enterprise Network Manager]({{< relref "../../../../../en/platform/corda/1.2/cenm/enm-components.md" >}})
* [The workflow]({{< relref "../../../../../en/platform/corda/1.2/cenm/workflow.md" >}})
* [Databases]({{< relref "../../../../../en/platform/corda/1.2/cenm/database-set-up.md" >}})
* [Public Key Infrastructure (PKI)]({{< relref "../../../../../en/platform/corda/1.2/cenm/pki-tool.md" >}})
* [The node](../../../../../en/platform/corda/1.2/cenm/network-map.html#node-certificate-revocation-checking)
* [Sub Zones]({{< relref "../../../../../en/platform/corda/1.2/cenm/sub-zones.md" >}})
* [Network Map overview]({{< relref "../../../../../en/platform/corda/1.2/cenm/network-map-overview.md" >}})
* [Certificate Revocation List]({{< relref "../../../../../en/platform/corda/1.2/cenm/certificate-revocation.md" >}})




CENM Releases

* [Release notes]({{< relref "../../../../../en/platform/corda/1.2/cenm/release-notes.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "../../../../../en/platform/corda/1.2/cenm/upgrade-notes.md" >}})
* [Changelog]({{< relref "../../../../../en/platform/corda/1.2/cenm/changelog.md" >}})
* [Legal notice]({{< relref "../../../../../en/platform/corda/1.2/cenm/legal-info/legal-info-1.2.3.md" >}})




Operations

* [Enterprise Network Manager Quick-Start Guide]({{< relref "../../../../../en/platform/corda/1.2/cenm/quick-start.md" >}})
* [Deployment with Kubernetes]({{< relref "../../../../../en/platform/corda/1.2/cenm/deployment-kubernetes.md" >}})
* [Identity Manager Service]({{< relref "../../../../../en/platform/corda/1.2/cenm/identity-manager.md" >}})
* [Network Map Service]({{< relref "../../../../../en/platform/corda/1.2/cenm/network-map.md" >}})
* [Signing Services]({{< relref "../../../../../en/platform/corda/1.2/cenm/signing-service.md" >}})
* [Updating the network parameters]({{< relref "../../../../../en/platform/corda/1.2/cenm/updating-network-parameters.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "../../../../../en/platform/corda/1.2/cenm/upgrade-notes.md" >}})
* [CENM Databases]({{< relref "../../../../../en/platform/corda/1.2/cenm/database-set-up.md" >}})
* [Troubleshooting Common Issues]({{< relref "../../../../../en/platform/corda/1.2/cenm/troubleshooting-common-issues.md" >}})
* [CENM support matrix]({{< relref "../../../../../en/platform/corda/1.2/cenm/cenm-support-matrix.md" >}})




Configuration

* [Identity Manager Configuration Parameters]({{< relref "../../../../../en/platform/corda/1.2/cenm/config-identity-manager-parameters.md" >}})
* [Network Map Configuration Parameters]({{< relref "../../../../../en/platform/corda/1.2/cenm/config-network-map-parameters.md" >}})
* [Network Parameters]({{< relref "../../../../../en/platform/corda/1.2/cenm/config-network-parameters.md" >}})
* [Configuring the ENM services to use SSL]({{< relref "../../../../../en/platform/corda/1.2/cenm/enm-with-ssl.md" >}})
* [Workflow]({{< relref "../../../../../en/platform/corda/1.2/cenm/workflow.md" >}})




Tools & Utilities

* [Tools and Utilities]({{< relref "../../../../../en/platform/corda/1.2/cenm/tools-index.md" >}})
* [Embedded Shell]({{< relref "../../../../../en/platform/corda/1.2/cenm/shell.md" >}})




Public Key Infrastructure

* [Certificate Hierarchy Guide]({{< relref "../../../../../en/platform/corda/1.2/cenm/pki-guide.md" >}})
* [Public Key Infrastructure (PKI) Tool]({{< relref "../../../../../en/platform/corda/1.2/cenm/pki-tool.md" >}})




Signing Plugin Samples

* [EJBCA Sample Plugin]({{< relref "../../../../../en/platform/corda/1.2/cenm/ejbca-plugin.md" >}})
