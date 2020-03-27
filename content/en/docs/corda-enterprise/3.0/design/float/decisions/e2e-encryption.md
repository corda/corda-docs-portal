---
aliases:
- /releases/3.0/design/float/decisions/e2e-encryption.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- e2e
- encryption
title: 'Design Decision: End-to-end encryption'
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Design Decision: End-to-end encryption


## Background / Context

End-to-end encryption is a desirable potential design feature for the [float](../design.md).


## Options Analysis


### 1. No end-to-end encryption


#### Advantages


* Least effort
* Easier to fault find and manage


#### Disadvantages


* With no placeholder, it is very hard to add support later and maintain wire stability.
* May not get past security reviews of Float.


### 2. Placeholder only


#### Advantages


* Allows wire stability when we have agreed an encrypted approach
* Shows that we are serious about security, even if this isn’t available yet.
* Allows later encrypted version to be an enterprise feature that can interoperate with OS versions.


#### Disadvantages


* Doesn’t actually provide E2E, or define what an encrypted payload looks like.
* Doesn’t address any crypto features that target protecting the AMQP headers.


### 3. Implement end-to-end encryption


* Will protect the sensitive data fully.


#### Disadvantages


* Lots of work.
* Difficult to get right.
* Re-inventing TLS.


## Recommendation and justification

Proceed with Option 2: Placeholder


## Decision taken

Proceed with Option 2 - Add placeholder, subject to more detailed design proposal (RGB, JC, MH agreed)



* [Design Review Board Meeting Minutes](drb-meeting-20171116.md)
    * [Attendees](drb-meeting-20171116.md#attendees)
    * [Minutes](drb-meeting-20171116.md#minutes)
        * [TLS termination](drb-meeting-20171116.md#id1)
        * [E2E encryption](drb-meeting-20171116.md#id2)
        * [AMQP vs. custom protocol](drb-meeting-20171116.md#id3)
        * [Pluggable broker prioritisation](drb-meeting-20171116.md#id4)
        * [Inbound only vs. inbound & outbound connections](drb-meeting-20171116.md#inbound-only-vs-inbound-outbound-connections)
        * [Overall design and implementation plan](drb-meeting-20171116.md#overall-design-and-implementation-plan)







