---
date: '2023-06-22'
title: "External Messaging"
project: corda
version: 'Corda 5.0 Beta 4'
menu:
  corda5:
    identifier: corda5-develop-external-messaging
    parent: corda5-develop
    weight: 7050
section_menu: corda5
---

# External Messaging

A running Corda flow can send simple messages via Kafka to external systems. 
In 5.0, this is limited to sending messages, but a future version will support both send and send-and-receive messages. 

External messaging is implemented in CorDapps by the following components:
* **Channels** - abstract representations of routes from a flow to an external system. They allow Cluster Aministrators and Network Operators to control the Kafka implementation of a logical channel at the cluster and virtual node level. A CorDapp Developer is responsible for defining the channels as part of the CorDapp.
* **Routes** - a per virtual node configuration of the channel and its behaviour for the specific virtual node. This includes the actual Kafka topic to be used, if the route is active or not, and how the flow API responds to an inactive route.
* **Default Route Configuration** - the route configuration used, along with any channels defined in the CorDapp, to generate the virtual node’s routes. <!--The default route configuration is cluster level configuration and can be updated via the configuration API (Note: updates are not retrospective and will not change routes on existing virtual nodes).-->
* **Flow API** - an injectable flow service allows the flow to send messages via a configured, named channel to external systems. 

To create a CorDapp that can use external messaging, you must add a resource file to define the channel(s) to use and inject the external messaging API service into the flow: 

1. To define the channel(s) to use:

   Create a JSON configuration file, `external-channels.json`, in `resources\config\` and define a list of the named channels and their type. For exampple:
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

2. Add the API service using `@CordaInject`. The following example flow shows how the API is injected and how the API can be called, sending a simple string message to the defined channel `external_app`:  
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
{{< note >}}
Channel names are case sensitive.
{{< /note >}}
