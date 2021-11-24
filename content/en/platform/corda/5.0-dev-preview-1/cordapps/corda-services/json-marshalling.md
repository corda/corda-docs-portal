---
title: "JsonMarshallingService"
date: '2021-11-10'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 4500
section_menu: corda-5-dev-preview
description: >
  Parse arbitrary content in and out of JSON within flows and services.
---

Use `JsonMarshallingService` in your CorDapps and Corda services to parse arbitrary
content in and out of JSON using standard, approved mappers.

```kotlin
interface JsonMarshallingService : CordaServiceInjectable, CordaFlowInjectable {

    // Parse an [input] into a JSON string.
    fun formatJson(input: Any): String

    // Parse an [input] into an instance of [T].
    // [input] must be a JSON string.
    // Specify the [Class] type of [T].
    fun <T> parseJson(input: String, clazz: Class<T>): T

    // Parse an [input] into a list of instances of [T].
    // [input] must be a JSON string.
    // Specify the [Class] type of [T].
    fun <T> parseJsonList(input: String, clazz: Class<T>): List<T>
}
```

If you are a Kotlin developer, you also have access to some `inline` functions:

```kotlin
// Parse an [input] into an instance of [T].
// [input] must be a JSON string.
inline fun <reified T> JsonMarshallingService.parseJson(input: String): T {
    return parseJson(input, T::class.java)
}

// Parse an [input] into a list of instances of [T].
// [input] must be a JSON string.
inline fun <reified T> JsonMarshallingService.parseJsonList(input: String): List<T> {
    return parseJsonList(input, T::class.java)
}
```

## Kotlin example

Here's an example of how you can use `jsonMarshallingService` in a flow:

```kotlin
@StartableByRPC
    class InjectCordaServiceFlow @JsonConstructor constructor(private val params: RpcStartFlowRequestParameters) : Flow<Unit> {
        @CordaInject
        lateinit var jsonMarshallingService: JsonMarshallingService

        @Suspendable
        override fun call(): Unit {
            val paramsMap: Map<String, String> = jsonMarshallingService.parseJson(params.parametersInJson)
            ...
        }
    }
```
