---
aliases:
- /releases/4.2/notary-reg-tool.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-2:
    identifier: corda-enterprise-4-2-notary-reg-tool
    parent: corda-enterprise-4-2-tools-index-enterprise
    weight: 1040
tags:
- notary
- tool
title: Notary Registration Tool
---


# Notary Registration Tool

The notary registration tool is used to register the identity of the notary service, and receive a keystore file that is shared by all members of the notary cluster.

The notary registration tool is distributed with the Corda Enterprise dev pack.


## Running the notary registration tool

```sh
java -jar notary-registration.jar register \
     --config-file=node.conf \
     --network-root-truststore=<trust store> \
     --network-root-truststore-password=<password>
```

After successful registration, a keystore file is created by the tool in *certificates/nodekeystore.jks* this keystore contains the service identity key that all notary workers of this notary cluster share.

Copy the file before registering the individual identity of the notary, to be able to distribute the file to all other notary workers.

