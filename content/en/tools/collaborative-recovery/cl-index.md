---
date: '2021-04-24T00:00:00Z'
section_menu: tools
description: "Documentation for Collaborative Recovery; this is a secure, privacy-oriented solution that helps you identify and retrieve data if you ever encounter a disaster recovery (DR) scenario on your business network"
menu:
  tools:
    name: Collaborative recovery
    weight: 600
    identifier: tools-collaborative-recovery
title: Collaborative Recovery
---

# Collaborative Recovery

{{< note >}}
The Collaborative Recovery solution, along with the associated CorDapps (LedgerSync and LedgerRecover), is deprecated in Corda 4.11 and will be removed in Corda 4.12. You are now advised to use the new recovery tools introduced in version 4.11, as detailed in the [Corda Enterprise Edition 4.11 release notes]({{< relref "../../platform/corda/4.11/enterprise/release-notes-enterprise.md#corda-enterprise-edition-411-release-notes-1" >}}).
{{</ note >}}

Collaborative Recovery is a secure, privacy-oriented solution that helps you identify and retrieve data if you ever encounter a disaster recovery (DR) scenario on your Business Network.

Once you have installed the Collaborative Recovery CorDapps, you can safely use Collaborative Recovery to detect potential ledger inconsistencies and recover any missing data from parties you have transacted with. Designed to ensure the continued security and privacy of Corda, this feature runs in the background, acting as an additional layer of security when using Corda.

As the name suggests, this is a collaborative method for recovering data. For maximum peace of mind, you should seek agreement across your Business Network to make this feature part of the overall disaster recovery policy.
