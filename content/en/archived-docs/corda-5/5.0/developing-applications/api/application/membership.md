---
date: '2023-02-10'
version: 'Corda 5.0'
title: "application.membership"
menu:
  corda5:
    identifier: corda5-api-app-membership
    parent: corda5-api-application
    weight: 4000
section_menu: corda5
---
# net.corda.v5.application.membership
The `membership` package provides services for working with {{< tooltip >}}membership groups{{< /tooltip >}}. The <a href="../../../../../../api-ref/corda/5.0/net/corda/v5/application/membership/MemberLookup.html" target="_blank">`MemberLookup`</a> service allows a {{< tooltip >}}flow{{< /tooltip >}} to discover what counterparties are available in the membership group or retrieve full details of a counterparty with a given name.

For information about other services that you can use to retrieve information about a {{< tooltip >}}member{{< /tooltip >}}, see the [membership module]({{< relref "../api-membership.md" >}}).
