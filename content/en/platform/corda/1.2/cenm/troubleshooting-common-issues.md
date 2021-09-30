---
aliases:
- /releases/release-1.2/troubleshooting-common-issues.html
- /docs/cenm/head/troubleshooting-common-issues.html
- /docs/cenm/troubleshooting-common-issues.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-2:
    identifier: cenm-1-2-troubleshooting-common-issues
    parent: cenm-1-2-operations
    weight: 190
tags:
- troubleshooting
- common
- issues
title: Troubleshooting Common Issues
---


# Troubleshooting Common Issues



## General Debugging


### Enabling debug/trace logging

Each service can be configured to run with a deeper log level via command line flags passed at startup:

```bash
java -DdefaultLogLevel=TRACE -DconsoleLogLevel=TRACE -jar <enm-service-jar>.jar --config-file <config file>
```


### Verifying an ENM service is running and responsive

As well as the service logs, the ENM services provide the following endpoints which can be used to determine the current
status of the service (whether it is executing and if it is reachable):


{{< table >}}

|**Service**|**Request Type**|**Endpoint**|**Return Value**|
|:--|:--|:--|:--|
|Identity Manager service|GET|`/status`|Status information of the Identity Manager deployment.|
|Network Map service|GET|`/network-map/my-hostname`|IP address of the caller.|
|Revocation Workflow (sub-service of Identity Manager)|GET|`/status`|Status information of the Identity Manager deployment.|

{{< /table >}}

Note that the endpoints should be preceded with the address of the respective service. For example, if the Identity
Manager is reachable on `im-host.com:1234` then the status endpoint would be `im-host.com:1234/status`.


## Nodes are not appearing in the Network Map


### Issue

The Network Map service and node is up and running, but the node cannot be seen from any other nodes on the network.


### Solution/Explanation

There are a few different reasons why this could be:


* The publishing of the node info was successfully, but the updated network map has not been signed yet.
* There was an issue with the node info publishing such as the node’s certificate was not valid.
* The publishing of a node info is still in progress, and the Network Map service is awaiting a response from the
Identity Manager service.

To verify that issue 1 is not the culprit - verify that the Network Map signing process is still successfully running
periodically. Unless the Network Map service is configured for testing, it should have an external signing process
configured. See the “Signing Network Map and Network Parameters” section of [Signing Services](signing-service.md). If the service is
configured to run with a local signer then verify that the configured sign interval is something fairly low to ensure
that updates to the network map are persisted often (e.g. 1 minute).

To verify that issue 2 is not the culprit - the logs of the Network Map service should be checked. An error such as an
invalid certificate is not recoverable and should be resolved out of band with the node operator and support.
If there are any communication issues with the Identity Manager then the error will be logged and communication will be
retried after a short break. See the “Identity Manager Communication” section of [Network Map Service](network-map.md) to verify that the
Identity Manager communication is correctly configured for the Network Map service.


## The CENM Service hangs on startup


### Issue

The CENM service (Network Map, Identity Manager or Signer) hangs on startup and throws a *HikariPool* related exception:

```guess
[ERROR] 2018-11-19T15:50:54,327Z [main] ConsolePrint.uncaughtException - Unexpected Error: Failed to initialize pool: Connection reset
com.zaxxer.hikari.pool.HikariPool$PoolInitializationException: Failed to initialize pool: Connection reset ClientConnectionId:765c4b14-
8486-48fc-ba75-b4606917ab98
```


### Solution

Run the service with the command `-Djava.security.egd=file:/dev/./urandom`. For example:

```bash
java -Djava.security.egd=file:/dev/./urandom -jar identitymanager.jar --config-file identitymanager.conf
```


### Explanation

This issue *should* be Linux specific. During the establishing of the DB connection certain DB APIs (such as JDBC) use
random number generation via `java.security.SecureRandom` API. This API uses `/dev/random` which checks if there is
enough available estimated entropy. If it thinks that there is not enough then it will block whilst more is generated.
Depending on the underlying system and API usage this can cause a progressive slow down of random number generation.
Eventually random number generation will become so slow that a timeout occurs during the establishing of the initial
login, resulting in an error.

Switching the `java.security.SecureRandom` API to utilise `/dev/urandom` (which is non-blocking) should prevent this
issue. See [myths about urandom](https://www.2uo.de/myths-about-urandom/) for a more in-depth discussion around
`/dev/random` vs `/dev/urandom`.


## Signing process timing out


### Issue

When running the Identity Manager or Network Map service with local signer enabled the signing process times out
resulting in an error within the local signer log file.


### Solution

There are multiple possible causes for this. The most likely candidates are:

**DB overloaded and causing the signing process to dramatically slow**
The DB instance should be inspected to verify that machine is adequately sized and no unknown processes are utilising
IO.

**Signing process is working as intended but timeout is configured too low**
The timeout for a local signer can be configured via the service’s configuration file. See
[Identity Manager Configuration Parameters](config-identity-manager-parameters.md) and [Network Map Configuration Parameters](config-network-map-parameters.md) for more information.


### Explanation

Each execution of the signing process is run with a timeout equal to the specified value in the configuration file (see
above linked docs for defaults). If this timeout limit is reached then an error will be logged and the process will be
retried using an exponential backoff strategy, doubling the wait period after each failure.


## SMR Service throws `java.lang.NoClassDefFoundError` on startup


### Issue

When starting up SMR service it throws `java.lang.NoClassDefFoundError`.


### Solution

Make sure that the given JAR file path in the SMR config under `pluginJar` property is correct.
Similarly check class names correctly (i.e. copy & paste rather than manually typing), as they must match exactly.
Also make sure that the given JAR file does not attempt to use invalid or non-existent dependencies.

If a class in the JAR file tries to import a class that does not exist the SMR will not be able to load the JAR
and throw this error.
