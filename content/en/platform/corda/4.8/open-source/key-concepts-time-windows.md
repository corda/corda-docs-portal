---
aliases:
- /head/key-concepts-time-windows.html
- /HEAD/key-concepts-time-windows.html
- /key-concepts-time-windows.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-key-concepts-time-windows
    parent: corda-os-4-8-key-concepts
    weight: 1100
tags:
- concepts
- time
- windows
title: Time-windows
---


# Time-windows

## Summary

* *If a transaction includes a time-window, it can only be committed during that window*
* *The notary is the timestamping authority and refuses to commit transactions outside the time-window*
* *Time-windows can have a start and end time, or be open at either end*

## Video

{{% vimeo 213879314 %}}

## Time in a distributed system

The [notary cluster](../../../../../en/platform/corda/4.8/open-source/key-concepts-notaries.md) acts as the *timestamping authority*.
It verifies that a transaction occurred during a specific time-window before notarizing it.

A party obtains a time-window signature in order to prove a transaction happened *before*, *on*, or *after* a particular point in time.
As long as the party is not required to commit to the associated transaction, it can choose to reveal this fact at some point in the future. As a result the notary
timestamps and notarizes at the same time.

Thus, the time at which the transaction is sent for notarization may be
different to the transaction creation time. There will never be exact clock synchronization between the party creating the transaction and the notary for two reasons:
* Issues of physics and network latency
* Between inserting the command and getting the notary to sign there may be many other steps, such as sending the transaction to other parties involved in the
trade, or requesting human sign-off.

## Time-windows

Times in transactions are specified as time *windows*, not absolute times. Time-windows can be open-ended, and specify only
“before” **or** “after”, or they can be fully bounded.

{{< figure alt="time window" width=80% zoom="/en/images/time-window.gif" >}}

When both a before and an after time are included, the transaction could have occurred at any point within that time-window.

By creating a range that can be either closed or open at one end, we allow all the following situations to be
modelled:

* A transaction occurring at some point after the given time, such as after a maturity event.
* A transaction occurring at any time before the given time, such as before a bankruptcy event.
* A transaction occurring at some point roughly around the given time, such as on a specific day.

If a time-window needs to be converted to an absolute time, such for display purposes, there is a utility method to
calculate the mid-point.

{{< note >}}
It is assumed that the time feed for a notary is [GPS/NaviStar time as defined by the atomic
clocks at the US Naval Observatory](https://www.usno.navy.mil/USNO/time/display-clocks/simpletime). This time feed is extremely accurate and available globally for free.

{{< /note >}}
