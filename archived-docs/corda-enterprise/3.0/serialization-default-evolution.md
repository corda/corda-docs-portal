---
aliases:
- /releases/3.0/serialization-default-evolution.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-3-0:
    identifier: corda-enterprise-3-0-serialization-default-evolution
    parent: corda-enterprise-3-0-other-docs
    weight: 1030
tags:
- serialization
- default
- evolution
title: Default Class Evolution
---
{{% important %}}
This documentation is unsupported.
Try [Corda Enterprise 3.3 documentation](/docs/corda-enterprise/3.3/_index.md) instead
{{% /important %}}


# Default Class Evolution


Whilst more complex evolutionary modifications to classes require annotating, Corda’s serialization
framework supports several minor modifications to classes without any external modification save
the actual code changes. These are:



* Adding nullable properties
* Removing properties
* Reordering constructor parameters



## Adding Nullable Properties

The serialization framework allows nullable properties to be freely added. For example:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
// Initial instance of the class
data class Example1 (val a: Int, b: String) // (Version A)

// Class post addition of property c
data class Example1 (val a: Int, b: String, c: Int?) // (Version B)
```
{{% /tab %}}

{{< /tabs >}}

A node with version A of class `Example1`  will be able to deserialize a blob serialized by a node with it
at version B as the framework would treat it as a removed property.

A node with the class at version B will be able to deserialize a serialized version A of `Example1` without
any modification as the property is nullable and will thus provide null to the constructor.


## Adding Non Nullable Properties

Corda Enterprise 3.0 does not support class evolution using non-nullable properties.


## Removing Properties

Property removal is effectively a mirror of adding properties given that this functionality
is required to facilitate the addition of properties. When this state is detected by the serialization framework, properties
that don’t have matching parameters in the main constructor are simply omitted from object construction.

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// Initial instance of the class
data class Example4 (val a: Int?, val b: String?, val c: Int?) // (Version A)


// Class post removal of property 'a'
data class Example4 (val b: String?, c: Int?) // (Version B)
```
{{% /tab %}}

{{< /tabs >}}


## Reordering Constructor Parameter Order

Properties (in Kotlin this corresponds to constructor parameters) may be reordered freely. The evolution serializer will create a
mapping between how a class was serialized and its current constructor parameter order. This is important to our AMQP framework as it
constructs objects using their primary (or annotated) constructor. The ordering of whose parameters will have determined the way
an object’s properties were serialised into the byte stream.

For an illustrative example consider a simple class:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
data class Example5 (val a: Int, val b: String)

val e = Example5(999, "hello")
```
{{% /tab %}}

{{< /tabs >}}

When we serialize `e` its properties will be encoded in order of its primary constructors parameters, so:

`999,hello`

Were those parameters to be reordered post serialisation then deserializing, without evolution, would fail with a basic
type error as we’d attempt to create the new value of `Example5` with the values provided in the wrong order:

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
// changed post serialisation
data class Example5 (val b: String, val a: Int)
```
{{% /tab %}}

{{% tab name="shell" %}}
```shell
| 999 | hello |  <--- Extract properties to pass to constructor from byte stream
   |      |
   |      +--------------------------+
   +--------------------------+      |
                              |      |
deserializedValue = Example5(999, "hello")  <--- Resulting attempt at construction
                              |      |
                              |      \
                              |       \     <--- Will clearly fail as 999 is not a
                              |        \         string and hello is not an integer
data class Example5 (val b: String, val a: Int)
```
{{% /tab %}}

{{< /tabs >}}

