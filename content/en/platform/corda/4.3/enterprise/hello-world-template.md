---
aliases:
- /releases/4.3/hello-world-template.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-3:
    identifier: corda-enterprise-4-3-hello-world-template
    parent: corda-enterprise-4-3-hello-world-introduction
    weight: 1010
tags:
- template
title: The CorDapp Template
---




# The CorDapp Template

When writing a new CorDapp, you’ll generally want to start from one of the standard templates:


* The [Java Cordapp Template](https://github.com/corda/cordapp-template-java)
* The [Kotlin Cordapp Template](https://github.com/corda/cordapp-template-kotlin)

The Cordapp templates provide the boilerplate for developing a new CorDapp. CorDapps can be written in either Java or Kotlin. We will be
providing the code in both languages throughout this tutorial.

Note that there’s no need to download and install Corda itself. The required libraries are automatically downloaded from an online Maven
repository and cached locally.


## Downloading the template

Open a terminal window in the directory where you want to download the CorDapp template, and run the following command:

{{< tabs name="tabs-1" >}}
{{% tab name="java" %}}
```java
git clone https://github.com/corda/cordapp-template-java.git ; cd cordapp-template-java
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
git clone https://github.com/corda/cordapp-template-kotlin.git ; cd cordapp-template-kotlin
```
{{% /tab %}}

{{< /tabs >}}


## Opening the template in IntelliJ

Once the template is download, open it in IntelliJ by following the instructions here:
[https://docs.corda.net/tutorial-cordapp.html#opening-the-example-cordapp-in-intellij](https://docs.corda.net/tutorial-cordapp.html#opening-the-example-cordapp-in-intellij).


## Template structure

For this tutorial, we will only be modifying the following files:

{{< tabs name="tabs-2" >}}
{{% tab name="java" %}}
```java
// 1. The state
contracts/src/main/java/com/template/states/TemplateState.java

// 2. The flow
workflows/src/main/java/com/template/flows/Initiator.java
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
// 1. The state
contracts/src/main/kotlin/com/template/states/TemplateState.kt

// 2. The flow
workflows/src/main/kotlin/com/template/flows/Flows.kt
```
{{% /tab %}}

{{< /tabs >}}


## Progress so far

We now have a template that we can build upon to define our IOU CorDapp. Let’s start by defining the `IOUState`.
