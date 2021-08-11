---
aliases:
- /head/error-codes.html
- /HEAD/error-codes.html
- /error-codes.html
date: '2020-05-05T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-error-codes
    parent: corda-os-4-6-clientrpc
    weight: 4000
tags:
- error
- codes
title: Node error codes
---

# Overview of node error codes

A Corda node can report a number of error codes. The table below provides a non-exhaustive list of such error codes.

For each error code in the tables, there is additional information about its aliases, the reason why that error occurred, and instructions on what actions
you can take to address the problem reported by the error.

{{< note >}}

It is possible that a node fails for reasons not listed on this page as the set of error codes in the platform is not exhaustive.

{{< /note >}}

Versions of Corda prior to 4.5 generated error codes using a different mechanism. In cases where an old error code is
known to map to a new error code, the old code will appear in the `Aliases` column of the table below.

Table contents:
 - **Error code**: the error code as reported by the Corda node.
 - **Aliases**: other codes this error may have been known as under previous reporting systems.
 - **Description**: a description of what has gone wrong.
 - **Actions to fix**: what actions to take in order to address the problem.

To make use of this table, search the console or node logs for lines indicating an error has occurred. Errors that have
corresponding codes will contain a message with the error code and a link pointing to this page.

## Error code details

{{< table >}}

| Error Code | Aliases | Description | Actions to fix |
| :---------- | :------- | :----------- | :-------------- |
| `cordapp-duplicate-cordapps-installed` | `iw8d4e` | A CorDapp was installed multiple times on the same node. This is not permitted and causes the node to shut down. | Investigate the logs to determine the CorDapps with duplicate content, and remove one of them from the `cordapps` directory. It does not matter which of the CorDapps you choose to remove as their content is identical. |
| `cordapp-invalid-version-identifier` | `1nskd37` | A version attribute with an invalid value was specified in the manifest of the CorDapp `.jar` file. The version attribute value must be a whole number that is greater than or equal to 1. | Investigate the logs to find the invalid version attribute, and change its value to a valid one (a whole number greater than or equal to 1). |
| `cordapp-missing-version-attribute` | `1nskd37` | A required version attribute was not specified in the manifest of the CorDapp `.jar` file. | Investigate the logs to find out which version attribute was not specified, and add that version attribute to the CorDapp manifest. |
| `cordapp-multiple-cordapps-for-flow` |  | Multiple CorDapp `.jar` files on the classpath define the same flow class. As a result, the platform will not know which version of the flow to start when the flow is invoked. | Investigate the logs to find out which CorDapp `.jar` files define the same flow classes. The developers of these apps will need to resolve the clash. |
| `database-could-not-connect` |  | The node failed to connect to the database on node startup and thus prevented the node from starting correctly. | This happened either because the database connection was misconfigured or because the database was unreachable. Check that the JDBC URL is configured correctly in your `node.conf` file. If this is correctly configured, then check your database connection. |
| `database-failed-startup` |  | The datasource could not be created for unknown reasons. | The logs in the logs directory should contain more information on what went wrong. |
| `database-missing-driver` |  | The node could not find the driver in the `drivers` directory. | Ensure that the `drivers` directory contains the correct database driver. The driver must contain the driver class as specified in `node.conf`.  |
| `database-password-required-for-h2` |  | The node is trying to access an H2 server that requires a password, which is missing. | Add the required password to the `datasource.password` configuration section in the `node.conf` file. |

{{< /table >}}
