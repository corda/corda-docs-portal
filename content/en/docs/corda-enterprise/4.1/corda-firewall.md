---
title: "Corda Firewall"
date: 2020-01-08T09:59:25Z
---


# Corda Firewall
Corda Enterprise ships a component called the *Corda Firewall*. The firewall is actually made up of two separate modules,
            called the *bridge* and the *float*. These handle outbound and inbound connections respectively, and allow a node
            administrator to minimise the amount of code running in a network’s DMZ. The firewall provides some basic protection
            features in this release: future releases may add enhanced monitoring and audit capabilities.


* [Firewall Component Overview]({{< relref "corda-firewall-component" >}})
    * [Introduction]({{< relref "corda-firewall-component#introduction" >}})

    * [Terminology]({{< relref "corda-firewall-component#terminology" >}})

    * [Message path between peer nodes]({{< relref "corda-firewall-component#message-path-between-peer-nodes" >}})

    * [Operating modes of the Bridge and Float with a single node]({{< relref "corda-firewall-component#operating-modes-of-the-bridge-and-float-with-a-single-node" >}})
        * [Embedded Developer Node (node + artemis + internal bridge, no float, no DMZ)]({{< relref "corda-firewall-component#embedded-developer-node-node-artemis-internal-bridge-no-float-no-dmz" >}})
            * [Prerequisites]({{< relref "corda-firewall-component#prerequisites" >}})


        * [Node + Combined Bridge/Float (no DMZ)]({{< relref "corda-firewall-component#node-combined-bridge-float-no-dmz" >}})
            * [Prerequisites]({{< relref "corda-firewall-component#id1" >}})

            * [node.conf]({{< relref "corda-firewall-component#node-conf" >}})

            * [bridge.conf]({{< relref "corda-firewall-component#bridge-conf" >}})


        * [DMZ ready (node + bridge + float)]({{< relref "corda-firewall-component#dmz-ready-node-bridge-float" >}})
            * [Prerequisites]({{< relref "corda-firewall-component#id2" >}})

            * [node.conf]({{< relref "corda-firewall-component#id3" >}})

            * [bridge.conf]({{< relref "corda-firewall-component#id4" >}})

            * [float.conf]({{< relref "corda-firewall-component#float-conf" >}})


        * [DMZ ready with outbound SOCKS]({{< relref "corda-firewall-component#dmz-ready-with-outbound-socks" >}})
            * [Prerequisites]({{< relref "corda-firewall-component#id5" >}})

            * [node.conf]({{< relref "corda-firewall-component#id6" >}})

            * [bridge.conf]({{< relref "corda-firewall-component#id7" >}})

            * [float.conf]({{< relref "corda-firewall-component#id8" >}})


        * [Full production HA DMZ ready mode (hot/cold node, hot/warm bridge)]({{< relref "corda-firewall-component#full-production-ha-dmz-ready-mode-hot-cold-node-hot-warm-bridge" >}})
            * [Prerequisites]({{< relref "corda-firewall-component#id9" >}})

            * [node.conf]({{< relref "corda-firewall-component#id10" >}})

            * [bridge.conf]({{< relref "corda-firewall-component#id11" >}})

            * [float.conf]({{< relref "corda-firewall-component#id12" >}})



    * [Operating modes of shared Bridge and Float]({{< relref "corda-firewall-component#operating-modes-of-shared-bridge-and-float" >}})
        * [Multiple nodes + Bridge (no float, no DMZ)]({{< relref "corda-firewall-component#multiple-nodes-bridge-no-float-no-dmz" >}})
            * [Prerequisites]({{< relref "corda-firewall-component#id13" >}})

            * [bank-a-node.conf]({{< relref "corda-firewall-component#bank-a-node-conf" >}})

            * [bank-b-node.conf]({{< relref "corda-firewall-component#bank-b-node-conf" >}})

            * [bridge.conf]({{< relref "corda-firewall-component#id14" >}})


        * [Adding new nodes to existing shared Bridge]({{< relref "corda-firewall-component#adding-new-nodes-to-existing-shared-bridge" >}})


    * [Standalone Artemis server]({{< relref "corda-firewall-component#standalone-artemis-server" >}})

    * [Apache ZooKeeper]({{< relref "corda-firewall-component#apache-zookeeper" >}})
        * [Setting up ZooKeeper cluster]({{< relref "corda-firewall-component#setting-up-zookeeper-cluster" >}})

        * [Sharing ZooKeeper]({{< relref "corda-firewall-component#sharing-zookeeper" >}})


    * [ZooKeeper alternative]({{< relref "corda-firewall-component#zookeeper-alternative" >}})


* [Firewall Configuration]({{< relref "corda-firewall-configuration-file" >}})
    * [File location]({{< relref "corda-firewall-configuration-file#file-location" >}})

    * [Format]({{< relref "corda-firewall-configuration-file#format" >}})

    * [Defaults]({{< relref "corda-firewall-configuration-file#defaults" >}})

    * [Firewall operating modes]({{< relref "corda-firewall-configuration-file#firewall-operating-modes" >}})

    * [Fields]({{< relref "corda-firewall-configuration-file#fields" >}})

    * [Complete example]({{< relref "corda-firewall-configuration-file#complete-example" >}})
        * [Keystores generation]({{< relref "corda-firewall-configuration-file#keystores-generation" >}})
            * [Tunnel keystore generation]({{< relref "corda-firewall-configuration-file#tunnel-keystore-generation" >}})

            * [Artemis keystore generation]({{< relref "corda-firewall-configuration-file#artemis-keystore-generation" >}})


        * [Node VMs setup]({{< relref "corda-firewall-configuration-file#node-vms-setup" >}})
            * [Prerequisites]({{< relref "corda-firewall-configuration-file#prerequisites" >}})
                * [Corda Network connectivity]({{< relref "corda-firewall-configuration-file#corda-network-connectivity" >}})

                * [Nodes inbound connectivity provisions]({{< relref "corda-firewall-configuration-file#nodes-inbound-connectivity-provisions" >}})

                * [Databases setup]({{< relref "corda-firewall-configuration-file#databases-setup" >}})

                * [Base directory setup]({{< relref "corda-firewall-configuration-file#base-directory-setup" >}})


            * [Creating node configuration files]({{< relref "corda-firewall-configuration-file#creating-node-configuration-files" >}})

            * [Nodes keystores generation]({{< relref "corda-firewall-configuration-file#nodes-keystores-generation" >}})

            * [CorDapps installation]({{< relref "corda-firewall-configuration-file#cordapps-installation" >}})

            * [DB drivers installation]({{< relref "corda-firewall-configuration-file#db-drivers-installation" >}})

            * [Keystore aggregation for the Bridge]({{< relref "corda-firewall-configuration-file#keystore-aggregation-for-the-bridge" >}})

            * [`vmNodeSecondary` setup]({{< relref "corda-firewall-configuration-file#vmnodesecondary-setup" >}})


        * [Float VMs setup]({{< relref "corda-firewall-configuration-file#float-vms-setup" >}})

        * [Infra VMs setup]({{< relref "corda-firewall-configuration-file#infra-vms-setup" >}})
            * [Apache ZooKeeper setup]({{< relref "corda-firewall-configuration-file#apache-zookeeper-setup" >}})

            * [Bridge instances setup]({{< relref "corda-firewall-configuration-file#bridge-instances-setup" >}})

            * [Artemis cluster participant]({{< relref "corda-firewall-configuration-file#artemis-cluster-participant" >}})

            * [`vmInfra2` setup]({{< relref "corda-firewall-configuration-file#vminfra2-setup" >}})
                * [`vmInfra2` Artemis cluster participant setup]({{< relref "corda-firewall-configuration-file#vminfra2-artemis-cluster-participant-setup" >}})

                * [`vmInfra2` Bridge instance setup]({{< relref "corda-firewall-configuration-file#vminfra2-bridge-instance-setup" >}})



        * [Starting all up]({{< relref "corda-firewall-configuration-file#starting-all-up" >}})
            * [Starting Float processes]({{< relref "corda-firewall-configuration-file#starting-float-processes" >}})

            * [Starting Apache ZooKeeper processes]({{< relref "corda-firewall-configuration-file#starting-apache-zookeeper-processes" >}})

            * [Starting Artemis cluster]({{< relref "corda-firewall-configuration-file#starting-artemis-cluster" >}})

            * [Starting Bridge processes]({{< relref "corda-firewall-configuration-file#starting-bridge-processes" >}})

            * [Domino effect]({{< relref "corda-firewall-configuration-file#domino-effect" >}})

            * [Starting node processes]({{< relref "corda-firewall-configuration-file#starting-node-processes" >}})


        * [Performing basic health checks]({{< relref "corda-firewall-configuration-file#performing-basic-health-checks" >}})
            * [Checking Float port is open]({{< relref "corda-firewall-configuration-file#checking-float-port-is-open" >}})

            * [Checking Float is reachable from the outside]({{< relref "corda-firewall-configuration-file#checking-float-is-reachable-from-the-outside" >}})

            * [Running some flows]({{< relref "corda-firewall-configuration-file#running-some-flows" >}})




* [Firewall upgrade]({{< relref "corda-firewall-upgrade" >}})
    * [Introduction]({{< relref "corda-firewall-upgrade#introduction" >}})

    * [Upgrade]({{< relref "corda-firewall-upgrade#upgrade" >}})
        * [Node + Bridge (no float, no DMZ)]({{< relref "corda-firewall-upgrade#node-bridge-no-float-no-dmz" >}})

        * [DMZ ready (node + bridge + float)]({{< relref "corda-firewall-upgrade#dmz-ready-node-bridge-float" >}})

        * [DMZ ready with outbound SOCKS]({{< relref "corda-firewall-upgrade#dmz-ready-with-outbound-socks" >}})

        * [Full production HA DMZ ready (hot/cold node, hot/warm bridge)]({{< relref "corda-firewall-upgrade#full-production-ha-dmz-ready-hot-cold-node-hot-warm-bridge" >}})


    * [Reconfiguring to the shared Corda Firewall Architecture]({{< relref "corda-firewall-upgrade#reconfiguring-to-the-shared-corda-firewall-architecture" >}})
        * [Node + Bridge to Node + Artemis + Bridge]({{< relref "corda-firewall-upgrade#node-bridge-to-node-artemis-bridge" >}})

        * [Multiple nodes behind the Bridge]({{< relref "corda-firewall-upgrade#multiple-nodes-behind-the-bridge" >}})





