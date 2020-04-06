---
aliases:
- /releases/3.2/json.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-2:
    identifier: corda-enterprise-3-2-json
    parent: corda-enterprise-3-2-development
    weight: 190
tags:
- json
title: JSON
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}




# JSON

Corda provides a module that extends the popular Jackson serialisation engine. Jackson is often used to serialise
to and from JSON, but also supports other formats such as YaML and XML. Jackson is itself very modular and has
a variety of plugins that extend its functionality. You can learn more at the [Jackson home page](https://github.com/FasterXML/jackson).

To gain support for JSON serialisation of common Corda data types, include a dependency on `net.corda:jackson:3.0`
in your Gradle or Maven build file.
Then you can obtain a Jackson `ObjectMapper` instance configured for use using the `JacksonSupport.createNonRpcMapper()`
method. There are variants of this method for obtaining Jackson’s configured in other ways: if you have an RPC
connection to the node (see “[Client RPC](clientrpc.md)”) then your JSON mapper can resolve identities found in objects.

The API is described in detail here:


* [JavaDoc](https://api.corda.net/api/corda-enterprise/3.2/html/api/javadoc/net/corda/client/jackson/package-summary.html)
* [Kotlin API docs](https://api.corda.net/api/corda-enterprise/3.2/html/api/kotlin/corda/net.corda.client.jackson/-jackson-support/index.html)

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
