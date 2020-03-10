---
aliases:
- /releases/release-V4.0/design/sgx-infrastructure/details/host.html
date: '2020-01-08T09:59:25Z'
menu:
- corda-os-4-0
tags:
- host
title: Enclave host
---


# Enclave host

An enclave host’s responsibility is the orchestration of the communication with hosted enclaves.

It is responsible for:


* Leasing a sealing identity
* Getting a CPU certificate in the form of an Intel-signed quote
* Downloading and starting of requested enclaves
* Driving attestation and subsequent encrypted traffic
* Using discovery to connect to other enclaves/services
* Various caching layers (and invalidation of) for the CPU certificate, hosted enclave quotes and enclave images

