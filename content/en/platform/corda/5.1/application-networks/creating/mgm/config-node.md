---
description: "Learn how to configure the communication properties for the MGM."
date: '2023-04-13'
version: 'Corda 5.1'
title: "Configure Communication Properties for the MGM"
menu:
  corda51:
    parent: corda51-networks-mgm
    identifier: corda51-networks-mgm-config-node
    weight: 5000
    name: "Configure Communication Properties"
section_menu: corda51
---

# Configure Communication Properties for the MGM

To configure the {{< tooltip >}}MGM{{< /tooltip >}} virtual node as a network participant with the properties required for peer-to-peer messaging, run the following command, setting these properties:

* `p2pTlsCertificateChainAlias` — the alias used when importing the {{< tooltip >}}TLS{{< /tooltip >}} certificate.
* `p2pTlsTenantId` — the tenant ID under which the TLS cert was stored ("p2p" for cluster level).
* `sessionKeysAndCertificates` — contains a list of objects as you can specify multiple {{< tooltip >}}session initiation keys{{< /tooltip >}} and certificates. Each object contains the fields *[sessionKeyId]({{< relref "./key-pairs.md#generate-a-session-initiation-key-pair" >}})*, *sessionCertificateChainAlias* and *preferred*. One object in the list must have the *preferred* Boolean field set to `true`. The list cannot be empty.
* `useClusterLevelTlsCertificateAndKey` - `true` if the TLS certificate and key are cluster-level certificates and keys.

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "useClusterLevelTlsCertificateAndKey": true, "sessionKeysAndCertificates": [{"sessionKeyId": "'$SESSION_KEY_ID'", "preferred": true}]}' $REST_API_URL/network/setup/$MGM_HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/network/setup/$MGM_HOLDING_ID" -Method Put -Body (ConvertTo-Json @{
    p2pTlsCertificateChainAlias = "p2p-tls-cert"
    useClusterLevelTlsCertificateAndKey = $true
    sessionKeysAndCertificates" = [{"sessionKeyId": "'$SESSION_KEY_ID'", "preferred": true}]}
})
```
{{% /tab %}}
{{< /tabs >}}
