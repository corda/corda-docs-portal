---
title: Commands
date: 2020-10-15T00:00:00+01:00
menu:
  cdl:
    parent: "cdl-to-code"
    identifier: "cdl-to-code-commands"
    weight: 30

tags:
- cdl
- cordapp design language
- contract to code
- cordapp diagram
---

# Commands

The Commands are implemented in the normal way as classes inside an interface class in the `AgreementContract`, each inheriting from CommandData. The list of Commands can be taken from the Path arrows on the Smart Contract view.

AgreementContract.kt:

{{< tabs name="implement the commands" >}}
{{% tab name="kotlin" %}}
```kotlin
class AgreementContract : Contract {
    ...
    interface Commands : CommandData {
        class Propose : Commands
        class Repropose: Commands
        class Reject: Commands
        class Agree: Commands
        class Complete: Commands
    }
    ...
}
```
{{% /tab %}}
{{< /tabs >}}
