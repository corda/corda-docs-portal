---
aliases:
- /head/serialization-default-evolution.html
- /HEAD/serialization-default-evolution.html
- /serialization-default-evolution.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-os-4-6:
    identifier: corda-os-4-6-serialization-default-evolution
    parent: corda-os-4-6-serialization-index
    weight: 1030
tags:
- serialization
- default
- evolution
title: Default Class Evolution
---




# Default Class Evolution


Whilst more complex evolutionary modifications to classes require annotating, Corda’s serialization
framework supports several minor modifications to classes without any external modification save
the actual code changes. These are:



* Adding nullable properties
* Adding non nullable properties if, and only if, an annotated constructor is provided
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

If a non null property is added, unlike nullable properties, some additional code is required for
this to work. Consider a similar example to our nullable example above

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
// Initial instance of the class
data class Example2 (val a: Int, b: String) // (Version A)

// Class post addition of property c
data class Example1 (val a: Int, b: String, c: Int) { // (Version B)
     @DeprecatedConstructorForDeserialization(1)
     constructor (a: Int, b: String) : this(a, b, 0) // 0 has been determined as a sensible default
}
```
{{% /tab %}}

{{< /tabs >}}

For this to work we have had to add a new constructor that allows nodes with the class at version B to create an
instance from serialised form of that class from an older version, in this case version A as per our example
above. A sensible default for the missing value is provided for instantiation of the non null property.

{{< note >}}
The `@DeprecatedConstructorForDeserialization` annotation is important, this signifies to the
serialization framework that this constructor should be considered for building instances of the
object when evolution is required.

Furthermore, the integer parameter passed to the constructor if the annotation indicates a precedence
order, see the discussion below.

{{< /note >}}
As before, instances of the class at version A will be able to deserialize serialized forms of example B as it
will simply treat them as if the property has been removed (as from its perspective, they will have been).


### Constructor Versioning

If, over time, multiple non nullable properties are added, then a class will potentially have to be able
to deserialize a number of different forms of the class. Being able to select the correct constructor is
important to ensure the maximum information is extracted.

Consider this example:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
// The original version of the class
data class Example3 (val a: Int, val b: Int)
```
{{% /tab %}}

{{< /tabs >}}

{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
// The first alteration, property c added
data class Example3 (val a: Int, val b: Int, val c: Int)
```
{{% /tab %}}

{{< /tabs >}}

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
// The second alteration, property d added
data class Example3 (val a: Int, val b: Int, val c: Int, val d: Int)
```
{{% /tab %}}

{{< /tabs >}}

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}
```kotlin
// The third alteration, and how it currently exists, property e added
data class Example3 (val a: Int, val b: Int, val c: Int, val d: Int, val: Int e) {
    // NOTE: version number purposefully omitted from annotation for demonstration purposes
    @DeprecatedConstructorForDeserialization
    constructor (a: Int, b: Int) : this(a, b, -1, -1, -1)          // alt constructor 1
    @DeprecatedConstructorForDeserialization
    constructor (a: Int, b: Int, c: Int) : this(a, b, c, -1, -1)   // alt constructor 2
    @DeprecatedConstructorForDeserialization
    constructor (a: Int, b: Int, c: Int, d) : this(a, b, c, d, -1) // alt constructor 3
}
```
{{% /tab %}}

{{< /tabs >}}

In this case, the deserializer has to be able to deserialize instances of class `Example3` that were serialized as, for example:

{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}
```kotlin
Example3 (1, 2)             // example I
Example3 (1, 2, 3)          // example II
Example3 (1, 2, 3, 4)       // example III
Example3 (1, 2, 3, 4, 5)    // example IV
```
{{% /tab %}}

{{< /tabs >}}

Examples I, II, and III would require evolution and thus selection of constructor. Now, with no versioning applied there
is ambiguity as to which constructor should be used. For example, example II could use ‘alt constructor 2’ which matches
it’s arguments most tightly or ‘alt constructor 1’ and not instantiate parameter c.

`constructor (a: Int, b: Int, c: Int) : this(a, b, c, -1, -1)`

or

`constructor (a: Int, b: Int) : this(a, b, -1, -1, -1)`

Whilst it may seem trivial which should be picked, it is still ambiguous, thus we use a versioning number in the constructor
annotation which gives a strict precedence order to constructor selection. Therefore, the proper form of the example would
be:

{{< tabs name="tabs-8" >}}
{{% tab name="kotlin" %}}
```kotlin
// The third alteration, and how it currently exists, property e added
data class Example3 (val a: Int, val b: Int, val c: Int, val d: Int, val: Int e) {
    @DeprecatedConstructorForDeserialization(1)
    constructor (a: Int, b: Int) : this(a, b, -1, -1, -1)          // alt constructor 1
    @DeprecatedConstructorForDeserialization(2)
    constructor (a: Int, b: Int, c: Int) : this(a, b, c, -1, -1)   // alt constructor 2
    @DeprecatedConstructorForDeserialization(3)
    constructor (a: Int, b: Int, c: Int, d) : this(a, b, c, d, -1) // alt constructor 3
}
```
{{% /tab %}}

{{< /tabs >}}

Constructors are selected in strict descending order taking the one that enables construction. So, deserializing examples I to IV would
give us:

{{< tabs name="tabs-9" >}}
{{% tab name="kotlin" %}}
```kotlin
Example3 (1, 2, -1, -1, -1) // example I
Example3 (1, 2, 3, -1, -1)  // example II
Example3 (1, 2, 3, 4, -1)   // example III
Example3 (1, 2, 3, 4, 5)    // example IV
```
{{% /tab %}}

{{< /tabs >}}


## Removing Properties

Property removal is effectively a mirror of adding properties (both nullable and non nullable) given that this functionality
is required to facilitate the addition of properties. When this state is detected by the serialization framework, properties
that don’t have matching parameters in the main constructor are simply omitted from object construction.

{{< tabs name="tabs-10" >}}
{{% tab name="kotlin" %}}
```kotlin
// Initial instance of the class
data class Example4 (val a: Int?, val b: String?, val c: Int?) // (Version A)


// Class post removal of property 'a'
data class Example4 (val b: String?, c: Int?) // (Version B)
```
{{% /tab %}}

{{< /tabs >}}

In practice, what this means is removing nullable properties is possible. However, removing non nullable properties isn’t because
a node receiving a message containing a serialized form of an object with fewer properties than it requires for construction has
no capacity to guess at what values should or could be used as sensible defaults. When those properties are nullable it simply sets
them to null.


## Reordering Constructor Parameter Order

Properties (in Kotlin this corresponds to constructor parameters) may be reordered freely. The evolution serializer will create a
mapping between how a class was serialized and its current constructor parameter order. This is important to our AMQP framework as it
constructs objects using their primary (or annotated) constructor. The ordering of whose parameters will have determined the way
an object’s properties were serialised into the byte stream.

For an illustrative example consider a simple class:

{{< tabs name="tabs-11" >}}
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

{{< tabs name="tabs-12" >}}
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

