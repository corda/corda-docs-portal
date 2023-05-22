---
date: '2023-04-07'
version: 'Corda 5.0'
title: "Configure Communication Properties"
menu:
  corda5:
    parent: corda5-networks-mgm
    identifier: corda5-networks-mgm-config-node
    weight: 5000
section_menu: corda5
---

# Configure Communication Properties

To configure the MGM virtual node as a Network Participant with the properties required for peer-to-peer messaging, run the following command, setting these properties: 

* `p2pTlsCertificateChainAlias` — the alias used when importing the TLS certificate.
* `p2pTlsTenantId` — the tenant ID under which the TLS cert was stored ("p2p" for cluster level).
* `sessionKeyId` — the [session key ID previously generated]({{< relref "./key-pairs.md#assign-a-soft-hsm">}}).
* `useClusterLevelTlsCertificateAndKey` - `true` if the TLS certificate and key are cluster-level certificates and keys.

{{< tabs >}}
{{% tab name="Bash"%}}
```shell
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "useClusterLevelTlsCertificateAndKey": true, "sessionKeyId": "'$SESSION_KEY_ID'"}' $REST_API_URL/network/setup/$MGM_HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/network/setup/$MGM_HOLDING_ID" -Method Put -Body (ConvertTo-Json @{
    p2pTlsCertificateChainAlias = "p2p-tls-cert"
    useClusterLevelTlsCertificateAndKey = $true
    sessionKeyId = $SESSION_KEY_ID
})
```
{{% /tab %}}
{{< /tabs >}}