---
title: "Privacy"
date: 2023-06-07
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-fundamentals-privacy
    parent: corda5-fundamentals
    weight: 3000
section_menu: corda5
---

# Privacy

## Communication

Through its attested identity model, Corda allows for direct [peer-to-peer messaging]({{< relref "../application-networks/_index.md/#peer-to-peer-communication" >}}) between identities. 
A proposal to mutate the global state can be undertaken without the knowledge of those not a party to that mutation; there is no need to globally broadcast updates and thus avoid leaking sensitive information.
At any single point in time, an identity can be involved in any number of distinct transactions.

{{< 
  figure
	 src="private-communication.png"
   width="50%"
	 figcaption="Private Communication"
>}}

## Global State

In Corda, as in all DLT systems, there exists a global state. 
However, in Corda, that global state is not globally visible. 
Each participant's identity only has visibility over those portions of the global data that are relevant to it.

{{< 
  figure
	 src="global-state.png"
   width="50%"
	 figcaption="Global State"
>}}

There is no single storage point or distribution of data globally. 
Each identity locally stores the slices of the global state it needs to, either because:
* it is a direct participant in a mutation of the global state.
* it was added as an interested party by a participant.

{{< 
  figure
	 src="global-state-facts.png"
   width="50%"
	 figcaption="Historic and Current Facts in the Global State"
>}}

Therefore, multiple copies of data are distributed and replicated where needed.

{{< 
  figure
	 src="multiple-copies-data.png"
   width="50%"
	 figcaption="Distributed and Replicated Copies of Data"
>}}

## Trust

Ultimately, the fundamental promise of Corda and all DLTs is that, once committed to the global state and accepted as valid, there can be no disagreement that an event has occurred.

{{< 
  figure
	 src="trust.png"
   width="50%"
	 figcaption="You See What I See"
>}}

Reconciliation is not needed as there is a single accepted version of valid that has been attested by all parties and that those with visibility trust.