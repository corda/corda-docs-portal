---
aliases:
- /config-shell.htmls
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-7:
    identifier: cenm-1-7-config-shell
    parent: cenm-1-7-configuration
    weight: 250
tags:
- config
- shell
title: Shell configuration parameters
---


# Shell configuration parameters


* **shell**:
*(Optional)* Configuration for the embedded shell.


  * **sshdPort**:
  The port that the shell ssh daemon should listen on.


  * **sshdHost**:
  *(Optional)* The host or IP for the shell ssh daemon.


  * **user**:
  The username for connecting to the shell via SSH.


  * **password**:
  The password for connecting to the shell via SSH.


  * **commandsDirectory**:
  *(Optional)* The path to the directory containing additional CRaSH shell commands.


  * **sshdHostKeyDirectory**:
  *(Optional)* The path to the directory containing the hostkey.pem file for connecting to the shell via SSH.


  * **localShell**:
  *(Optional)* Boot straight into shell upon start-up
