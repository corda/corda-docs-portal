---
date: '2021-07-07T12:00:00Z'
menu:
  corda-enterprise-4-8:
    parent: corda-enterprise-4-8-node-serialization
tags:
- json
title: JSON
weight: 9
---




# JSON serialization

Corda provides a module that extends the popular Jackson serialization engine. Jackson can serialize
to and from JSON, and formats such as YAML and XML. Jackson is very modular - you can use
several plugins to extend its functionality. See the [Jackson home page](https://github.com/FasterXML/jackson).

To gain support for JSON serialization of common Corda data types:

1. Include a dependency on `net.corda:jackson:XXX` in your Gradle or Maven build file, where XXX is the Corda version you are targeting (0.9 for M9, for instance).
2. Obtain a Jackson `ObjectMapper` instance configured using the `JacksonSupport.createNonRpcMapper()`
method.

You can use variations of this method to get alternative Jacksons configurations. For example, if you have an RPC
connection to the node (see [Interacting with the node]({{< relref "../../../../../en/platform/corda/4.8/enterprise/node/operating/clientrpc.md" >}})) then your JSON ObjectMapper can resolve identities found in objects. The `ObjectMapper` provides a straightforward, flexible way to parse and generate JSON response objects.

For the full API details, see the:

* [Kotlin API docs](../../../../../en/api-ref/corda/4.8/open-source/kotlin/corda/net.corda.client.jackson/-jackson-support/index.html)
* [JavaDoc](../../../../../en/api-ref/corda/4.8/open-source/javadoc/net/corda/client/jackson/JacksonSupport.html)

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
import net.corda.jackson.JacksonSupport

val mapper = JacksonSupport.createNonRpcMapper()
val json = mapper.writeValueAsString(myCordaState)  // myCordaState can be any object.
```
{{% /tab %}}

{{% tab name="java" %}}
```java
import net.corda.jackson.JacksonSupport

ObjectMapper mapper = JacksonSupport.createNonRpcMapper()
String json = mapper.writeValueAsString(myCordaState)  // myCordaState can be any object.
```
{{% /tab %}}

{{< /tabs >}}

{{< note >}}
The way mappers interact with identity and RPC is likely to change in a future release.

{{< /note >}}
