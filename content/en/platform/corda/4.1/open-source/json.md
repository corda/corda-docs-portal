---
aliases:
- /releases/release-V4.1/json.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-1:
    identifier: corda-os-4-1-json
    parent: corda-os-4-1-development
    weight: 160
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

For more details, see [API reference](api-ref.md).

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
