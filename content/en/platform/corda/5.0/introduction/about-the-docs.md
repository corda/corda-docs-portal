---
title: "About the Docs"
date: 2023-04-21
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-about-the-docs
    parent: corda5-intro
    weight: 1000
section_menu: corda5
---
# About the Docs
The following topics are explained on this page:
* [Documenting Product Editions](#documenting-product-editions)
* [End of Life Strategy](#end-of-life-strategy)
* [Reporting an Error in the Docs](#reporting-an-error-in-the-docs)

## Documenting Product Editions
The Corda 5 documentation is structured differently than in previous versions of Corda. Previously, Corda Enterprise and Corda Community content was published in separate documentation sets. 
From Corda 5.0 onwards, there is one documentation set, but the features that relate to Corda Enterprise are marked to avoid confusion. 

{{< 
  figure
	 src="docs-enterprise-icon-use-case.png"
   width=55%
	 figcaption="Documentation heading with Enterprise icon"
	 alt="Enterprise icon"
>}}

* **A**: The heading without the ‘Enterprise only' icon is the most common and it is used where the content relates to both Corda Community and Corda Enterprise editions of the product.
* **B**: The ‘Enterprise only' icon is used mostly in headings, indicating that the entire content under that heading relates only to Corda Enterprise. On occasions, the icon may be used inline to identify sentences, paragraphs, or tables that are for Corda Enterprise only. 

## End of Life Strategy
Use the following table to track the end of life schedule for each version of Corda 5. Each version of Corda has R3 support available for a fixed period. 
After this period has ended, these versions are no longer supported by R3 and associated documentation is archived. You should always aim to upgrade to the latest version of Corda whenever possible.

Definitions:

* **End of maintenance**: This release will no longer receive functional patches after the date shown.
* **End of security**: This release will no longer be eligible for security patches after the date shown.
* **End of support**: Support (including documentation) provided by R3 is no longer available after this date.

| **Version** | **Date of Release** | **End of Maintenance** | **End of Security**   | **End of Support**    |
|:-------------:|:-------------------:|:----------------------:|:---------------------:|:---------------------:|
| **Corda 5.0** | Jun-23              | Upon release of 5.2    | Upon release of 5.2   | Upon release of 5.2   |
| **Corda 5.1** | TBC                 | Upon release of 5.2    | Upon release of 5.2   | Upon release of 5.2   |
| **Corda 5.2** | TBC                 | 2 years after release  | 2 years after release | 2 years after release |


## Reporting an Error in the Docs
In 2023, the R3 Technical Writing team will be making big changes to our documentation and our overall content strategy. As we make improvements, we’d love to get your feedback on what we’re doing well, and what we could be doing better. 

Click [here](mailto:docs@r3.com) to email the R3 Technical Writing team. To help us deal with your feedback effectively, please include all of the following:

* Your name
* Your company name
* Your email address (if different from the one being used to report)
* The URL of the documentation page (if it is an issue being reported)

Please include as much detail as you can in your feedback, as it is valuable to us and it will be read and shared with the rest of the team. A ticket is then created for any issues received, which will be quickly triaged and if necessary, assigned to a Technical Writer to effect changes.

{{< note >}}
We are working on refining our documentation feedback process. In the near future, you will be able to submit feedback more interactively and directly from the documentation.
{{</ note >}}

