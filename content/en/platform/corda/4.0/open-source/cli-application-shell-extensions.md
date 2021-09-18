---
aliases:
- /releases/release-V4.0/cli-application-shell-extensions.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-0:
    identifier: corda-os-4-0-cli-application-shell-extensions
    parent: corda-os-4-0-operations
    weight: 220
tags:
- cli
- application
- shell
- extensions
title: Shell extensions for CLI Applications
---


# Shell extensions for CLI Applications



## Installing shell extensions

Users of `bash` or `zsh` can install an alias and auto-completion for Corda applications that contain a command line interface. Run:

```shell
java -jar <name-of-JAR>.jar install-shell-extensions
```

Then, either restart your shell, or for `bash` users run:

```shell
. ~/.bashrc
```

Or, for `zsh` run:

```shell
. ~/.zshrc
```

You will now be able to run the command line application from anywhere by running the following:

```shell
<alias> --<option>
```

For example, for the Corda node, install the shell extensions using

```shell
java -jar corda-<version>.jar install-shell-extensions
```

And then run the node by running:

```shell
corda --<option>
```


## Upgrading shell extensions

Once the shell extensions have been installed, you can upgrade them in one of two ways.


* Overwrite the existing JAR with the newer version. The next time you run the application, it will automatically update
the completion file. Either restart the shell or see [above](#installing-shell-extensions) for instructions
on making the changes take effect immediately.
* If you wish to use a new JAR from a different directory, navigate to that directory and run:

```shell
java -jar <name-of-JAR>
```

Which will update the alias to point to the new location, and update command line completion functionality. Either
restart the shell or see [above](#installing-shell-extensions) for instructions on making the changes take effect immediately.


## List of existing CLI applications


{{< table >}}

|Description|JAR name|Alias|
|[Corda node](running-a-node.html#starting-an-individual-corda-node)|`corda-<version>.jar`|`corda --<option>`|
|[Network bootstrapper]({{% ref "network-bootstrapper.md" %}})|`corda-tools-network-bootstrapper-<version>.jar`|`bootstrapper --<option>`|
|[Standalone shell](shell.html#standalone-shell)|`corda-tools-shell-cli-<version>.jar`|`corda-shell --<option>`|
|[Blob inspector]({{% ref "blob-inspector.md" %}})|`corda-tools-blob-inspector-<version>.jar`|`blob-inspector --<option>`|

{{< /table >}}

