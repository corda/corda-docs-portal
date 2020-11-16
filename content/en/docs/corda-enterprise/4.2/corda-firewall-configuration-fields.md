---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-2:
    parent: corda-enterprise-4-2-corda-firewall-configuration-file
    identifier: corda-enterprise-4-2-corda-nodes-firewall-config-file
tags:
- corda
- firewall
- configuration
- file
title: Configuration fields
weight: 1
---
# Corda Enterprise Firewall configuration fields

The available configuration fields are listed below. `baseDirectory` is available as a substitution value and contains the absolute path to the firewall’s base directory.

## certificatesDirectory
An optional configuration field that specifies directory from which SSL keys and truststore keys will be loaded. The default is `baseDirectory/certificates`.

## sslKeystore
An optional configuraton field that specifies the file from which SSL keys stores will be loaded. The default value is `<certificatesDirectory>/sslkeystore.jks`.

## trustStoreFile
An optional configuration field that specifies the file from which truststore keys will be loaded. The default value is `<certificatesDirectory>/truststore.jks`.

## firewallMode
Determines operating mode of the firewall. See [Firewall operating modes](corda-firewall-configuration-file.md#firewall-operating-modes).

## keyStorePassword
The password to unlock the TLS keystore file (`<workspace>/<certificatesDirectory>/sslkeystore.jks`) containing the node certificate and private key. Due to limitations in the Artemis libraries, the private key password must be the same.

{{< note >}}
This is the non-secret value for the development certificates automatically generated during the first node run. Longer term these keys will be managed in secure hardware devices.
{{< /note >}}

## trustStorePassword 
The password to unlock the truststore file (`<workspace>/<certificatesDirectory>/truststore.jks`) containing the Corda network root certificate. This is the non-secret value for the development certificates automatically generated during the first node run.

{{< note >}}
Longer term these keys will be managed in secure hardware devices.
{{< /note >}}

##  networkParametersPath
This a mandatory configuration field that only makes sense in case of `SenderReceiver` and `BridgeInner` modes.

This is the absolute file path to a copy of the `network-parameters` as copied from a node after it has fetched the latest version from the network-map via http.

It is used to correctly configure the maximum allowed message size. The maximum message size limit is already enforced by the P2P Artemis inside the `node`, but the `bridge` also enforces this before forwarding messages to remote peers.

`Float` learns about maximum message size from `bridge` and enforces this on received packets. If the size limit is breached these messages will be consumed and discarded, so that they are not replayed forever.


## outboundConfig
This field is used to configure the processing of outbound messages. It is required for `SenderReceiver` and `BridgeInner` modes and must be absent for `FloatOuter` mode. It contains the following fields:

* [artemisBrokerAddress](#artemisbrokeraddress).
* [alternateArtemisBrokerAddresses](#alternateartemisbrokeraddresses).
* [artemisSSLConfiguration](#artemissslconfiguration).
* [proxyConfig](#proxyconfig).

### artemisBrokerAddress
The primary host and port for peer-to-peer Artemis broker. This may be running inside to the node, in which case it will hosted on the port of the `p2pAddress`,
or the `messagingServerAddress` if that is defined and `messagingServerExternal` is `false`. Otherwise, it could be an independently run Artemis broker.

### alternateArtemisBrokerAddresses
Optionally if there are multiple Artemis broker address (such as for hot-cold node deployment) then additional hosts and ports may be included in a list.

### artemisSSLConfiguration
The default behaviour is that the outgoing `TLS 1.2/AMQP 1.0` connections present certificate details from (`<workspace>/<certificatesDirectory>/sslkeystore.jks`)
and validate against (`<workspace>/<certificatesDirectory>/truststore.jks`), using the passwords defined in the root configuration. However, distinct keystores may be configured in this field. It contains the following fields:

* **keyStorePassword**:
The password for the TLS keystore.

* **keyStorePrivateKeyPassword**:
Optional configuration field to lock the private keys within the keystore. If it is missing, it will be assumed that the private keys password is the same as
`keyStorePassword` above.

* **trustStorePassword**:
The password for TLS truststore.

* **sslKeystore**:
The path to the keystore file to use in outgoing `TLS 1.2/AMQP 1.0` connections.

* **trustStoreFile**:
The path to the truststore file to use in outgoing `TLS 1.2/AMQP 1.0` connections.

### proxyConfig
This field is optionally present if outgoing peer connections should go via a SOCKS4, SOCKS5, or HTTP CONNECT tunnelling proxy. It contains the following fields:

* **version**:
Either SOCKS4, SOCKS5, or HTTP to define the protocol version used in connecting to the SOCKS proxy.

* **proxyAddress**:
Host and port of the proxy.

* **userName**:
Optionally a user name that will be presented to the proxy after connect.

* **password**:
Optionally, a password to present to the SOCKS5 or HTTP Proxy. It is not valid for SOCKS4 proxies and it should always be combined with `userName`.

* **proxyTimeoutMS**:
optionally, specify a timeout in milliseconds if the proxy is unusually slow to initate connections. The default value used is `10000`.

## inboundConfig 
This field is used to configure the properties of the listening port. It is required for `SenderReceiver` and `FloatOuter` modes and must be absent for `BridgeInner` mode. It contains the `listeningAddress` field.

### listeningAddress
The host and port to bind to as `TLS 1.2/AMQP 1.0` listener. This may be a specific network interface on multi-homed machines.

It may also differ from the externally exposed public `p2pAddress` of the port if the firewalls, or load balancers transparently reroute the traffic.

## bridgeInnerConfig
This field is required for `BridgeInner` mode and configures the tunnel connection to the `FloatOuter` (s) in the DMZ. The field should be absent in `SenderReceiver` and `FloatOuter` modes. It contains the following fields:

* [floatAddresses](#floataddresses).
* [expectedCertificateSubject](#expectedcertificatesubject).
* [tunnelSSLConfiguration](#tunnelsslconfiguration).

### floatAddresses
The list of host and ports to connect the available `FloatOuter` instances. At least one must be present.

The active `BridgeInner` will round-robin over available `FloatOuter` addresses until it can connect and activate one.

### expectedCertificateSubject
The X500 Subject name that will be presented in client certificates from the remote `FloatOuter` instances.

### tunnelSSLConfiguration
{{< note >}}
For ease of use the TLS default control tunnel connections present certificate details from (`<workspace>/<certificatesDirectory>/sslkeystore.jks`).
and validate against (`<workspace>/<certificatesDirectory>/truststore.jks`), using the passwords defined in the root config.
However, it is strongly recommended that distinct keystores should be configured in this field to use locally valid certificates only, so that compromise of the DMZ machines does not give access to the node’s primary TLS keys.
{{< /note >}}

It contains the following fields:

* **keyStorePassword**:
The password for the TLS keystore.

* **keyStorePrivateKeyPassword**:
Optional configuration field to lock the private keys within the keystore. If it is missing, it will be assumed that the private keys password is the same as
`keyStorePassword` above.

* **trustStorePassword**:
The password for TLS truststore.

* **sslKeystore**:
The path to the keystore file to use in control tunnel connections.

* **trustStoreFile**:
The path to the truststore file to use in control tunnel connections.

## floatOuterConfig
This field is required for `FloatOuter` mode and configures the control tunnel listening socket. It should be absent for `SenderReceiver` and `BridgeInner` modes. It contains the following fields:

* [floatAddress](#floataddress).
* [expectedCertificateSubject](#expectedcertificatesubject-1).
* [tunnelSSLConfiguration](#tunnelsslconfiguration-1).

### floatAddress
The host and port to bind the control tunnel listener socket to. This can be for a specific interface if used on a multi-homed machine.

### expectedCertificateSubject
The X500 Subject name that will be presented in client certificates from the `BridgeInner` when it connects to this `FloatOuter` instance.

### tunnelSSLConfiguration
{{< note >}}
For ease of use the TLS default control tunnel connection presents certificate details from (`<workspace>/<certificatesDirectory>/sslkeystore.jks`)
and validate against (`<workspace>/<certificatesDirectory>/truststore.jks`), using the passwords defined in the root config.
However, it is strongly recommended that distinct keystores should be configured in this field to use locally valid certificates only, so that compromise of the DMZ machines does not give access to the node’s primary TLS keys.
{{< /note >}}

It contains the following fields:

* **keyStorePassword**:
The password for the TLS keystore.

* **keyStorePrivateKeyPassword**:
Optional configuration field to lock the private keys within the keystore. If it is missing, it will be assumed that the private keys password is the same as
`keyStorePassword` above.

* **trustStorePassword**:
The password for TLS truststore.

* **sslKeystore**:
The path to the keystore file to use in control tunnel connections.

* **trustStoreFile**:
The path to the truststore file to use in control tunnel connections.

## haConfig 
Optionally the `SenderReceiver` and `BridgeInner` modes can be run in a hot-warm configuration, which determines the active instance using an external master election service.
Currently, the leader election process can be delegated to Zookeeper, or the firewall can use the `Bully Algorithm` (see [Bully algorithm on Wikipedia](https://en.wikipedia.org/wiki/Bully_algorithm)) via Publish/Subscribe messages on the artemis broker.

For production it is recommended that a Zookeeper cluster be used as this will protect against network partitioning scenarios. However, the `Bully Algorithm` mode does not require any additional server processes.

Eventually other electors may be supported e.g. `etcd`. 

This configuration field contains the following fields:

* [haConnectionString](#haconnectionstring).
* [haPriority](#hapriority).
* [haTopic](#hatopic).

### haConnectionString
A string containing the connection details of the master electors as a comma delimited list of individual connection strings.

* To use an external Zookeeper cluster each connection item should be in the format `zk://<host>:<port>`.

* To use the `Bully Algorithm` running over artemis the single connection string should be set to `bully://localhost`.

### haPriority
The implementation uses a prioritise leader election algorithm, so that a preferred master instance can be set. The highest priority is 0 and larger integers have lower priority.
At the same level of priority, it is random which instance wins the leader election. If a `bridge` instance dies another will have the opportunity to become master in instead.

### haTopic
Sets the zookeeper/artemis topic that the nodes used in resolving the election and must be the same for all `bridge` instances competing for master status. This is available to allow a single zookeeper/artemis cluster to be reused with multiple sets of `bridges` (e.g. in test environments).

The default value is `bridge/ha` and would not normally need to be changed if the cluster is not shared. 

## auditServiceConfiguration
Both `FloatOuter` and `BridgeInner` components have an audit service which is currently outputting into the process log some traffic statistics. It contains the `loggingIntervalSec` field.

### loggingIntervalSec
This is an integer value that controls how frequently, in seconds, statistics will be written into the logs.

## artemisReconnectionIntervalMin
If connection to the local Artemis server fails the initial reconnection attempt will be
after `artemisReconnectionIntervalMin` ms. The default interval is 5000 ms.
Subsequent retries will take be exponentially backed off until they reach `artemisReconnectionIntervalMax` ms.

## artemisReconnectionIntervalMax
The worst case Artemis retry period after repeated failure to connect is `artemisReconnectionIntervalMax` ms. The default interval is 60000 ms.

## p2pConfirmationWindowSize
This is a performance tuning detail within the Artemis connection setup that controls the send acknowledgement behaviour.

Its value should only be modified from the default if suggested by R3 to resolve issues.

## enableAMQPPacketTrace
Set this developer flag to `true` if very detailed logs are required for connectivity debugging. Note that the logging volume is substantial, so do not enable in production systems.

## healthCheckPhrase
An optional Health Check Phrase which if passed through the channel will cause AMQP Server to echo it back instead of doing normal pipeline processing.

This parameter can be used to facilitate F5 “TCP Echo” health-check monitor. Only when TCP posting starting with `healthCheckPhrase` in UTF-8 encoding is sent to application port the server will echo the same pass phrase back.

## silencedIPs
An optional list of strings of that will be compared to the remote IPv4/IPv6 source address of inbound socket connections.

If there is a match all logging for this connection will be reduced to TRACE level. The intention is to allow simple filtering of health check connections from load balancers and other monitoring components.

## custom.jvmArgs
Allows a list of jvm argument overrides to be sent to the Corda firewall process spawned by the capsule wrapper.

For instance `custom.jvmArgs = ["-Xmx2G"]` in the configuration file will set 2GByte of memory for the firewall.

This is equivalent to specifying `-Dcapsule.jvm.args="-Xmx2G"` on the command line, but is easier to track with other configuration and does not risk accidentally setting the properties onto the capsule parent process (e.g. wasting 2Gbyte of memory).

See [Setting JVM arguments](running-a-node.md#setting-jvm-arguments) for examples and details on the precedence of the different approaches to settings arguments.

## revocationConfig
Controls the way Certificate Revocation Lists (CRL) are handled for TLS connections. It contains the `mode` field.

### mode
Either `SOFT_FAIL` or `HARD_FAIL` or `OFF` or `EXTERNAL_SOURCE`

* `SOFT_FAIL` Causes CRL checking to use soft fail mode. Soft fail mode allows the revocation check to succeed if the revocation status cannot be determined because of a network error.

* `HARD_FAIL` Rigorous CRL checking takes place. This involves each certificate in the certificate path being checked for a CRL distribution point extension, and that this extension points to a URL serving a valid CRL.
This means that if any CRL URL in the certificate path is inaccessible, the connection with the other party will fail and be marked as bad.
Additionally, if any certificate in the hierarchy, including the self-generated node SSL certificate, is missing a valid CRL URL, then the certificate path will be marked as invalid.

* `OFF` : do not perform CRL check.

* `EXTERNAL_SOURCE` only makes sense for Float component i.e. with `firewallMode = FloatOuter`. When `mode = EXTERNAL_SOURCE` is specified, Float component will fetch CRLs using tunnel connection it maintains with Bridge. This allows Float to correctly obtain CRLs without
initiating direct outgoing connections to the Delivery Points specified in TLS certificates.

## p2pTlsSigningCryptoServiceConfig
This is an optional crypto service configuration that will be used for HSM TLS signing when incoming P2P connection by external party attempted into
Float.  See [Use of HSM in Corda Firewall](corda-firewall-component.md#use-of-hsm-in-corda-firewall) for an overview.

Since Float is by design a lightweight component that does not store any sensitive information locally, when it comes to TLS signing, Float will talk to the Bridge for TLS signing to take place.
Therefore, this option only makes sense for `BridgeInner` and `SenderReceiver` modes. 

It contains the following fields:

* [name](#name).
* [conf](#conf).

### name
The name of HSM provider to be used. E.g.: `UTIMACO`, `GEMALTO_LUNA`, etc. See [Using an HSM with Corda Enterprise](cryptoservice-configuration.md).

### conf
Absolute path to HSM provider specific configuration that will contain everything necessary to establish connection with HSM.

## artemisCryptoServiceConfig
This is an optional crypto service configuration that will be used for HSM TLS signing when interacting with Artemis message bus.
This option only makes sense for `SenderReceiver` and `BridgeInner` modes. In terms of structure it is very similar to [p2pTlsSigningCryptoServiceConfig](#p2ptlssigningcryptoserviceconfig) above.
If this option is missing, local file system will be used to store private keys inside `JKS` keystores.

## tunnelingCryptoServiceConfig
This is an optional crypto service configuration that will be used for HSM TLS signing during communication between Bridge and Float.
This option only makes sense for `BridgeInner` and `FloatOuter`. In terms of structure it is very similar to [p2pTlsSigningCryptoServiceConfig](#p2ptlssigningcryptoserviceconfig) above.
If this option is missing, local file system will be used to store private keys inside `JKS` keystores.