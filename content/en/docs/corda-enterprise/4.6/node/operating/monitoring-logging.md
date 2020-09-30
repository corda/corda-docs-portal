---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-monitoring-logging
    parent: corda-enterprise-4-6-corda-nodes-operating
tags:
- monitoring
- logging
title: Node monitoring and logging
weight: 5
---


# Node monitoring and logging


## Logging

By default the node log files are stored to the `logs` subdirectory of the working directory and are rotated. Logging can be printed to the console by passing the `--log-to-console` command line flag. The default logging level is `INFO` which can be adjusted by the `--logging-level` command line argument. This configuration option will affect all modules. Hibernate (the JPA provider used by Corda) specific log messages of level `WARN` and above will be logged to the diagnostic log file, which is stored in the same location as other log files (`logs` subdirectory by default). This is because Hibernate may log messages at WARN and ERROR that are handled internally by Corda and do not need operator attention. If they do, they will be logged by Corda itself in the main node log file.

It may be the case that you require to amend the log level of a particular subset of modules (e.g., if you’d like to take a closer look at Hibernate activity). So, for more bespoke logging configuration, the logging settings can be completely overridden with a [Log4j2](https://logging.apache.org/log4j/2.x) configuration file assigned to the `log4j.configurationFile` system property.

The node is using log4j2 asynchronous logging by default (configured via log4j2 properties file in its resources) to ensure that log message flushing is not slowing down the actual processing. If you need to switch to synchronous logging (e.g. for debugging/testing purposes), you can override this behaviour by adding `-DLog4jContextSelector=org.apache.logging.log4j.core.selector.ClassLoaderContextSelector` to the node’s command line or to the `jvmArgs` section of the node configuration.


### Example

Create a file `sql.xml` in the current working directory. Add the following text:

```xml
<?xml version="1.0" encoding="UTF-8"?>
    <Configuration status="WARN">
        <Appenders>
            <Console name="Console" target="SYSTEM_OUT">
                <PatternLayout pattern="%d{HH:mm:ss.SSS} [%t] %-5level %logger{36} - %msg%n"/>
            </Console>
        </Appenders>
        <Loggers>
            <Logger name="org.hibernate" level="debug" additivity="false">
                <AppenderRef ref="Console"/>
            </Logger>
            <Root level="error">
                <AppenderRef ref="Console"/>
            </Root>
        </Loggers>
    </Configuration>
```

Note the addition of a logger named `org.hibernate` that has set this particular logger level to `debug`.

Now start the node as usual but with the additional parameter `log4j.configurationFile` set to the filename as above, for example:

`java <Your existing startup options here> -Dlog4j.configurationFile=sql.xml -jar corda.jar`

To determine the name of the logger, for Corda objects, use the fully qualified name (e.g., to look at node output in more detail, use `net.corda.node.internal.Node` although be aware that as we have marked this class `internal` we reserve the right to move and rename it as it’s not part of the public API as yet). For other libraries, refer to their logging name construction. If you can’t find what you need to refer to, use the `--logging-level` option as above and then determine the logging module name from the console output.


## SSH access

Node can be configured to run SSH server.


## Database access

When running a node backed with a H2 database, the node can be configured to expose the database over a socket
(see [database access when running H2](../../node-database-access-h2.html)).

Note that in a production set up, it is highly recommended to use an enterprise grade database, and access to the
database should be via the usual database tools mechanisms, including access control and restrictions.


## Monitoring your node

This section covers monitoring performance and health of a node in Corda Enterprise with Jolokia and Graphite. General best practices for monitoring (e.g. setting up TCP checks for the ports the node communicates on, database health checks etc.) are not covered here but should be followed.


### Monitoring via Jolokia

Like most Java servers, the node can be configured to export various useful metrics and management operations via the industry-standard
[JMX infrastructure](https://en.wikipedia.org/wiki/Java_Management_Extensions). JMX is a standard API
for registering *MBeans* … objects whose properties and methods are intended for server management. As Java
serialization in the node has been restricted for security reasons, the metrics can only be exported via a Jolokia agent.

[Jolokia](https://jolokia.org/) allows you to access the raw data and operations without connecting to the JMX port
directly. Nodes can be configured to export the data over HTTP on the `/jolokia` HTTP endpoint, Jolokia defines the JSON and REST
formats for accessing MBeans, and provides client libraries to work with that protocol as well.

Here are a few ways to build dashboards and extract monitoring data for a node:


* [Hawtio](http://hawt.io) is a web based console that connects directly to JVM’s that have been instrumented with a
jolokia agent. This tool provides a nice JMX dashboard very similar to the traditional JVisualVM / JConsole MBbeans original.
* [JMX2Graphite](https://github.com/logzio/jmx2graphite) is a tool that can be pointed to /monitoring/json and will
scrape the statistics found there, then insert them into the Graphite monitoring tool on a regular basis. It runs
in Docker and can be started with a single command.
* [JMXTrans](https://github.com/jmxtrans/jmxtrans) is another tool for Graphite, this time, it’s got its own agent
(JVM plugin) which reads a custom config file and exports only the named data. It’s more configurable than
JMX2Graphite and doesn’t require a separate process, as the JVM will write directly to Graphite.
* Cloud metrics services like New Relic also understand JMX, typically, by providing their own agent that uploads the
data to their service on a regular schedule.
* [Telegraf](https://github.com/influxdata/telegraf) is a tool to collect, process, aggregate, and write metrics.
It can bridge any data input to any output using their plugin system, for example, Telegraf can
be configured to collect data from Jolokia and write to DataDog web api.

In order to ensure that a Jolokia agent is instrumented with the JVM run-time, you can choose one of these options:


* Specify the Node configuration parameter `jmxMonitoringHttpPort` which will attempt to load the Jolokia driver.
* Start the node with `java -Dcapsule.jvm.args="-javaagent:path/to/jolokia-jvm-{VERSION}-agent.jar=port=7777,host=localhost" -jar corda.jar` where `path/to/jolokia-jvm-{VERSION}-agent.jar` is the path to the driver, and `{VERSION}` is the version required by Corda, currently 1.6.1.

The following JMX statistics are exported:


* Corda specific metrics: see [Node metrics](../../node-metrics.md) for a list.
* Apache Artemis metrics: queue information for P2P and RPC services.
* JVM statistics: classloading, garbage collection, memory, runtime, threading, operating system.


### Notes for production use

When using Jolokia monitoring in production, it is recommended to use a Jolokia agent that reads the metrics from the node
and pushes them to the metrics storage, rather than exposing a port on the production machine/process to the internet.

Also ensure to have restrictive Jolokia access policy in place for access to production nodes. The Jolokia access is controlled
via a file called `jolokia-access.xml`.
Several Jolokia policy based security configuration files (`jolokia-access.xml`) are available for dev, test, and prod
environments under `/config/<env>`.


### Notes for development use

When running in dev mode, Hibernate statistics are also available via the Jolkia interface. These are disabled otherwise
due to expensive run-time costs. They can be turned on and off explicitly regardless of dev mode via the
`exportHibernateJMXStatistics` flag on the [database configuration](../setup/corda-configuration-file.md#database-properties-ref).

When starting Corda nodes using Cordformation runner (see [running nodes locally](../deploy/running-a-node.html)), you should see a startup message similar to the following:
**Jolokia: Agent started with URL http://127.0.0.1:7005/jolokia/**

When starting Corda nodes using the ‘driver DSL’, you should see a startup message in the logs similar to the following:
**Starting out-of-process Node USA Bank Corp, debug port is not enabled, jolokia monitoring port is 7005 {}**

The following diagram illustrates Corda flow metrics visualized using hawtio:

{{< figure alt="hawtio jmx" zoom="/en/images/hawtio-jmx.png" >}}

### Monitoring via Graphite

Corda nodes alternatively support publishing metrics collected via the Codahale metrics library directly to a graphite
server. This needs to be configured in the node configuration file:

```kotlin
graphiteOptions = {
  prefix = "<node specific prefix>"
  server = <host name of the graphite server>
  port = <write port on the graphite server>
  sampleIntervalSeconds = 60
}
```

The prefix should clearly indicate the node where the metrics are coming from, as this will be the top level discrimator
in the graphite metric hierarchy.
The graphite server must be running with python pickle transport enabled. Please refer to the documentation on
[https://graphiteapp.org](https://graphiteapp.org) on how to install and run a graphite server.

### Monitoring scenarios

See [Monitoring scenarios](monitoring-scenarios.md) for a description of some common node monitoring scenarios when using [node metrics](../../node-metrics.md).

## Memory usage and tuning

All garbage collected programs can run faster if you give them more memory, as they need to collect less
frequently. As a default JVM will happily consume all the memory on your system if you let it, Corda is
configured with a 512mb Java heap by default. When other overheads are added, this yields
a total memory usage of about 800mb for a node (the overheads come from things like compiled code, metadata,
off-heap buffers, thread stacks, etc).

If you want to make your node go faster and profiling suggests excessive GC overhead is the cause, or if your
node is running out of memory, you can give it more by running the node like this:

`java -Dcapsule.jvm.args="-Xmx1024m" -jar corda.jar`

The example command above would give a 1 gigabyte Java heap.

{{< note >}}
Unfortunately the JVM does not let you limit the total memory usage of Java program, just the heap size.
{{< /note >}}

## Hiding sensitive data

A frequent requirement is that configuration files must not expose passwords to unauthorised readers. By leveraging environment variables, it is possible to hide passwords and other similar fields.

Take a simple node config that wishes to protect the node cryptographic stores:

```kotlin
myLegalName = "O=PasswordProtectedNode,OU=corda,L=London,C=GB"
keyStorePassword = ${KEY_PASS}
trustStorePassword = ${TRUST_PASS}
p2pAddress = "localhost:12345"
devMode = false
networkServices {
    doormanURL = "https://cz.example.com"
    networkMapURL = "https://cz.example.com"
}
```

By delegating to a password store, and using *command substitution* it is possible to ensure that sensitive passwords never appear in plain text.
The below examples are of loading Corda with the KEY_PASS and TRUST_PASS variables read from a program named `corporatePasswordStore`.


### Bash

```shell
KEY_PASS=$(corporatePasswordStore --cordaKeyStorePassword) TRUST_PASS=$(corporatePasswordStore --cordaTrustStorePassword) java -jar corda.jar
```


{{< warning >}}
If this approach is taken, the passwords will appear in the shell history.

{{< /warning >}}



### Windows PowerShell

```shell
$env:KEY_PASS=$(corporatePasswordStore --cordaKeyStorePassword); $env:TRUST_PASS=$(corporatePasswordStore --cordaTrustStorePassword); java -jar corda.jar
```

For launching on Windows without PowerShell, it is not possible to perform command substitution, and so the variables must be specified manually, for example:

```shell
SET KEY_PASS=mypassword & SET TRUST_PASS=mypassword & java -jar corda.jar
```


{{< warning >}}
If this approach is taken, the passwords will appear in the windows command prompt history.

{{< /warning >}}



## Obfuscating sensitive data

Instead of hiding sensitive data using environment variables, another option is to use configuration obfuscation. Corda ships with a [configuration obfuscator](../../tools-config-obfuscator.md/) which allows the user to censor string properties in the configuration file. The config would look something like this:

```kotlin
keyStorePassword = "<{Kwby0G9c/+jxJM+c7Vaiow==:pdy+UaakdFSmmh8WWuBOoQ==}>"
trustStorePassword = "<{Kwby0G9c/+jxJM+c7Vaiow==:pdy+UaakdFSmmh8WWuBOoQ==}>"
p2pAddress = "localhost:12345"
devMode = false
```

The values for `keyStorePassword` and `trustStorePassword` in the above example are encrypted, using a key that is tied to the hosting machine’s primary hardware address. The implications of this is that:



* The configuration file is rendered unusable on other machines without manually decrypting obfuscated fields beforehand (since the hardware address would be different).
* Sensitive data is unreadable without additional processing.
* It becomes harder for adversaries to trawl for passwords and sensitive data on disk.



{{< warning >}}
This method does not offer full protection. We recommend using further obfuscation methods for sensitive data.

{{< /warning >}}
