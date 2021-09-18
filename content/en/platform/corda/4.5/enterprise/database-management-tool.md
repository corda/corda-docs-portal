---
date: '2020-04-07T12:00:00Z'
menu:
  corda-enterprise-4-5:
    parent: corda-enterprise-4-5-corda-nodes-operating-db
tags:
- tool
- database
title: Database Management Tool
weight: 60
---

# Database Management Tool

{{< warning >}}
Corda Enterprise 4.5.4 fixes a security vulnerability in the JPA notary. Before upgrading to Corda Enterprise 4.5.4 please read the guidance on [upgrading your notary service](notary/upgrading-the-ha-notary-service.md/).
{{< /warning >}}

The database management tool is distributed as a standalone JAR file named `tools-database-manager-${corda_version}.jar`.
It is intended to be used by Corda Enterprise node administrators who want more control over database changes made in production
environments.

The following sections document the available subcommands suitable for a node operator or database administrator.

{{< note >}}
The database management tool is for production databases only. H2 databases cannot be upgraded using the Database Management tool.
{{< /note >}}

## Executing a dry run of the SQL migration scripts

The `dry-run` subcommand can be used to output the database migration to the specified output file or to the console.
The output directory is the one specified by the `--base-directory` parameter.

Usage:

```shell
database-manager dry-run [-hvV] [--doorman-jar-path=<doormanJarPath>]
                         [--logging-level=<loggingLevel>] [--mode=<mode>]
                         -b=<baseDirectory> [-f=<configFile>] [<outputFile>]
```

The `outputFile` parameter can be optionally specified determine what file to output the generated SQL to, or use
`CONSOLE` to output to the console.

Additional options:

* `--base-directory`, `-b`: (Required) The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the config file. Defaults to `node.conf`.
* `--mode`: The operating mode. Possible values: NODE, DOORMAN, JPA_NOTARY. Default: NODE.
* `--doorman-jar-path=<doormanJarPath>`: The path to the doorman JAR.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.


## Executing SQL migration scripts

The `execute-migration` subcommand runs migration scripts on the node’s database.

Usage:

```shell
database-manager execute-migration [-hvV] [--doorman-jar-path=<doormanJarPath>]
                                   [--logging-level=<loggingLevel>]
                                   [--mode=<mode>] -b=<baseDirectory>
                                   [-f=<configFile>]
```


* `--base-directory`, `-b`: (Required) The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the config file. Defaults to `node.conf`.
* `--mode`: The operating mode. Possible values: NODE, DOORMAN, JPA_NOTARY. Default: NODE.
* `--doorman-jar-path=<doormanJarPath>`: The path to the doorman JAR.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.


## Releasing database locks

The `release-lock` subcommand forces the release of database locks. Sometimes, when a node or the database management
tool crashes while running migrations, Liquibase will not release the lock. This can happen during some long
database operations, or when an admin kills the process (this cannot happen during normal operation of a node,
only [during the migration process](http://www.liquibase.org/documentation/databasechangeloglock_table.html).

Usage:

```shell
database-manager release-lock [-hvV] [--doorman-jar-path=<doormanJarPath>]
                              [--logging-level=<loggingLevel>] [--mode=<mode>]
                              -b=<baseDirectory> [-f=<configFile>]
```

Additional options:

* `--base-directory`, `-b`: (Required) The node working directory where all the files are kept (default: `.`).
* `--config-file`, `-f`: The path to the config file. Defaults to `node.conf`.
* `--mode`: The operating mode. Possible values: NODE, DOORMAN, JPA_NOTARY. Default: NODE.
* `--doorman-jar-path=<doormanJarPath>`: The path to the doorman JAR.
* `--verbose`, `--log-to-console`, `-v`: If set, prints logging to the console as well as to a file.
* `--logging-level=<loggingLevel>`: Enable logging at this level and higher. Possible values: ERROR, WARN, INFO, DEBUG, TRACE. Default: INFO.
* `--help`, `-h`: Show this help message and exit.
* `--version`, `-V`: Print version information and exit.


## Database Manager shell extensions

The `install-shell-extensions` subcommand can be used to install the `database-manager` alias and auto completion for
bash and zsh. See [Shell extensions for CLI Applications]({{% ref "node/operating/cli-application-shell-extensions.md" %}}) for more info.

{{< note >}}
When running the database management tool, it is preferable to use absolute paths when specifying the “base-directory”.
{{< /note >}}

{{< warning >}}
It is good practice for node operators to back up the database before upgrading to a new version.
{{< /warning >}}


## Troubleshooting

Symptom: Problems acquiring the lock, with output like this:

```
Waiting for changelog lock….
Waiting for changelog lock….
Waiting for changelog lock….
Waiting for changelog lock….
Waiting for changelog lock….
Waiting for changelog lock….
Waiting for changelog lock….
Liquibase Update Failed: Could not acquire change log lock.  Currently locked by SomeComputer (192.168.15.X) since 2013-03-20 13:39
SEVERE 2013-03-20 16:59:liquibase: Could not acquire change log lock.  Currently locked by SomeComputer (192.168.15.X) since 2013-03-20 13:39
liquibase.exception.LockException: Could not acquire change log lock.  Currently locked by SomeComputer (192.168.15.X) since 2013-03-20 13:39

at liquibase.lockservice.LockService.waitForLock(LockService.java:81)
at liquibase.Liquibase.tag(Liquibase.java:507)
at liquibase.integration.commandline.Main.doMigration(Main.java:643)
at liquibase.integration.commandline.Main.main(Main.java:116)
```

Advice: See [this StackOverflow question](https://stackoverflow.com/questions/15528795/liquibase-lock-reasons).
Run the following command to force Liquibase to give up the lock:

```
java -jar tools-database-manager-4.0.jar --base-directory /path/to/node --release-lock
```
