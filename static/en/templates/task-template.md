---

date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-updating-network-parameters
    parent: cenm-1-2-operations
    weight: 160
tags:
- updating
- network
- parameters
title: Updating the network parameters
---

Introduce the task. Write a sentence or two summarizing the answers the reader's two main questions:
* What will I learn to do?
* How will I do it?


## Before you start
<!-- Delete this section if your readers don't need any prerequisite knowledge. -->
This section prevents readers from getting halfway through and discovering that they need to do something else before they can continue, like download software or get permissions. Use this section to guide the reader to any resources they need before starting this task. Include other important information here, such as known issues or bugs. For example:

Before you begin, make sure you meet these prerequisites:

* Pre-requisite one
* Pre-requisite two



## Active voice header

<!-- If an image would be easier to interpret than descriptive text, put the image first. Otherwise, lead with the text. -->

![alt text](https://docs.corda.net/en/images/node-architecture.png "Image title that describes image.")

Explanation of image.

## Active voice header - ordered list example

<!-- Use ordered lists for sequential steps. Do not use unordered lists for tasks that must be performed in a specific order. -->

Start with a lead-in sentence for an ordered list:

1. Sub-step A
    * Use bullet points for binary options within the step or non-ordered sub-sub steps
2. Sub-step B
    1. Use ordered nested lists for sequential sub-sub tasks. NB: Basic markdown does not support lettered lists.
3. Sub-step C

Include step results where appropriate. For example, if you select an option and it opens a confirmation window, include a step result saying "A confirmation window opens".

## Active voice header - code snippet example

Lead with a sentence explaining the code snippet. For example:

You can configure the node to use a time window reservoir. Add the following configuration block to the `node.conf` file:

<!-- Wrap code examples in backticks ```. You can define a specific coding language as syntax highlighting. See https://www.markdownguide.org/extended-syntax/#syntax-highlighting.-->

enterpriseConfiguration {
    metricsConfiguration {
        reservoirType = TIME_WINDOW // Can also be EDR, but this is the default if this item is absent
        timeWindow = <Duration> // Optional - will default to 5m if not specified
    }

## Outcome

What has changed now that the task is finished? Summarize the steps completed and explain what the user has achieved by following them. This should reiterate and match the step sequence.


## Related content
You can also include links to related articles, such as:
* Concept documents that give background information about the task.
* Related task articles.
* Relevant reference material.
