---
aliases:
- /head/serialization.html
- /HEAD/serialization.html
- /serialization.html
date: '2020-04-07T12:00:00Z'
menu:
  corda-community-4-10:
    identifier: corda-community-4-10-serialization
    parent: corda-community-4-10-serialization-index
    weight: 1010
tags:
- serialization
title: Object serialization
---


# Object serialization



Serialization converts objects into a stream of bytes. Deserialization, the reverse
process, creates objects from a stream of bytes. These two processes take place every time nodes pass objects to each other as
messages, when the node sends objects to or from RPC clients, and when you store transactions in the database.

## Corda's custom, type-safe binary serialization

Corda uses a custom form of type-safe binary serialization, which is more secure than systems that use
weakly or untyped string-based serialization schemes, such as JSON or XML. The benefits of Corda's system include:


* A schema describing what has been serialized included with the data. This allows:
  * Improved versioning, enabling easier interpretation of archived data (for example, trades from
    a decade ago, long after the code has changed) and differing code versions.
  * Ease of writing generic code - for example, user interfaces that can navigate the serialized form of data.
  * Support for cross-platform (non-JVM) interaction, where the format of a class file can be difficult to interpret.

* A platform-independent, documented, and static wire format that is not subject to change with third-party library upgrades.
* Support for open-ended polymorphism, where the number of subclasses of a superclass can expand over time,
  and subclasses do not need to be defined in the schema upfront. This is key to many Corda concepts, such as states.
* Increased security. Deserialized objects go through supported constructors, rather than having
  data inserted directly into their fields without an opportunity to validate consistency or intercept attempts to manipulate
  supposed invariants.
* Improved digital signature handling. Binary formats work better with digital signatures than text based-formats, because it reduces the scope for
  changes that modify syntax but not semantics.


## Whitelisting

In classic Java serialization, any class on the JVM classpath can be deserialized. This can be exploited by adding a stream of malicious bytes to the large set of third-party libraries that are added to the classpath as part of a JVM
application’s dependencies. Corda strictly
controls which classes can be deserialized (and, proactively, serialized) by insisting that each (de)serializable class
is on a whitelist of allowed classes.

To add a class to the whitelist, you must either:


* Add the `@CordaSerializable` annotation to the class. This annotation can be present on the
  class itself, on any super-class of the class, on any interface implemented by the class or its super-classes, or on any
  interface extended by an interface implemented by the class or its super-classes. This is the preferred method.
* Implement the `SerializationWhitelist` interface and specify a list of whitelisted classes.

The built-in default whitelist (see the `DefaultWhitelist` class) allows common JDK classes for
convenience. You cannot edit the default whitelist.

You can see both methods in action in the [client RPC tutorial](../../../../../en/tutorials/corda/4.10/community/supplementary-tutorials/tutorial-clientrpc-api.md). Here's a sample:

```kotlin
// Not annotated, so need to whitelist manually.
data class ExampleRPCValue(val foo: String)

// Annotated, so no need to whitelist manually.
@CordaSerializable
data class ExampleRPCValue2(val bar: Int)

class ExampleRPCSerializationWhitelist : SerializationWhitelist {
    // Add classes like this.
    override val whitelist = listOf(ExampleRPCValue::class.java)
}

```

{{< note >}}
Several of the core interfaces at the heart of Corda are already annotated, so any classes that implement
them are whitelisted automatically. This includes `Contract`, `ContractState`, and `CommandData`.

{{< /note >}}

{{< warning >}}
Java 8 Lambda expressions are not serializable except in flow checkpoints, and then not by default. The syntax to declare a serializable Lambda
expression that will work with Corda is `Runnable r = (Runnable & Serializable) () -> System.out.println("Hello World");`, or
`Callable<String> c = (Callable<String> & Serializable) () -> "Hello World";`.

{{< /warning >}}




## AMQP

Corda uses an extended form of AMQP 1.0 as its binary wire protocol. You can learn more about the [Wire format](wire-format.md) Corda
uses if you intend to parse Corda messages from non-JVM platforms.

Corda serialization is used for:

* Peer-to-peer networking.
* Persisted messages, such as signed transactions and states.


Corda checkpoints flows using a private scheme based on the Kryo framework.

This separation of serialization schemes into different contexts lets Corda use the most suitable framework for a context, rather than
attempting to force a one-size-fits-all approach. Kryo is more suited to the serialization of a program’s stack frames, as it is more flexible
than Corda's AMQP framework in what it can construct and serialize. However, that flexibility makes it difficult to secure. Conversely,
Corda's AMQP framework lets users concentrate on creating a secure framework that can be reasoned about and made safer.

Selection of serialization context is usually opaque to CorDapp developers. The Corda framework selects
the correct context as configured.

This document describes what is currently and what will be supported in the Corda AMQP format from the perspective
of CorDapp developers, to allow CorDapps to take into consideration the future state.  The AMQP serialization format will
continue to apply the whitelisting functionality that is already in place and described in this page.


## Core Types

This section describes the classes and interfaces that the AMQP serialization format supports.


### Collection types

Corda supports the collection types listed below. Any implementation of these types will be mapped to *an* implementation
of the interface or class on the other end. For example, if you use a Guava implementation of a collection, it will
deserialize as the primitive collection type.

The declared types of properties should only use these types, and not any concrete implementation types (for example,
Guava implementations). Collections must specify their generic type. The generic type parameters are included in
the schema, and the element’s type is checked against the generic parameters when deserialized.

```kotlin
java.util.Collection
java.util.List
java.util.Set
java.util.SortedSet
java.util.NavigableSet
java.util.NonEmptySet
java.util.Map
java.util.SortedMap
java.util.NavigableMap
```

Corda explicitly supports the concrete implementation types below. You can use them as the
declared types of properties.

```kotlin
java.util.LinkedHashMap
java.util.TreeMap
java.util.EnumSet
java.util.EnumMap (but only if there is at least one entry)
```


### JVM primitives

All the primitive types are supported:

```kotlin
boolean
byte
char
double
float
int
long
short
```


### Arrays

Corda supports all arrays.


### JDK types

Corda supports these JDK library types:

```kotlin
java.io.InputStream

java.lang.Boolean
java.lang.Byte
java.lang.Character
java.lang.Class
java.lang.Double
java.lang.Float
java.lang.Integer
java.lang.Long
java.lang.Short
java.lang.StackTraceElement
java.lang.String
java.lang.StringBuffer

java.math.BigDecimal

java.security.PublicKey

java.time.DayOfWeek
java.time.Duration
java.time.Instant
java.time.LocalDate
java.time.LocalDateTime
java.time.LocalTime
java.time.Month
java.time.MonthDay
java.time.OffsetDateTime
java.time.OffsetTime
java.time.Period
java.time.YearMonth
java.time.Year
java.time.ZonedDateTime
java.time.ZonedId
java.time.ZoneOffset

java.util.BitSet
java.util.Currency
java.util.UUID
```


### Third-party types

Corda supports these third-party types:

```kotlin
kotlin.Unit
kotlin.Pair

org.apache.activemq.artemis.api.core.SimpleString
```


### Corda types

Corda supports all classes and interfaces in the codebase that are annotated with `@CordaSerializable`.

All Corda exceptions that are expected to be serialized inherit from `CordaThrowable`, either via `CordaException` (for
checked exceptions) or `CordaRuntimeException` (for unchecked exceptions).  Any `Throwable` that is serialized but does
not conform to `CordaThrowable`, is converted to a `CordaRuntimeException`, with the original exception type
and other properties retained within it.



## Custom types

Your own types must adhere to the following rules to be supported.


### Classes


#### General rules

For all classes, you must:

* Include the parameter names in the `.class` file when compiling a class. This is the default in Kotlin.
  In Java, turn it on using the `-parameters` command line option to `javac`. If you cannot recompile classes, such as when using a third-party library, you can use a
  proxy serializer. See [Pluggable Serializers for CorDapps](cordapp-custom-serializers.md).
* Annotate the class with `@CordaSerializable`.
* Make sure Corda supports the declared types of constructor arguments, getters, and setters. If you use generics, the
  generic parameter must be a supported type, an open wildcard (`*`), or a bounded wildcard that has been
  widened to an open wildcard.
* Design your objects so that they *do not* refer to themselves, directly or indirectly. Object graph cycles are not supported.

Super-classes must adhere the same rules, but can be abstract.


#### Constructor instantiation

Corda’s AMQP serialization framework primarily instantiates objects via a specified constructor. First, the constructor determines which properties of an object to serialize. Then, on deserialization, it
instantiates the object with the serialized values.

For immutable state objects to be deserializable, serializable objects must have:

* A Java Bean getter for each of the properties in the constructor, with a name of the form `getX`.  For example, for a constructor
  parameter `foo`, there must be a getter called `getFoo()`. If `foo` is a boolean, the getter may
  optionally be called `isFoo()`. This is why the class must be compiled with parameter names turned on.
* A constructor that takes all the properties you wish to record in the serialized form. This is required for the serialization framework to reconstruct an instance of your class.
* If more than one constructor is provided, the serialization framework needs to know which one to use. You can use the `@ConstructorForDeserialization`
  annotation to indicate which one. For example, if you use a Kotlin class without the `@ConstructorForDeserialization` annotation, the
  *primary constructor* will be selected.


In Kotlin, this maps cleanly to a data class where the getters are synthesized automatically. For example, suppose you
have this data class:

{{< tabs name="tabs-1" >}}
{{% tab name="kotlin" %}}
```kotlin
data class Example (val a: Int, val b: String)
```
{{% /tab %}}

{{< /tabs >}}

Properties `a` and `b` are included in the serialized form.

However, properties not mentioned in the constructor will not be serialized. For example, in the following code,
property `c` will not be considered part of the serialized form:

{{< tabs name="tabs-2" >}}
{{% tab name="kotlin" %}}
```kotlin
data class Example (val a: Int, val b: String) {
    var c: Int = 20
}

var e = Example (10, "hello")
e.c = 100;

val e2 = e.serialize().deserialize() // e2.c will be 20, not 100!!!
```
{{% /tab %}}

{{< /tabs >}}


#### Setter instantiation

{{< warning >}}
Corda uses immutable data structures by default. If you rely heavily on mutable JavaBean style objects, the API may behave unintuitively.
{{< /warning >}}

Constructor-based initialization works best with the API. However, if you require an alternative, Corda can also determine the important elements of an
object by inspecting the getter and setter methods present on the class. If a class *only* has a default
constructor **and** properties, then the serializable properties are determined by the presence of
both a getter and setter for that property, which are both publicly visible. In essence, the class adheres to
the classic idiom of mutable JavaBeans.

On deserialization, a default instance is created first. Then, the setters are invoked on that object to
populate it with the correct values.

For example:

{{< tabs name="tabs-3" >}}
{{% tab name="kotlin" %}}
```kotlin
class Example(var a: Int, var b: Int, var c: Int)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
class Example {
    private int a;
    private int b;
    private int c;

    public int getA() { return a; }
    public int getB() { return b; }
    public int getC() { return c; }

    public void setA(int a) { this.a = a; }
    public void setB(int b) { this.b = b; }
    public void setC(int c) { this.c = c; }
}
```
{{% /tab %}}

{{< /tabs >}}




### Inaccessible private properties

The Corda AMQP serialization framework supports private object properties without publicly
accessible getter methods, but using this development idiom is strongly discouraged because it can create conflict between
the semantics of the object as written and the semantics required to serialize it normally.


{{< tabs name="tabs-4" >}}
{{% tab name="kotlin" %}}
```kotlin
class C(val a: Int, private val b: Int)
```
{{% /tab %}}

{{% tab name="java" %}}
```java
class C {
    public Integer a;
    private Integer b;

    public C(Integer a, Integer b) {
        this.a = a;
        this.b = b;
    }
}
```
{{% /tab %}}

{{< /tabs >}}

Corda states are *not* traditional OOP-style objects. They are signed over, transformed, serialized, and relationally mapped. As such,
all elements should be publicly accessible by design.


{{< warning >}}
Make sure your properties have public visibility, even if your IDE indicates that other settings are possible.

{{< /warning >}}


Providing a public getter, as per the following example, is acceptable:

{{< tabs name="tabs-5" >}}
{{% tab name="kotlin" %}}
```kotlin
class C(val a: Int, b: Int) {
    var b: Int = b
       private set
}
```
{{% /tab %}}

{{% tab name="java" %}}
```java
class C {
    public Integer a;
    private Integer b;

    C(Integer a, Integer b) {
        this.a = a;
        this.b = b;
    }

    public Integer getB() {
        return b;
    }
}
```
{{% /tab %}}

{{< /tabs >}}


### Mismatched class properties/constructor parameters

Consider an example where you wish to ensure that a property of a class, whose type is some form of container, is always sorted using a specific criteria. However, you want to maintain the immutability of the class.

You could codify this as:

{{< tabs name="tabs-6" >}}
{{% tab name="kotlin" %}}
```kotlin
@CordaSerializable
class ConfirmRequest(statesToConsume: List<StateRef>, val transactionId: SecureHash) {
    companion object {
        private val stateRefComparator = compareBy<StateRef>({ it.txhash }, { it.index })
    }

    private val states = statesToConsume.sortedWith(stateRefComparator)
}
```
{{% /tab %}}

{{< /tabs >}}

The intention in the example is to ensure that the states are stored in a specific order, regardless of the ordering
of the list used to initialize instances of the class. This is achieved by using the first constructor parameter as the
basis for a private member. However, because that member is not mentioned in the constructor (whose parameters determine
what is serializable as discussed above) it would not be serialized. Because no mechanism provided to retrieve
a value for `statesToConsume`, the constructor would fail to build a serializer for this class.

In this case, a secondary constructor annotated with `@ConstructorForDeserialization` would not be a valid solution as the
two signatures would be the same. The best practice is to provide a getter for the constructor parameter which explicitly
associates it with the actual member variable.

{{< tabs name="tabs-7" >}}
{{% tab name="kotlin" %}}
```kotlin
@CordaSerializable
class ConfirmRequest(statesToConsume: List<StateRef>, val transactionId: SecureHash) {
    companion object {
        private val stateRefComparator = compareBy<StateRef>({ it.txhash }, { it.index })
    }

    private val states = statesToConsume.sortedWith(stateRefComparator)

    //Explicit "getter" for a property identified from the constructor parameters
    fun getStatesToConsume() = states
}
```
{{% /tab %}}

{{< /tabs >}}


### Mutable containers

Java does not provide a mechanism for determining the mutability of a class. Corda preserves the immutability of immutable objects rather than forcing mutability on presumed-immutable objects.  However, you can make an object immutable when you reconstruct it, as shown in these examples:


```kotlin
data class C(val l : MutableList<String>)

val bytes = C(mutableListOf ("a", "b", "c")).serialize()
val newC = bytes.deserialize()

newC.l.add("d")
```

The call to `newC.l.add` throws an `UnsupportedOperationException`.

You can use several workarounds to preserve the mutability of reconstituted objects.

If the class *is not* a Kotlin data class, then it doesn't require a primary constructor:

```kotlin
class C {
    val l : MutableList<String>

    @Suppress("Unused")
    constructor (l : MutableList<String>) {
        this.l = l.toMutableList()
    }
}

val bytes = C(mutableListOf ("a", "b", "c")).serialize()
val newC = bytes.deserialize()

// This time this call will succeed
newC.l.add("d")
```

If the class *is* a Kotlin data class, you can use a secondary constructor:

```kotlin
data class C (val l : MutableList<String>){
    @ConstructorForDeserialization
    @Suppress("Unused")
    constructor (l : Collection<String>) : this (l.toMutableList())
}

val bytes = C(mutableListOf ("a", "b", "c")).serialize()
val newC = bytes.deserialize()

// This will also work
newC.l.add("d")
```

To preserve immutability of objects, mutate the
contents of the class by creating a new copy of the data class with the altered list passed in as the constructor parameter:

```kotlin
data class C(val l : List<String>)

val bytes = C(listOf ("a", "b", "c")).serialize()
val newC = bytes.deserialize()

val newC2 = newC.copy (l = (newC.l + "d"))
```

{{< note >}}
If mutability isn’t an issue, you can use a single constructor for data classes. Make the property `var` instead of `val`, then reassign the property to a mutable instance in the `init` block.

{{< /note >}}

### Enums

Corda supports all enums (provided they are annotated with `@CordaSerializable`) and the interoperability of
enumerated type versions. That means you can change these types over time without affecting backward (or forward)
compatibility. See [Enum Evolution](serialization-enum-evolution.md).


### Exceptions

The following rules apply to supported `Throwable` implementations.



* If you wish for your exception to be serializable and transported type safely it should inherit from either
  `CordaException` or `CordaRuntimeException`
* If not, the `Throwable` will deserialize to a `CordaRuntimeException` with the details of the original
  `Throwable` contained within it, including the class name of the original `Throwable`



### Kotlin Objects

Kotlin’s non-anonymous `object` s (i.e. constructs like `object foo : Contract {...}`) are singletons and
treated differently.  They are recorded into the stream with no properties, and deserialize back to the
singleton instance. Currently, the same is not true of Java singletons, which will deserialize to new instances
of the class. This is hard to fix because there’s no perfectly standard idiom for Java singletons.

Kotlin’s anonymous `object` s (i.e. constructs like `object : Contract {...}`) are not currently supported
and will not serialize correctly. They need to be re-written as an explicit class declaration.


## Class synthesis

Corda serialization supports dynamically synthesising classes from the supplied schema when deserializing,
without requiring the supporting classes to be present on the classpath. This can be useful for:
* Generic code that might expect to use reflection over the deserialized data.
* Scripting languages that run on the JVM.
* Ensuring classes that are not on the classpath can be deserialized without loading potentially malicious code.

If the original class implements interfaces, the carpenter makes sure that all of the interface methods are
backed by fields. If that’s not the case, then an exception is thrown during deserialization. You can disable this check with `SerializationContext.withLenientCarpenter`. This can be useful if you only need the field getters, for example in an object viewer.


### Calculated values

In some cases, a property in an interface may normally be implemented
as a *calculated* value, with a “getter” method for reading it, but without a corresponding constructor parameter or a
“setter” method for writing it. An example is the *exitKeys* field in `FungibleState`. In this case, it is not automatically included in the properties to be serialized because the receiving class can re-calculate it on demand. However, a synthesized class will not
have that method implementation, so a cast to the interface will fail because the
property is not serialized. The lack of serialization means the “getter” method present in the interface will not be synthesized.

The solution is to annotate the method with the `SerializableCalculatedProperty` annotation, which will cause the value
exposed by the method to be read and transmitted during serialization, but discarded during normal deserialization. The
synthesized class will then include a backing field together with a “getter” for the serialized calculated value, and will
remain compatible with the interface.

If the annotation is added to the method in the *interface*, then all implementing classes must calculate the value and
none may have a corresponding backing field; alternatively, it can be added to the overriding method on each implementing
class where the value is calculated and there is no backing field. If the field is a Kotlin `val`, then the annotation
should be targeted at its getter method - for example, `@get:SerializableCalculatedProperty`.


## Type evolution

Type evolution lets you alter classes over time, while keeping them serializable and deserializable across
all versions of the class. This ensures an object serialized with an older idea of what the class “looked like” can be deserialized,
and a version of the current state of the class instantiated.

More detail can be found in [Default Class Evolution](serialization-default-evolution.md).
