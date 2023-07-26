---
date: '2023-06-22'
title: "External Messaging CorDapps"
project: corda
version: 'Corda 5.0'
menu:
  corda5:
    identifier: corda5-develop-external-messaging
    parent: corda5-develop
    weight: 7050
section_menu: corda5
---

# External Messaging CorDapps {{< enterprise-icon >}}
A running Corda flow can send simple messages via Kafka to external systems. 
In Corda 5.0, this is limited to sending messages, but a future version will support both send and send-and-receive messages. 

External messaging is implemented in CorDapps by the following components:
* **Channels** - abstract representations of routes from a flow to an external system. They allow Cluster Administrators and Network Operators to control the Kafka implementation of a logical channel at the cluster and virtual node level. A CorDapp Developer is responsible for defining the channels as part of the CorDapp.
* **Routes** - configuration of the channel and its behavior for a specific virtual node. This includes the actual Kafka topic to be used, if the route is active or not, and how the flow API responds to an inactive route.
* **Default Route Configuration** - the route configuration used, along with any channels defined in the CorDapp, to generate the virtual node’s routes. The default route configuration is defined at the cluster level and can be updated via the <a href="../reference/rest-api/C5_OpenAPI.html#tag/Configuration-API/operation/put_config">`config` endpoint</a> of the REST API. For more information see [Configuring External Messaging]({{< relref "../deploying-operating/external-messaging/_index.md">}}).
* **Flow API** - an injectable flow service allows the flow to send messages via a named and configured channel to external systems. 

To create a CorDapp that can use external messaging, you must add a resource file to define the channel(s) to use and inject the external messaging API service into the flow: 

1. To define the channel(s) to use:

   Create a JSON configuration file, `external-channels.json`, in `resources\config\` and define a list of the named channels and their type. For example:
   ```json
   {
     "channels": [
       {
         "name": "external_app",
         "type": "SEND"
       }
     ]
   }
   ```
   {{< note >}}
   * Both the `name` and `type` fields are mandatory.
   * In this version, `type` must be set to `SEND`.
   * Names can contain alphanumeric values, underscores, periods, and dashes and must have between 1 and 100 characters. Topic names with a period or underscore could clash in internal data structures, so we recommend that you use either but not both.
   {{< /note >}}

2. Add the API service using `@CordaInject`. The following example flow shows how the API is injected and how the API can be called, sending a simple string message to the defined channel `external_app`:  

   {{< note >}}
   Channel names are case sensitive.
   {{< /note >}}

   ```java
   class ExternalMessageTestFlow : ClientStartableFlow {
   
       private companion object {
           val log = LoggerFactory.getLogger(this::class.java.enclosingClass)
       }

       @CordaInject
       lateinit var externalMessaging: ExternalMessaging

       @Suspendable
       override fun call(requestBody: ClientRequestBody): String {
           log.info("Starting Test Flow...")
           try {
               externalMessaging.send("external_app", "hello outside world!")

               return ""

           } catch (e: Exception) {
               log.error("Unexpected error while processing the flow", e)
               throw e
           }
       }
   }
   ``` 

   Once your CorDapp has been [packaged]({{< relref "./packaging/_index.md">}}), the Network Operator can [create a virtual node]({{< relref "../application-networks/creating/members/cpi.md">}}) to run the CorDapp. Corda creates routes for the virtual node as part of the virtual node creation process.  The Cluster Administrator must manually [create the required Kafka topics]({{< relref "../deploying-operating/external-messaging/_index.md#creating-kafka-topics">}}) and can also optionally [change the default route configuration]({{< relref "../deploying-operating/external-messaging/_index.md#configuring-external-messaging-routes">}}).