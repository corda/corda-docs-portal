---
title: "Using the Corda Node CLI and curl"
date: '2021-08-26'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-operating
    identifier: corda-5-dev-preview-1-nodes-operating-cli-curl
    weight: 4800
section_menu: corda-5-dev-preview
description: >
  How to interact with your node using the Corda Node command-line interface (CLI) or `curl` commands.
expiryDate: '2022-09-28'  
---

Use this guide to interact with your node using the Corda Node command-line interface (CLI) or `curl` commands.

The Corda Node command-line interface (CLI) allows you to interact with nodes using the new HTTP-RPC API. It offers a convenient way of calling HTTP-RPC methods, and formats their results so that they are easy to understand.

## Download the Corda Node CLI

Download either the Corda Node CLI's <a href="https://download.corda.net/corda-node-cli/5.0.0-DevPreview-1.0.1/corda-node-cli.tar">`.tar`</a> or <a href="https://download.corda.net/corda-node-cli/5.0.0-DevPreview-1.0.1/corda-node-cli.zip">`.zip`</a> file.

{{< note >}}

You must save the Corda Node CLI `.jar` file locally to your computer (you don't need to run an installation process). How you achieve this will depend on your organisation's software distribution policies. This guide assumes you have downloaded the file, and saved it locally as `corda-node-cli.jar`.

{{< /note >}}


### Explore the Corda Node CLI

The Corda Node CLI is built to be discoverable. Start by invoking it without any arguments:

```console
java -jar corda-node-cli.jar --help

Specify a sub-command

Usage:

corda [-hvV] [--logging-level=<loggingLevel>] [COMMAND]

Description:


Options:

  -h, --help      Show this help message and exit.
      --logging-level=<loggingLevel>
                  Enable logging at this level and higher. Possible values:
                    ERROR, WARN, INFO, DEBUG, TRACE
  -v, --verbose, --log-to-console
                  If set, prints logging to the console as well as to a file.
  -V, --version   Print version information and exit.

Commands:

  endpoint  Performs operations on HTTP RPC endpoints. HTTP RPC endpoints
              should be created first before any subsequent commands executed
              on them.
  flow      Allows you to start and kill flows, list the ones available and to
              watch flows currently running on the node.
  vault     Allows to query Corda Node's vault and retrieve various types of
              persistent objects from it.
```

As you can see from the response, the interface expects a sub-command to be specified and provides a list and description of the ones available. The list of commands will evolve as this is pluggable functionality. Use the `--help` option to see the complete list of commands and to learn how to correctly structure arguments. For example `flow --help`, `flow list --help`, `flow start --help`.

### Connect to your node

Connections are managed on a per-node basis, with the node address and user account constituting an **endpoint**. Every command sent using the interface targets a single endpoint (node).

To manage your endpoints, use the command `corda-node-cli endpoint [command] ...`, replacing `[command]` with:
* `add` to register a new endpoint.
* `remove` to remove a registered endpoint.
* `set` to set an endpoint as the default for successive commands.
* `get` to show the current default endpoint.

Endpoints are identified by their full address (http[s]://address:port/api/v1). For convenience, you can set an alias for an endpoint when registering it, using the `-n` argument:
```console
> ./corda-node-cli endpoint add -n node-a ...
```

#### Supported user authentication methods

`corda-node-cli` supports OAuth2 with Azure Active Directory (AD) as well as basic authentication methods.
Where possible, you should use OAuth2. However, there may be occasions when basic authentication is better suited, such as in automation scripts.

If a given endpoint supports both authentication methods, then it will check for authentication credentials in the following order when a `corda-node-cli` command is issued:

1. Username/password in the command line arguments (using `-u` and `-P` options).
2. Username/password provided in the system variables (`CORDA_NODE_CLI_USERNAME` and `CORDA_NODE_CLI_PASSWORD`),
   unless `--azure-ad` option is specified.
3. Endpoint's default authentication as specified during registration.

#### Connect to nodes using basic authentication

{{< warning >}}

Where possible, you should use OAuth2. Basic authentication is not a secure login method because:
* Passwords are exposed in client-server communication (if you aren't using HTTPS).
* Node administrators will need to populate `node.conf` with account credentials for other users.

{{< /warning >}}

To connect to a node that does not use single sign-on (SSO), you can use basic username/password authentication. For this, you need to make sure that the user account is set up in `node.conf`. Here's an example:

```console
> corda-node-cli endpoint add -n mynode --basic-auth -u [username] -P -- [address]/api/v1
Enter value for --password (Password for password based authentication.):
```

Don't supply an argument for -P. The double dash tells the Corda Node CLI that the subsequent string is the address of the node (rather than the password). Although you can supply the password inline, this approach is discouraged as you run the risk of having your credentials stored in your command line history, which can persist even after you disconnect from the current terminal session.

When using basic authentication, the Corda Node CLI doesn't save your credentials locally as that would expose them. To avoid having to set `-u` and `-P` for every command, you can set the `CORDA_NODE_CLI_USERNAME` and `CORDA_NODE_CLI_PASSWORD` environment variables in your current session.

#### Connect to nodes using OAuth2 with Azure AD

To connect to a node using Azure AD:

1. Run:

   ```console
   corda-node-cli endpoint add -n azure-node --azure-ad -- [address]/api/v1

   The HTTP RPC at https://[address]/api/v1 has a X.509 key fingerprint:
   ```

2. Respond to the prompt and login via the link provided.
   ```console
   Do you trust this host? (Y/N)
   y
   To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code [code] to authenticate.
   ```

### Verify the Corda Node CLI functionality

There are also commands to verify the Corda Node CLI functionality. For example, to verify a node's network membership registration, run:

```console
> corda-node-cli healthCheck group
Network ready: Ready
```

### Delete the Corda Node CLI

To delete the Corda Node CLI, simply delete the application's folder at its location.

## Invoke HTTP-RPC using `curl`

You can invoke any method inside a [@HttpRpcResource](../../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/expose-rpc/annotation.html#annotations-and-meta-annotation-fields)
annotated interface if the method itself is also annotated with
[@HttpRpcGET](../../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/expose-rpc/annotation.html#annotations-and-meta-annotation-fields) or
[@HttpRpcPOST](../../../../../../../en/platform/corda/5.0-dev-preview-1/nodes/developing/expose-rpc/annotation.html#annotations-and-meta-annotation-fields).

If you haven't specified the `path` in the annotation, the generated URL will contain the name of the interface and the name of the method (converted to lowercase).
You can override this by providing a value for the `path` parameter in the annotation.

If you have configured HTTP-RPC to run locally on `localhost:9090`, you can use the commands in the following sections to invoke HTTP-RPC methods.

### Execute an ordinary method call

This example shows a `curl` command that executes the method `listActive` inside the `FlowManagerRPCOps` interface (assuming the username is `default`):

```shell
curl -u default -X GET "https://0.0.0.0:9090/api/v1/flowmanagerrpcops/listactive"
```

{{<table>}}
| Options    | Description                  |
|------------|------------------------------|
| `-u`       | Specifies the username. You can also include the password after a colon, otherwise a prompt will appear. |
| `-X`       | `GET` or `POST`.                 |
| `-d`       | Specifies the data to be sent. |
| `--insecure` | For testing purposes only. Used to ignore certificate errors.  |
{{</table>}}

You may find it useful to look at the `curl` commands generated by Swagger UI.
These become visible once you have sent a request in the `Try it out` section of an operation:

{{<
  figure
      src="tryitout.png"
      zoom="tryitout.png"
    width=80%
      figcaption="curl commands in Swagger UI"
      alt="curl commands in Swagger UI"
>}}

### Start a flow

A flow can be started by invoking `/flowstarter/startflow` with the correct request parameters.

For example, the `MessageStateIssue` flow can be started via HTTP-RPC by passing in this body parameter to the
`startflow` endpoint:

```json
{
  "rpcStartFlowRequest": {
    "clientId": "id",
    "flowName": "net.corda.httprpcdemo.workflows.MessageStateIssue",
    "parameters": {
      "parametersInJson": "{\"message\":\"hello\"}"
    }
  }
}
```

When storing the above data in `startflow-req.json`, use the `curl` command:

```shell
curl --user default -X POST "https://0.0.0.0:9090/api/v1/flowstarter/startflow" -d "@startflow-req.json"
```

Or, if you aren't using a file to store the requested data, use:
```shell
curl --user default -X POST "https://0.0.0.0:9090/api/v1/flowstarter/startflow" -d "{\"rpcStartFlowRequest\":{\"clientId\":\"client\",\"flowName\":\"net.corda.httprpcdemo.workflows.MessageStateIssue\",\"parameters\":{\"parametersInJson\":\"{\\\"message\\\":\\\"hello\\\"}\"}}}"
```
