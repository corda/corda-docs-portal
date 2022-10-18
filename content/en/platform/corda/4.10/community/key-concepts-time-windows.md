---
aliases:
- /head/key-concepts-time-windows.html
- /HEAD/key-concepts-time-windows.html
- /key-concepts-time-windows.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-9-key-concepts-time-windows
    parent: corda-community-4-9-key-concepts
    weight: 1100
tags:
- concepts
- time
- windows
title: Time-windows
---


# Time windows

## Summary

* If a transaction includes a time window, it can only be committed during that window
* The notary is the timestamping authority. The notary only commits transactions that are inside the time window.
* Time windows can have a start and end time, or be open at either end.

## Video

{{% vimeo 213879314 %}}

## Time in a distributed system

The [notary cluster](../../../../../en/platform/corda/4.8/open-source/key-concepts-notaries.md) acts as the *timestamping authority*.
It verifies that a transaction occurred during a specific time window before notarizing it.

[Nodes](key-concepts-node.md) get time window signatures to prove a transaction happened before, during, or after a specific time. The notary timestamps and notarizes at the same time, so if the node doesn't need to commit to the associated transaction, it can reveal the time window in the future.

A node may not send a transaction to the notary right away—they might need to circulate the transaction to other nodes involved in the transaction, or request human sign-off. Even if the node sends it as soon as it's generated, the node's clock and the notary's clock will never be perfectly in sync due to latency and physics. This means that the timestamp on a transaction is usually different from the time it was created.
* Issues of physics and network latency
* Between inserting the command and getting the notary to sign there may be many other steps, such as sending the transaction to other parties involved in the
trade, or requesting human sign-off.

## Time windows

Times in transactions are specified as time *windows*, not absolute times. Time windows can be open-ended, and specify only
“before” **or** “after”, or they can be fully bounded.

{{< figure alt="time window" width=80% zoom="/en/images/time-window.gif" >}}

When both a before and an after time are included the transaction occurred at some point within that time window.

Time windows let you represent transactions that follow different models, such as those that occur:

* At some point after the given time, such as after a maturity event.
* At any time before the given time, such as before a bankruptcy event.
* Around the given time, such as on a specific day.

If you need to convert a time window to an absolute time, such as for display purposes, you can use a utility method to calculate the midpoint.

{{< note >}}
Most notaries use [GPS/NaviStar time](https://www.usno.navy.mil/USNO/time/display-clocks/simpletime) as defined by the atomic clocks at the US Naval Observatory. This time feed is extremely accurate and available globally for free.

{{< /note >}}
