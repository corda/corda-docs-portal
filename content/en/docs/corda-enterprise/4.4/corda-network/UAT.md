---
aliases:
- /releases/4.4/corda-network/uat.html
- /docs/corda-enterprise/head/uat.html
- /docs/corda-enterprise/uat.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-the-corda-network
tags:
- UAT
title: Corda Network Pre-Production environment
weight: 1000
---

# Corda Network Pre-Production environment

The Corda Network Pre-Production (also known as the User Acceptance Testing/UAT) environment seeks to provide a test environment which is as close as possible to Corda Network in its make-up and operation.

For owners of tested CorDapps with a firm plan to take them into production, a bespoke Pre-Production environment is provided. Here, such CorDapps can be further tested in the network configuration they will experience in production, utilising relevant Corda Network services (including the Identity Operator, Network Map and notaries).

The Corda Network Pre-Production environment is not intended for customers’ full test cycles, as it is expected that the bulk of CorDapp testing will occur in simpler network configurations run by the CorDapp provider, but is available for testing of functionally complete and tested CorDapps in realistic network settings. The environment simulates the real-world business environment, including the production settings of network parameters, Corda network services and supported Corda versions.

The environment is therefore more aligned to the testing of the operational characteristics of networked CorDapps rather than their specific functional features, although we recognise there can be overlap between the two. Realistic test data is therefore expected to be used and may include data copied from production environments and hence representing real world entities and business activities. It will be up to the introducer of such data to ensure that all relevant data protection legislation is complied with and, in particular, that the terms and conditions under which Corda Network services process such data is suitable for their needs. All test data will be cleared from Corda Network services on the completion of testing.


## Pre-requisites to joining the Pre-Production environment

*The below pre-requisites assume the potential participant is joining the Pre-Production environment directly, and as such is not "sponsoring" or onboarding other participants. If this is the case, please contact your Corda representative for how to "sponsor" end-participants.*

### Technical pre-requisites

* One or more physical or virtual machines with a compatible operating system and a compatible Java version (for example, Oracle JDK 8u131+) upon which to deploy Corda
* Corda software - either Open Source or Corda Enterprise (Corda Enterprise requires a license from R3)
* A static external IP address for each machine on which Corda will be run

### Business pre-requisites

* Appropriate contractual terms have been agreed for access to the Corda Network services
* Access to the appropriate environment has been agreed with your project representative with sufficient advance notice (4 weeks is standard but may be longer if you have special service requirements) to ensure appropriate SLAs can be in place. Your project representative will be able to supply the booking template.

{{< note >}}
Corda Network Pre-Production is governed by an [independent Foundation](https://corda.network/governance/index.html).
{{< /note >}}

##  Joining the Pre-Production environment

*The below joining steps assume the potential participant is joining the Pre-Production environment directly, and as such is not "sponsoring" or onboarding other participants. If this is the case, please contact your Corda representative for how to "sponsor" end-participants.*

Steps to join are outlined on the [Corda Network site](https://corda.network/participation/index.html).

For further questions on this process, please contact us - preferably on the mailing list: [https://groups.io/g/corda-network](https://groups.io/g/corda-network) or at [info@corda.network](mailto:info@corda.network)
