---
title: "IdentityService"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 4000
section_menu: corda-5-dev-preview
description: >
  Retrieving `Party` and `AnonymousParty` instances with the IdentityService.
expiryDate: '2022-09-28'  
---

The `IdentityService` provides methods to retrieve `Party` and `AnonymousParty` instances. `IdentityService` can be injected into flows and services.

## Retrieve `Party` instances

To retrieve a `Party` instance from `IdentityService`, you must provide a `CordaX500Name`:

{{< tabs name="IdentityService">}}
{{% tab name="Kotlin"%}}
```kotlin
val party: Party? = identityService.partyFromName(CordaX500Name("Alice Corp", "Madrid", "ES"))
```
{{% /tab %}}

{{% tab name="Java"%}}
```java
Party party = identityService.partyFromName(new CordaX500Name("Alice Corp", "Madrid", "ES"))
```
{{% /tab %}}
{{< /tabs >}}
This will return the `Party` that matches the input `CordaX500Name`, otherwise `null` is returned if the party does not exist.

{{< note >}}
`MemeberLookupService.lookup` provides improved functionality over `IdentityService.partyFromName`.
{{< /note >}}

You can also retrieve the `Party` that matches an `AbstractParty` (which could be an `AnonymousParty`):

{{< tabs name="AbstractParty">}}
{{% tab name="Kotlin"%}}
```kotlin
val party: Party? = identityService.partyFromAnonymous(anonymousParty)
```
{{% /tab %}}

{{% tab name="Java"%}}
```java
Party party = identityService.partyFromAnonymous(anonymousParty)
```
{{% /tab %}}
{{< /tabs >}}

This will return the `Party` that matches the input `AbstractParty` if the well-known identity is known, otherwise `null` is returned.

## Retrieve `AnonymousParty` instances

To retrieve an `AnonymousParty` instance from `IdentityService` you must provide the `PublicKey` that is used to represent the anonymous party:

{{< tabs name="AnonymousParty">}}
{{% tab name="Kotlin"%}}

```kotlin
val anonymousParty: AnonymousParty = identityService.anonymousPartyFromKey(publicKey)
```

{{% /tab %}}

{{% tab name="Java"%}}

```java
AnonymousParty anonymousParty = identityService.anonymousPartyFromKey(publicKey)
```
{{% /tab %}}
{{< /tabs >}}
