---
aliases:
- /setting-up-notary.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- setting
- notary
title: Setting Up A Notary Node
---


# Setting Up A Notary Node


## Purpose

A notary node is a well known and trusted node that provides uniqueness consensus. Because of this, creating and running a notary node is
slightly more involved compared with a regular node.

The Network Map Service broadcasts information (stored in the network parameters file) that every participant in the network needs to
agree on. One piece of information is the list of notaries. Because all notaries within this list need to be well known and trusted,
the process of adding a new one requires some manual intervention on the Network Map Service side.


## Configuration

The exact configuration will depend on the Corda version that the notary node is running.


### Example Configuration

```guess
myLegalName="O=Example Notary,L=London,C=GB"
notary {
    validating=false
}

networkServices {
  doormanURL="http://<IDENTITY_MANAGER_HOST>:<IDENTITY_MANAGER_PORT>"
  networkMapURL="http://NETWORK_MAP_SERVICE_HOST>:<NETWORK_MAP_SERVICE_PORT>"
}

devMode = false

sshd {
  port = <SSH_PORT>
}

p2pAddress="<NOTARY_HOST>:<NOTARY_PORT>"
```


## Initial Setup

The steps to integrate the notary node into the network are:


* Register the node with the Identity Manager
* Generate the node info file
* Copy the node info file to the Network Map Service
* Update the network parameters file on the Network Map Service to reference the new node info file
* Start (or restart) the Network Map Service
* Start the notary node as normal


### Create Notary Node And Register With The Identity Manager

Ensuring that the Identity Manager Service is successfully running, start the notary node for registration.

```bash
java -jar corda.jar --config-file <NODE_CONF_FILE> --initial-registration --network-root-truststore-password <TRUST_STORE_PASSWORD> --network-root-truststore <PATH_TO_TRUST_STORE>
```

{{< note >}}
The network trust store should contain the trusted root certificate of the network. This should be created
during the initial setup of the network and therefore should be distribute by the network operator.

{{< /note >}}

### Generate Node Info File

The node info file contains information such as address and certificates. The file will be used by all participants on the network to enable them to
connect to, and trust, the new notary node.

```bash
java -jar corda.jar --config-file <NODE_CONF_FILE> --just-generate-node-info
```


### Setup Network Map Service

Follow instructions here [Network Map Service](network-map.md)


### Run The Notary

```bash
java -jar corda.jar --config-file <NODE_CONF_FILE>
```
