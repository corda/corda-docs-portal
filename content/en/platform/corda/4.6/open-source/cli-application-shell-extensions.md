---
aliases:
- /head/cli-application-shell-extensions.html
- /HEAD/cli-application-shell-extensions.html
- /cli-application-shell-extensions.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-cli-application-shell-extensions
    parent: corda-os-4-6-operations
    weight: 390
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
java -jar corda-4.6.jar install-shell-extensions
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

|Description|Alias|JAR Name|
|---------------------------------------------------------|------------------------------|----------------------------------------------------------|
|[Corda node](running-a-node.html#starting-an-individual-corda-node)|`corda --<option>`|`corda-4.6.jar`|
|[Network bootstrapper]({{% ref "network-bootstrapper.md" %}})|`bootstrapper --<option>`|`corda-tools-network-bootstrapper-4.6.jar`|
|[Standalone shell](shell.html#standalone-shell)|`corda-shell --<option>`|`corda-tools-shell-cli-4.6.jar`|
|[Blob inspector]({{% ref "blob-inspector.md" %}})|`blob-inspector --<option>`|`corda-tools-blob-inspector-4.6.jar`|

{{< /table >}}
