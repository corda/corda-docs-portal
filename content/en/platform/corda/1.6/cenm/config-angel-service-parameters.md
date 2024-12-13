---
aliases:
- /config-angel-service-parameters.html
date: '2024-09-24'
menu:
  cenm-1-6:
    identifier: cenm-1-6-config-angel-service-parameters
    parent: cenm-1-6-configuration
    weight: 255
tags:
- config
- angel service
title: Angel Service Configuration Parameters
---

# Angel Service Configuration Parameters

The configuration references for the Angel Service are given below:

* **pollingTimeSeconds**:
*(Optional)* The time in seconds to wait before polling the Zone Service.

* **networkParametersFile**:
The path to the network parameters file. This is the plain-text version of the network parameters used when setting the initial network parameters. This is not the binary `network-parameters` file that Corda nodes use. Only used for the `NETWORK_MAP` service type.

  {{< important >}}
  The `networkParametersFile` property can only be specified if `service.type` is set to `NETWORK_MAP`.
  {{< /important >}}

* **webServiceHost**:
*(Optional)* The IP address for the Angel web service to bind to.

* **webServicePort**:
*(Optional)* The port for the Angel web service to run. Must be specified for the web service to be started.

* **service**:

  * **type**:
  The main class of the plugin being loaded.

  * **jarFile**:
  *(Optional - defaults to one of: `identitymanager.jar`, `networkmap.jar`, `signer.jar`)* The path to the service JAR.

  * **enmListener**:
  Information about the way the service will communicate with the rest of the CENM deployment.

    * **host**:
    *(Optional)* The host or IP address of the service.

    * **port**:
    The port that the service binds to, and other CENM components it connects to.

    * **verbose**:
    *(Optional)* Enables verbose logging for the socket layer.

    * **reconnect**:
    Determines if a client should attempt to reconnect if the connection is dropped.

    * **ssl**:
    See [SSL Settings]({{< relref "../../../../../en/platform/corda/1.6/cenm/config-ssl.md" >}}).

  * **pluginJar**:
  *(Optional)* The absolute path to the JAR file of the workflow plugin.

  * **networkRootTrustStore**:
  Information about the network root trust store file.

    * **location**:
    The path to the network parameters file. Only used for the Network Map Service.

    * **password**:
    The password for the truststore file.

    * **rootAlias**:
    The root alias.


  {{< important >}}
  As with the `networkParametersFile` property, the `networkRootTrustStore` can only be specified if `service.type` is set to `NETWORK_MAP`.
  {{< /important >}}

* **zone**:

  * **host**:
  The host or IP address of the Zone Service.

  * **port**:
  The port number of the Zone Service.

  * **authToken**:
  The Authentication token used to interact with the Zone Service.

## Obfuscated configuration files

To view the latest changes to the obfuscated configuration files,
see [Obfuscation configuration file changes]({{< relref "../../../../../en/platform/corda/1.6/cenm/obfuscated-config-file-changes.md" >}}).
