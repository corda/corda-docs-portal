---
aliases:
- /releases/release-1.2/index.html
date: '2020-01-08T09:59:25Z'
project: Corda
section_menu: cenm-1-2
version: 'CENM 1.2'
description: "Documentation for the 1.2 release of Corda Enterprise Network Manager (CENM)"
menu:
  versions:
    weight: 320
  cenm-1-2:
    weight: 1
    name: CENM 1.2
project: Corda
section_menu: cenm-1-2
title: CENM 1.2
version: 'CENM 1.2'
---


# Welcome to the Corda Enterprise Network Manager

The Corda Enterprise Network Manager is a commercial offering from R3 that facilitates the operation of a bespoke
Corda network that gives the operator full control over all aspects of deployment, operation, and the consensus rules.


The *Corda Enterprise Network Manager* encompasses three main services:


* [Identity Manager service]({{< relref "identity-manager.md" >}}) - Enables nodes to join the network, as well as handles revocation of a nodes certificate
* [Network Map service]({{< relref "network-map.md" >}}) - Provides a global view of the network
* [Signing services]({{< relref "signing-service.md" >}}) - Provides a way to sign approved requests to join the network (CSRs) or revoke a certificate
(CRRs) as well as changes to the network map

For a quick start guide on running the ENM services see [Network Manager quick-start guide]({{< relref "quick-start.md" >}}).


Concepts and Overview

* [Corda Networks]({{< relref "corda-networks.md" >}})
* [Network Manager components]({{< relref "enm-components.md" >}})
* [The workflow]({{< relref "workflow.md" >}})
* [Databases]({{< relref "database-set-up.md" >}})
* [Public Key Infrastructure (PKI)]({{< relref "pki-tool.md" >}})
* [The node]({{< relref "network-map.md#node-certificate-revocation-checking" >}})
* [Subzones]({{< relref "sub-zones.md" >}})
* [Network Map overview]({{< relref "network-map-overview.md" >}})
* [Certificate Revocation List]({{< relref "certificate-revocation.md" >}})




CENM Releases

* [Release notes]({{< relref "release-notes.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes.md" >}})
* [Changelog]({{< relref "changelog.md" >}})
* [Legal notice]({{< relref "legal-info/legal-info-1.2.3.md" >}})




Operations

* [Network Manager quick-start guide]({{< relref "quick-start.md" >}})
* [Deployment with Kubernetes]({{< relref "deployment-kubernetes.md" >}})
* [Identity Manager service]({{< relref "identity-manager.md" >}})
* [Network Map service]({{< relref "network-map.md" >}})
* [Signing services]({{< relref "signing-service.md" >}})
* [Updating the network parameters]({{< relref "updating-network-parameters.md" >}})
* [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes.md" >}})
* [CENM Databases]({{< relref "database-set-up.md" >}})
* [Troubleshooting common issues]({{< relref "troubleshooting-common-issues.md" >}})
* [CENM support matrix]({{< relref "cenm-support-matrix.md" >}})




Configuration

* [Identity Manager configuration parameters]({{< relref "config-identity-manager-parameters.md" >}})
* [Network Map configuration parameters]({{< relref "config-network-map-parameters.md" >}})
* [Network parameters]({{< relref "config-network-parameters.md" >}})
* [Configuring the ENM services to use SSL]({{< relref "enm-with-ssl.md" >}})
* [Workflow]({{< relref "workflow.md" >}})




Tools & Utilities

* [Tools and utilities]({{< relref "tools-index.md" >}})
* [Embedded Shell]({{< relref "shell.md" >}})




Public Key Infrastructure

* [Certificate hierarchy guide]({{< relref "pki-guide.md" >}})
* [Public key infrastructure (PKI) tool]({{< relref "pki-tool.md" >}})




Signing Plugin Samples

* [EJBCA sample plugin]({{< relref "ejbca-plugin.md" >}})
