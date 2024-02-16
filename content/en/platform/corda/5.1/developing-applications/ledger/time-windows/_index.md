---
description: "Learn the fundamentals of Corda 5 transaction time windows."
title: "Time Windows"
date: 2023-06-08
menu:
  corda51:
    identifier: corda51-fundamentals-ledger-time-window
    parent: corda51-fundamentals-ledger
    weight: 7000
---

# Time Windows

Every {{< tooltip >}}transaction{{< /tooltip >}} includes a *time window*: the transaction can only be committed during that window. Times in transactions are specified as time windows and not absolute times. Transaction time windows must have one of the following:
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
