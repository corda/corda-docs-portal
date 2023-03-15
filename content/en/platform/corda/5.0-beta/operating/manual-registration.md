---
date: '2023-03-15'
title: "Manual Registration"
menu:
  corda-5-beta:
    identifier: corda-5-beta-manual-egistration
    parent: corda-5-beta-operate
    weight: 1000
section_menu: corda-5-beta
---

You can configure membership groups to approve (or decline) member registration requests manually. The MGM operator can configure the approval method for joining the group, so that requests satisfying pre-defined criteria would require manual approval, while others would be auto-approved. Manual approval presents the request to the MGM operator, and allows the operator to review the request before approving/declining it via the REST API. This applies to registration and re-registration requests alike. The configuration may be added at any point in time, and only affects future registration requests - previously approved members will not be required to re-register.