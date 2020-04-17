---
aliases:
- /releases/3.2/design/design-review-process.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- design
- review
- process
title: Design review process
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Design review process

The Corda design review process defines a means of collaborating approving Corda design thinking in a consistent,
structured, easily accessible and open manner.

The process has several steps:


* High level discussion with the community and developers on corda-dev.
* Writing a design doc and submitting it for review via a PR to this directory. See other design docs and the
design doc template (below).
* Respond to feedback on the github discussion.
* You may be invited to a design review board meeting. This is a video conference in which design may be debated in
real time. Notes will be sent afterwards to corda-dev.
* When the design is settled it will be approved and can be merged as normal.

The following diagram illustrates the process flow:

[![designReviewProcess](design/./designReviewProcess.png "designReviewProcess")](designReviewProcess.png)
At least some of the following people will take part in a DRB meeting:


* Richard G Brown (CTO)
* James Carlyle (Chief Engineer)
* Mike Hearn (Lead Platform Engineer)
* Mark Oldfield (Lead Platform Architect)
* Jonathan Sartin (Information Security manager)
* Select external key contributors (directly involved in design process)

The Corda Technical Advisory Committee may also be asked to review a design.

Here’s the outline of the design doc template:



* [Design doc template](template/design.md)
    * [Overview](template/design.md#overview)
    * [Background](template/design.md#background)
    * [Goals](template/design.md#goals)
    * [Non-goals](template/design.md#non-goals)
    * [Timeline](template/design.md#timeline)
    * [Requirements](template/design.md#requirements)
    * [Design Decisions](template/design.md#design-decisions)
        * [Design Decision: <Description heading>](template/decisions/decision.md)
            * [Background / Context](template/decisions/decision.md#background-context)
            * [Options Analysis](template/decisions/decision.md#options-analysis)
                * [A. <Option summary>](template/decisions/decision.md#a-option-summary)
                    * [Advantages](template/decisions/decision.md#advantages)
                    * [Disadvantages](template/decisions/decision.md#disadvantages)


                * [B. <Option summary>](template/decisions/decision.md#b-option-summary)
                    * [Advantages](template/decisions/decision.md#id1)
                    * [Disadvantages](template/decisions/decision.md#id2)




            * [Recommendation and justification](template/decisions/decision.md#recommendation-and-justification)




    * [Design](template/design.md#design)





