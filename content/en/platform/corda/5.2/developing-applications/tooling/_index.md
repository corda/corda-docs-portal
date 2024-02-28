---
description: "Review the tools required by CorDapp Developers."
date: '2023-02-23'
title: "Application Developer Tooling"
menu:
  corda52:
    identifier: corda52-develop-tooling
    parent: corda52-develop
    weight: 1000
---
<style>
table th:first-of-type {
    width: 30%;
}
table th:nth-of-type(2) {
    width: 70%;
}

</style>

# Application Developer Tooling

{{< tooltip >}}CorDapp{{< /tooltip >}} Developers require the following:

| Tool                                            | Description                                                                                                                                                                                                                                                                                                |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CorDapp Template | The [CorDapp template]({{< relref "../cordapp-template/_index.md" >}}) guides developers who are new to Corda 5 through the stages from initially setting up their development environment through to writing, compiling, and running their first basic CorDapp.                                                                       |
| {{< tooltip >}}Corda CLI{{< /tooltip >}}        | The CorDapp template uses the Corda CLI in the background. CorDapp developers also require the Corda CLI to build {{< tooltip >}}CPB{{< /tooltip >}} files. For information about installation, see [Installing the Corda CLI]({{< relref "./installing-corda-cli.md" >}}).                                            |
| curl                                            | Examples in this documentation for Linux and macOS use the curl CLI to interact with HTTP endpoints. See the [curl documentation](https://everything.curl.dev/get) for details on how to install curl. Alternatives may be used if desired. On Windows, PowerShell contains native support for HTTP calls. |
| IDE                                             | R3 recommends IntelliJ as your development IDE.                                                                                                                                                                                                                                                            |
