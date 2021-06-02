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


# Title

Summarize what the reader will get out of the document in a short overview. This could be a sentence or two for simpler documents, or bullet points for longer ones.

* Match the order of the bullet points to the order of the topics.
* Keep bullet points grammatically consistent. Start each bullet with either a verb or a noun. Verbs are more action-oriented and usually the best choice.
* Remember to keep your audience in mind - what points interest them the most?


## Topic

The structure of reference articles varies based on the information you are documenting. In most cases, reference information is easiest to express as a table or list. Make sure the information is presented in a logical order that makes it easy to find a specific piece of information without reading the entire document. For example, you could order content chronologically or alphabetically.

## Example list

Use unordered lists for data that:

* Does not need to be actioned in a specific sequence. If it does, use an ordered list - and make sure you are not writing a [task document](task.md).
* Does not have multiple attributes. If it does, use a table with a column for each attribute.

Present information in a list logically, even if it is not sequential. Depending on the content, you could order it alphabetically, chronologically, or in order of importance. Consider what information the reader needs from the list and order it accordingly - are they scanning for one particular item, or ensuring they have met a list of requirements?

## Example tables

Use tables for data that:

* Has multiple attributes. Use one column for each attribute.
* Requires comparison.
* Untangles "if, then" sentences.

Order the columns and rows in your table logically according to the content and the needs of the reader.

### Example parameter reference

<--Wrap tables in Hugo shortcode table tags. -->
|Name |Type |Required |Description |
|:--- |:--- |:--- |:--- |
|productCode|`string`|Yes|Code of the document product to return the schema for. <br> <ul><li>Here is a bulleted list with a \| (pipe) inside a table.</li><li>Another bulleted list.<ul><li>An indented list</li></ul></li><li>Back to the list.</li></ul> |
|||||


### Example field name reference
<--Wrap tables in Hugo shortcode table tags. -->
|Name |Type |Required |Description |
|:--- |:--- |:--- |:--- |
|Company|`string`|No|The name of the company the person works at or is representing.|
|First Name|`string`|Yes|The first name of the person requiring training.|
|Last Name|`string`|Yes|The surname of the person requiring training.|


### Example nested table
<--Wrap tables in Hugo shortcode table tags. -->
<table>
  <tr>
    <th>Col 1</th>
    <th>Col 2</th>
  </tr>
  <tr>
    <th>Cell 1.1</th>
    <th>Cell 1.2</th>
  </tr>
  <tr>
    <th>Cell 2.1</th>
    <th>Cell 2.2
        <table>
            <tr>
              <th>Nested header 1</th>
              <th>Nested header 2</th>
            </tr>
            <tr>
              <th>Nested cell 1</th>
              <th>Nested cell 2</th>
            </tr>
        </table>
    </th>
  </tr>
  <tr>
     <th>Cell 3.1</th>
     <td>Cell 3.2</td>
  </tr>
</table>



## Related content

You can include links to related articles, such as:
* Conceptual documents that give background information about the topic.
* Related task articles.
* Additional reference material.
