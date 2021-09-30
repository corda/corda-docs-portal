---
aliases:
- /releases/release-1.0/tool-health-check.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-0:
    identifier: cenm-1-0-tool-health-check
    parent: cenm-1-0-tools-index
    weight: 1100
tags:
- tool
- health
- check
title: Inter-service Communication Health Checking Tool
---


# Inter-service Communication Health Checking Tool

The purpose of this tool is to confirm correct client and server-side configuration of ENM services necessary for
inter-service communication. There are two types of connection:


* Outgoing, via a client
* Inbound, hitting a listening service


## Client Health Check Tool

In this context, a client is either:


* The Network Map, which consumes the Doorman and Revocation services
* The Signing Service, comprised of the CRL Signer and Network Map Signer, which consume the Revocation and Network Map services respectively


### Usage

Provide the config file used to configure the client (Network Map/Signing Service) that is being tested.

The tool reads the config file and pings the relevant services.

```bash
java -jar utilities-<VERSION>.jar client-health-check --config-file <CONFIG_FILE>
```


* Either `--network-map` or `--signing-service` flag must be set
* Service keystore and truststore files must be held locally and corresponding keys `keyStore` and `trustStore` must be configured


## Server Health Check Tool

The server health check tool reads an ENM service config file and pings the service to confirm correct configuration and availability.

In this context, a server hosts either:


* The Doorman and Revocation services. These services reside on the same remote host and listen on different ports, sharing a single config file
* The Network Map


### Usage

Provide the config file used to configure the ENM service (Doorman/Network Map/Revocation) that is being tested.

```bash
java -jar utilities-<VERSION>.jar server-health-check --config-file <CONFIG_FILE>
```


* Service keystore and truststore files must be held locally and corresponding keys `keyStore` and `trustStore` must be configured

