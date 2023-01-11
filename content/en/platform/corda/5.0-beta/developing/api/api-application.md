---
date: '2021-04-24T00:00:00Z'
title: "net.corda.v5.application"
menu:
  corda-5-beta:
    identifier: corda-5-beta-api-application
    parent: corda-5-beta-api
    weight: 1000
section_menu: corda-5-beta
---

The `corda-application` module provides the fundamental building blocks required to create a [flow](../../introduction/key-concepts.html#flows) and so all CorDapps use this module.

`corda-application` sits at a higher level in the module hiarachy and exposes the following modules as API dependencies:

- `corda-base`
- `corda-crypto`
- `corda-membership`
- `corda-serialization`

By depending on `corda-application`, your CorDapp does not need to directly depend on the modules listed above.

`corda-application` provides a number of packages. The most significant package for defining flows is `flows`, which contains the interfaces to implement and annotations to use to customize flow behaviour. The remaining packages provide some services for use within a flow. A description of each of these packages is provided below. For further details of what is present in each of these packages and what is available via these APIs, consult the API documentation.

### `crypto`

The `crypto` package provides services and types for performing cryptographic operations. The main services are the `SigningService` for signing objects, and the `DigitalSignatureVerificationService` for verifying signatures.

### `flows`

The `flows` package contains interfaces and annotations for defining flows. The main interfaces are `RPCStartableFlow` for flows expected to be started via the REST API, and `ResponderFlow` for flows expected to be started via a peer-to-peer session. Annotations in this package are used to customize flow behaviour by marking properties for service injection (`@CordaInject`) or marking either side of a peer-to-peer session (`@InitiatingFlow` and `@InitiatedBy`).

### `marshalling`

The `marshalling` package provides services for working with parameters input over the REST API and generating suitable output to return via the REST API. The main service is `JSONMarshallingService`, which allows you to work with JSON input and output data.

### `membership`

The `membership` package provides services for working with membership groups. The `MemberLookup` service allows a flow to discover what counterparties are available in the membership group or retrieve full details of a counterparty with a given name.

### `messaging`

The `messaging` package provides services and types for creating and working with peer-to-peer sessions. The `FlowMessaging` service allows you to create new sessions with counterparties. Once created, a `FlowSession` can be used to send and receive messages from a peer.

Corda creates a `FlowSession` instance for a flow created via a peer-to-peer message (one implementing `ResponderFlow` in the `flows` package) for communication with the peer that initiated the flow.

### `persistence`

The `persistence` package provides services for performing persistence operations; mainly reading and writing data to and from the database. The `PersistenceService` is the main service for providing this functionality.

### `serialization`

The `serialization` package provides services for working with data marked as `@CordaSerializable`, in order to render it into a form suitable for sending to a counterparty. Usually this is handled by the messaging layer (see the [messaging package](#messaging)), but if you require access to serialization directly it is exposed here. The main service for serailization is the `SerializationService`. At present, the only scheme available via this service is AMQP.
