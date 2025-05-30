---
date: '2024-04-09'
title: "Service Injection"
menu:
  corda5-tools:
    weight: 3000
    identifier: contract-testing-service-injection
    parent: contract-testing
---

# Service Injection

Some of your contracts may contain injectable service fields that are annotated with `@CordaInject`. You can inject your own mocks into these fields using the contract testing framework.

You can define two levels of service mocks:

* [Test-Class-Level Mock Services](#test-class-level-mock-services)
* [Verify-Level Mock Services](#verify-level-mock-services)

{{< note >}}
* If no mock services are provided in the assert call, the class-level mocks are used.
* The mock passed in during the assert call overwrites the class-level mock of the same type.
{{< /note >}}

## Test-Class-Level Mock Services

To implement test-class-level mock services, implement the `classLevelMockServices()` function.

{{< note >}}
No class-level mock services are defined by default.
{{< /note >}}

For example:

{{< tabs >}}
{{% tab name="Java" %}}
```java
@NotNull
@Override
protected final Map<Class<?>, Object> classLevelMockServices() {
    return Map.of(JsonMarshallingService.class, dummyJsonMarshallingService, DigestService.class, dummyDigestService);
}
```
{{% /tab %}}
{{% tab name="Kotlin" %}}
```Kotlin
override fun classLevelMockServices() = mapOf(
    JsonMarshallingService::class.java to dummyJsonMarshallingService,
    DigestService::class.java to dummyDigestService
)
```
{{% /tab %}}
{{< /tabs >}}

## Verify-Level Mock Services

You can also inject mock services when verifying your transaction. The scope of these services only last until the verification runs. This might be useful when you want to test multiple negative paths that all require different mock services.

{{< tabs >}}
{{% tab name="Java" %}}
```java
assertFailsWith(
    issueTransaction,
    "Default digest algorithm must be \"SHA2_256D\".",
    Map.of(DigestService.class, invalidDigestService)
);
```
{{% /tab %}}
{{% tab name="Kotlin" %}}
```Kotlin
assertFailsWith(
    issueTransaction,
    "Default digest algorithm must be \"SHA2_256D\".",
    mapOf(DigestService::class.java to invalidDigestService)
)
```
{{% /tab %}}
{{< /tabs >}}