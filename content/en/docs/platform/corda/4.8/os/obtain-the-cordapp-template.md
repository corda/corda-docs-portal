---
aliases:
- /head/hello-world-template.html
- /HEAD/hello-world-template.html
- /hello-world-template.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-8:
    identifier: corda-os-4-8-hello-world-template
    parent: corda-os-4-8-hello-world-introduction
    weight: 1010
tags:
- template
title: Get the CorDapp Template
---

# Get the CorDapp Template

When writing a new CorDapp, it is helpful to start from one of the following standard templates:

* [Java CorDapp template](https://github.com/corda/cordapp-template-java)
* [Kotlin CorDapp template](https://github.com/corda/cordapp-template-kotlin)

The CorDapp templates provide the boilerplate for developing a new CorDapp. CorDapps can be written in either Java or Kotlin. Sample code is provided in both languages throughout this tutorial.

{{< note >}}

You do not have to download and install Corda. The required libraries are automatically downloaded from an online Maven
repository and cached locally.

{{< /note >}}


## Download the template

1. Open a terminal window in the directory where you want to download the CorDapp template, and run the following command:

   {{< tabs name="tabs-1" >}}
   {{% tab name="kotlin" %}}
   ```kotlin
   git clone https://github.com/corda/cordapp-template-kotlin.git
   ```
   {{% /tab %}}

   {{% tab name="java" %}}
   ```java
   git clone https://github.com/corda/cordapp-template-java.git
   ```
   {{% /tab %}}

   {{< /tabs >}}

2. Once you have cloned the repository you wish to use, navigate to the correct subdirectory:

   {{< tabs name="tabs-2" >}}
   {{% tab name="kotlin" %}}
   ```kotlin
   cd cordapp-template-kotlin
   ```
   {{% /tab %}}

   {{% tab name="java" %}}
   ```java
   cd cordapp-template-java
   ```
   {{% /tab %}}

   {{< /tabs >}}


3. Once you have successfully cloned the CorDapp template, open the `cordapp-template-kotlin` or `cordapp-template-java` in IntelliJ IDEA.

   If you are unsure of how to open a CorDapp in IntelliJ, see the documentation on [Running a sample CorDapp](tutorial-cordapp.html##opening-the-sample-cordapp-in-intellij-idea).


## Template structure

For this tutorial, you will only be modifying the following files:

{{< tabs name="tabs-3" >}}

{{% tab name="kotlin" %}}
```kotlin
// 1. The state
contracts/src/main/kotlin/com/template/states/TemplateState.kt

// 2. The flow
workflows/src/main/kotlin/com/template/flows/Flows.kt
```
{{% /tab %}}

{{% tab name="java" %}}
```java
// 1. The state
contracts/src/main/java/com/template/states/TemplateState.java

// 2. The flow
workflows/src/main/java/com/template/flows/Initiator.java
```
{{% /tab %}}

{{< /tabs >}}


## Progress so far

You now have a template that you can build upon to define your IOU CorDapp. Let’s start by defining the `IOUState`.
