---
aliases:
- /releases/4.3/notary-reg-tool.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-notary-reg-tool
    parent: corda-enterprise-4-3-tools-index-enterprise
    weight: 1040
tags:
- notary
- tool
title: Notary Registration Tool
---



# Notary Registration Tool

The notary registration tool is used to register the identity of the notary service,
and generates the key of the notary service that is shared by all workers of the notary cluster.

The tool is distributed with the Corda Enterprise developer pack.


## Running the notary registration tool

```sh
java -jar corda-tools-notary-registration-4.3.jar register \
     --config-file=node.conf \
     --network-root-truststore=<trust store> \
     --network-root-truststore-password=<password>
```

After successful registration, a keystore file is created by the tool in `certificates/nodekeystore.jks`
this keystore contains the service identity key that all notary workers of this notary cluster share.

Copy the file before registering the individual identity of the notary worker, to be able to distribute the file to all other notary
workers. The registration of the individual workers adds additional entries to the keystore that are not shared among the worker
nodes.
HSM Support
———–

The registration tool supports `Azure Key Vault` and `Securosys Primus X`, and if any of those is configured in the `node.config` the keys will be installed
there instead of `certificates/nodekeystore.jks`. See [HSM Support](running-a-notary-cluster/hsm-support.md#hsm-support) for more information.
