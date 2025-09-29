---
aliases:
- /tools-index.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-5:
    identifier: cenm-1-5-tools-index
    weight: 280
tags:
- tools
title: Tools and utilities
---

# Tools and utilities

A small number of tools and utilities are available to help with setting up, running, and testing a network.

## Public Key Infrastructure

* [Public key infrastructure (PKI) tool]({{< relref "pki-tool.md" >}})

## Node Certificate Rotation Tool

This tool enables the reissuing of node legal identity keys and certificates, allowing CENM to re-register a node (including a notary node) with a new certificate in the Network Map. You must not change the node's `myLegalName` during certificate rotation.

For more information about this feature, contact your R3 account manager.

## General running of network

* [Certificate revocation request submission tool]({{< relref "tool-crr-submission.md" >}})

## Operations and administration

* [CENM Command-line Interface]({{< relref "cenm-cli-tool.md" >}})
* [CENM User Admin tool]({{< relref "user-admin.md" >}})
* [CENM management console]({{< relref "cenm-console.md" >}})

## Other Tools

* {{< cordalatestrelref "enterprise/tools-config-obfuscator.md" "Config obfuscation tool" >}}
* [CRL Endpoint Check Tool]({{< relref "crl-endpoint-check-tool.md" >}})
