---
aliases:
- /setting-up-notary.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-7:
    identifier: cenm-1-7-setting-up-notary
    parent: cenm-1-7-tools-index
    weight: 1010
tags:
- setting
- notary
title: Setting up a notary node
---


# Setting up a notary node

A *notary node* is a well-known and trusted node that provides uniqueness consensus. Because of this, creating and running a notary node is
slightly more involved compared with a regular node.

The Network Map Service broadcasts information (stored in the network parameters file) that every participant in the network needs to
agree on. One piece of information is the list of notaries. Because all notaries within this list need to be well known and trusted,
the process of adding a new one requires some manual intervention on the Network Map Service side.


The steps to integrate the notary node into the network are:

1. [Create the notary node configuration](#create-the-notary-node-configuration).
2. [Register the node with the Identity Manager](#register-the-node-with-the-identity-manager).
3. [Generate the node info file](#generate-the-node-info-file).
4. [Set up the Network Map Service](#set-up-the-network-map-service):
   1. Copy the node info file to the Network Map Service.
   2. Update the network parameters file on the Network Map Service to reference the new node info file.
   3. Start (or restart) the Network Map Service.
5. [Run the notary node](#run-the-notary-node).

### Create the notary node configuration

The exact configuration will depend on the Corda version that the notary node is running.


#### Example configuration

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


### Register the node with the Identity Manager

Ensuring that the Identity Manager Service is successfully running, start the notary node for registration.

```bash
java -jar corda.jar --config-file <NODE_CONF_FILE> --initial-registration --network-root-truststore-password <TRUST_STORE_PASSWORD> --network-root-truststore <PATH_TO_TRUST_STORE>
```

{{< note >}}
The network trust store should contain the trusted root certificate of the network. This should be created
during the initial setup of the network and therefore should be distribute by the network operator.

{{< /note >}}

### Generate the node info file

The node info file contains information such as address and certificates. The file will be used by all participants on the network to enable them to
connect to, and trust, the new notary node.

```bash
java -jar corda.jar --config-file <NODE_CONF_FILE> --just-generate-node-info
```


### Set up the Network Map Service

For full instructions, see [Network Map service]({{< relref "network-map.md" >}})


### Run the notary node

```bash
java -jar corda.jar --config-file <NODE_CONF_FILE>
```
