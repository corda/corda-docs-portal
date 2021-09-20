---
aliases:
- /releases/4.4/notary/installing-the-notary-service-bootstrapper.html
- /docs/corda-enterprise/head/notary/installing-the-notary-service-bootstrapper.html
- /docs/corda-enterprise/notary/installing-the-notary-service-bootstrapper.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-corda-nodes-notary-config
tags:
- installing
- notary
- service
- bootstrapper
title: Joining a bootstrapped network
weight: 3
---


# Joining a bootstrapped network

You can skip this section when you’re setting up or joining a cluster with CENM.

Once the database is set up, you can prepare your configuration files of your notary
nodes and use the bootstrapper to create a Corda network. Remember to configure
`notary.serviceLegalName` in addition to `myLegalName` for all members of
your cluster.

Note that the bootstrapper will set up the shared notary service key for
transaction signing, in addition to the individual keys of the notary workers
used for P2P messaging.

For more information about the bootstrapper, see [Network Bootstrapper](../network-bootstrapper.md).


## Expected Outcome

You will go from a set of configuration files to a directory tree containing a fully functional Corda network.

The notaries will be visible and available on the network. You can list available notaries using the node shell.

```sh
run notaryIdentities
```

The output of the above command should include the `notary.serviceLegalName`
you have configured, e.g. `O=HA Notary, L=London, C=GB`.

CorDapp developers should select the notary service identity from the network map cache.

```kotlin
serviceHub.networkMapCache.getNotary(CordaX500Name("HA Notary", "London", "GB"))
```
