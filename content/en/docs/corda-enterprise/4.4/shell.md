---
aliases:
- /releases/4.4/shell.html
- /docs/corda-enterprise/head/shell.html
- /docs/corda-enterprise/shell.html
date: '2020-01-08T09:59:25Z'
tags:
- shell
title: Embedded Shell
---


# Embedded Shell


The embedded shell allows an administrator to control and monitor the suite of CENM services being run (Network Map,
Identity Manager and Signing service). It is based on the [CRaSH](http://www.crashub.org/) shell and provides certain functions such as viewing
the current state of the network (via the Network Map shell), viewing the CSRs awaiting approval (via the Identity
Manager shell) or executing signing tasks (via the Signing Service shell).



## Shell Configuration

The optional `shell` configuration block can be added to the given CENM service configuration file to enable the
embedded shell. There are two modes that the shell can run in:


### SSH Mode

The most versatile method to access the shell is via SSH. This can be configured by specifying the port, user and
password within the `shell` configuration block:

```guess
...
shell {
    sshdPort = <PORT>
    user = <USERNAME>
    password = <PASSWORD>
}
...
```


### Local Mode

The service can be configured to boot straight into the local shell upon startup by setting the `shell.localShell`
optional configuration parameter to be true:

```guess
...
shell {
    localShell = true
}
...
```


## SSH Authentication

The host key is loaded from the `<BASE_DIRECTORY>/sshkey/hostkey.pem` file, where <BASE_DIRECTORY> corresponds to the
directory that the service is being run from. This can be overloaded with the `shell.sshHostKeyDirectory` config
parameter option. If this file does not exist, it is generated automatically.


## Connecting to the shell via SSH

For Linux/Mac OS user, the following commands can be run from the terminal:

```bash
ssh -p [portNumber] [host] -l [user]
```

Where:


* `[portNumber]` is the port number specified by the `shell.sshdPort` config parameter
* `[host]` is the service’s host (e.g. `localhost` if running the service locally)
* `[user]` is the username specified by the `shell.user` config parameter

The password will be requested after a connection is established.

{{< note >}}
Restarting the service frequently may cause the host key to be regenerated. SSH usually saves
trusted hosts and will refuse to connect in case of a change. This check can be disabled using the
`-o StrictHostKeyChecking=no` flag. This option should never be used in production environment!

{{< /note >}}

## Supported Commands

The top level list of available commands can be seen by executing `help` from the shell. There are currently two types
of commands:


* `view` - Commands relating to viewing properties and states relating to the current service.
* `run` - Commands that interact with the service and change the state in some manner.

The list of available commands in each subsection can be viewed by executing either `view` or `run` from the shell.
A shell command can by run by executing the type of the command followed by the command name
(`[view|run] <COMMAND_NAME>`). For example, to view all notaries within the Network Map service:

```bash
view notaries
```

More information, including an command line example, for each command can be acquired by using the built-in `man`
functionality (`man <COMMAND_NAME>`). For example, to find out more about the view all notaries command listed above:

```bash
man notaries
```


### Network Map Service

The current supported commands that can be run from the shell are:


### Identity Manager Service

The current supported commands that can be run from the shell are:


### Signing Service

The current supported commands that can be run from the shell are:
