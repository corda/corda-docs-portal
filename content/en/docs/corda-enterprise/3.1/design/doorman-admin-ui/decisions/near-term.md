---
aliases:
- /releases/3.1/design/doorman-admin-ui/decisions/near-term.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- near
- term
title: 'Design Decision: Near-term solution for Doorman Administration UI'
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}

[![fg005 corda b](https://www.corda.net/wp-content/uploads/2016/11/fg005_corda_b.png "fg005 corda b")](https://www.corda.net/wp-content/uploads/2016/11/fg005_corda_b.png)


# Design Decision: Near-term solution for Doorman Administration UI


## Background / Context

A decision is required specifically on the doorman UI to be used for the near-term Pilot network, to be launched on Feb 1, 2018. See [main design doc](../design.md) for more context.


## Options Analysis


### A. Existing R3 Atlassian-Hosted JIRA


#### Advantages


* Incumbent option - no change required


#### Disadvantages


* Risk to R3 corporate operations exposed by JIRA integration of Doorman
* Potential security challenges (See [main design doc](../design.md))


### B. Separate Atlassian-Hosted JIRA


#### Advantages


* Minimal infrastructure deployment requirement - just buy a new account
* HA and DR provided by Atlassian (in principle - no easily enforceable SLAs etc.)


#### Disadvantages


* Scalability and performance under large loads unclear
* Flexibility to support long term requirements unclear - may be just a ‘stop-gap’


### C. Private JIRA installation


#### Advantages


* Low/no development effort to change
* A single installation with no HA etc. may be relatively cheap - [$10 for 10 users](https://www.atlassian.com/software/jira/pricing?tab=self-hosted)
* Self-ownership of HA/DR issues may provide greater certainty
* Easier to secure (can put behind a firewall with extra authentication etc.)


#### Disadvantages


* Scalability and performance under large loads unclear - may end up spending c. ?12k for a data centre license.
* Flexibility to support long term requirements unclear - may be just a ‘stop-gap’


### D. Bespoke application

Code a bespoke client UI (e.g. in AngularJS) that administers the doorman via direct calls to the API.


#### Advantages


* Starting point for eventual strategic solution that meets precise onboarding process requirements
* No flexibility issues
* No performance issues (driven off doorman database)
* Easier to secure (can put behind a firewall with extra authentication etc.)


#### Disadvantages


* Extra development effort
* Higher potential for bugs and security vulnerabilities
* Replication of workflow logic that already exists
* Harder for business-side employees to change workflow or logic vs. JIRA


## Recommendation and justification

Proceed with Option C - Private JIRA installation

