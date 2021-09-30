---
aliases:
- /head/json.html
- /HEAD/json.html
- /json.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-json
    parent: corda-os-4-6-serialization-index
    weight: 1050
tags:
- json
title: JSON
---




# JSON

Corda provides a module that extends the popular Jackson serialisation engine. Jackson is often used to serialise
to and from JSON, but also supports other formats such as YaML and XML. Jackson is itself very modular and has
a variety of plugins that extend its functionality. You can learn more at the [Jackson home page](https://github.com/FasterXML/jackson).

To gain support for JSON serialisation of common Corda data types, include a dependency on `net.corda:jackson:XXX`
in your Gradle or Maven build file, where XXX is of course the Corda version you are targeting (0.9 for M9, for instance).
Then you can obtain a Jackson `ObjectMapper` instance configured for use using the `JacksonSupport.createNonRpcMapper()`
method. There are variants of this method for obtaining Jackson’s configured in other ways: if you have an RPC
connection to the node (see “[Interacting with a node](clientrpc.md)”) then your JSON mapper can resolve identities found in objects.

The API is described in detail here:


* [Kotlin API docs](https://api.corda.net/api/corda-os/4.6/html/api/kotlin/corda/net.corda.client.jackson/-jackson-support/index.html)
* [JavaDoc](https://api.corda.net/api/corda-os/4.6/html/api/javadoc/net/corda/client/jackson/package-summary.html)

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
