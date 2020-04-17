---
aliases:
- /releases/3.1/design/float/decisions/ssl-termination.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- ssl
- termination
title: 'Design Decision: TLS termination point'
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Design Decision: TLS termination point


## Background / Context

Design of the [float](../design.md) is critically influenced by the decision of where TLS connections to the node should
be terminated.


## Options Analysis


### 1. Terminate TLS on Firewall


#### Advantages


* Common practice for DMZ web solutions, often with an HSM associated with the Firewall and should be familiar for banks to setup.
* Doesn’t expose our private key in the less trusted DMZ context.
* Bugs in the firewall TLS engine will be patched frequently.
* The DMZ float server would only require a self-signed certificate/private key to enable secure communications, so theft of this key has no impact beyond the compromised machine.


#### Disadvantages


* May limit cryptography options to RSA, and prevent checking of X500 names (only the root certificate checked) - Corda certificates are not totally standard.
* Doesn’t allow identification of the message source.
* May require additional work and SASL support code to validate the ultimate origin of connections in the float.


#### Variant option 1a: Include SASL connection checking


##### Advantages


* Maintain authentication support
* Can authenticate against keys held internally e.g. Legal Identity not just TLS.


##### Disadvantages


* More work than the do-nothing approach
* More protocol to design for sending across the inner firewall.


### 2. Direct TLS Termination onto Float


#### Advantages


* Validate our PKI certificates directly ourselves.
* Allow messages to be reliably tagged with source.


#### Disadvantages


* We don’t currently use the identity to check incoming packets, only for connection authentication anyway.
* Management of Private Key a challenge requiring extra work and security implications. Options for this are presented below.


#### Variant Option 2a: Float TLS certificate via direct HSM


##### Advantages


* Key can’t be stolen (only access to signing operations)
* Audit trail of signings.


##### Disadvantages


* Accessing HSM from DMZ probably not allowed.
* Breaks the inbound-connection-only rule of modern DMZ.


#### Variant Option 2b: Tunnel signing requests to bridge manager


##### Advantages


* No new connections involved from Float box.
* No access to actual private key from DMZ.


##### Disadvantages


* Requires implementation of a message protocol, in addition to a key provider that can be passed to the standard SSLEngine, but proxies signing requests.


#### Variant Option 2c: Store key on local file system


##### Advantages


* Simple with minimal extra code required.
* Delegates access control to bank’s own systems.
* Risks losing only the TLS private key, which can easily be revoked. This isn’t the legal identity key at all.


##### Disadvantages


* Risks losing the TLS private key.
* Probably not allowed.


## Recommendation and justification

Proceed with Variant option 1a: Terminate on firewall; include SASL connection checking.


## Decision taken

[DNB Meeting, 16/11/2017](drb-meeting-20171116.md): Proceed with option 2b - Terminate on float, inject key from internal portion of the float  (RGB, JC, MH agreed)

