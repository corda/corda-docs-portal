---
date: '2023-06-14'
menu:
  tools:
    identifier: release-notes-archiving
    parent: tools-archiving
    name: "Release notes"
title: Archive Service release notes
weight: 705
---

# Archive Service release notes

The Archive Service is a standalone service that operates on a different release cadence to the Corda platform.

The following table shows the compatibility of the Archive Service versions with Corda Enterprise:

| Archive Service version | Corda Enterprise version | JDK version |
|------------------------|--------------------------|-------------|
| 2.x                    | 4.12.x                   | JDK 17      |

{{< note >}}
If you deviate from the above compatibility guidelines, the Archive Service will not work.
{{< /note >}}

## Corda Enterprise 4.12

### Archive Service 2.0

Archive Service 2.0 is a major release supporting Java 17 and Kotlin 1.9.20. This version works with Corda 4.12.

The 1.x series release notes can be found in the [Archive Service 1.x release notes]({{< relref "../archiving-service-1.x/archiving-release-notes.md" >}}) page.
