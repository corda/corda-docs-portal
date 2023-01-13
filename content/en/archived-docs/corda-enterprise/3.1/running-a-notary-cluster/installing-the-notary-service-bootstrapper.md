---
aliases:
- /releases/3.1/running-a-notary-cluster/installing-the-notary-service-bootstrapper.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-1:
    identifier: corda-enterprise-3-1-installing-the-notary-service-bootstrapper
    parent: corda-enterprise-3-1-installing-the-notary-service
    weight: 1010
tags:
- installing
- notary
- service
- bootstrapper
title: Using the Bootstrapper
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Using the Bootstrapper

Once the database is set up, you can prepare your configuration files of your notary
nodes and use the bootstrapper to create a Corda network, see
[Setting up a Corda network](../setting-up-a-corda-network.md). Remember to configure
`notary.serviceLegalName` in addition to `myLegalName` for all members of
your cluster.

You can find the documentation of the bootstrapper at [Setting up a Corda network](../setting-up-a-corda-network.md).


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

