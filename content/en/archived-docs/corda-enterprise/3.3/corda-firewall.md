---
aliases:
- /releases/3.3/corda-firewall.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-3:
    identifier: corda-enterprise-3-3-corda-firewall
    parent: corda-enterprise-3-3-corda-enterprise
    weight: 70
tags:
- corda
- firewall
title: Corda Firewall
---


# Corda Firewall

Corda Enterprise ships a component called the *Corda Firewall*. The firewall is actually made up of two separate programs,
called the *bridge* and the *float*. These handle outbound and inbound connections respectively, and allow a node
administrator to minimise the amount of code running in a network’s DMZ. The firewall provides some basic protection
features in this release: future releases may add enhanced monitoring and audit capabilities.



* [Bridge component overview](corda-bridge-component.md)
    * [Introduction](corda-bridge-component.md#introduction)
    * [Terminology](corda-bridge-component.md#terminology)
    * [Message path between peer nodes](corda-bridge-component.md#message-path-between-peer-nodes)
    * [Operating modes of the Bridge and Float](corda-bridge-component.md#operating-modes-of-the-bridge-and-float)
        * [Embedded Developer Node (node + artemis + internal bridge, no float, no DMZ)](corda-bridge-component.md#embedded-developer-node-node-artemis-internal-bridge-no-float-no-dmz)
        * [Node + Bridge (no float, no DMZ)](corda-bridge-component.md#node-bridge-no-float-no-dmz)
        * [DMZ ready (node + bridge + float)](corda-bridge-component.md#dmz-ready-node-bridge-float)
        * [DMZ ready with outbound SOCKS](corda-bridge-component.md#dmz-ready-with-outbound-socks)
        * [Full production HA DMZ ready mode (hot/cold node, hot/warm bridge)](corda-bridge-component.md#full-production-ha-dmz-ready-mode-hot-cold-node-hot-warm-bridge)




* [Bridge configuration](bridge-configuration-file.md)
    * [File location](bridge-configuration-file.md#file-location)
    * [Format](bridge-configuration-file.md#format)
    * [Defaults](bridge-configuration-file.md#defaults)
    * [Bridge operating modes](bridge-configuration-file.md#bridge-operating-modes)
    * [Fields](bridge-configuration-file.md#fields)
    * [Complete example](bridge-configuration-file.md#complete-example)





