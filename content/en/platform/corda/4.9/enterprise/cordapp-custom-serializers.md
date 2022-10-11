---
date: '2021-07-12'
menu:
  corda-enterprise-4-9:
    parent: corda-enterprise-4-9-node-serialization
tags:
- cordapp
- custom
- serializers
title: Custom serializers for CorDapps
weight: 10
---




# Custom serializers for CorDapps

You must compile Java classes with the `-parameters` switch for Corda to serialize them. This matches the class properties
to the constructor parameters, allowing Corda’s internal AMQP serialization scheme to construct the
objects. If recompilation isn’t possible, or your classes cannot be easily modified for simple serialization, CorDapps can provide custom proxy serializers that Corda
can use to move from types it cannot serialize to interim representations that it can. The supplied serializer handles the transformation to and
from the proxy object.


## Serializer location

Custom serializer classes should follow the [rules for including classes](../../../../../en/platform/corda/4.9/enterprise/cordapps/cordapp-build-systems.md).


## Writing a custom serializer

Serializers must:

* Inherit from `net.corda.core.serialization.SerializationCustomSerializer`.
* Provide a proxy class to transform the object to and from.
* Implement the `toProxy` and `fromProxy` methods.
* Be either included in the CorDapp `.jar` or made available in the system class path of the running process.

Serializers inheriting from `SerializationCustomSerializer` must implement two methods and two types.


## Custom serializer example

In the example below, imagine that you must serialize this class, but are constrained from making the constructor public. That means you can't use a public constructor to initialize all the properties, and therefore can't serialize the class.

```java
public final class Example {
    private final Int a
    private final Int b

    // Because this is marked private the serialization framework will not
    // consider it when looking to see which constructor should be used
    // when serializing instances of this class.
    private Example(Int a, Int b) {
        this.a = a;
        this.b = b;
    }

    public static Example of (int[] a) { return Example(a[0], a[1]); }

    public int getA() { return a; }
    public int getB() { return b; }
}
```

To be serializable by Corda, this example requires a custom serializer that transforms the unserializable
class into a form the platform can serialize. You could write a serializer like this:

{{< tabs name="tabs-1" >}}
{{% tab name="java" %}}
```java
/**
 * The class lacks a public constructor that takes parameters it can associate
 * with its properties, so it isn't serializable by the Corda serialization
 * framework.
 */
class Example {
    private int a;
    private int b;

    public int getA() { return  a; }
    public int getB() { return  b; }

    public Example(List<int> l) {
        this.a = l.get(0);
        this.b = l.get(1);
    }
}

/**
 * This class proxies instances of Example within the serializer.
 */
public class ExampleProxy {
    /**
     * These properties will be serialized into the byte stream. This is where we choose how to
     * represent instances of the object we're proxying. In this example, which is somewhat
     * contrived, this choice is obvious. In your own classes / 3rd party libraries, however, this
     * may require more thought.
     */
    private int proxiedA;
    private int proxiedB;

    /**
     * The proxy class itself must be serializable by the framework. That means it must have a constructor that
     * can be mapped to the properties of the class via getter methods.
     */
    public int getProxiedA() { return proxiedA; }
    public int getProxiedB() { return  proxiedB; }

    public ExampleProxy(int proxiedA, int proxiedB) {
        this.proxiedA = proxiedA;
        this.proxiedB = proxiedB;
    }
}

/**
 * This is the custom serializer that will automatically loaded into the serialization
 * framework when the CorDapp JAR is scanned at runtime.
 */
public class ExampleSerializer implements SerializationCustomSerializer<Example, ExampleProxy> {

    /**
     *  Given an instance of the Example class, create an instance of the proxying object ExampleProxy.
     *
     *  Essentially, convert Example to ExampleProxy.
     */
    public ExampleProxy toProxy(Example obj) {
        return new ExampleProxy(obj.getA(), obj.getB());
    }

    /**
     * Conversely, given an instance of the proxy object, revert that back to an instance of the
     * type being proxied.
     *
     *  Essentially, convert ExampleProxy to Example
     */
    public Example fromProxy(ExampleProxy proxy) {
        List<int> l = new ArrayList<int>(2);
        l.add(proxy.getProxiedA());
        l.add(proxy.getProxiedB());
        return new Example(l);
    }
}
```
{{% /tab %}}

{{% tab name="kotlin" %}}
```kotlin
class ExampleSerializer : SerializationCustomSerializer<Example, ExampleSerializer.Proxy> {
    /**
     * This is the actual proxy class that is used as an intermediate representation
     * of the Example class.
     */
    data class Proxy(val a: Int, val b: Int)

    /**
     * This method takes an instance of the type being proxied and
     * transposes it into that form, instantiating an instance of the Proxy object. It
     * is this class instance that is serialized into the byte stream.
     */
    override fun toProxy(obj: Example) = Proxy(obj.a, obj.b)

    /**
     * This method is used during deserialization. The bytes will have been read
     * from the serialized blob, and an instance of the Proxy class returned. You must
     * now transform that back into an instance of the original class.
     *
     * In this example, you must evoke the static "of" method on the
     * Example class, transforming the serialized properties of the Proxy instance
     * into a form expected by the construction method of Example.
     */
    override fun fromProxy(proxy: Proxy) : Example {
        val constructorArg = IntArray(2);
        constructorArg[0] = proxy.a
        constructorArg[1] = proxy.b
        return Example.of(constructorArg)
    }
}
```
{{% /tab %}}

{{< /tabs >}}

In the above examples:

* `ExampleSerializer` is the serializer that is loaded by the framework to serialize instances of the `Example` type.
* `ExampleSerializer.Proxy`, in the Kotlin example, and `ExampleProxy` in the Java example, is the intermediate representation used by the framework to represent instances of `Example` within the wire format.


## The proxy object

The proxy object is an intermediate representation that the serialization framework
can reason about. Therefore, the proxy class must
only contain elements the framework can reason about.

The proxy class itself is distinct from the proxy serializer. The serializer must refer to the unserializable
type in the `toProxy` and `fromProxy` methods.

For example, the first thought a developer may have when implementing a proxy class is to simply *wrap* an
instance of the object being proxied, like this:

```kotlin
class ExampleSerializer : SerializationCustomSerializer<Example, ExampleSerializer.Proxy> {
    /**
     * In this example, we are trying to wrap the Example type to make it serializable
     */
    data class Proxy(val e: Example)

    override fun toProxy(obj: Example) = Proxy(obj)

    override fun fromProxy(proxy: Proxy) : Example {
        return proxy.e
    }
}
```

However, this will not work because it creates a recursive loop. Synthesizing a serializer
for the `Example` type requires synthesising one for `ExampleSerializer.Proxy`. However, that requires
one for `Example` and so on and so forth until we get a `StackOverflowException`.

The solution is to create the intermediate form (the proxy object) purely in terms
the serialization framework can reason about, as shown in the initial example.


{{< important >}}
When composing a proxy object for a class, be aware that everything within that structure will be written
into the serialized byte stream.

{{< /important >}}


## Whitelisting

Classes with custom serializers are added to the CorDapp's whitelist automatically.
