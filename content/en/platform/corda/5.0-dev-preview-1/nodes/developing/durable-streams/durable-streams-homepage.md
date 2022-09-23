---
title: "Using durable streams"
date: '2021-09-16'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing
    identifier: corda-5-dev-preview-1-nodes-developing-durable-streams
    weight: 3000
section_menu: corda-5-dev-preview
description: >
  How to use durable streams in HTTP-RPC methods.
---

Traditional HTTP request/response interaction may not be sufficient for all scenarios. For example, an HTTP-RPC client
may want to subscribe to specific events that are happening on the server side. These could include when:
* New transactions with certain characteristics are committed.
* Contract states with certain characteristics are saved to the node's vault.
* New participants are registered in the Corda Network.
* Previously-started flows complete.

This type of interaction between an HTTP-RPC client and HTTP-RPC server uses **durable streams**.

Durable streams also provide reliability with no data loss, and a mechanism to recover from scenarios where:
* Communication between an HTTP-RPC client and HTTP-RPC server is interrupted.
* Either an HTTP-RPC client or HTTP-RPC server process crashes abruptly.

Durable streams restart where they left off and carry on consuming elements of interest when a connection
is restored and/or a backup mechanism engages to replace a previously-failed client or server process. Therefore, those
consuming a durable stream are guaranteed not to *miss* an important event they have an interest in, even if they've been
slow to process the underlying transactional data or have been unavailable.

## Positions

Every element of transactional data on a durable stream is coupled with a 64-bit integer value representing a sequence
number, also known as **position**.

The value of an element's position has no particular meaning, and it may not increment by 1 with the addition of every
element. However, there are a few rules:
* The position of an element must be a positive value.
* The value can only increase from one element to the next.
* Once a position has been created, it cannot be changed.

{{<
  figure
      src="1.png"
      zoom="1.png"
    width=80%
      figcaption="Transactional elements with positions"
      alt="Transactional elements with positions"
>}}

## Polling requests

An HTTP-RPC client can make durable query polling requests to retrieve a sub-set of server side data by specifying:
* Selection criteria (parameters) for transaction data.
* Position where it left off or `-1` if this is the first polling request for a set of parameters.
* Maximum number of elements it is prepared to consume in the server response. `3` has been used in this example.

{{<
  figure
      src="2.png"
      zoom="2.png"
    width=80%
      figcaption="First durable query polling request"
      alt="First durable query polling request"
>}}

The server identifies the requested transactional data and includes it in the response.

Multiple clients can connect to an HTTP-RPC server at the same time, with each client requesting different sets of data
and processing server side responses at varying speeds.

A second client could make a separate polling request to the server using different parameters, resulting in a
different set of transactional elements:

{{<
  figure
      src="3.png"
      zoom="3.png"
    width=80%
      figcaption="Second client durable query polling request"
      alt="Second client durable query polling request"
>}}

{{< note >}}
A client can supply exactly the same parameters as another as each client has an independent streaming session with the
server. Clients progress through the elements of the stream at their own pace.
{{< /note >}}

Once the first client has processed the server's reply, it can make a second polling request:

{{<
  figure
      src="4.png"
      zoom="4.png"
    width=80%
      figcaption="First client, second poll"
      alt="First client, second poll"
>}}

The first client's second polling request is processed independently of the second client, who might still be processing the
result of its first polling request.

## Requirements for functionally pureness

In computer programming, there is a concept of a **[pure function](https://en.wikipedia.org/wiki/Pure_function)**.
Pure functions:
* Produce a result which is dependent only on the input parameters and nothing else, such as, current
  time, state of the file system, or random number generator.
* Only produce results; they don't cause any side effects.

The intention of durable streams API methods is to make them as close as possible to a pure function.
Although, strictly speaking, this is not possible as at least some log lines will be recorded on the server side
which represent a form of a side effect.

However, when it comes to input parameters for durable streams they **must**
remain constant and not be dependent on external factors.

### Durable stream API method examples

Here is a good example, as the client has provided parameters for `transactionTime` that will not change as time passes
and are not dependent on the timezone of the HTTP-RPC server:
```console
where transactionTime between (2021-06-14T09:55:59Z and 2021-06-15T09:55:59Z)
```

Here is a bad example, as the client has provided parameters for `transactionTime` that are a function of the current
server time and will change depending on when the server processes the request.
```console
where transactionTime between (T-1 and T)
```

## Tracking positions

The HTTP-RPC client is responsible for tracking positions/sequence.

When using a durable streaming API, the HTTP-RPC client polls the server for a specific remote method with some fixed
parameters. The position from which the client is interested to receive streaming payload changes for each request. The client
can retain the latest position they successfully processed as an in-memory variable, in the file
on the file system, or in the database (if they have one to use).

For native Java/Kotlin HTTP-RPC clients, you can use the interface <a href="java-client/java-client.html#positionmanager">`PositionManager`</a>.
