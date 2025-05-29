---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-11:
    parent: corda-enterprise-4-11-corda-networks
tags:
- network
title: Corda network considerations
weight: 20
---


# Corda network considerations


## Corda network parameters

There is a set of network parameters that all nodes on the network must agree on in order to interoperate. For more information, see [Network parameters]({{< relref "network-parameters.md" >}}).

### Flag days

Network parameters are distributed alongside the network map in a separate file stored locally by each node.

From time to time the Corda Network Operator (R3) will need to update parameters, for example if a new notary is added.

The current update process is a 3 step operation.

* Day 1 Publicise the intended changes
* Day 1-N Collect node acceptances
* Day N* Update the central file and distribute

Most network parameter changes require that a node is stopped and restarted before the changes are accepted. The exception to this is when the network parameter changes _only_ update **notaries**. Updates that have only changes to **notaries** can be accepted without a restart.

### Flag day communications

The Corda Network Operator will ensure customers are fully aware of impending and in-flight network parameter changes:


* Forward Calendars


* Publicise 12 month forward calendar and explanatory notes for next update:
* Production calendar on [https://corda.network](https://corda.network)
* UAT calendar on [https://docs.r3.com](https://docs.r3.com)


* Event Communications


* Announcement day explanatory email to:


* Customer node operators (contact email address as supplied in original Certificate Signing Request or as amended by email to [doorman@r3.com](mailto:doorman@r3.com) or [uatdoorman@r3.com](mailto:uatdoorman@r3.com).
* Customer business operations contacts (advised during implementation projects)
* Business network operator key contact (as defined in service agreement).


* Pre-execution email to the same contacts 3 business days ahead of update to confirm go ahead.
* Publicise on Support Service Desk and cascade to customer support contacts.

Segregated Zones

Detail on the thinking and concepts around what a segregated subzone is can be found here : [https://groups.io/g/corda-network/topic/design_proposal_for/28792765?p=,,,20,0,0,0::recentpostdate%2Fsticky,,,20,2,0,28792765](https://groups.io/g/corda-network/topic/design_proposal_for/28792765?p=,,,20,0,0,0::recentpostdate%2Fsticky,,,20,2,0,28792765)

Here are the basis goals of a segregated subzone:


* The ability to hive off members of the business network into a private enclave
* The ability to cloak the members of the business network
* That is where the notary is not whitelisted globally and is operated to the standard deemed acceptable by the BNO, not the Zone operator and members (as per those in the global whitelist)
* The ability to operate “private” notary service> 
That is where the notary can exist in the global whitelist but is restricted to notarisation of specific State types
The ability to operate non whitelisted, “less universally trusted”, notaries.
The ability to operate their own Compatibility Zone.

* Segregated subzones only share the Identity Operator service. Each subzone therefore has its own independent network map and set of network parameters
* Subzones allow more flexibility in setting network parameters as each zone is able to have its own settings
* Subzones will be able to opt out of specific events* where:


* The parameters are not used in their business network(s) e.g. for contract constraints or private notaries
* Opting-out does not compromise the subzone’s long term plan to join the public zone


* It should be noted however, the more subzones diverge in parameter settings over time the harder it will be to merge back in to the public zone in future
* Segregated subzones capability is estimated to be available in Corda Network Q3 2018
* Production will follow after successful customer test in UAT

The diagram below outlines the overview of SSZ.



### Constraints


* Subzones must be mergeable
* No nodes (including notaries) can exist in more than one subzone
* There must be no asymmetry of identification
* The identity service for subzones must be managed by a single Doorman
* Should require no changes to the Corda node
* Notaries will not exist in multiple subzones

