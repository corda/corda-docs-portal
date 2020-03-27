---
aliases:
- /releases/3.0/hello-world-template.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-hello-world-template
    parent: corda-enterprise-3-0-hello-world-introduction
    weight: 1010
tags:
- template
title: The CorDapp Template
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}




# The CorDapp Template

When writing a new CorDapp, you’ll generally want to base it on the standard templates:


* The [Java Cordapp Template](https://github.com/corda/cordapp-template-java)
* The [Kotlin Cordapp Template](https://github.com/corda/cordapp-template-kotlin)

The Cordapp templates provide the required boilerplate for developing a CorDapp, and allow you to quickly deploy your
CorDapp onto a local test network of dummy nodes to test its functionality.

CorDapps can be written in both Java and Kotlin, and will be providing the code in both languages in this tutorial.

Note that there’s no need to download and install Corda itself. Corda V1.0’s required libraries will be downloaded
automatically from an online Maven repository.


## Downloading the template

To download the template, open a terminal window in the directory where you want to download the CorDapp template, and
run the following command:

```bash
git clone https://github.com/corda/cordapp-template-java.git ; cd cordapp-template-java

*or*

git clone https://github.com/corda/cordapp-template-kotlin.git ; cd cordapp-template-kotlin
```


## Opening the template in IntelliJ

Once the template is download, open it in IntelliJ by following the instructions here:
[https://docs.corda.net/tutorial-cordapp.html#opening-the-example-cordapp-in-intellij](https://docs.corda.net/tutorial-cordapp.html#opening-the-example-cordapp-in-intellij).


## Template structure

The template has a number of files, but we can ignore most of them. We will only be modifying the following files:

{{< tabs name="tabs-1" >}}
{{% tab name="java" %}}
```java
// 1. The state
cordapp-contracts-states/src/main/java/com/template/TemplateState.java

// 2. The flow
cordapp/src/main/java/com/template/TemplateFlow.java
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
// 1. The state
cordapp-contracts-states/src/main/kotlin/com/template/StatesAndContracts.kt

// 2. The flow
cordapp/src/main/kotlin/com/template/App.kt
```
{{% /tab %}}

{{< /tabs >}}


## Clean up

To prevent build errors later on, we should delete the following files before we begin:


* Java: `cordapp/src/main/java/com/template/TemplateClient.java`
* Kotlin: `cordapp/src/main/kotlin/com/template/Client.kt`


## Progress so far

We now have a template that we can build upon to define our IOU CorDapp. Let’s start by defining the `IOUState`.

