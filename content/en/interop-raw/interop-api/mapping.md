---
date: '2023-08-02'
title: "Mapping Façade onto a Java Interface"
project: corda
version: 'Corda 5.2'
menu:
  corda5:
    identifier: corda5-interop-mapping
    parent: corda5-interop-cordapp-api
    weight: 4000
section_menu: corda5
---

# Mapping Façade onto a Java Interface

Defining a Façade using the JSON schema provides a platform-independent and descriptive way of specifying the
methods and data types that a system should support. To map a Façade JSON into a Java interface, you can use
annotations to link interface methods and parameters to the corresponding Façade methods and types. This allows for a
flexible and decoupled approach, where the implementation naming of methods/parameters can differ from the Façade names.

Corda provides the following annotations to map a Java (or Kotlin) interface onto a Façade JSON specification:

* `@BindsFacade` associates the Java interface with the Façade name.
* `@FacadeVersions` indicates the supported versions of the Façade by the Java interface.
* `@BindsFacadeMethod` specifies the corresponding command or query from the Façade JSON for each interface method.
* annotation type definition is declared for each alias; annotate all method parameters which type is defined in the alias
  section.

The following is an example Java interface which maps the Façade definition from the Façade Definition section:

```java

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.PARAMETER)
@interface Denomination {
  String value() default "org.corda.interop/platform/tokens/types/denomination/1.0";
}

public interface TokensFacade {

  @BindsFacade("org.corda.interop/platform/tokens")
  @FacadeVersions({"v1.0", "v2.0"})
  public interface TokensFacade {

    @BindsFacadeMethod
    @Suspendable
    Double getBalance(@Denomination String denomination);

    @FacadeVersions("v1.0")
    @BindsFacadeMethod("reserve-tokens")
    @Suspendable
    UUID reserveTokensV1(@Denomination String denomination, BigDecimal amount);
  }
}
```

When a CorDapp calls a Façade, no other code is required apart from the Corda Interoperable service which will create
a Façade Proxy object from the Java interface.
For the other side of interoperable call, the CorDapp will need to implement the interface to provide the actual
logic behind the Façade. Both steps are described in the Calling Façades and Implementing Façades sections.
