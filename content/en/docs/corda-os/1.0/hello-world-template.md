---
aliases:
- /releases/release-V1.0/hello-world-template.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-1-0:
    identifier: corda-os-1-0-hello-world-template
    parent: corda-os-1-0-hello-world-index
    weight: 1020
tags:
- template
title: The CorDapp Template
---




# The CorDapp Template

When writing a new CorDapp, you’ll generally want to base it on the
[Java Cordapp Template](https://github.com/corda/cordapp-template-java) or the equivalent
[Kotlin Cordapp Template](https://github.com/corda/cordapp-template-kotlin). The Cordapp Template allows you to
quickly deploy your CorDapp onto a local test network of dummy nodes to evaluate its functionality.

Note that there’s no need to download and install Corda itself. As long as you’re working from a stable Milestone
branch, the required libraries will be downloaded automatically from an online repository.

If you do wish to work from the latest snapshot, please follow the instructions
[here](https://docs.corda.net/tutorial-cordapp.html#using-a-snapshot-release).


## Downloading the template

Open a terminal window in the directory where you want to download the CorDapp template, and run the following commands:

```bash
# Clone the template from GitHub:
git clone https://github.com/corda/cordapp-template-java.git ; cd cordapp-template-java

*or*

git clone https://github.com/corda/cordapp-template-kotlin.git ; cd cordapp-template-kotlin
```


## Template structure

We can write our CorDapp in either Java or Kotlin, and will be providing the code in both languages throughout. To
implement our IOU CorDapp in Java, we’ll need to modify three files. For Kotlin, we’ll simply be modifying the
`App.kt` file:

{{< tabs name="tabs-1" >}}
{{% tab name="java" %}}
```java
// 1. The state
src/main/java/com/template/state/TemplateState.java

// 2. The contract
src/main/java/com/template/contract/TemplateContract.java

// 3. The flow
src/main/java/com/template/flow/TemplateFlow.java
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
src/main/kotlin/com/template/App.kt
```
{{% /tab %}}

{{< /tabs >}}


## Progress so far

We now have a template that we can build upon to define our IOU CorDapp.

We’ll begin writing the CorDapp proper by writing the definition of the `IOUState`.

