---
date: '2023-08-10'
version: 'Corda 5.1'
title: "application.membership"
menu:
  corda51:
    identifier: corda51-api-app-membership
    parent: corda51-api-application
    weight: 4000
section_menu: corda51
---
# net.corda.v5.application.membership
The `membership` package provides services for working with {{< tooltip >}}membership groups{{< /tooltip >}}. The <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/membership/MemberLookup.html" target="_blank">`MemberLookup`</a> service allows a {{< tooltip >}}flow{{< /tooltip >}} to discover what counterparties are available in the membership group or retrieve full details of a counterparty with a given name. For more information, see the documentation for the package in the <a href="/en/api-ref/corda/{{<version-num>}}/net/corda/v5/application/membership/package-summary.html" target=" blank">Java API documentation</a>.

For information about other services that you can use to retrieve information about a {{< tooltip >}}member{{< /tooltip >}}, see the [membership module]({{< relref "../api-membership.md" >}}).
