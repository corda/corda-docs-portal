---
date:
menu:
tags:
- end of life
- schedule
- support
title: End of life schedule
weight:
---

Use the following table to track the end of life schedule for each version of Corda and CENM. Each version of Corda Enterprise, Corda Community Edition, and CENM has support available from R3 for a fixed period. After this period has ended, these versions are no longer supported by R3 and associated documentation is archived. You should always aim to upgrade to the latest version of Corda or CENM whenever possible.

Definitions:

* **End of maintenance:** This release will no longer receive functional patches after the date shown.
* **End of security:** This release will no longer be eligible for security patches after the date shown.
* **End of support:** Support provided by R3 is no longer available after this date.

{{< note >}}
All dates refer to the end of the month indicated.
{{< /note >}}

## Corda 4

{{< note >}}
The highest released version of Corda 4 Enterprise Edition at any point in time will be supported, including maintenance, until at least 31st December 2029 or until superseded by a higher version number of Corda 4 Enterprise Edition, at which point the dates in the table take precedence.
{{< /note >}}

{{< snippet "corda-4/end-of-life-corda4.md" >}}

## CENM

{{< note >}}
The highest released version of Corda Enterprise Network Manager at any
point in time will be supported, including maintenance, until at least
31st December 2029 or until superseded by a higher version number of
Corda Enterprise Network Manager, at which point the dates in the table
take precedence.
{{< /note >}}

The following table lists the end of life schedules for all CENM versions:

<style>
table th:first-of-type {
    width: 40%;
}
table th:nth-of-type(2) {
    width: 15%;
}
table th:nth-of-type(3) {
    width: 15%;
}
table th:nth-of-type(4) {
    width: 15%;
}
table th:nth-of-type(5) {
    width: 15%;
}
</style>

| Version                                        | Date of Release     | End of Maintenance     | End of Security     | End of Support     |
| ---------------------------------------------- | ------------------- | ---------------------- | ------------------- | ------------------ |
| **Corda Enterprise Network Manager 1.3**       | 06/2020             | 06/2022                | 6/2023              | 06/2023            |
| **Corda Enterprise Network Manager 1.4**       | 09/2020             | 09/2022                | 09/2023             | 09/2023            |
| **Corda Enterprise Network Manager 1.5**       | 12/2020             | 12/2023                | 12/2024             | 12/2024            |
| **Corda Enterprise Network Manager 1.6\***       | 12/2023             | 12/2026                | 12/2026             | 12/2026            |
| **Corda Enterprise Network Manager 1.7\*\***   | 09/2025             | 09/2027                | 09/2028             | 09/2028            |

\* Corda Enterprise Network Manager 1.6 is a low-risk, drop-in
replacement for 1.5 with security related minor dependency updates,
small additional options (see [release notes]({{< relref "1.6/cenm/release-notes.md" >}})) and no changes to existing
features

** Not released yet. Future releases as indicative only.