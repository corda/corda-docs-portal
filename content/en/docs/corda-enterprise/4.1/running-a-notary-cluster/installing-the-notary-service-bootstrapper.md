---
aliases:
- /releases/4.1/running-a-notary-cluster/installing-the-notary-service-bootstrapper.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-1:
    identifier: corda-enterprise-4-1-installing-the-notary-service-bootstrapper
    parent: corda-enterprise-4-1-installing-the-notary-service
    weight: 1010
tags:
- installing
- notary
- service
- bootstrapper
title: Using the Bootstrapper
---

# Using the Bootstrapper

You can skip this section when you're setting up or joining a cluster with
doorman and network map.

Once the database is set up, you can prepare your configuration files of your notary
nodes and use the bootstrapper to create a Corda network, see
[Network Bootstrapper](../network-bootstrapper.md). Remember to configure
`notary.serviceLegalName` in addition to `myLegalName` for all members of
your cluster.




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

