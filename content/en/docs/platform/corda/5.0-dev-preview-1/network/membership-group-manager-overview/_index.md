---
date: '2021-08-11'
menu:
  versions: Corda 5
    weight: 200
project: corda-5
section_menu: corda-5-dev-preview
title: Membership Group Manager
version: 'dev-preview'
---

# Networks

Corda Membership Groups allow Corda deployments to discover and interact with each other.

## Glossary

**Corda Identity**

An identity claim in a Membership Group with a unique X-500 name.


**Membership Group**

A logical grouping of a number of Corda Identities to communicate and transact with each other using a specific set of CorDapps.


**Group Member**

A Corda Identity that has been granted admission into to a Membership Group.


**Group Notary**

A Corda Identity deployed to Corda in Notary mode and granted admission into a Membership Group.

*Member* - Someone wishing to communicate\* with a selected group of peers.
- *Membership Group* (or *Group*) - Set of members able to communicate with each other.
- *MGM* (*Membership Group Manager*) - Member responsible for maintaining membership group.
- *MemberInfo* - C5 structure representing individual member. Equivalent of C4 *NodeInfo*.
- *MembershipGroupCache* - C5 service storing information about group members. Equivalent of C4 *NetworkMapCache*.
- *CPK* (*CordApp Package*) - CorDapps bundle, which includes dependency tree and version information.
- *CPI* (*Cordapp Packaged Installation file*) - Single distributable file, which contains CPKs and group information.


##
