---
aliases:
- /pki-specifications.html
date: '2020-01-08T09:59:25Z'
menu:
  cenm-1-3:
    identifier: cenm-1-3-pki-specifications
    parent: cenm-1-3-public-key-infrastructure
    weight: 310
tags:
- pki
- guide
title: PKI Specifications
---

# Public Key Infrastructure (PKI) Specifications

As described in the [Certificate Hierarchy Guide](pki-guide.md), Corda security relies heavily on the use of Public Key Infrastructure (PKI). Whether creating this hierarchy using the [PKI Tool](pki-tool.md) or setting up a Corda network on your own, your PKI must comply with existing Corda specifications.

Specifications and instructions are referenced here for the four scenarios below. Follow these guidelines to successfully create a Corda compliant hierarchy for your own use or to pass on to a third party service.

## Generating root, subordinate, and network certificates

For instructions on generating certificates, see the [PKI Tool](pki-tool.html#running-the-pki-tool) documentation.

## Setting up a network under an existing root

If you wish to set up a Corda network under an existing root and therefore are not using the PKI Tool, the certificate hierarchy you create should follow the guidelines specified in the [Certificate Hierarchy Guide](pki-guide.md). You may also find it helpful to reference the [Corda network policies](https://corda.network/trust-root/index/).

## Delegating network signing to a third party

If you wish to delegate network signing to a third party software provider, this can be done partially (with the Certificate Authority only) or fully (with the Certificate Authority and the non-Certificate Authority).

Follow the specifications outlined in the [Signing and SMR Services](signing-service.md#using-a-signing-plugins) documentation to delegate this task to a third party software provider.

## Using your own Certificate Authority software

To set up a Corda network using your own Certificate Authority software, use the Signable Material Retriever service. This service acts as a bridge between CENM services and one or more signing services. See the [Signable Material Retriever Service](signing-service.html#signable-material-retriever) documentation for instructions and specifications for using this service.
