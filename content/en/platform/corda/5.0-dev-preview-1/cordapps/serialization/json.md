---
date: '2021-09-03T12:00:00Z'
title: "JSON serialization"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-serialization
    weight: 600
project: corda-5
section_menu: corda-5-dev-preview

---

Corda provides a module that extends the popular Jackson serialisation engine. Jackson is often used to serialize
to and from JSON, but also supports other formats such as YAML and XML. Jackson is itself very modular and has
a variety of plugins that extend its functionality. You can learn more at the [Jackson home page](https://github.com/FasterXML/jackson).

To gain support for JSON serialization of common Corda data types, include a dependency on `net.corda:jackson:XXX`
in your Gradle or Maven build file, where `XXX` is the Corda version you are targeting (0.9 for M9, for instance).
Then you can obtain a Jackson `ObjectMapper` instance configured for use using the `JacksonSupport.createNonRpcMapper()`
method.

The API is described in detail here:

* [Kotlin API docs](https://api.corda.net/api/corda-os/4.8/html/api/kotlin/corda/net.corda.client.jackson/-jackson-support/index.html)
* [JavaDoc](https://api.corda.net/api/corda-os/4.8/html/api/javadoc/net/corda/client/jackson/package-summary.html)

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

