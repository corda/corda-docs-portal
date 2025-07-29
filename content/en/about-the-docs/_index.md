---
title: "About the Docs"
date: 2023-08-16
section_menu: about-the-docs
---
# About the Docs

The following topics are explained on this page:

* [Reading the Docs]({{< relref "#reading-the-docs">}})
* [Documentation End of Life Strategy]({{< relref "#documentation-end-of-life-strategy">}})
* [Reporting an Error in the Docs]({{< relref "#reporting-an-error-in-the-docs">}})

## Reading the Docs

The Corda documentation is written from the perspectives of a collection of people; each with their own problems to solve. Relevant sections of the documentation should resonate with you, depending on the persona whose goals you share. The documentation currently addresses the following personas:

* [Architect]({{< relref "#architect">}})
* [CorDapp Developer]({{< relref "#cordapp-developer">}})
* [Cluster Administrator]({{< relref "#cluster-administrator">}})
* [Network Operator]({{< relref "#network-operator">}})

### Architect

As an Architect considering or planning a project with Corda, you:

* are curious about the benefits of adopting {{< tooltip >}}DLT{{< /tooltip >}} technology, but also concerned about any risks.
* want to know why DLT is a better fit for your business problem than a centralized solution.
* are for looking for answers and guidance to the following questions:
  * Who has access to my {{< tooltip >}}vault{{< /tooltip >}} data and how is privacy preserved in Corda?
  * How do I manage the compromising of cryptographic key material?
  * How do I maintain compliance with GDPR (and other data protection regulations) if personal data is stored in Corda?
  * How do I scale Corda?
  * How do I maintain business continuity for Corda?
  * How do I deploy Corda into my enterprise infrastructure and integrate it with my enterprise applications?

### CorDapp Developer

A {{< tooltip >}}CorDapp{{< /tooltip >}} Developer uses Corda to:

* explore DLT and create their own chain of shared facts to experiment with.
* design an enterprise production-grade distributed application.
* work as part of a team to build an enterprise production-grade distributed application.
* understand the software development lifecycle (SDLC) of a distributed application.
* implement a method in the API to make something simpler.
* discover best practice design tips for distributed applications.

### Cluster Administrator

A Cluster Administrator is responsible for:

* making informed decisions to deliver the prerequisites for Corda.
* installing and operating the Corda software.
* integrating Corda into Continuous Integration and Delivery CI/CD pipelines.
* understanding how Corda manages errors to deliver continuous execution.
* the disaster recovery story for Corda.
* monitoring the health metrics of Corda.

### Network Operator

The Network Operator is concerned with:

* how Corda delivers on the _permissioned_ aspect of a private permissioned DLT platform.
* service levels for participants on the business network.
* defining permissions for actions on the business network.
* “know your customer” (KYC) regulations.

The Network Operator:

* onboards participants of a business network.
* manages the lifecycle of participants on the network.
* defines and applies network membership rules for participation in the business network.
* distributes CorDapps to network participants.

## Documentation End of Life Strategy

Use the following table to track the end of life schedule for each version of Corda. Each version of Corda has R3 support available for a fixed period.
After this period has ended, these versions are no longer supported by R3 and associated documentation is archived. You should always aim to upgrade to the latest version of Corda whenever possible.

Definitions:

* **End of maintenance**: This release will no longer receive functional patches after the date shown.
* **End of security**: This release will no longer be eligible for security patches after the date shown.
* **End of support**: Support (including documentation) provided by R3 is no longer available after this date.

{{< note >}}
All dates refer to the end of the month indicated.
{{< /note >}}

{{< note >}}
The highest released version of Corda 4 Enterprise Edition at any point in time will be supported, including maintenance, until at least 31st December 2029 or until superseded by a higher version number of Corda 4 Enterprise Edition, at which point the dates in the table take precedence.
{{< /note >}}

### Corda 4

{{< snippet "corda-4/end-of-life-corda4.md" >}}

### CENM

{{< snippet "cenm/end-of-life-cenm.md" >}}

## Reporting an Error in the Docs

The R3 Technical Writing team continuously strive to improve our documentation and overall content strategy. As we make improvements, we would love to get your feedback on what we are doing well, and what we could be doing better.

To contact the R3 Technical Writing team, send an e-mail to [docs@r3.com](mailto:docs@r3.com). To help us deal with your feedback effectively, please include all of the following:

* Your name
* Your company name
* Your email address (if different from the one being used to report)
* The URL of the documentation page (if it is an issue being reported)

Please include as much detail as you can in your feedback, as it is valuable to us and it will be read and shared with the rest of the team. A ticket is then created for any issues received, which will be quickly triaged and, if necessary, assigned to a Technical Writer to effect changes.
