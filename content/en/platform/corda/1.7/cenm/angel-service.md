---
date: '2020-06-06T18:19:00Z'
menu:
  cenm-1-7:
    identifier: cenm-1-7-angel
    parent: cenm-1-7-operations
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

This should either be specified in a config file or on the command line. You can start the Angel Service with the following command:

``` {.bash}
java -jar angel-<VERSION>.jar -f angel.conf
```

Alternatively, you can start the Angel Service with the following command and arguments:

``` {.bash}
java -jar angel-<VERSION>.jar --zone-host zone.example.org --zone-port 5050 --token <zone-token> --service IDENTITY_MANAGER
```

The full list of arguments you can use when starting the Angel Service are described below:

- `--jar-name`: The name of the service JAR file. Optional.
- `--webservice-host`: The IP address for the Angel Service's web service to bind to. Optional.
- `--webservice-port`: The port for the Angel Service's web service to run. Optional, but must be specified for the web service to be started.
- `--zone-host`: The host or IP address of the Zone Service.
- `--zone-port`: The port number of the Zone Service.
- `--token`: Authentication token to pass to the Zone Service.
- `--polling-interval`: Time (in seconds) to wait before polling the Zone Service.
- `--service`: The name of the service being managed. The possible values are `IDENTITY_MANAGER`, `NETWORK_MAP`, or `SIGNER`.
- `--network-truststore`: The network truststore file path. Optional, but must be specified if the managed service is Network Map, otherwise the Angel Service cannot execute the flag day workflow.
- `--truststore-password`: The password for the network truststore file. Optional, but must be specified if the managed service is Network Map, otherwise the Angel Service cannot execute the flag day workflow.
- `--root-alias`: The root alias. Optional, but must be specified if the managed service is Network Map, otherwise the Angel Service cannot execute the flag day workflow.
- `--tls`: Defines whether TLS is used on listening sockets (CENM and admin). Defaults to `false` if no value is provided.
- `--tls-keystore`: The path for the TLS keystore. Required if `--tls` is set to `true`.
- `--tls-keystore-password`: The password for the TLS keystore. Required if `--tls` is set to `true`.
- `--tls-truststore`: The path for the TLS truststore. Required if `--tls` is set to `true`.
- `--tls-truststore-password`: The password for the TLS truststore. Required if `--tls` is set to `true`.

## Configuration

The Angel Service can either be configured via the command-line or with a configuration file. It then downloads the configuration of the managed service from the Zone Service.

The main elements that need to be configured for the Angel Service are:

* [Service](#service)
  * [Type](#type)
  * [JAR File](#jar-file)
* [Zone](#zone)

### Service

The service component of the Angel Service is the service that is started and managed by the Angel Service.

#### Type

The service type can be one of three services that the Angel Service can manage:

* `IDENTITY_MANAGER`
* `NETWORK_MAP`
* `SIGNER`

The configuration for the `IDENTITY_MANAGER` and `SIGNER` managed service types are more or less the same. However, when running the Angel Service with the `NETWORK_MAP` as the managed service type, then two additional configuration parameters need to be specified:

##### networkParametersFile

The network parameters are the set of values that every node participating in the network needs to agree on to interoperate with each other. See [Network Parameters Configuration Parameters]({{< relref "config-network-map-parameters.md" >}}) for a detailed explanation.

The file specified for this parameter needs to be the plain-text version of the network parameters used when setting the initial network parameters. This is not the binary `network-parameters` file that Corda nodes use.

##### networkRootTrustStore

This should be set as the path for the `network-root-truststore.jks` of the network (initially generated using the PKI tool).

The network root truststore should be configured inside the `service` configuration block:

```guess
service = {
    type = NETWORK_MAP
    jarFile = "networkmap.jar"
    ...
    networkRootTrustStore = {
        rootAlias = "cordarootca"
        location = "./certificates/network-root-truststore.jks"
        password = "trustpass"
    }
}
```

#### JAR file

The `jarFile` parameter is the path to the JAR which the Angel Service uses to start a new Java process. There is a default file name for each managed service type:

* `identitymanager.jar`
* `networkmap.jar`
* `signer.jar`

### Zone

The `zone` configuration block details the connection to the Zone Service. This is needed to download the configuration file for the managed service. To configure the `zone` configuration, make sure you have generated a zone token for the corresponding managed service:

```guess
zone = {
    host = "localhost"
    port = 5063
    token = "<zone token>"
}
```

{{< note >}}
See [Angel Service Configuration Parameters]({{< relref "config-angel-service-parameters.md" >}}) for a detailed explanation of each possible parameter.
{{< /note >}}

**Workflow**

1. On start-up, the Angel Service requests the configuration for its managed service from the Zone Service, providing the authentication token to identify itself.
2. It then performs basic validation of the configuration, writes it to disk, and starts the managed service.
3. Following this, at regular intervals, it polls the Zone Service for changes to the configuration, and if any are found:
    1. It backs up the existing configuration.
    2. It shuts down the managed service.
    3. It writes the new configuration.
    4. It starts the managed service.

If the managed service is Network Map, the Zone Service can reply with a lifecycle event (flag day). This is because only the Network Map Service holds the network parameters that flag days update. In this case, the Angel Service will automatically perform the [required steps]({{< relref "updating-network-parameters.md" >}}) on the managed Network Map Service.

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
