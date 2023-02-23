---
date: '2023-02-23'
title: "Mutual TLS"
menu:
  corda-5-beta:
    identifier: corda-5-beta-mutual-tls
    parent: corda-5-beta-operate
    weight: 1000
section_menu: corda-5-beta
---
Corda 5 uses TLS to secure a connection between two clusters. While establishing a TLS connection between the gateways of two clusters, the server gateway sends its certificate to the client gateway. The client gateway verifies the server certificate using its trust root certificate. In mutual TLS, in addition to that, the server gateway also requests the client gateway to send a client certificate and verify that it is using its trust root certificate.

As the gateway manages the TLS connections for an entire cluster, the TLS mode (mutual or one-way) is defined in the gateway configuration and applies to the entire cluster. As a result, any group hosted in a mutual TLS cluster has to be a mutual TLS group, and all its members must be hosted on a mutual TLS cluster.

{{< note >}}
Mutual TLS is relevant only for [dynamic networks](../deploying/network-types.html#dynamic-networks), as [static networks](../deploying/network-types.html#static-networks) can only span a single cluster.
{{< /note >}}

The server gateway has a set of accepted certificate subjects. As part of the client certificate verification, the server rejects a connection with a certificate that has a subject not in the allowed list.

For information about how to onboard to dynamic networks, see the [operating tutorial](operating-tutorials/onboarding/mutual-tls.md).