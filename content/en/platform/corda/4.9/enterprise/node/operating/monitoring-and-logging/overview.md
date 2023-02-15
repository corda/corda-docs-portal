---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-9:
    identifier: corda-enterprise-4-9-monitoring-logging
    parent: corda-enterprise-4-9-corda-nodes-operating
tags:
- monitoring
- logging
title: Node monitoring and logging
weight: 5
---

Corda nodes use [log4j2 asynchronous logging](https://logging.apache.org/log4j/2.x/manual/async.html) to ensure that log message flushing is not slowing down node processing. Log4j2 is configured via a log4j2 properties file in the node resources. You can get the configuration file from the `config/dev` folder in [Corda Community Edition repository](https://github.com/corda/corda). By default, the node log files are stored to the `logs` subdirectory of the working node directory. You can print logs to the console using the `--log-to-console` command line flag when starting the node.

Corda uses the Hibernate JPA provider. Some `WARN` and `ERROR` level messages from Hibernate do not require operator attention because Corda handles them internally. If Corda handles the message internally it will be logged in a separate diagnostic file in the `logs` subdirectory. If the messages require operator attention, they will be recorded in the main node log file.


### Set the logging level

There are seven valid logging levels: `TRACE`, `DEBUG`, `INFO`, `WARN`, `ERROR`, `FATAL`, and `OFF`. By default, Corda uses the `INFO` logging level.

The logging level can be set in two ways:

- Set the logging level for all modules.
- Set the logging level for specific modules.

See the [Log4j2](https://logging.apache.org/log4j/2.x) documentation for more information.

#### Set the logging level for all modules

To adjust the logging level for all modules:

1. Safely shut down the node.
2. Restart the node specifying the `--logging-level` command line option:

    `java <Your existing startup options here> --logging-level <new level here> -jar corda.jar`

You have set a new logging level for all modules.

#### Set the logging level for specific modules

You can fine-tune the recorded logs by specifying a logging level for specific modules.

To set the logging level for specific modules:

1. Safely shut down the node.
2. In the node working directory, create a file named `sql.xml`. This will be the new configuration source for [Log4j2](https://logging.apache.org/log4j/2.x).
3. In `sql.xml` add the following code:

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
        <Configuration status="WARN" shutdownHook="disable">
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

    In this instance, the `org.hibernate` logger has been set to the `DEBUG` log level.
4. Add a `<Logger>` entry for each module for which you intend to set a logging level. To determine the name of the logger, for Corda objects, use the fully qualified name e.g. `net.corda.node.internal.Node`. For other libraries, refer to their logging name construction. If you can’t find what you need to refer to, use the `--logging-level` option and then determine the logging module name from the console output.
5. Save the `sql.xml` file.
6. Restart the node:
    `java <Your existing startup options here> -Dlog4j.configurationFile=sql.xml -jar corda.jar`

### Switching to synchronous logging

Synchronous logging provides poorer node performance, but may be useful for development or debugging. To switch to synchronous logging:

1. Safely shut down the node.
2. Open the `node.conf` configuration file.
3. In the `jvmArgs` section, add `-DLog4jContextSelector=org.apache.logging.log4j.core.selector.ClassLoaderContextSelector`.
4. Save the `node.conf` file and restart the node.

{{< warning >}}
When using synchronous logging with `RollingRandomAccessFile` appenders in the configuration file, make sure that they DO NOT have `immediateFlush=false` setting.
{{< /warning >}}

### Detailed logging

Detailed logging around interactions with the node database or HSM can be enabled by setting the `logging-level` to `TRACE`. Detailed logs will be saved to a separate file with the `details` prefix. Detailed logs are structured to allow for log processing by third-party tools. Mapped Diagnostic Context is also enabled for it. The types are supported:

| Fields | Actions |
|--------|---------|
| `action`, `id`, `uploader` | `loading`, `loaded`, `store_start`, `store_created`, `store_updated`, `query_start`, `query_end`, `query_version_start`, `query_version_end` |
| `action`, `type`, `criteria`, `pagination`, `sorting` | `query_start`, `query_end` |
| `action`, `alias`, `scheme`, `found`, `algorithm`, `id`, `path`, `authState` | `generate_key_pair_start`, `generate_key_pair_end`, `key_lookup_start`, `key_lookup_end`, `key_get_start`, `key_get_end`, `signing_start`, `signing_end`, `get_signer`, `create_client`, `key_import`, `authenticate_start`, `authenticate_end`, `keystore_load_start`, `keystore_load_end` |
| `action`, `flowId`, `flow`, `state`, `flowState`, `subFlows`, `subFlowStack`, `exception`, `reason`, `error`, `suspends`, `session`, `errorState`, `numberOfSuspends` | `start`, `add_and_start`, `create_from_checkpoint`, `retry_safe_point`, `propagate_error`, `remove` |
| `action`, `flowId`, `size`, `platformVersion`, `id`, `to`, `from` | `send`, `receive` |
| `action`, `party` | `save_start`, `save_end` |
| `action`, `className`, `status` | `save_start`, `save_end` |
| `action`, `refs` | `loading`, `loaded` |
| `action`, `flowId`, `id`, `appName`, `message`, `flowVersion`, `recipient` | `send_initial_message`, `send_existing_message` |
| `action`, `flowId` | `rollback` |


See below for some example detailed logs:

```none
[TRACE] 2019-07-18T15:39:29,741Z Flow(action=start;logic=net.corda.finance.internal.CashConfigDataFlow@2000e5f3;flowId=5eae65e6-a2c9-4eb8-a984-2b7f6877d2ee) {actor_id=user1, actor_owning_identity=O=PartyA, L=London, C=GB, actor_store_id=NODE_CONFIG, invocation_id=9ea253f7-72f9-40cc-a85e-727d0f3bbb42, invocation_timestamp=2019-07-18T15:39:29.718Z, origin=user1, session_id=881e4323-4353-43c3-b2e7-2146ffc32095, session_timestamp=2019-07-18T15:39:28.663Z}
[TRACE] 2019-07-18T15:39:29,828Z Flow(action=add_and_start;flowId=5eae65e6-a2c9-4eb8-a984-2b7f6877d2ee;flowState=Unstarted(flowStart=Explicit, frozenFlowLogic=4596BC25EB7986B7C0AB31F70A1DCC6628955983D5EB489B6C73AE6B6A849970);session={};subFlowStack=[Inlined(flowClass=class net.corda.finance.internal.CashConfigDataFlow, subFlowVersion=CorDappFlow(platformVersion=5, corDappName=corda-finance-workflows-5.0-SNAPSHOT, corDappHash=AD8EC11D5FF082D000245CEFB8F236EF231AAA5CC2E023DBED72B72A750B60D2), isEnabledTimedFlow=false)];errorState=Clean;numberOfSuspends=0) {actor_id=user1, actor_owning_identity=O=PartyA, L=London, C=GB, actor_store_id=NODE_CONFIG, invocation_id=9ea253f7-72f9-40cc-a85e-727d0f3bbb42, invocation_timestamp=2019-07-18T15:39:29.718Z, origin=user1, session_id=881e4323-4353-43c3-b2e7-2146ffc32095, session_timestamp=2019-07-18T15:39:28.663Z}
[TRACE] 2019-07-18T15:39:29,966Z Flow(action=remove;flowId=5eae65e6-a2c9-4eb8-a984-2b7f6877d2ee;reason=OrderlyFinish(flowReturnValue=CashConfiguration(issuableCurrencies=[], supportedCurrencies=[USD, GBP, CHF, EUR]))) {actor_id=user1, actor_owning_identity=O=PartyA, L=London, C=GB, actor_store_id=NODE_CONFIG, fiber-id=10000001, flow-id=5eae65e6-a2c9-4eb8-a984-2b7f6877d2ee, invocation_id=9ea253f7-72f9-40cc-a85e-727d0f3bbb42, invocation_timestamp=2019-07-18T15:39:29.718Z, origin=user1, session_id=881e4323-4353-43c3-b2e7-2146ffc32095, session_timestamp=2019-07-18T15:39:28.663Z, thread-id=219}
[TRACE] 2019-07-18T15:39:49,606Z Message(action=receive;size=2232;id=N-D-1338028259437713213--5426630988224494415-0-0;platformVersion=5;from=O=Notary, L=New York, C=US) {}
[TRACE] 2019-07-18T15:39:49,729Z Party(action=save;party=Anonymous(DL55FjJhasWWssQAFimPrwCMpzn5BHXX4CFS7yDuBPs3c1)) {actor_id=user1, actor_owning_identity=O=PartyA, L=London, C=GB, actor_store_id=NODE_CONFIG, fiber-id=10000002, flow-id=9fa62b8d-7229-478a-9a6c-0e0b8e9e3afb, invocation_id=7240b531-512a-4042-b5a9-45aa3ca5e62b, invocation_timestamp=2019-07-18T15:39:46.084Z, origin=user1, session_id=881e4323-4353-43c3-b2e7-2146ffc32095, session_timestamp=2019-07-18T15:39:28.663Z, thread-id=279, tx_id=C4EF4FD371B5E5839901A28DADF7BECFB745BFE274EA1EE5C8DBEEDC3BA5BA23}
```

## Node monitoring

This section covers some scenarios for monitoring node performance. General best practices like setting up TCP checks for the ports the node communicates on, or running database health checks are not covered here.

You can monitor node metrics using Jolokia or Graphite.

### Monitor your node using Jolokia

Corda nodes can be configured to export metrics and management operations via the industry-standard [JMX infrastructure](https://en.wikipedia.org/wiki/Java_Management_Extensions). JMX is a standard API for registering *MBeans*. Mbeans are objects with properties and methods intended for server management. As Java serialization in the node has been restricted for security reasons the metrics can only be exported using a Jolokia agent.

To monitor your node using Jolokia you must:

1. Acquire the Jolokia 1.6.1 agent `.jar` file.
2. Save the Jolokia `.jar` file in the `drivers` directory of the node. The driver name must be `jolokia-jvm-1.6.1-agent.jar`.
3. Either:
    a. Specify the `jmxMonitoringHttpPort` parameter in the node configuration file. The `jmxMonitoringHttpPort` parameter loads the Jolokia driver from the `drivers` directory.
    b. Start the node with `java -Dcapsule.jvm.args="-javaagent:drivers/jolokia-jvm-1.6.1-agent.jar=port=7777,host=localhost" -jar corda.jar`.

The following JMX statistics are exported:

* [Corda specific metrics](../../../../../../../../en/platform/corda/4.9/enterprise/node/operating/monitoring-and-logging/node-metrics.md).
* Apache Artemis queue information for P2P and RPC services.
* JVM classloading, garbage collection, memory, runtime, threading, and operating system metrics.

[Jolokia](https://jolokia.org/) allows you to access the raw data and operations without connecting to the JMX port directly. Nodes can be configured to export the data over HTTP on the `/jolokia` HTTP endpoint. Jolokia defines the JSON and REST formats for accessing MBeans, and provides client libraries to work with that protocol.

You can display monitoring data using third-party dashboards:

* [Hawtio](http://hawt.io)
* [JMX2Graphite](https://github.com/logzio/jmx2graphite)
* [JMXTrans](https://github.com/jmxtrans/jmxtrans)
* [Telegraf](https://github.com/influxdata/telegraf)


#### Monitor production systems with Jolokia

If you are using Jolokia monitoring on a production system, you should use a Jolokia agent that pushes metrics to metrics storage rather than exposing a port on the production machine.

You should set a restrictive access policy for production nodes. Jolokia access is set in a file called `jolokia-access.xml`. Several Jolokia policy based security configuration files (`jolokia-access.xml`) are available for different environments under `/config/<env>`.

To add a security policy use `java -Dcapsule.jvm.args=-javaagent:./drivers/jolokia-jvm-1.6.0-agent.jar,policyLocation=file:./config-path/jolokia-access.xml -jar corda.jar` when you start each node.


#### Monitor development systems with Jolokia

If you Corda instance is set to dev mode you can access Hibernate statistics using the Jolokia interface. Hibernate statistics are disabled outside of dev mode due to expensive runtime costs. Hibernate statistics reporting can be enabled or disabled regardless of dev mode using the `exportHibernateJMXStatistics` flag on the [database configuration](../../../../../../../../en/platform/corda/4.9/enterprise/node/setup/corda-configuration-fields.html#database).

### Monitoring your node using Graphite

Corda supports publishing metrics directly to a Graphite server if those metrics were collected using the Codahale metrics library. The Graphite server must be running with python pickle transport enabled. Please refer to the documentation on [https://graphiteapp.org](https://graphiteapp.org) on how to install and run a Graphite server.

To publish metrics to a Graphite server:

1. Open your node configuration file.
2. Add the following section:

    ```kotlin
    graphiteOptions = {
      prefix = "<node specific prefix>"
      server = <host name of the Graphite server>
      port = <pickle receiver port on the Graphite server>
    }
    ```

    The node specific prefix must clearly indicate which node is the source of the metrics.
3. Save the node configuration file.
4. Start or restart your node.


## Related content

* [Node metrics](../../../../../../../../en/platform/corda/4.9/enterprise/node/operating/monitoring-and-logging/node-metrics.md)
* [Monitoring scenarios](../../../../../../../../en/platform/corda/4.9/enterprise/node/operating/monitoring-and-logging/monitoring-scenarios.md)
