---
description: "Learn how to re-register an MGM in order to update its member-provided context or endpoint information."
date: '2024-01-11'
title: "Re-register an MGM"
menu:
  corda53:
    identifier: corda53-networks-mgm-reregister
    parent: corda53-networks-mgm
    weight: 6000
---

# Re-register an MGM

An {{< tooltip >}}MGM{{< /tooltip >}} may need to update its own member-provided context; for example, as part of a [platform upgrade]({{< relref "../../upgrading/_index.md" >}}) or [changes to its endpoint information]({{< relref "./endpoints.md">}}). Additionally, an MGM that previously attempted to register but failed may wish to try again. The instructions on this page assume that you have completed the [registration]({{< relref "register.md" >}}) steps.

To re-register an MGM:

1. Send a re-registration request using the common [registration/re-registration endpoint](../../../reference/rest-api/openapi.html#tag/Member-Registration/operation/get_membership__holdingidentityshorthash_):

   {{< tabs >}}
   {{% tab name="Bash"%}}
   ```bash
   export REGISTRATION_REQUEST='{"memberRegistrationRequest":{"context": '$REGISTRATION_CONTEXT'}}'
   curl --insecure -u admin:admin -d "$REGISTRATION_REQUEST" $API_URL/membership/$HOLDING_ID
   ```
   {{% /tab %}}
   {{% tab name="PowerShell" %}}
   ```shell
   $REGISTER_RESPONSE = Invoke-RestMethod -SkipCertificateCheck  -Headers @{Authorization=("Basic {0}" -f $AUTH_INFO)} -Method Post -Uri "$API_URL/membership/$HOLDING_ID" -Body (ConvertTo-Json -Depth 4 @{
       memberRegistrationRequest = @{
           context = $REGISTRATION_CONTEXT
       }
   })
   $REGISTER_RESPONSE.registrationStatus
   ```
   {{% /tab %}}
   {{< /tabs >}}

   This request should return a successful response with the status `SUBMITTED`. The cluster that hosts the MGM processes the request. You can check if the request was approved by checking the status of the registration request.

1. [Upgrade the member {{< tooltip >}}CPIs{{< /tooltip >}}]({{< relref "../../upgrading/_index.md" >}}) to distribute the MGM's `MemberInfo` to the members of the network.

{{< note >}}
If changes made to the MGM's `MemberInfo` are not backwards-compatible, members can not communicate with the MGM until they have successfully updated their CPI. An example of a non backwards-compatible change is changing the endpoint without keeping the old endpoint in the list of endpoints.
{{< /note >}}
