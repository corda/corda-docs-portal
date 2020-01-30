---
title: "Welcome to the Corda Enterprise Network Manager"
date: 2020-01-08T09:59:25Z
---


# Welcome to the Corda Enterprise Network Manager
The Corda Enterprise Network Manager is a commercial offering from R3 that facilitates the operation of a bespoke
            Corda network that gives the operator full control over all aspects of deployment, operation, and the consensus rules.
            This is provided as an alternative to taking advantage of utilising the service-level-managed production components
            that are otherwise be available from [Corda Network](https://corda.network), governed by the independent
            Corda Network Foundation.

The *Corda Enterprise Network Manager* encompasses three main services:


* [Identity Manager Service]({{< relref "identity-manager" >}}) - Enables nodes to join the network, as well as handles revocation of a nodes certificate


* [Network Map Service]({{< relref "network-map" >}}) - Provides a global view of the network


* [Signing Services]({{< relref "signing-service" >}}) - Provides a way to sign approved requests to join the network (CSRs) or revoke a certificate
                    (CRRs) as well as changes to the network map


For a quick start guide on running the ENM services see [Enterprise Network Manager Quick-Start Guide]({{< relref "quick-start" >}}).


Concepts and Overview
* [Corda Networks]({{< relref "corda-networks" >}})

* [Components of the Corda Enterprise Network Manager]({{< relref "enm-components" >}})

* [The Workflow]({{< relref "enm-components#the-workflow" >}})

* [Databases]({{< relref "enm-components#databases" >}})

* [Public Key Infrastructure]({{< relref "enm-components#public-key-infrastructure" >}})

* [The Node]({{< relref "enm-components#the-node" >}})

* [Sub Zones]({{< relref "sub-zones" >}})

* [Network Map Overview]({{< relref "network-map-overview" >}})

* [Certificate Revocation List (CRL)]({{< relref "certificate-revocation" >}})



CENM Releases
* [Release notes]({{< relref "release-notes" >}})

* [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes" >}})

* [Changelog]({{< relref "changelog" >}})



Operations
* [Enterprise Network Manager Quick-Start Guide]({{< relref "quick-start" >}})

* [Identity Manager Service]({{< relref "identity-manager" >}})

* [Network Map Service]({{< relref "network-map" >}})

* [Signing Services]({{< relref "signing-service" >}})

* [Updating the network parameters]({{< relref "updating-network-parameters" >}})

* [Upgrading Corda Enterprise Network Manager]({{< relref "upgrade-notes" >}})

* [CENM Databases]({{< relref "database-set-up" >}})

* [Troubleshooting Common Issues]({{< relref "troubleshooting-common-issues" >}})

* [CENM support matrix]({{< relref "cenm-support-matrix" >}})



Configuration
* [Identity Manager Configuration Parameters]({{< relref "config-identity-manager-parameters" >}})

* [Network Map Configuration Parameters]({{< relref "config-network-map-parameters" >}})

* [Network Parameters]({{< relref "config-network-parameters" >}})

* [Configuring the ENM services to use SSL]({{< relref "enm-with-ssl" >}})

* [Workflow]({{< relref "workflow" >}})



Tools & Utilities
* [Tools & Utilities]({{< relref "tools-index" >}})

* [Embedded Shell]({{< relref "shell" >}})



Public Key Infrastructure
* [Certificate Hierarchy Guide]({{< relref "pki-guide" >}})

* [Public Key Infrastructure (PKI) Tool]({{< relref "pki-tool" >}})



