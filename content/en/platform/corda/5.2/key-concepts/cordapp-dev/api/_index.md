---
description: "An introduction to the CorDapp and Corda REST APIs for CorDapp Developers."
title: "Introducing the Corda APIs"
date: 2023-07-26
menu:
  corda52:
    identifier: corda52-cordapp-dev-api
    parent: corda52-key-concepts-cordapp-dev
    weight: 3000
---

# Introducing the Corda APIs

There are two types of Corda {{< tooltip >}}APIs{{< /tooltip >}} that are relevant to a {{< tooltip >}}CorDapp{{< /tooltip >}} Developer:
* [CorDapp API]({{< relref "#cordapp-api" >}})
* [Corda REST API]({{< relref "#corda-rest-api" >}})

## CorDapp API
 
The [CorDapp API]({{< relref "../../../developing-applications/api/_index.md">}}) is the API that a CorDapp uses to interact with the Corda platform. This supports, for example, interacting with other members of the network, signing transactions, verifying contracts, persisting data etc. This API is provided as JVM compatible libraries.

{{< 
  figure
	 src="corda-api.png"
   width="50%"
	 figcaption="CorDapp API"
>}}

## Corda REST API

The [Corda REST API]({{< relref "../../../reference/rest-api/_index.md">}}) enables you to interact with your CorDapp. For example, to start a {{< tooltip >}}flow{{< /tooltip >}} or retrieve the result of a flow. This API is exposed as a REST service. This same REST API is also used by Cluster Administrators to manage virtual nodes and the Corda platform itself.

HTTP requests are authenticated using basic authentication, and authorization is based on Corda’s [RBAC capabilities]({{< relref "../../../deploying-operating/config-users/_index.md" >}}).