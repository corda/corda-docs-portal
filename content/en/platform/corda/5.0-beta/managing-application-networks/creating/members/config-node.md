---
date: '2023-04-13'
title: "Configure Communication Properties"
menu:
  corda-5-beta:
    identifier: corda-5-beta-app-networks-members-node-config
    parent: corda-5-beta-app-networks-members
    weight: 4000
section_menu: corda-5-beta
---

You must configure the virtual node as a network participant with the properties required for peer-to-peer messaging. The order is slightly different to MGM onboarding because you must perform this step before registering a member.

To configure the member virtual node, run the following command, setting these properties: 

* `p2pTlsCertificateChainAlias` — the alias used when importing the TLS certificate.
* `sessionKeyId` — the [session key ID previously generated]({{< relref "./key-pairs.md#generate-a-session-initiation-key-pair" >}}).
* `useClusterLevelTlsCertificateAndKey` — `true` if the TLS certificate and key are cluster-level certificates and keys.

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "useClusterLevelTlsCertificateAndKey": true, "sessionKeyId": "'$SESSION_KEY_ID'"}' $API_URL/network/setup/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/network/setup/$HOLDING_ID" -Method Put -Body (ConvertTo-Json @{
    p2pTlsCertificateChainAlias = "p2p-tls-cert"
    useClusterLevelTlsCertificateAndKey = $true
    sessionKeyId = $SESSION_KEY_ID
})
```
{{% /tab %}}
{{< /tabs >}}