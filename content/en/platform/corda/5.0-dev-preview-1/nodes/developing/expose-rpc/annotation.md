---
title: "Annotating RPC functionality"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing-exposing-rpc
    identifier: corda-5-dev-preview-1-nodes-developing-exposing-rpc-annotations
    weight: 2000
project: corda-5
section_menu: corda-5-dev-preview
description: >
  How to annotate `RPCOps` interface classes and methods.
---

The HTTP-RPC module exposes RPC functionality via a web interface. Use this guide to annotate custom RPC interface classes and methods that you wish to expose.

[Annotations](https://kotlinlang.org/docs/reference/annotations.html) can be used in both Java and Kotlin and are a
way of attaching metadata to code.

You must add annotations to the interface classes and methods. Only annotated methods appear on the web service
interface, non-annotated methods are excluded. In addition to exposing annotated RPC classes and methods through the web
interface, the HTTP-RPC module also generates an OpenAPI schema that clients can use to call the exposed methods.

## Glossary

{{< table >}}
| Term        | Definition                                    |
|-------------|-----------------------------------------------|
| `Endpoints` | `RPCOps` interface methods that are semantically similar to `REST` resource actions. |
| `Resources` | `RPCOps` interface classes that are semantically similar to `REST` resources. |
{{< /table >}}

## Annotate RPC endpoints and resources

Use annotations to identify the resources (classes) and endpoints (methods) that will be exposed on the web
interface and to add additional meta-annotations.

When annotating custom RPC endpoints and resources, you must:
* Specify the type of endpoint (only `GET` and `POST` are allowed).
* Provide a unique path for each resource and endpoint to avoid ambiguity on the mapping API.
* Map parameters for each endpoint to a type of `REST` call argument (query, path, or body). If no type is specified for a `POST` endpoint, it defaults to `body`. `body` parameters are not permitted for `GET` endpoints and will cause the annotation parser to throw an exception.
* <a href="../extending-rpc.md">Extend and implement the `RPCOps` interface</a> so that it includes any custom endpoints. If an endpoint is not included, the annotation parser throws an exception when generating the structure. Multiple preconditions must be satisfied for the parsing to be successful. Such errors are expected to be non-recoverable in the scope of the server. As such, the HTTP server would shut down and provide a detailed message in the log output, while maintaining the rest of the node operational.

The annotation parser checks that each resource and endpoint has a unique path. However:
* Where more than one resource shares the same path, a warning is displayed.
* Where more than one endpoint shares the same resource and endpoint path, the annotation parser throws an error that the client can handle.

You can also specify in your annotations:
* An alternative name for the method.
* An alternative API path and parameter names for the method.
* A description that appears on the OpenAPI spec.

The annotation parser collects information about:
* Class name, type, and the name of the package the class belongs to.
* Class meta-annotations provided via pre-defined, applicable annotation fields.
* Method name, signature (input parameters and output type), and containing class.
* Method meta-annotations provided via pre-defined, applicable annotation fields.

### Annotations and meta-annotation fields
Available meta-annotation fields for each annotation:

{{< table >}}
| Annotation                    | Applicable on      | Available meta-annotation fields                           |
|-------------------------------|--------------------|------------------------------------------------------------|
| `HttpRpcResource`             | Interface          | `description`, `name`, and `path`.                         |
| `HttpRpcGET`                  | Endpoints          | `description`, `path`, `responseDescription`, and `title`. |
| `HttpRpcPOST`                 | Endpoints          | `description`, `path`, `responseDescription`, and `title`. |
| `HttpRpcPathParameter`        | Endpoint parameter | `description` and `name`.                                  |
| `HttpRpcQueryParameter`       | Endpoint parameter | `default`, `description`, `name`, and `required`.          |
| `HttpRpcRequestBodyParameter` | Endpoint parameter | `description`, `name`, and `required`.                     |
{{< /table >}}

Field attributes for each meta-annotation field:

{{< table >}}
| Name                 | Type    | Default | Required |
|----------------------|---------|---------|----------|
| default              | String  | ""      | false    |
| description          | String  | ""      | false    |
| name                 | String  | ""      | false    |
| path                 | String  | ""      | false    |
| required             | Boolean | true    | false    |
| responseDescription  | String  | ""      | false    |
| title                | String  | ""      | false    |
{{< /table >}}

## Validation of annotations

Validation happens at node startup. The `RPCOps` interfaces are scanned for HTTP-RPC specific annotations and annotated
parameters are validated against these rules:

* You need to annotate fields and endpoints within an `RPCOps` interface with `HttpRpcResource`, otherwise they will be ignored.

* You can only annotate a `resource` method with either `@HttpRpcPOST` or `@HttpRpcGET`. Therefore, this example is invalid:
    ```kotlin
    @HttpRpcResource
    class Example {
        @HttpRpcGET
        @HttpRpcPOST
        fun example() {}
    }
    ```

* Resources must have a unique, case-insensitive path. Classes can have identical names in different packages, as long
  as their path value in `@HttpRpcResource` is different. Therefore, this example is invalid:
    ```kotlin
    @HttpRpcResource(path = "exampleWithSameResourceName")
    class Example {}

    @HttpRpcResource(path = "exampleWithSameResourceName")
    class OtherExample {}
    ```

* Endpoints within the same resource must have a unique, case-insensitive path. Therefore, this example is invalid:
    ```kotlin
    @HttpRpcResource
    class Example {
        @HttpRpcGET(path = "exampleWithSameEndpointName")
        fun example() {}

        @HttpRpcGET(path = "exampleWithSameEndpointName")
        fun otherExample() {}
    }
    ```

* You must annotate endpoint parameters with either `@HttpRpcPathParameter`, `@HttpRpcQueryParameter`, or `@HttpRpcRequestBodyParameter`. If left unannotated, `@HttpRpcRequestBodyParameter` behavior is used. Therefore, this example is invalid:
    ```kotlin
    @HttpRpcResource
    class Example {
        @HttpRpcGET(path = "exampleWithMissingParameterAnnotation")
        fun example(foo: String) {}
    }
    ```

* You can use `@HttpRpcRequestBodyParameter` in multiple `POST` endpoint parameters, but you can't use it in any `GET` endpoint parameter. Therefore, this example is invalid:
    ```kotlin
    @HttpRpcResource
    class Example {
        @HttpRpcGET(path = "exampleWithBodyParameterOnGet")
        fun example(@HttpRpcRequestBodyParameter foo: String) {}
    }
    ```

* You can only use these simple types for path and query parameters: `enum`, `boolean`, `double`, `int`, `long`, and `string`. Query parameters may also be lists of strings. Therefore, this example is invalid:
    ```kotlin
    class CustomClass {}

    @HttpRpcResource
    class Example {
        @HttpRpcGET(path = "examplePathParameterOfComplexType")
        fun example(@HttpRpcPathParameter foo: CustomClass) {}
    }
    ```

* Endpoint parameters of the same type (query, path) must have unique, case-insensitive names. Therefore, this example is invalid:
    ```kotlin
    @HttpRpcResource
    class Example {
        @HttpRpcGET(path = "exampleEndpointParametersWithSameTypeAndName")
        fun example(@HttpRpcQueryParameter(name = "foo") foo: String, @HttpRpcQueryParameter(name = "foo") bar: Int) {}
    }
    ```

* If you annotate a method parameter with `@HttpRpcPathParameter`, then you must declare it by its name in the method's `@HttpRpcGET` or `@HttpRpcPOST` annotation's path value. Therefore, this example is invalid:
    ```kotlin
    @HttpRpcResource
    class Example {
        @HttpRpcGET(path = "examplePathParameterNotDeclaredInEndpointPath")
        fun example(@HttpRpcPathParameter foo: String) {}
    }
    ```
* If you have declared a parameter in the `@HttpRpcGET` or `@HttpRpcPOST` annotation's path value, then it must be an input parameter of the method with the same name and be annotated with `@HttpRpcPathParameter`. The function parameter name could be different if its name is overridden in the `@HttpRpcPathParameter` annotation's name value. Therefore, this example is invalid:
    ```kotlin
    @HttpRpcResource
    class Example {
        @HttpRpcGET(path = "examplePathParameterNotDeclaredInTheFunctionParameter/:foo")
        fun example() {}
    }
    ```

* When using classes as body parameters, annotate them with `@CordaSerializable`. Nested custom types do not need to have this annotation. This is not necessary for primitive types, primitive type wrappers, and strings. Here is a *valid* example:
    ```kotlin
    data class CustomNestedClass(
        val s: String
    )

    @CordaSerializable
    data class CustomClass(
        val foo: CustomNestedClass
    )

    @HttpRpcResource
     class Example {
         @HttpRpcPOST(path = exampleBodyParameterAnnotatedWithCordaSerializable")
         fun example(@HttpRpcRequestBodyParameter body: CustomClass) {}

        @HttpRpcPOST(path = exampleBodyParameterPrimitiveTypeWrapper")
         fun example2(@HttpRpcRequestBodyParameter body: Long) {}
     }
    ```

  And here is an *invalid* example:
    ```kotlin
    data class CustomClass(
        val s: String
    )

    @HttpRpcResource
     class Example {
         @HttpRpcPOST(path = exampleBodyParameterNotAnnotatedWithCordaSerializable")
         fun example(@HttpRpcRequestBodyParameter body: CustomClass) {}
     }
    ```

{{< note >}}

You can use the validation functions for testing and to validate your code during development. You can find the validations
used in the `net.corda.v5.httprpc.tools.annotations.validation` package. Use the `HttpRpcInterfaceValidator`
object to run all available validation functions against your `RPCOps` interface.

{{< /note >}}


## Implicitly exposed endpoints

This endpoint is defined in the `RPCOps` interface and is automatically exposed through the server:

{{< table >}}
| Endpoint              | Type     | Response    | Authorization |
|-----------------------|----------|-------------|---------------|
| `GET getProtocolVersion\` | Integer | The protocol version of the implementation. | None, regardless of the resource's permission. |
{{< /table >}}

{{< note >}}

Implicitly exposed endpoints are validated against the relevant rules (for example,
endpoint name clash), and are accessible through the OpenAPI specification.

{{< /note >}}

## OpenAPI generation

The annotation parser also generates a complete OpenAPI schema.

The `OpenApiInfoProvider` connects internal business logic and the party interested in the OpenAPI schema
(the server in this case).
The `OpenApiInfoProvider` maps every resource and endpoint into a schema object, and uses the `openapi.schema`
package to convert classes into their schema representation, which is necessary for input and response class types.
