---
aliases:
- /releases/3.0/shell.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-shell
    parent: corda-enterprise-3-0-corda-nodes-index
    weight: 1070
tags:
- shell
title: Shell
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}




# Shell


The Corda shell is an embedded or standalone command line that allows an administrator to control and monitor a node. It is based on
the [CRaSH](http://www.crashub.org/) shell and supports many of the same features. These features include:


* Invoking any of the node’s RPC methods
* Viewing a dashboard of threads, heap usage, VM properties
* Uploading and downloading attachments
* Issuing SQL queries to the underlying database
* Viewing JMX metrics and monitoring exports
* UNIX style pipes for both text and objects, an `egrep` command and a command for working with columnar data
* Shutting the node down.


## Permissions

When accessing the shell (embedded, standalone, via SSH) RPC permissions are required. This is because the shell actually communicates
with the node using RPC calls.


* Watching flows (`flow watch`) requires `InvokeRpc.stateMachinesFeed`
* Starting flows requires `InvokeRpc.startTrackedFlowDynamic`, `InvokeRpc.registeredFlows` and `InvokeRpc.wellKnownPartyFromX500Name`, as well as a
permission for the flow being started


## The shell via the local terminal

In development mode, the shell will display in the node’s terminal window.
The shell connects to the node as ‘shell’ user with password ‘shell’ which is only available in dev mode.
It may be disabled by passing the `--no-local-shell` flag when running the node.



## The shell via SSH

The shell is also accessible via SSH.


### Enabling SSH access

By default, the SSH server is *disabled*. To enable it, a port must be configured in the node’s `node.conf` file:

```bash
sshd {
    port = 2222
}
```


### Authentication

Users log in to shell via SSH using the same credentials as for RPC.
No RPC permissions are required to allow the connection and log in.

The host key is loaded from the `<node root directory>/sshkey/hostkey.pem` file. If this file does not exist, it is
generated automatically. In development mode, the seed may be specified to give the same results on the same computer
in order to avoid host-checking errors.


### Connecting to the shell


#### Linux and MacOS

Run the following command from the terminal:

```bash
ssh -p [portNumber] [host] -l [user]
```

Where:


* `[portNumber]` is the port number specified in the `node.conf` file
* `[host]` is the node’s host (e.g. `localhost` if running the node locally)
* `[user]` is the RPC username

The RPC password will be requested after a connection is established.

{{< note >}}
In development mode, restarting a node frequently may cause the host key to be regenerated. SSH usually saves
trusted hosts and will refuse to connect in case of a change. This check can be disabled using the
`-o StrictHostKeyChecking=no` flag. This option should never be used in production environment!

{{< /note >}}

#### Windows

Windows does not provide a built-in SSH tool. An alternative such as PuTTY should be used.


## The standalone shell

The standalone shell is a standalone application interacting with a Corda node via RPC calls.
RPC node permissions are necessary for authentication and authorisation.
Certain operations, such as starting flows, require access to CordApps jars.


### Starting the standalone shell

Run the following command from the terminal:


#### Linux and MacOS

```bash
java -jar corda-tools-shell-cli-VERSION_NUMBER.jar [--config-file PATH | --cordpass-directory PATH --commands-directory PATH --host HOST --port PORT
         --user USER --password PASSWORD --sshd-port PORT --sshd-hostkey-directory PATH --keystore-password PASSWORD
         --keystore-file FILE --truststore-password PASSWORD --truststore-file FILE | --help]
```


#### Windows

```bash
java -jar  corda-tools-shell-cli-VERSION_NUMBER.jar [--config-file PATH | --cordpass-directory PATH --commands-directory PATH --host HOST --port PORT
         --user USER --password PASSWORD --sshd-port PORT --sshd-hostkey-directory PATH --keystore-password PASSWORD
         --keystore-file FILE --truststore-password PASSWORD --truststore-file FILE | --help]
```

Where:


* `config-file` is the path to config file, used instead of providing the rest of command line options
* `cordpass-directory` is the directory containing Cordapps jars, Cordapps are require when starting flows
* `commands-directory` is the directory with additional CrAsH shell commands
* `host` is the Corda node’s host
* `port` is the Corda node’s port, specified in the `node.conf` file
* `user` is the RPC username, if not provided it will be requested at startup
* `password` is the RPC user password, if not provided it will be requested at startup
* `sshd-port` instructs the standalone shell app to start SSH server on the given port, optional
* `sshd-hostkey-directory` is the directory containing hostkey.pem file for SSH server
* `keystore-password` the password to unlock the KeyStore file containing the standalone shell certificate and private key, optional, unencrypted RPC connection without SSL will be used if the option is not provided
* `keystore-file` is the path to the KeyStore file
* `truststore-password` the password to unlock the TrustStore file containing the Corda node certificate, optional, unencrypted RPC connection without SSL will be used if the option is not provided
* `truststore-file` is the path to the TrustStore file
* `help` prints Shell help

The format of `config-file`:

```bash
node {
    addresses {
        rpc {
            host : "localhost"
            port : 10006
        }
    }
}
shell {
        workDir : /path/to/dir
}
extensions {
    cordapps {
        path : /path/to/cordapps/dir
    }
    sshd {
        enabled : "false"
        port : 2223
    }
}
ssl {
    keystore {
        path: "/path/to/keystore"
        type: "JKS"
        password: password
    }
    trustore {
        path: "/path/to/trusttore"
        type: "JKS"
        password: password
    }
}
user : demo
password : demo
```


## Standalone Shell via SSH

The standalone shell can embed an SSH server which redirects interactions via RPC calls to the Corda node.
To run SSH server use `--sshd-port` option when starting standalone shell or `extensions.sshd` entry in the configuration file.
For connection to SSH refer to [Connecting to the shell](#connecting-to-the-shell).
Certain operations (like starting Flows) will require Shell’s `--cordpass-directory` to be configured correctly (see [Starting the standalone shell](#starting-the-standalone-shell)).


## Interacting with the node via the shell

The shell interacts with the node by issuing RPCs (remote procedure calls). You make an RPC from the shell by typing
`run` followed by the name of the desired RPC method. For example, you’d see a list of the registered flows on your
node by running:

`run registeredFlows`

Some RPCs return a stream of events that will be shown on screen until you press Ctrl-C.

You can find a list of the available RPC methods
[here](https://docs.corda.net/api/kotlin/corda/net.corda.core.messaging/-corda-r-p-c-ops/index.html).


### Shutting down the node

You can shut the node down via shell:


* `gracefulShutdown` will put node into draining mode, and shut down when there are no flows running
* `shutdown` will shut the node down immediately


### Flow commands

The shell also has special commands for working with flows:


* `flow list` lists the flows available on the node
* `flow watch` shows all the flows currently running on the node with result (or error) information
* `flow start` starts a flow. The `flow start` command takes the name of a flow class, or
*any unambiguous substring* thereof, as well as the data to be passed to the flow constructor. If there are several
matches for a given substring, the possible matches will be printed out. If a flow has multiple constructors then the
names and types of the arguments will be used to try and automatically determine which one to use. If the match
against available constructors is unclear, the reasons each available constructor failed to match will be printed
out. In the case of an ambiguous match, the first applicable constructor will be used


### Parameter syntax

Parameters are passed to RPC or flow commands using a syntax called [Yaml](http://www.yaml.org/spec/1.2/spec.html) (yet another markup language), a
simple JSON-like language. The key features of Yaml are:


* Parameters are separated by commas
* Each parameter is specified as a `key: value` pair> 

    * There **MUST** to be a space after the colon, otherwise you’ll get a syntax error



* Strings do not need to be surrounded by quotes unless they contain commas, colons or embedded quotes
* Class names must be fully-qualified (e.g. `java.lang.String`)
* Nested classes are referenced using `$`. For example, the `net.corda.finance.contracts.asset.Cash.State`
class is referenced as `net.corda.finance.contracts.asset.Cash$State` (note the `$`)

{{< note >}}
If your CorDapp is written in Java, named arguments won’t work unless you compiled the node using the
`-parameters` argument to javac. See [Creating nodes locally](generating-a-node.md) for how to specify it via Gradle.

{{< /note >}}

#### Creating an instance of a class

Class instances are created using curly-bracket syntax. For example, if we have a `Campaign` class with the following
constructor:

`data class Campaign(val name: String, val target: Int)`

Then we could create an instance of this class to pass as a parameter as follows:

`newCampaign: { name: Roger, target: 1000 }`

Where `newCampaign` is a parameter of type `Campaign`.


#### Mappings from strings to types

In addition to the types already supported by Jackson, several parameter types can automatically be mapped from strings.
We cover the most common types here.


##### Amount

A parameter of type `Amount<Currency>` can be written as either:


* A dollar ($), pound (£) or euro (€) symbol followed by the amount as a decimal
* The amount as a decimal followed by the ISO currency code (e.g. “100.12 CHF”)


##### SecureHash

A parameter of type `SecureHash` can be written as a hexadecimal string: `F69A7626ACC27042FEEAE187E6BFF4CE666E6F318DC2B32BE9FAF87DF687930C`


##### OpaqueBytes

A parameter of type `OpaqueBytes` can be provided as a UTF-8 string.


##### PublicKey and CompositeKey

A parameter of type `PublicKey` can be written as a Base58 string of its encoded format: `GfHq2tTVk9z4eXgyQXzegw6wNsZfHcDhfw8oTt6fCHySFGp3g7XHPAyc2o6D`.
`net.corda.core.utilities.EncodingUtils.toBase58String` will convert a `PublicKey` to this string format.


##### Party

A parameter of type `Party` can be written in several ways:


* By using the full name: `"O=Monogram Bank,L=Sao Paulo,C=GB"`
* By specifying the organisation name only: `"Monogram Bank"`
* By specifying any other non-ambiguous part of the name: `"Sao Paulo"` (if only one network node is located in Sao
Paulo)
* By specifying the public key (see above)


##### NodeInfo

A parameter of type `NodeInfo` can be written in terms of one of its identities (see `Party` above)


##### AnonymousParty

A parameter of type `AnonymousParty` can be written in terms of its `PublicKey` (see above)


##### NetworkHostAndPort

A parameter of type `NetworkHostAndPort` can be written as a “host:port” string: `"localhost:1010"`


##### Instant and Date

A parameter of `Instant` and `Date` can be written as an ISO-8601 string: `"2017-12-22T00:00:00Z"`


#### Examples


##### Starting a flow

We would start the `CashIssue` flow as follows:

`flow start CashIssueFlow amount: $1000, issuerBankPartyRef: 1234, notary: "O=Controller, L=London, C=GB"`

This breaks down as follows:


* `flow start` is a shell command for starting a flow
* `CashIssue` is the flow we want to start
* Each `name: value` pair after that is a flow constructor argument

This command invokes the following `CashIssue` constructor:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
class CashIssueFlow(val amount: Amount<Currency>,
                    val issueRef: OpaqueBytes,
                    val recipient: Party,
                    val notary: Party) : AbstractCashFlow(progressTracker)
```
{{% /tab %}}

{{< /tabs >}}


##### Querying the vault

We would query the vault for `IOUState` states as follows:

`run vaultQuery contractStateType: com.template.IOUState`

This breaks down as follows:


* `run` is a shell command for making an RPC call
* `vaultQuery` is the RPC call we want to make
* `contractStateType: com.template.IOUState` is the fully-qualified name of the state type we are querying for


### Attachments

The shell can be used to upload and download attachments from the node. To learn more, see the tutorial
“[Using attachments](tutorial-attachments.md)”.


### Getting help

You can type `help` in the shell to list the available commands, and `man` to get interactive help on many
commands. You can also pass the `--help` or `-h` flags to a command to get info about what switches it supports.

Commands may have subcommands, in the same style as `git`. In that case, running the command by itself will
list the supported subcommands.


## Extending the shell

The shell can be extended using commands written in either Java or [Groovy](http://groovy-lang.org/) (a Java-compatible scripting language).
These commands have full access to the node’s internal APIs and thus can be used to achieve almost anything.

A full tutorial on how to write such commands is out of scope for this documentation. To learn more, please refer to
the [CRaSH](http://www.crashub.org/) documentation. New commands are placed in the `shell-commands` subdirectory in the node directory. Edits
to existing commands will be used automatically, but currently commands added after the node has started won’t be
automatically detected. Commands must have names all in lower-case with either a `.java` or `.groovy` extension.


{{< warning >}}
Commands written in Groovy ignore Java security checks, so have unrestricted access to node and JVM
internals regardless of any sandboxing that may be in place. Don’t allow untrusted users to edit files in the
shell-commands directory!

{{< /warning >}}



## Limitations

The shell will be enhanced over time. The currently known limitations include:


* Flows cannot be run unless they override the progress tracker
* If a command requires an argument of an abstract type, the command cannot be run because the concrete subclass to use cannot be specified using the YAML syntax
* There is no command completion for flows or RPCs
* Command history is not preserved across restarts
* The `jdbc` command requires you to explicitly log into the database first
* Commands placed in the `shell-commands` directory are only noticed after the node is restarted
* The `jul` command advertises access to logs, but it doesn’t work with the logging framework we’re using




