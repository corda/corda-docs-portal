---
aliases:
- /releases/release-1.0/config-shell.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- config
- shell
title: Shell Configuration Parameters
---

# Shell Configuration Parameters

{{% table %}}

|Name|Description|
|----|-----------|
| shell |  *(Optional)* Configuration for the embedded shell
| sshdPort |  The port that the shell ssh daemon should listen on. |
| user |  The username for connecting to the shell via SSH. |
| password |  The password for connecting to the shell via SSH. |
| commandsDirectory |  *(Optional)* The path to the directory containing additional CRaSH shell commands. |
| sshHostKeyDirectory |  *(Optional)* The path to the directory containing the `hostkey.pem` file for connecting to the shell via SSH. |
| localShell |  *(Optional)* Boot straight into shell upon startup |

{{% /table %}}
