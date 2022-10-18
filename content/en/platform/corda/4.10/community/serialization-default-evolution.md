---
aliases:
- /head/serialization-default-evolution.html
- /HEAD/serialization-default-evolution.html
- /serialization-default-evolution.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-9-serialization-default-evolution
    parent: corda-community-4-9-serialization-index
    weight: 1030
tags:
- serialization
- default
- evolution
title: Default Class Evolution
---


# Default class evolution


Corda’s serialization framework supports minor modifications to default classes without requiring external modification or annotation. You can:

* Add nullable properties.
* Add non-nullable properties *if* you also provide an annotated constructor.
* Remove properties.
* Reorder constructor parameters.


## Adding nullable properties

You can add nullable properties without any additional code. For example:


```kotlin
// Initial instance of the class
data class Example1 (val a: Int, b: String) // (Version A)

// Class post addition of property c
data class Example1 (val a: Int, b: String, c: Int?) // (Version B)
```


If a node has version A of class `Example1`, it can deserialize a blob that has been serialized by a node with version B of `Example1`. The framework treats it as a removed property.

A node with class `Example1` at version B can deserialize a serialized version A of `Example1` without
any modification. The property is nullable, so it provides `null` to the constructor.


## Adding non-nullable properties

If you add a non-nullable property, you need to add some additional code:


```kotlin
// Initial instance of the class
data class Example2 (val a: Int, b: String) // (Version A)

// Class post addition of property c
data class Example1 (val a: Int, b: String, c: Int) { // (Version B)
     @DeprecatedConstructorForDeserialization(1)
     constructor (a: Int, b: String) : this(a, b, 0) // 0 has been determined as a sensible default
}
```

For this example to work, you must add a new constructor. The constructor allows nodes that have the class at version B to create an
instance from the serialized form of that class in an older version (version A). The example provides A sensible default for the missing value is provided for instantiation of the non-null property.

{{< note >}}
The `@DeprecatedConstructorForDeserialization` annotation indicates to the
serialization framework that it should use that constructor to build instances of the
object when evolution is required. If the annotation indicates an order of precedence, it passes an integer parameter (see example below).


{{< /note >}}
As with nullable properties, if a node has version A of class `Example1`, it can deserialize a blob that has been serialized by a node with version B of `Example1`.  It treats them as if the property has been removed.


### Constructor versioning

If you add multiple non-nullable properties over time, then a class may need
to deserialize several forms of the class. Select the correct constructor to maximize information extraction.

Consider this example:


```kotlin
// The original version of the class
data class Example3 (val a: Int, val b: Int)
```
```kotlin
// The first alteration, property c added
data class Example3 (val a: Int, val b: Int, val c: Int)
```



```kotlin
// The second alteration, property d added
data class Example3 (val a: Int, val b: Int, val c: Int, val d: Int)
```



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


In this case, the deserializer must deserialize instances of class `Example3` that were serialized as:


```kotlin
Example3 (1, 2)             // example I
Example3 (1, 2, 3)          // example II
Example3 (1, 2, 3, 4)       // example III
Example3 (1, 2, 3, 4, 5)    // example IV
```


Examples I, II, and III require evolution, so you need to select a constructor for them. Here, it's difficult to tell which constructor to use because there is no versioning. For example, example II could use ‘alt constructor 2’ which matches
its arguments most tightly. It could also use ‘alt constructor 1’ and not instantiate parameter c:

`constructor (a: Int, b: Int, c: Int) : this(a, b, c, -1, -1)`

or

`constructor (a: Int, b: Int) : this(a, b, -1, -1, -1)`

You can remove this ambiguity by adding version numbers to the constructor
annotation. This gives a strict precedence order to the constructor selection:


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


The framework selects constructors in descending order, until one enables construction. Deserializing examples I to IV would
result in:


```kotlin
Example3 (1, 2, -1, -1, -1) // example I
Example3 (1, 2, 3, -1, -1)  // example II
Example3 (1, 2, 3, 4, -1)   // example III
Example3 (1, 2, 3, 4, 5)    // example IV
```



## Removing properties

Removing non-nullable properties is impossible. If a node receives a message containing a serialized form of an object that has fewer properties than it requires for construction, it can't determine sensible defaults.

It is technically possible to [remove nullable properties](https://medium.com/corda/a-developers-primer-on-cordapp-upgrades-3806c2e7f81e) in some circumstances, but it often has unintended consequences. Deprecate the field instead.


## Reordering constructor parameter order

You can reorder properties (in Kotlin, this corresponds to constructor parameters) freely. The evolution serializer maps the class's serialization to its current constructor parameter order. This is important to our AMQP framework as it
constructs objects using their primary (or annotated) constructor. The ordering of that constructor's parameters determine the way
an object’s properties were serialized into the byte stream.

For an illustrative example, consider a simple class:


```kotlin
data class Example5 (val a: Int, val b: String)

val e = Example5(999, "hello")
```


When you serialize `e`, its properties are encoded in the order of its primary constructor's parameters:

`999,hello`

If you reorder those parameters post-serialization, then deserializing without evolution will fail with a basic
type error. This is because the framework would attempt to create the new value of `Example5` with the values provided in the wrong order:


```kotlin
// changed post serialisation
data class Example5 (val b: String, val a: Int)
```



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


## Related content

Learn more about:

* [Serialization](serialization.md)
* [Enum evolution](serialization-enum-evolution.md)
* [Wire formatting](wire-format.md)
