---
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-operations-guide-deployment-cenm-troubleshooting
    parent: corda-enterprise-4-6-operations-guide-deployment-cenm
    weight: 190
tags:
- troubleshooting
- common
- issues
title: Troubleshooting common issues
---


# Troubleshooting Common Issues



## General Debugging


### Enabling debug/trace logging

Each service can be configured to run with a deeper log level via command-line flags passed at start-up:

```bash
java -DdefaultLogLevel=TRACE -DconsoleLogLevel=TRACE -jar <enm-service-jar>.jar --config-file <config file>
```


### Verifying a service is running and responsive

As well as the service logs, the CENM services provide the following endpoints which can be used to determine the current
status of the service (whether it is executing and if it is reachable):


{{< table >}}

|Service|Request Type|Endpoint|Return Value|
|:--|:--|:--|:--|
|Identity Manager Service|GET|`/status`|Status information of the Identity Manager deployment.|
|Network Map Service|GET|`/network-map/my-hostname`|IP address of the caller.|
|Revocation Workflow (sub-service of Identity Manager)|GET|`/status`|Status information of the Identity Manager deployment.|

{{< /table >}}

Note that the endpoints should be preceded with the address of the respective service. For example, if the Identity
Manager is reachable on `im-host.com:1234` then the status endpoint would be `im-host.com:1234/status`.


## Nodes are not appearing in the Network Map


### Issue

The Network Map Service and node is up and running, but the node cannot be seen from any other nodes on the network.


### Solution/Explanation

There are a few different reasons why this could be:


* The publishing of the node info was successfully, but the updated network map has not been signed yet.
* There was an issue with the node info publishing such as the node’s certificate was not valid.
* The publishing of a node info is still in progress, and the Network Map Service is awaiting a response from the
Identity Manager Service.

To verify that issue 1 is not the culprit - verify that the Network Map signing process is still successfully running
periodically. Unless the Network Map Service is configured for testing, it should have an external signing process
configured. See the “Signing Network Map and Network Parameters” section of [Signing Services](../../../../cenm/1.4/signing-service.md). If the service is
configured to run with a local signer then verify that the configured sign interval is something fairly low to ensure
that updates to the network map are persisted often (e.g. 1 minute).

To verify that issue 2 is not the culprit - the logs of the Network Map Service should be checked. An error such as an
invalid certificate is not recoverable and should be resolved out of band with the node operator and support.
If there are any communication issues with the Identity Manager then the error will be logged and communication will be
retried after a short break. See the “Identity Manager Communication” section of [Network Map Service](../../../../cenm/1.4/network-map.md) to verify that the
Identity Manager communication is correctly configured for the Network Map Service.


## The CENM Service hangs on start-up


### Issue

A Network Map, Identity Manager or Signing Service hangs on start-up and throws a *HikariPool* related exception:

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

This issue *should* be Linux specific. During the establishing of the database connection certain database APIs (such as JDBC) use
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

When running the Identity Manager or Network Map Service with local signer enabled the signing process times out
resulting in an error within the local signer log file.


### Solution

There are multiple possible causes for this. The most likely candidates are:

**database overloaded and causing the signing process to dramatically slow**
The database instance should be inspected to verify that machine is adequately sized and no unknown processes are utilising
IO.

**Signing process is working as intended but timeout is configured too low**
The timeout for a local signer can be configured via the service’s configuration file. See
[Identity Manager Configuration Parameters](../../../../cenm/1.4/config-identity-manager-parameters.md) and [Network Map Configuration Parameters](../../../../cenm/1.4/config-network-map-parameters.md) for more information.


### Explanation

Each execution of the signing process is run with a timeout equal to the specified value in the configuration file (see
above linked docs for defaults). If this timeout limit is reached then an error will be logged and the process will be
retried using an exponential backoff strategy, doubling the wait period after each failure.


## SMR Service throws `java.lang.NoClassDefFoundError` on start-up


### Issue

When starting up SMR Service it throws `java.lang.NoClassDefFoundError`.


### Solution

Make sure that the given `.jar` file path in the SMR configuration under `pluginJar` property is correct.
Similarly check class names correctly (i.e. copy & paste rather than manually typing), as they must match exactly.
Also make sure that the given `.jar` file does not attempt to use invalid or non-existent dependencies.

If a class in the `.jar` file tries to import a class that does not exist the SMR will not be able to load the `.jar`
and throw this error.
