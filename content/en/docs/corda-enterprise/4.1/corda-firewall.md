---
aliases:
- /releases/4.1/corda-firewall.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-corda-firewall
    parent: corda-enterprise-4-1-corda-enterprise
    weight: 130
tags:
- corda
- firewall
title: Corda Firewall
---


# Corda Firewall

Corda Enterprise ships a component called the *Corda Firewall*. The firewall is actually made up of two separate modules,
called the *bridge* and the *float*. These handle outbound and inbound connections respectively, and allow a node
administrator to minimise the amount of code running in a network's DMZ. The firewall provides some basic protection
features in this release: future releases may add enhanced monitoring and audit capabilities.

* [Firewall Component Overview](corda-firewall-component.md)
* [Firewall Configuration](corda-firewall-configuration-file.md)
* [Firewall upgrade](corda-firewall-upgrade.md)







