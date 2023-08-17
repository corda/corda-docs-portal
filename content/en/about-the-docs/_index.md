---
title: "About the Docs"
date: 2023-08-16
---
# About the Docs
The following topics are explained on this page:
* [Reporting an Error in the Docs]({{< relref "#reporting-an-error-in-the-docs">}})
* [Documentation End of Life Strategy]({{< relref "#documentation-end-of-life-strategy">}})
* [Documenting Corda 5]({{< relref "#documenting-corda-5">}})

## Reporting an Error in the Docs
The R3 Technical Writing team continuously strive to improve our documentation and overall content strategy. As we make improvements, we would love to get your feedback on what we are doing well, and what we could be doing better. 

Click [here](mailto:docs@r3.com) to email the R3 Technical Writing team. To help us deal with your feedback effectively, please include all of the following:

* Your name
* Your company name
* Your email address (if different from the one being used to report)
* The URL of the documentation page (if it is an issue being reported)

Please include as much detail as you can in your feedback, as it is valuable to us and it will be read and shared with the rest of the team. A ticket is then created for any issues received, which will be quickly triaged and, if necessary, assigned to a Technical Writer to effect changes.

{{< note >}}
We are working on refining our documentation feedback process. In the near future, you will be able to submit feedback more interactively and directly from the documentation.
{{</ note >}}

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

### Corda 5

{{< snippet "corda-5.0/end-of-life-corda5.md" >}}

### Corda 4

{{< snippet "corda-4/end-of-life-corda4.md" >}}

## Documenting Corda 5
The Corda 5 documentation is structured differently to previous versions of Corda. Previously, Corda Enterprise and Corda Community content was published in separate documentation sets. 
From Corda 5.0 onwards, there is one documentation set, but the features that relate to Corda Enterprise are marked to avoid confusion. 

{{< 
  figure
	 src="docs-enterprise-icon-use-case.png"
   width=55%
	 figcaption="Documentation heading with Enterprise icon"
	 alt="Enterprise icon"
>}}

* **A**: The heading without the 'Enterprise only' icon is the most common and it is used where the content applies to all Corda users.
* **B**: The ‘Enterprise only' icon is used mostly in headings, indicating that the content under that heading relates to a Corda Enterprise feature. On occasions, the icon may be used inline to identify sentences, paragraphs, or tables that apply to a Corda Enterprise feature.