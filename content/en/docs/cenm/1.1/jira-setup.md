---
title: "JIRA Set-Up"
date: 2020-01-08T09:59:25Z
---


# JIRA Set-Up
The following are the instructions on setting up the JIRA in order to satisfy minimal requirements from the point of view
            of the Identity Manager Certificate Signing Request (CSR)/Certificate Revocation Request (CRR) approval workflow. This will enable
            a user to integrate such JIRA deployment with the CENM CSR/CRR approval workflow plugin.


## User Set-Up
Create a user with an administrative permissions and make sure it is assigned to the default groups:
                `jira-administrators` and `jira-software-users`. The following shows an example for a `Test` user setup.

{{< img src="resources/jira-7.png" alt="jira 7" >}}


## Project Set-Up
Create two projects (one for Certificate Signing Requests and one for Certificate Revocation Requests) of the type of
                `Process Management`. The following shows final settings for both projects.

{{< img src="resources/jira-6.png" alt="jira 6" >}}


## Project Workflow
Make sure that both projects (CSR and CRR) have the following workflow configured.

{{< img src="resources/jira-1.png" alt="jira 1" >}}


## Custom fields
Additionally, the following 3 custom fields need to be created and configured in JIRA.

> 
> 
> * Request ID
> 
> 
> * Reject Reason
> 
> 
> * Reject Reason Description
> 
> 

{{< note >}}
These fields are global and applicable to both CSR and CRR projects. Screen selection (see snippets below) alows
                    for field assignment to a specific project.


{{< /note >}}
The following snippets depict the configuration for those fields:

{{< img src="resources/jira-4.png" alt="jira 4" >}}

{{< img src="resources/jira-3.png" alt="jira 3" >}}

{{< img src="resources/jira-2.png" alt="jira 2" >}}

{{< img src="resources/jira-5.png" alt="jira 5" >}}


