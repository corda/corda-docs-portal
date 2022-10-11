---
title: "SerializationService"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 5000
section_menu: corda-5-dev-preview
description: >
  Serializing and deserializing within flows and services.
---

Object serialization is the process of converting objects into a stream of bytes and, deserialization, the reverse process of creating objects from a stream of bytes. You can serialize and deserialize outputted bytes using the `SerializationService`, which can be injected into flows and services.

## Examples
{{< tabs name="serialization">}}
{{% tab name="Kotlin"%}}
```kotlin
class SerializationExampleFlow : Flow<Unit> {

  @CordaInject
  private lateinit var serializationService: SerializationService

  @Suspendable
  override fun call() {
    // Serialize an object
    val serialized: SerializedBytes<String> = serializationService.serialize("string to serialize")
    // Deserialize the serialized bytes
    val deserialized: String = serializationService.deserialize(serialized, String::class.java)
  }
}
```
{{% /tab %}}

{{% tab name="Java"%}}
```java
public class SerializationExampleFlow implements Flow<Void> {

  @CordaInject
  private SerializationService serializationService;

  @Override
  @Suspendable
  public Void call() {
    // Serialize an object
    SerializedBytes<String> serialized = serializationService.serialize("string to serialize");
    // Deserialize the serialized bytes
    String deserialized = serializationService.deserialize(serialized, String.class);
    return null;
  }
}
```
{{% /tab %}}
{{< /tabs >}}

{{< note >}}
Injection is done in the same way into `CordaService`s.
{{< /note >}}

If you are a Kotlin developer, you also have access to some `inline` functions:

```kotlin
// Serialize an object
val serialized: SerializedBytes<String> = serializationService.serialize("string to serialize")
// Deserialize the serialized bytes
// The class doesn't have to be included directly when using the inline version
val deserialized: String = serializationService.deserialize(serialized)
```
