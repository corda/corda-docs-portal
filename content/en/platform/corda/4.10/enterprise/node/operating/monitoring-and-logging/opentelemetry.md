---
date: '2023-01-09'
menu:
  corda-enterprise-4-10:
    parent: corda-enterprise-4-10-monitoring-logging
title: OpenTelemetry
weight: 350
---

# OpenTelemetry

This section describes how to setup OpenTelemetry and the simple log telemetry.

Telemetry has been implemented in Corda 4.10 with a pluggable architecture. There are two telemetry components:

* **OpenTelemetry**: This component links with the OpenTelemetry API and issues spans for flows and certain significant operations.
* **Simple log telemetry**: This component issues log lines for flows and certain significant operations. These logs lines contain a trace ID. The complete call sequence of flows can be identified via the trace ID.

{{< note >}}
The two types of telemetry are completely independent. You can have both, one, or none of them enabled.
{{< /note >}}


## Corda OpenTelemetry integration

The Corda OpenTelemetry component links at compile time with the OpenTelemetry API. In order to produce spans, there is a runtime dependency on the OpenTelemetry SDK. 

There are two ways to make the OpenTelemetry SDK available to the Corda node:

* Include the `corda-opentelemetry-driver` into the drivers directory of the Corda node.
* Start the Corda node with an OpenTelemetry Java agent installed.

## Using the OpenTelemetry driver

To use the OpenTelemetry driver, copy `corda-opentelemetry-driver-%VERSION%.jar` into the drivers directory of the Corda node. This driver can be downloaded from Artifactory and is included in the release pack.

## Using the OpenTelemetry Java agent

To use the OpenTelemetry Java agent:

1. Download the agent from [GitHub](https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases). The file you need is `opentelemetry-javaagent.jar`.
2. Start the Corda node with the following example command line: `java -Dcapsule.jvm.args=“-javaagent:/PATH-TO-OT-JAVAAGENT/opentelemetry-javaagent.jar -Dotel.service.name=YOUR-SERVICE-NAME” -jar corda.jar`.
3. Replace `PATH-TO-OT-JAVAAGENT` with the full path to where you placed the OpenTelemetry Java agent.
4. Replace `YOUR-SERVICE-NAME` with the service name you would like the Corda node to be identified as.

{{< note >}}
This method of linking the SDK with the Corda node enables OpenTelemetry automated instrumentation, which means some other third-party libraries included with Corda will also generate spans. See the [OpenTelemetry](https://opentelemetry.io/docs/concepts/instrumenting-library/) website for details on which libraries are enabled.
{{< /note >}}


## Setting up OpenTelemetry

Corda has been tested with the OpenTelemetry collector and a Jaeger backend. Refer to the [OpenTelemetry](https://opentelemetry.io/docs/collector/) and [Jaeger](https://www.jaegertracing.io/) websites for details on how to setup a collector and Jaeger backend.

Corda OpenTelemetry can also be enabled or disabled via a node configuration parameter, such as `telementry.openTelemetryEnabled = true`.

If this setting is true and the OpenTelemetry SDK has been linked to Corda as described above, the node will generate spans. If this setting is false, the node won't generate spans, even if the node is linked with the SDK.

## Client API

OpenTelemetry span generation is also incorporated into the RPC client API. If you want your Corda client code to generate spans, you need to include the OpenTelemetry SDK as a dependency. The methods described above only apply to the Corda node. 

<!-- (TODO: Give example of dependencies needed). -->

## Creating your own Spans

The OpenTelemetry API may be used in your flows and in your client code to create spans and baggage. To get an instance of the OpenTelemetry API in a flow, make the following call:
`val openTelemetry: OpenTelemetry? = serviceHub.telemetryService.getTelemetryHandle(OpenTelemetry::class.java)`.

From the client API, where RPC is a CordaRPCConnection, you would use the following:
`val openTelemetry: OpenTelemetry? = rpc.getTelemetryHandle(OpenTelemetry::class.java)`.

When creating your own spans, you can also create your own baggage. If you create your own baggage, it will also be sent to other nodes, and you can specify if you want this baggage to be copied to span tags. If you do, all of the spans involved in the transaction for that node will also get a copy of the baggage. This can be enabled with the following parameter:
`telementry.copyBaggageToTags = true`.

The default value of this setting is `false`.

{{< note >}}
Within a checkpoint, only the span ID has a checkpoint, meaning spans do not survive a node restart. If the node restarts, the parent span information will be lost, and new spans will be generated for the flows. The root span after the node restart won't know who the parent span was before the node restart.
{{< /note >}}

## Start and End Spans

The current implementation of OpenTelemetry will send spans to the backend when the flow or operation is completed. This is handled via the OpenTelemetry SDK. If the flow somehow gets stuck or does not complete, the span representing that flow will never reach the backend. It can be difficult to figure out what went wrong by just looking at the spans, as you will only see the complete spans.

{{< note >}}
If a child span doesn't complete, parent spans also do not complete.
{{< /note >}}

As an alternative, the Corda OpenTelemetry component sends a start or end span to the backend when a flow or operation starts or stops, in addition to the normal spans sent for the operation. This is effectively a start flow span event and an end flow span event. With this view of the spans, it becomes easier to determine where the flow got stuck, as it will be the lowest child without an end span event. 

{{< note >}}
These start and end span events are only generated for spans that Corda generated. If you create a span in your own flow code, you won’t see equivalent start and end span events for your flows, as Corda knows nothing of them before the node restart.
{{< /note >}}

Creating these start and end span events will also cause more spans to be sent out to the network, meaning there could be a performance impact on the network. By default, this functionality is disabled, but can be enabled via the following configuration property:
`telementry. spanStartEndEventsEnabled = true`.

## Simple Log Telemetry Component

The Simple log telemetry component is the second type of telemetry supported. Instead of creating spans, this component simply writes log lines which record the trace ID. The trace ID is propagated to flows and other nodes involved in the transaction. By using grep on the trace ID, you can see all of the flows on different nodes involved in the same transaction. This component is enabled via the following configuration flag: `telementry.simpleLogTelemeteryEnabled = true`.

The default value of this flag is `false`. The logger associated with this component is `SimpleLogTelemetryComponent`.