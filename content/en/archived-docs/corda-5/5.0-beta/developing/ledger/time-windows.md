---
date: '2023-01-05'
title: "Time Windows"
menu:
  corda-5-beta:
    parent: corda-5-beta-ledger
    identifier: corda-5-beta-time-windows
    weight: 8000
section_menu: corda-5-beta
---

Every transaction includes a *time window*: the transaction can only be committed during that window. Times in transactions are specified as time windows and not absolute times. Transaction time windows must have one of the following:
* a start time and an end time
* only an end time

{{< note >}}
Corda requires every transaction to be completed within a specified time, and thus requires a time window that at least specifies an end time. The end time can be long (for example, three months), but must be defined. This is required to implement a more efficient notary protocol where the notary only tracks valid input states.
{{< /note >}}

The notary cluster acts as the timestamping authority. It verifies that a transaction occurred during a specific time window before notarizing it.

A participant may not send a transaction to the notary right away; they might need to circulate the transaction to other participants involved in the transaction, or request human sign-off. Even if the participant sends it as soon as it is generated, the node’s clock and the notary’s clock will never be perfectly in sync due to latency and physics. This means that the timestamp on a transaction is usually different from the time it was created.

When both a before and an after time are included, the transaction occurred at some point within that time window.

Time windows let you represent transactions that follow different models, such as those that occur:

* At some point after a given time, such as after a maturity event.
* At any time before a given time, such as before a bankruptcy event.
* Around a given time, such as on a specific day.

If you need to convert a time window to an absolute time, such as for display purposes, you can use a utility method to calculate the midpoint.
