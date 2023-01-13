---
aliases:
- /releases/release-V3.2/cordapp-custom-serializers.html
date: '2020-01-08T09:59:25Z'
menu: []
tags:
- cordapp
- custom
- serializers
title: Pluggable Serializers for CorDapps
---


# Pluggable Serializers for CorDapps


To be serializable by Corda Java classes must be compiled with the -parameters switch to enable matching of its properties
to constructor parameters. This is important because Corda’s internal AMQP serialization scheme will only construct
objects using their constructors. However, when recompilation isn’t possible, or classes are built in such a way that
they cannot be easily modified for simple serialization, CorDapps can provide custom proxy serializers that Corda
can use to move from types it cannot serialize to an interim representation that it can with the transformation to and
from this proxy object being handled by the supplied serializer.


## Serializer Location

Custom serializer classes should follow the rules for including classes found in [Building a CorDapp](cordapp-build-systems.md)


## Writing a Custom Serializer


* Inherit from net.corda.core.serialization.SerializationCustomSerializer
* Provide a proxy class to transform the object to and from
* Implement the `toProxy` and `fromProxy` methods

Serializers inheriting from SerializationCustomSerializer have to implement two methods and two types.


## Example

Consider this example class

```java
public final class Example {
    private final Int a
    private final Int b

    private Example(Int a, Int b) {
        this.a = a;
        this.b = b;
    }

    public static Example of (int[] a) { return Example(a[0], a[1]); }

    public int getA() { return a; }
    public int getB() { return b; }
}
```

Without a custom serializer we cannot serialize this class as there is no public constructor that facilitates the
initialisation of all of its properties.

To be serializable by Corda this would require a custom serializer as follows:

```kotlin
class ExampleSerializer : SerializationCustomSerializer<Example, ExampleSerializer.Proxy> {
    data class Proxy(val a: Int, val b: Int)

    override fun toProxy(obj: Example) = Proxy(obj.a, obj.b)

    override fun fromProxy(proxy: Proxy) : Example {
        val constructorArg = IntArray(2);
        constructorArg[0] = proxy.a
        constructorArg[1] = proxy.b
        return Example.create(constructorArg)
    }
}
```


## Whitelisting

By writing a custom serializer for a class it has the effect of adding that class to the whitelist, meaning such
classes don’t need explicitly adding to the CorDapp’s whitelist.

