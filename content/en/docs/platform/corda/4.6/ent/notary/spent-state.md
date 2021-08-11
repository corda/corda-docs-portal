---
date: '2020-06-01T12:00:00Z'
menu:
  corda-enterprise-4-6:
    parent: corda-enterprise-4-6-corda-nodes-notary-operate
tags:
- scaling
- notary
- cluster
- tool
- audit
title: Spent state audit tool
weight: 9.5
---

# Spent State Audit Tool

A double-spend occurs when a state that the notary has marked as spent is used as input to a new transaction. Notaries
will reject transactions that attempt double-spends. The Spent State Audit Tool can be used to retrieve the history of states
involved in double-spend attempts.

{{< note >}}
The spend state audit tool is only compatible with a [high-availability implementation](ha-notary-service-overview.md) of the JPA notary.
{{< /note >}}

## Using the Spent State Audit Tool

The Spent State Audit Tool is distributed with Corda Enterprise as a `.jar` file that must be run from the command line using the following command:

```
java -jar corda-tools-notary-utilities-4.6.jar spent-state-audit <options> <state_reference>
```

The tool connects to the notary via RPC, and so must specify a valid RPC username and password, using the `-u` and `-p` options, unless an RPC username and password are specified in the notary worker's `node.conf` configuration file.

When running the tool, you must specify a state reference. The tool will return all requests for notarisation for that state reference including timestamps, transaction IDs, transaction result, requesting party, and notary worker.

### Command-line options

You can use the following parameters and options when running the Spent State Audit Tool:

**Parameters:**

* `<state_reference>`: A state reference in the form `txId:outputIndex`.

**Options:**

* `-v`, `--verbose`, `--log-to-console`: If set, prints logging to the console as well as to a file. Not set by default.
* `--logging-level=LOGGING_LEVEL`: Use this option to enable logging at this level and higher. Possible values: `ERROR`, `WARN`, `INFO` (default), `DEBUG`, `TRACE`.
* `-b`, `--base-directory=FOLDER`: The node working directory. Defaults to the current directory.
* `-c`, `--config-file=FILE`: The path to the `node.conf` configuration file. Defaults to `node.conf` in the current directory.
* `-u`, `--user-name=USER_NAME`: RPC username. Defaults to the first RPC username defined in the node configuration file.
* `-p`, `--password=PASSWORD`: RPC password. Defaults to the first RPC password defined in the node configuration file.
* `--max-results=LIMIT`: The maximum number of spend events to return, beginning with the most recent. If `--format` is not set, the user is prompted to get the next batch. Setting this value too high may result in the query timing out. The default value is 10.
* `--only-successful`: If set, the tool returns only successful spend events. By default, this option is not set.
* `--timezone=ZONE_ID`: Sets the time zone the returned events are returned in. If a `--start-time` or `--end-time` are set, this option also sets the time zone for those options. This option must be a valid Java `ZoneId` or `LOCAL`. Setting this option to `LOCAL` uses the server's timezone. The default value is `LOCAL`.
* `--start-time=LOCAL_DT`: Specifies a start time to search for results from, inclusively. Must be a valid Java `LocalDateTime`, the value of which is assumed to be in the `--timezone` zone.
* `--end-time=LOCAL_DT`: Specifies a time to search for results until, inclusively. Must be a valid Java `LocalDateTime`, the value of which is assumed to be in the `--timezone` zone.
* `--format=OUTPUT_FORMAT`: Defines the output format of the returned events. The only supported value is `CSV`. By default, this option is not set the output is printed in human readable text.
* `-h`, `--help`: Displays the help message.
* `-V`, `--version`: Displays version information and exit.
