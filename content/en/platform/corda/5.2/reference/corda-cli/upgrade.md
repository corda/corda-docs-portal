---
description: "List of upgrade commands for the Corda CLI. You can use these commands to migrate data during the upgrade."
date: '2024-05-15'
menu:
  corda52:
    identifier: corda52-cordacli-upgrade
    weight: 5500
    parent: corda52-cli-reference
title: "upgrade"
---
# upgrade

This section lists the {{< tooltip >}}Corda CLI{{< /tooltip >}} `upgrade` sub-commands and arguments. Use these commands to migrate data as part of the platform upgrade process from version 5.2 to 5.2.1.

<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}
</style>

| Argument           | Description                                                                             |
|--------------------|-----------------------------------------------------------------------------------------|
| migrate-data-5-2-1 | Reads records from Kafka and generates SQL for persisting them to the cluster database. |

## migrate-data-5-2-1

| Argument                  | Description                                                                                                          |
|---------------------------|----------------------------------------------------------------------------------------------------------------------|
| -b, \-\-bootstrap-server  | The address of the bootstrap server.                                                                                 |
| \-\-kafka-config          | The path to the Kafka configuration file.                                                                            |
| -n, \-\-name-prefix       | The name prefix for topics.                                                                                          |
| \-\-timeout               | Timeout, in milliseconds, to read from Kafka. If not specified, defaults to 3000.                                    |
| -l, \-\-location          | The directory to write all files to.                                                                                 |
| -t, \-\-target            | The target address of the REST endpoint, for example, `https://host:port`.                                           |
| -u, \-\-user              | The REST user name.                                                                                                  |
| -p, \-\-password          | The REST password.                                                                                                   |
| -pv, \-\-protocol-version | Minimum protocol version. If not specified, defaults to 1.                                                           |
| -y, \-\-yield             | The duration, in seconds, before the REST connection becomes available. If not specified, defaults to 10 seconds.    |
| -k, \-\-insecure          | Allows insecure server connections with SSL. If not specified, defaults to `false`.                                  |


{{< tabs name="">}}
{{% tab name="Bash" %}}
```sh
corda-cli.sh upgrade migrate-data-5-2-1 -b <BOOTSTRAP-SERVERS> --kafka-config <CLIENT-PROPERTIES-FILE> -t <REST-URL> -u <USER> -p <PASSWORD> --insecure --timeout <TIMEOUT>
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
corda-cli.cmd upgrade migrate-data-5-2-1 -b <BOOTSTRAP-SERVERS> --kafka-config <CLIENT-PROPERTIES-FILE> -t <REST-URL> -u <USER> -p <PASSWORD> --insecure --timeout <TIMEOUT>
```
{{% /tab %}}
{{< /tabs >}}
