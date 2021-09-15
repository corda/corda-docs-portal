---
aliases:
- /releases/4.3/corda-firewall.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-corda-firewall
    parent: corda-enterprise-4-3-corda-enterprise
    weight: 120
tags:
- corda
- firewall
title: Corda Firewall
---


# Corda Firewall

Corda Enterprise ships a component called the *Corda Firewall*. The firewall is actually made up of two separate modules,
called the *bridge* and the *float*. These handle outbound and inbound connections respectively, and allow a node
administrator to minimise the amount of code running in a network’s DMZ. The firewall provides some basic protection
features in this release: future releases may add enhanced monitoring and audit capabilities.



* [Firewall Component Overview](corda-firewall-component.md)
    * [Introduction](corda-firewall-component.md#introduction)
    * [Terminology](corda-firewall-component.md#terminology)
    * [Message path between peer nodes](corda-firewall-component.md#message-path-between-peer-nodes)
    * [Operating modes of the Bridge and Float with a single node](corda-firewall-component.md#operating-modes-of-the-bridge-and-float-with-a-single-node)
        * [Embedded Developer Node (node + artemis + internal bridge, no float, no DMZ)](corda-firewall-component.md#embedded-developer-node-node-artemis-internal-bridge-no-float-no-dmz)
            * [Prerequisites](corda-firewall-component.md#prerequisites)


        * [Node + Combined Bridge/Float (no DMZ)](corda-firewall-component.md#node-combined-bridge-float-no-dmz)
            * [Prerequisites](corda-firewall-component.md#id1)
            * [node.conf](corda-firewall-component.md#node-conf)
            * [bridge.conf](corda-firewall-component.md#bridge-conf)


        * [DMZ ready (node + bridge + float)](corda-firewall-component.md#dmz-ready-node-bridge-float)
            * [Prerequisites](corda-firewall-component.md#id2)
            * [node.conf](corda-firewall-component.md#id3)
            * [bridge.conf](corda-firewall-component.md#id4)
            * [float.conf](corda-firewall-component.md#float-conf)


        * [DMZ ready with outbound SOCKS](corda-firewall-component.md#dmz-ready-with-outbound-socks)
            * [Prerequisites](corda-firewall-component.md#id5)
            * [node.conf](corda-firewall-component.md#id6)
            * [bridge.conf](corda-firewall-component.md#id7)
            * [float.conf](corda-firewall-component.md#id8)


        * [Full production HA DMZ ready mode (hot/cold node, hot/warm bridge)](corda-firewall-component.md#full-production-ha-dmz-ready-mode-hot-cold-node-hot-warm-bridge)
            * [Prerequisites](corda-firewall-component.md#id9)
            * [node.conf](corda-firewall-component.md#id10)
            * [bridge.conf](corda-firewall-component.md#id11)
            * [float.conf](corda-firewall-component.md#id12)
            * [Notes on physical deployment of services](corda-firewall-component.md#notes-on-physical-deployment-of-services)




    * [Operating modes of shared Bridge and Float](corda-firewall-component.md#operating-modes-of-shared-bridge-and-float)
        * [Multiple nodes + Bridge (no float, no DMZ)](corda-firewall-component.md#multiple-nodes-bridge-no-float-no-dmz)
            * [Prerequisites](corda-firewall-component.md#id13)
            * [bank-a-node.conf](corda-firewall-component.md#bank-a-node-conf)
            * [bank-b-node.conf](corda-firewall-component.md#bank-b-node-conf)
            * [bridge.conf](corda-firewall-component.md#id14)


        * [Adding new nodes to existing shared Bridge](corda-firewall-component.md#adding-new-nodes-to-existing-shared-bridge)


    * [Standalone Artemis server](corda-firewall-component.md#standalone-artemis-server)
    * [Apache ZooKeeper](corda-firewall-component.md#apache-zookeeper)
        * [Setting up ZooKeeper cluster](corda-firewall-component.md#setting-up-zookeeper-cluster)
        * [Sharing ZooKeeper](corda-firewall-component.md#sharing-zookeeper)


    * [ZooKeeper alternative](corda-firewall-component.md#zookeeper-alternative)
    * [Use of HSM in Corda Firewall](corda-firewall-component.md#use-of-hsm-in-corda-firewall)
    * [Memory requirements for Corda Firewall](corda-firewall-component.md#memory-requirements-for-corda-firewall)


* [Firewall Configuration](corda-firewall-configuration-file.md)
    * [File location](corda-firewall-configuration-file.md#file-location)
    * [Format](corda-firewall-configuration-file.md#format)
    * [Defaults](corda-firewall-configuration-file.md#defaults)
    * [Firewall operating modes](corda-firewall-configuration-file.md#firewall-operating-modes)
    * [Fields](corda-firewall-configuration-file.md#fields)
    * [Complete example](corda-firewall-configuration-file.md#complete-example)
        * [Keystores generation](corda-firewall-configuration-file.md#keystores-generation)
            * [Tunnel keystore generation](corda-firewall-configuration-file.md#tunnel-keystore-generation)
            * [Artemis keystore generation](corda-firewall-configuration-file.md#artemis-keystore-generation)


        * [Node VMs setup](corda-firewall-configuration-file.md#node-vms-setup)
            * [Prerequisites](corda-firewall-configuration-file.md#prerequisites)
                * [Corda Network connectivity](corda-firewall-configuration-file.md#corda-network-connectivity)
                * [Nodes inbound connectivity provisions](corda-firewall-configuration-file.md#nodes-inbound-connectivity-provisions)
                * [Databases setup](corda-firewall-configuration-file.md#databases-setup)
                * [Base directory setup](corda-firewall-configuration-file.md#base-directory-setup)


            * [Creating node configuration files](corda-firewall-configuration-file.md#creating-node-configuration-files)
            * [Nodes keystores generation](corda-firewall-configuration-file.md#nodes-keystores-generation)
            * [CorDapps installation](corda-firewall-configuration-file.md#cordapps-installation)
            * [DB drivers installation](corda-firewall-configuration-file.md#db-drivers-installation)
            * [Keystore aggregation for the Bridge](corda-firewall-configuration-file.md#keystore-aggregation-for-the-bridge)
            * [`vmNodeSecondary` setup](corda-firewall-configuration-file.md#vmnodesecondary-setup)


        * [Float VMs setup](corda-firewall-configuration-file.md#float-vms-setup)
        * [Infra VMs setup](corda-firewall-configuration-file.md#infra-vms-setup)
            * [Apache ZooKeeper setup](corda-firewall-configuration-file.md#apache-zookeeper-setup)
            * [Bridge instances setup](corda-firewall-configuration-file.md#bridge-instances-setup)
            * [Artemis cluster participant](corda-firewall-configuration-file.md#artemis-cluster-participant)
            * [`vmInfra2` setup](corda-firewall-configuration-file.md#vminfra2-setup)
                * [`vmInfra2` Artemis cluster participant setup](corda-firewall-configuration-file.md#vminfra2-artemis-cluster-participant-setup)
                * [`vmInfra2` Bridge instance setup](corda-firewall-configuration-file.md#vminfra2-bridge-instance-setup)




        * [Starting all up](corda-firewall-configuration-file.md#starting-all-up)
            * [Starting Float processes](corda-firewall-configuration-file.md#starting-float-processes)
            * [Starting Apache ZooKeeper processes](corda-firewall-configuration-file.md#starting-apache-zookeeper-processes)
            * [Starting Artemis cluster](corda-firewall-configuration-file.md#starting-artemis-cluster)
            * [Starting Bridge processes](corda-firewall-configuration-file.md#starting-bridge-processes)
            * [Domino effect](corda-firewall-configuration-file.md#domino-effect)
            * [Starting node processes](corda-firewall-configuration-file.md#starting-node-processes)


        * [Performing basic health checks](corda-firewall-configuration-file.md#performing-basic-health-checks)
            * [Checking Float port is open](corda-firewall-configuration-file.md#checking-float-port-is-open)
            * [Checking Float is reachable from the outside](corda-firewall-configuration-file.md#checking-float-is-reachable-from-the-outside)
            * [Running some flows](corda-firewall-configuration-file.md#running-some-flows)






* [Firewall upgrade](corda-firewall-upgrade.md)
    * [Introduction](corda-firewall-upgrade.md#introduction)
    * [Upgrade](corda-firewall-upgrade.md#upgrade)
        * [Node + Bridge (no float, no DMZ)](corda-firewall-upgrade.md#node-bridge-no-float-no-dmz)
        * [DMZ ready (node + bridge + float)](corda-firewall-upgrade.md#dmz-ready-node-bridge-float)
        * [DMZ ready with outbound SOCKS](corda-firewall-upgrade.md#dmz-ready-with-outbound-socks)
        * [Full production HA DMZ ready (hot/cold node, hot/warm bridge)](corda-firewall-upgrade.md#full-production-ha-dmz-ready-hot-cold-node-hot-warm-bridge)


    * [Reconfiguring to the shared Corda Firewall Architecture](corda-firewall-upgrade.md#reconfiguring-to-the-shared-corda-firewall-architecture)
        * [Node + Bridge to Node + Artemis + Bridge](corda-firewall-upgrade.md#node-bridge-to-node-artemis-bridge)
        * [Multiple nodes behind the Bridge](corda-firewall-upgrade.md#multiple-nodes-behind-the-bridge)
