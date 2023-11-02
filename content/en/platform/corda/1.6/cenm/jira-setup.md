---
aliases:
- /jira-setup.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-5:
    identifier: cenm-1-5-jira-setup
    parent: cenm-1-5-configuration
    weight: 300
tags:
- jira
- setup
title: JIRA Set-Up
---


# Jira setup

To integrate a Jira deployment with the CENM CSR/CRR approval workflow plugin, it must meet the requirements of the Identity Manager Certificate Signing Request (CSR)/Certificate Revocation Request (CRR) approval workflow.

## Configure projects and users

1. Create two `Process Management` projects: one for CSRs and one for CRRs. The final settings for both projects should look like this:

![jira 6](/en/images/jira-6.png "jira 6")

2. Create a user with permission to:
    * Create tickets
    * Change ticket statuses


3. Assign the user to the CSR and CRR projects.

4. Supply the user credentials to the [CENM identity manager configuration](identity-manager.html#jira-workflow).

## Configure projects' workflow

Configure the following workflow for both projects (CSR and CRR):

![jira 1](/en/images/jira-1.png "jira 1")
When the HSM signs a request, the tickets move from the `Approved` status to `Done` automatically.


## Custom fields

You also need to create three custom fields:

* Request ID
* Reject Reason
* Reject Reason Description


{{< note >}}
These fields are global and applicable to both CSR and CRR projects. Screen selection (see snippets below) allows
for field assignment to a specific project.

{{< /note >}}
The following snippets depict the configuration for those fields:

![jira 4](/en/images/jira-4.png "jira 4")
![jira 3](/en/images/jira-3.png "jira 3")
![jira 2](/en/images/jira-2.png "jira 2")
![jira 5](/en/images/jira-5.png "jira 5")
