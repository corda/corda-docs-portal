---
aliases:
- /jira-setup.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- jira
- setup
title: JIRA Set-Up
---


# JIRA Set-Up

The following are the instructions on setting up the JIRA in order to satisfy minimal requirements from the point of view
of the Identity Manager Certificate Signing Request (CSR)/Certificate Revocation Request (CRR) approval workflow. This will enable
a user to integrate such JIRA deployment with the CENM CSR/CRR approval workflow plugin.


## User Set-Up

Create a user with an administrative permissions and make sure it is assigned to the default groups:
`jira-administrators` and `jira-software-users`. The following shows an example for a `Test` user setup.

![jira 7](/en/images/jira-7.png "jira 7")

## Project Set-Up

Create two projects (one for Certificate Signing Requests and one for Certificate Revocation Requests) of the type of
`Process Management`. The following shows final settings for both projects.

![jira 6](/en/images/jira-6.png "jira 6")

## Project Workflow

Make sure that both projects (CSR and CRR) have the following workflow configured.

![jira 1](/en/images/jira-1.png "jira 1")
Tickets are moved from `Approved` status to `Done` automatically, once the request is signed by the HSM.


## Custom fields

Additionally, the following 3 custom fields need to be created and configured in JIRA:



* Request ID
* Reject Reason
* Reject Reason Description


{{< note >}}
These fields are global and applicable to both CSR and CRR projects. Screen selection (see snippets below) alows
for field assignment to a specific project.

{{< /note >}}
The following snippets depict the configuration for those fields:

![jira 4](/en/images/jira-4.png "jira 4")
![jira 3](/en/images/jira-3.png "jira 3")
![jira 2](/en/images/jira-2.png "jira 2")
![jira 5](/en/images/jira-5.png "jira 5")
