---
title: "Adding Corda Node CLI commands"
date: '2021-09-14'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing
    identifier: corda-5-dev-preview-1-nodes-developing-new-cli-commands
    weight: 2800
project: corda-5
section_menu: corda-5-dev-preview
description: >
  How to add new commands to the Corda Node CLI.
---

Use this guide to learn about commands in the Corda Node CLI and how you can add new ones.

## Existing Corda Node CLI commands

Commands implemented in the Corda Node CLI are `endpoint`, `flow`, and `vault`. Each of these commands can have
one or more subcommands, and each subcommand can have further subcommands.

Use the `--help` option to see the complete list of commands:

```shell
java -jar corda-node-cli.jar --help

Usage:

corda [-hvV] [--logging-level=<loggingLevel>] [COMMAND]

Description:


Options:

  -h, --help      Shows this help message and exit.
      --logging-level=<loggingLevel>
                  Enable logging at this level and higher. Possible values:
                    ERROR, WARN, INFO, DEBUG, TRACE
  -v, --verbose, --log-to-console
                  If set, prints logging to the console as well as to a file.
  -V, --version   Print version information and exit.

Commands:

  endpoint  Performs operations on HTTP-RPC endpoints. HTTP-RPC endpoints
              should be created first before any subsequent commands executed
              on them.
  flow      Allows you to start and kill flows, list the ones available and to
              watch flows currently running on the node.
  vault     Allows you to query Corda node's vault and retrieve various types of
              persistent objects from it.
```

To learn more about how to use each of the commands (and subcommands), use the `--help` option:

```shell
java -jar corda-node-cli.jar endpoint add --help

Usage:

corda endpoint add [-hvV] [--logging-level=<loggingLevel>] [-n=<name>]
                   [[[--basic-auth] -u=<username> -P[=<password>]] |
                   [--azure-ad]] <url>

Description:

Allows to add HTTP-RPC endpoint of the Corda with necessary credentials to the
local cache. After endpoint is added other commands can be executed against it.

Parameters:

      <url>           HTTP-RPC endpoint URL in the form: https://<host>:
                        port/api/v1

Options:

  -h, --help          Shows this help message and exit.
      --logging-level=<loggingLevel>
                      Enable logging at this level and higher. Possible values:
                        ERROR, WARN, INFO, DEBUG, TRACE
  -n, --name=<name>   Human readable name which will be used to identify HTTP
                        RPC endpoint
  -v, --verbose, --log-to-console
                      If set, prints logging to the console as well as to a
                        file.
  -V, --version       Print version information and exit.
Username/password authentication      --basic-auth
  -P, --password[=<password>]
                      Password for password based authentication.
                      If present without value, the password can be entered
                        interactively.
  -u, --username=<username>
                      Username for password based authentication.
AzureAD authentication      --azure-ad
```

## Add new commands to the Corda Node CLI

To add a new command:
1. Define your new command as a child class of `ParentCommand` and as a subcommand of `CordaCommand`, specify your command's subcommands, and annotate all commands and subcommands with `@CommandLine.Command`.
2. Implement business logic in the `execute` method of each subcommand and override `validate` in `ValidatedCommand` (if required).
3. Add `@CommandLine.Option` and `@CommandLine.Parameters`annotations to receive argument and parameter values.

{{< note >}}

If you need access to HTTP-RPC services, create the subcommands of your new command as a child
of <a href="#2-implement-business-logic-and-validation">`ValidatedCommand`</a>
or <a href="#httprpccommand">`HttpRpcCommand`</a>.

{{< /note >}}

### 1. Define commands and subcommands

Each command can have one or more subcommands, and each subcommand can have further subcommands.

Add new commands as subcommands of `CordaCommand`. `CordaCommand` has three
subcommands:

```kotlin
@CommandLine.Command(name = "corda",
        subcommands = [NodeCommand::class, FlowCommand::class, VaultCommand::class])
internal class CordaCommand : ParentCommand(), LoggingOwner
```

Business logic is typically implemented through subcommands. Create a new command as an empty
child class of `ParentCommand` and define its subcommands as members of the `@CommandLine.Command` annotation.

See `NodeCommand` as an example:

```kotlin
@CommandLine.Command(name = "endpoint",
        subcommands = [AddNodeCommand::class,
            ListNodesCommand::class,
            RemoveNodeCommand::class,
            SetNodeCommand::class,
            GetNodeCommand::class],
        description = ["Performs operations on HTTP-RPC endpoints. HTTP-RPC endpoints should be created first before any subsequent commands " +
                "executed on them."])
internal class NodeCommand : ParentCommand()
```

### 2. Implement business logic and validation

Each subcommand has its own set of arguments and implements its own business logic. For each subcommand, you need to
implement the business logic in the `execute` method.

#### `ValidatedCommand`

`ValidatedCommand` is the base class that implements validation to verify arguments passed into the command.

`ValidatedCommand` defines:
* The `execute` method that you must override to provide the business logic:

   ```kotlin
   protected abstract fun execute(): Int
   ```

* An empty `validate` method that you can override if validation is required:

   ```kotlin
   protected open fun validate() {}
   ```
* the `output` method which you can use to print out results.

  See `ListNodesCommand`as a simple example:

  ```kotlin
  @CommandLine.Command(name = "list", description = [
      "Lists previously created HTTP-RPC endpoints along with their aliases."])
  internal class ListNodesCommand(private val storageService: StorageService) : ValidatedCommand() {
      override fun execute(): Int {
          storageService.getContexts().forEach {
              output("${it.name}: ${it.baseAddress}")
          }
          return ExitCodes.SUCCESS
      }
  }
  ```

#### `EndpointOrAliasCommand`

`EndpointOrAliasCommand` is a child of `ValidatedCommand` and defines an endpoint argument:

```kotlin
internal abstract class EndpointOrAliasCommand : ValidatedCommand() {
    @CommandLine.Option(names = ["--endpoint"], description = ["Url or alias for an existing endpoint."], required = false)
    var endpoint: String? = null
}
```

#### `HttpRpcCommand`

`HttpRpcCommand` extends `EndpointOrAliasCommand`.
It adds the capability to get a proxy for an `RPCOps` interface.
A command would typically extend `HttpRpcCommand` if its business logic needs to expose services via HTTP-RPC.

### 3. Annotate fields to receive command argument and parameter values

Picocli will initialize properly annotated fields with the matching arguments/positional parameters provided via the command line.
* Fields annotated with `@CommandLine.Option` will be initialized with matching arguments.
* Fields annotated with `@CommandLine.Parameters` will be initialized with positional parameters.

See `AddNodeCommand` as an example:

```kotlin
    @CommandLine.Option(names = ["-n", "--name"], description = ["Human readable name which will be used to identify HTTP-RPC endpoint"])
    var name: String? = null

    @CommandLine.Parameters(index = "0", description = ["HTTP-RPC endpoint URL in the form: https://<host>:port/api/v1"])
    lateinit var url: URL
```
