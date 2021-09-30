---
date: '2020-06-06T18:19:00Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-angel
    parent: cenm-1-3-operations
    weight: 25
tags:
- angel
title: Angel Service
---

# Angel Service

## Introduction

The Angel Service is an adapter, which manages the lifecycle of other
services such as the Network Map Service or the Identity Manager Service, to make them more
compatible with packaging tools such as Docker. You do not need to run this service directly
as it is typically packaged in a Docker image and it is run via Docker.

## Running the Angel Service

To run the Angel Service, you must specify the following:

- The service to be run.
- The hostname/IP of the Zone Service.
- The port number of the Zone Service.
- The authentication token to present to the Zone Service.

You can also provide the following:
- A host and a port to display the health check API for the Angel Service (to be used by Kubernetes, for example).
- A poll timeout for how often the Zone Service should be checked for changes.

You can start the Angel Service with the following command:

``` {.bash}
java -jar angel-<VERSION>.jar --zone-host zone.example.org --zone-port 5050 --token topsecret --service IDENTITY_MANAGER
```

The full list of arguments you can use when starting the Angel Service are described below:

- `--jar-name`: The name of the service `.jar` file. Optional.
- `--webservice-host`: The IP address for the Angel Service's web service to bind to. Optional.
- `--webservice-port`: The port for the Angel Service's web service to run. Optional, but must be specified for the web service to be started.
- `--zone-host`: The host or IP address of the Zone Service.
- `--zone-port`: The port number of the Zone Service.
- `--token`: Authentication token to pass to the Zone Service.
- `--polling-interval`: Time (in seconds) to wait before polling the Zone Service.
- `--service`: The name of the service being managed. The possible values are `IDENTITY_MANAGER`, `NETWORK_MAP`, or `SIGNER`.
- `--network-truststore`: The network truststore file path. Optional, but must be specified if the managed service is Network Map, otherwise the Angel Service cannot execute the Flag Day workflow.
- `--truststore-password`: The password for the network truststore file. Optional, but must be specified if the managed service is Network Map, otherwise the Angel Service cannot execute the Flag Day workflow.
- `--root-alias`: The root alias. Optional, but must be specified if the managed service is Network Map, otherwise the Angel Service cannot execute the Flag Day workflow.
- `--tls`: Defines whether TLS is used on listening sockets (CENM and admin). Defaults to `false` if no value is provided.
- `--tls-keystore`: The path for the TLS keystore. Required if `--tls` is set to `true`.
- `--tls-keystore-password`: The password for the TLS keystore. Required if `--tls` is set to `true`.
- `--tls-truststore`: The path for the TLS truststore. Required if `--tls` is set to `true`.
- `--tls-truststore-password`: The password for the TLS truststore. Required if `--tls` is set to `true`.

## Configuration

The Angel Service is configured via the command-line and it downloads the configuration of the managed service from the Zone Service.

**Workflow**

1. On start-up, the Angel Service requests the configuration for its managed service from the Zone Service, providing the authentication token to identify itself.
2. It then performs basic validation of the configuration, writes it to disk, and starts the managed service.
3. Following this, at regular intervals, it polls the Zone Service for changes to the configuration, and if any are found:
    1. It backs up the existing configuration.
    2. It shuts down the managed service.
    3. It writes the new configuration.
    4. It starts the managed service.

If the managed service is Network Map, the Zone Service can reply with a lifecycle event (Flag Day). This is because only the Network Map Service holds the network parameters that Flag Days update. In this case, the Angel Service will automatically perform the [required steps](updating-network-parameters.md) on the managed Network Map Service.

## Service health checking via API

The Angel Service provides a REST API where its health and that of the managed service can be checked. The API is described in the table below.

{{< table >}}
| Request method  | Path     | Description |
| :------------- | :------------- | :-----------|
| Get | /angel/health | Check the health of the Angel Service. |
| Get | /angel/service-health | Check the health of the managed service. |
{{< /table >}}

### Possible responses

#### /angel/health

{{< table >}}
| Response code     |  Description |
:------------- | :------------- |
| 200 OK | Success - a response has been received from both the Zone Service and the managed service. Both services are considered healthy. |
| 502 Bad Gateway | Failure - no response has been received from the managed service. The services are not considered healthy. |
| 406 Not Acceptable | Unknown - a response has been received from the managed service, but the protocol does not match `PING_RESPONSE`. |
{{< /table >}}

#### /angel/service-health

{{< table >}}
| Response code     |  Description |
:------------- | :------------- |
| 200 OK | Success - the managed service responded to the ping request - it is considered healthy. |
| 502 Bad Gateway | Failure - the managed service did not respond to the ping request - it is not considered healthy. |
{{< /table >}}
