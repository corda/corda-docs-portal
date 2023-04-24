---
date: '2023-04-07'
title: "Export the Group Policy"
menu:
  corda5:
    parent: corda5-networks-mgm
    identifier: corda5-networks-mgm-group-policy
    weight: 6000
section_menu: corda5
draft: "true"
---
Once the MGM is onboarded, you can export a group policy file with the MGM connection details. To output the full contents of the `GroupPolicy.json` file to package within the {{< tooltip >}}CPI{{< definition term="CPI" >}}{{< /tooltip >}} for members, run the following:
{{< tabs >}}
{{% tab name="Bash"%}}
```shell
mkdir -p "~/Desktop/register-member"
curl -u $REST_API_USER:$REST_API_PASSWORD -X GET $REST_API_URL/mgm/$MGM_HOLDING_ID/info > "~/Desktop/register-member/GroupPolicy.json"
```
{{% /tab %}}
{{% tab name="PowerShell" %}}
```shell
md ~/register-member -Force
Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Uri "$API_URL/mgm/$MGM_HOLDING_ID/info" | ConvertTo-Json -Depth 4 > ~/register-member/GroupPolicy.json
```
{{% /tab %}}
{{< /tabs >}}

You can now use the MGM to [set up members in your network]({{< relref"../members/overview.md" >}}).
