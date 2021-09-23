---
title: "IdentityService"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-cordapps-corda-services
    weight: 4000
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Retrieving `Party` and `AnonymousParty` instances with the IdentityService.
---

The `IdentityService` provides methods to retrieve `Party` and `AnonymousParty` instances. `IdentityService` can be injected into flows and services.

## Retrieving `Party` instances

To retrieve a `Party` instance from `IdentityService`, you must provide a `CordaX500Name`:

- Kotlin

```kotlin
val party: Party? = identityService.partyFromName(CordaX500Name("Alice Corp", "Madrid", "ES"))
```

- Java

```java
Party party = identityService.partyFromName(new CordaX500Name("Alice Corp", "Madrid", "ES"))
```

This will return the `Party` that matches the input `CordaX500Name`, otherwise `null` is returned if the party does not exist.

{{< note >}}
`MemeberLookupService.lookup` provides improved functionality over `IdentityService.partyFromName`.
{{< /note >}}

You can also retrieve the `Party` that matches an `AbstractParty` (which could be an `AnonymousParty`):

- Kotlin

```kotlin
val party: Party? = identityService.partyFromAnonymous(anonymousParty)
```

- Java

```java
Party party = identityService.partyFromAnonymous(anonymousParty)
```

This will return the `Party` that matches the input `AbstractParty` if the well-known identity is known, otherwise `null` is returned.

## Retrieving `AnonymousParty` instances

To retrieve an `AnonymousParty` instance from `IdentityService` you must provide the `PublicKey` that is used to represent the anonymous party:

- Kotlin

```kotlin
val anonymousParty: AnonymousParty = identityService.anonymousPartyFromKey(publicKey)
```

- Java

```java
AnonymousParty anonymousParty = identityService.anonymousPartyFromKey(publicKey)
```
