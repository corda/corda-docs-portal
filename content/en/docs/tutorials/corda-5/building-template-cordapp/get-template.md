---
date: 2021-08-24
section_menu: tutorials
menu:
  tutorials:
    parent: corda-5-building-template-cordapp-intro
    name: Get the template
    weight: 100
    identifier: corda-5-building-template-get
title: Get the template
---

Anytime you want to create a new CorDapp, it's helpful to start from one of R3's standard templates:

* [Java CorDapp template](XXX)
* [Kotlin CorDapp template](XXX)

The template is your boilerplate for developing new CorDapps. You can write a CorDapp in any language targeting the JVM. Templates and sample code snippets are provided in Kotlin and Java.

{{< note >}}
You do not have to install Corda. The required Corda 5 Developer Preview libraries are automatically downloaded from  an online Maven repository and cached locally.
{{< /note >}}

<!-- The details for how Corda 5 dev preview is included in the template repo need to be confirmed with Product and SMEs. -->

## Download the template

<!-- Update this section when repo details are provided.-->

1. Decide where you want to store the CorDapp.
2. Open that directory in the command line.
3. Run this command to clone the repository:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```
git clone git@github.com:corda/<kotlin-template-repo>.git
```
{{% /tab %}}

{{% tab name="java" %}}
```
git clone git@github.com:corda/<java-template-repo>.git
```
{{% /tab %}}

{{< /tabs >}}

4. Navigate to the root folder of the project:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```
cd cordapp-template-kotlin
```
{{% /tab %}}

{{% tab name="java" %}}
```
cd cordapp-template-java
```
{{% /tab %}}

{{< /tabs >}}

<!-- Update these code samples with names of repos. -->

5. [Open the CorDapp in IntelliJ IDEA](../run-demo-cordapp.md#open-the-sample-cordapp-in-intellij-idea).

## Next steps

You've now cloned the template project that you will build upon to define your CorDapp. Continue on this learning path by [defining the state](modify-state.md).
