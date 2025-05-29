---
aliases:
- /config-shell.htmls
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-4:
    identifier: cenm-1-4-config-shell
    parent: cenm-1-4-configuration
    weight: 250
tags:
- config
- shell
title: Shell configuration parameters
---


# Shell configuration parameters


* **shell**:
*(Optional)* Configuration for the embedded shell


* **sshdPort**:
The port that the shell ssh daemon should listen on.


* **user**:
The username for connecting to the shell via SSH.


* **password**:
The password for connecting to the shell via SSH.


* **commandsDirectory**:
*(Optional)* The path to the directory containing additional CRaSH shell commands.


* **sshHostKeyDirectory**:
*(Optional)* The path to the directory containing the hostkey.pem file for connecting to the shell via SSH.


* **localShell**:
*(Optional)* Boot straight into shell upon start-up
