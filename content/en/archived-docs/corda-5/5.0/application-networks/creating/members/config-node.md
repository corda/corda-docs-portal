---
date: '2023-04-13'
version: 'Corda 5.0'
title: "Configure Communication Properties for the Member"
menu:
  corda5:
    identifier: corda5-networks-members-node-config
    parent: corda5-networks-members
    weight: 4000
    name: "Configure Communication Properties"
section_menu: corda5
---

# Configure Communication Properties for the Member

You must configure the virtual node as a network participant with the properties required for peer-to-peer messaging. The order is slightly different to {{< tooltip >}}MGM{{< /tooltip >}} onboarding because you must perform this step before registering a {{< tooltip >}}member{{< /tooltip >}}.

To configure the member virtual node, run the following command, setting these properties: 

* `p2pTlsCertificateChainAlias` — the alias used when importing the {{< tooltip >}}TLS{{< /tooltip >}} certificate.
* `sessionKeysAndCertificates` — contains a list of objects as you can specify multiple {{< tooltip >}}session initiation keys{{< /tooltip >}} and certificates. Each object contains the fields *[sessionKeyId]({{< relref "./key-pairs.md#generate-a-session-initiation-key-pair" >}})*, *sessionCertificateChainAlias* and *preferred*. One object in the list must have the *preferred* Boolean field set to `true`. The list cannot be empty. 
* `useClusterLevelTlsCertificateAndKey` — `true` if the TLS certificate and key are cluster-level certificates and keys.

{{< tabs >}}
{{% tab name="Bash"%}}
```bash
curl -k -u $REST_API_USER:$REST_API_PASSWORD -X PUT -d '{"p2pTlsCertificateChainAlias": "p2p-tls-cert", "useClusterLevelTlsCertificateAndKey": true, "sessionKeysAndCertificates": [{"sessionKeyId": "'$SESSION_KEY_ID'", "preferred": true}]}' $REST_API_URL/network/setup/$HOLDING_ID
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$REST_API_URL/network/setup/$HOLDING_ID" -Method Put -Body (ConvertTo-Json @{
    p2pTlsCertificateChainAlias = "p2p-tls-cert"
    useClusterLevelTlsCertificateAndKey = $true
    sessionKeysAndCertificates = [{"sessionKeyId": "'$SESSION_KEY_ID'", "preferred": true}]
})
```
{{% /tab %}}
{{< /tabs >}}