---
date: '2020-06-18T12:00:00Z'
menu:
  corda-enterprise-4-6:
    identifier: corda-enterprise-4-6-ops-monitoring-logging
    name: "Monitoring and logging"
    parent: corda-enterprise-4-6-operations-guide
tags:
- operations
- deployment
- planning
title: Monitoring and maintaining a node
weight: 30
---
# Monitoring and maintaining the health of your node

When you are responsible for a node in a Corda Enterprise environment, you have a number of tools available to help you maintain the health and efficiency of your node. These tools range from general metrics monitoring using tools such as Jolokia or Graphite to Corda-built tools that allow you to run health-checks, and even check that your node is in sync with the rest of your ledger and help you recover data from a disaster scenario.

In this operational guide, you will find introductions to the main tools available to you for logging, monitoring and maximising the performance of your Corda Node.

You can find answers to questions like:

* What Java Management Extension (JMX) infrastructure do I follow?
* How do I raise a support issue?
* How do I raise a bug?
* What is important and unimportant in the logs?

Monitoring and logging topics:

* [Basics of logging on your node](#logging---the-basics).
* [Basics of monitoring your node](#monitoring---the-basics).
* [Node metrics](metrics-monitoring-scenarios).
* [Node monitoring scenarios](metrics-monitoring-scenarios).
* [Troubleshooting Corda Enterprise Network Manager (CENM) services on your node](monitoring-trouble-shooting).
* [The Corda Enterprise Health Survey tool](monitoring-trouble-shooting#corda-health-survey-tool).
* [Using Ledger Sync to check the status of data on your node and the rest of the ledger](monitoring-trouble-shooting#ledger-sync).

## Logging - the basics

Your Corda Enterprise node automatically keeps a log of how it is performing. You can retrieve logs kept by the node using simple command line instructions.

By default the node log files are stored to the logs subdirectory of the working directory and are rotated from time to time. You can have logging printed to the console as well by passing the --log-to-console command line flag. The default logging level is INFO which can be adjusted by the --logging-level command line argument. This configuration option will affect all modules. Hibernate (the JPA provider used by Corda) specific log messages of level WARN and above will be logged to the diagnostic log file, which is stored in the same location as other log files (logs subdirectory by default). This is because Hibernate may log messages at WARN and ERROR that are handled internally by Corda and do not need operator attention. If they do, they will be logged by Corda itself in the main node log file.

It may be the case that you require to amend the log level of a particular subset of modules (e.g., if you’d like to take a closer look at hibernate activity). So, for more bespoke logging configuration, the logger settings can be completely overridden with a Log4j2 configuration file assigned to the log4j.configurationFile system property.

To understand the information in the logs, which data is important, and what can be safely kept as a low priority, you can read the [logging documentation](../../node/operating/node-administration).

## Monitoring - the basics

You can monitor the health and performance of your node [using tools such as Jolokia and Graphite](../../node/operating/monitoring-logging#monitoring-your-node). Whenever using these tools, you should follow best-practice steps such as setting up TCP checks for the ports the node communicates on, database health checks etc.

### Monitoring via Jolokia

Like most Java servers, the node can be configured to export various useful metrics and management operations via the industry-standard
[JMX infrastructure](https://en.wikipedia.org/wiki/Java_Management_Extensions). JMX is a standard API
for registering *MBeans* … objects whose properties and methods are intended for server management. As Java
serialization in the node has been restricted for security reasons, the metrics can only be exported via a Jolokia agent.

[Jolokia](https://jolokia.org/) allows you to access the raw data and operations without connecting to the JMX port
directly. Nodes can be configured to export the data over HTTP on the `/jolokia` HTTP endpoint, Jolokia defines the JSON and REST
formats for accessing MBeans, and provides client libraries to work with that protocol as well.

When using Jolokia monitoring in production, it is recommended to use a Jolokia agent that reads the metrics from the node
and pushes them to the metrics storage, rather than exposing a port on the production machine/process to the internet.

Also ensure to have restrictive Jolokia access policy in place for access to production nodes. The Jolokia access is controlled
via a file called `jolokia-access.xml`.
Several Jolokia policy based security configuration files (`jolokia-access.xml`) are available for dev, test, and prod
environments under `/config/<env>`.

### Monitoring via graphite

Corda nodes alternatively support publishing metrics collected via the Codahale metrics library directly to a graphite
server. This needs to be configured in the node configuration file:

```kotlin
graphiteOptions = {
  prefix = "<node specific prefix>"
  server = <host name of the graphite server>
  port = <write port on the graphite server>
}
```

The prefix should clearly indicate the node where the metrics are coming from, as this will be the top level discrimator
in the graphite metric hierarchy.
The graphite server must be running with python pickle transport enabled. Please refer to the documentation on
[https://graphiteapp.org](https://graphiteapp.org) on how to install and run a graphite server.
