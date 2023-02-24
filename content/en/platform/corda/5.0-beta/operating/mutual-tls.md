---
date: '2023-02-23'
title: "Mutual TLS Connections"
menu:
  corda-5-beta:
    identifier: corda-5-beta-mutual-tls
    parent: corda-5-beta-operate
    weight: 1000
section_menu: corda-5-beta
---
Corda 5 uses TLS to secure a connection between two clusters. While establishing a TLS connection between the gateways of two clusters, the server gateway sends its certificate to the client gateway. The client gateway verifies the server certificate using its trust root certificate. In mutual TLS, in addition to the client verifying the server certificate, the server gateway also requests the client gateway send a client certificate and verifies that it is using its trust root certificate.

As the gateway manages the TLS connections for an entire cluster, the TLS mode (mutual or one-way) is defined in the gateway configuration and applies to the entire cluster. As a result, any group hosted in a mutual TLS cluster must be a mutual TLS group, and all its members must be hosted on a mutual TLS cluster.

The server gateway has a set of accepted certificate subjects. As part of the client certificate verification, the server rejects a connection with a certificate that has a subject not specified in the allowed list. Before a member can register with a cluster that is configured with mutual TLS, you must add the certificate subject of that member to the allowed list of the MGM. Once a member is successfully onboarded, the MGM distributes the certificate subject of the member to all other members in the group. The gateway in each member cluster uses this to accept TLS connections from any onboarded member.

For information about how to onboard to dynamic networks that use mutual TLS, see the [operating tutorial](operating-tutorials/onboarding/mutual-tls.md). Mutual TLS is relevant only for [dynamic networks](../deploying/network-types.html#dynamic-networks), as [static networks](../deploying/network-types.html#static-networks) can only span a single cluster.
