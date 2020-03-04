---
date: '2020-01-08T09:59:25Z'
menu:
  corda-enterprise-4-4:
    parent: corda-enterprise-4-4-tutorial
title: Writing a custom notary service (experimental)
---



# Writing a custom notary service (experimental)


{{< warning >}}
Customising a notary service is still an experimental feature and not recommended for most use-cases. The APIs
                for writing a custom notary may change in the future.

{{< /warning >}}

The first step is to create a service class in your CorDapp that extends the `NotaryService` abstract class.
            This will ensure that it is recognised as a notary service.
            The custom notary service class should provide a constructor with two parameters of types `ServiceHubInternal` and `PublicKey`.
            Note that `ServiceHubInternal` does not provide any API stability guarantees.

The next step is to write a notary service flow. You are free to copy and modify the existing built-in flows such
            as `ValidatingNotaryFlow`, `NonValidatingNotaryFlow`, or implement your own from scratch (following the
            `NotaryFlow.Service` template). Below is an example of a custom flow for a *validating* notary service:

To enable the service, add the following to the node configuration:

```none
notary : {
    validating : true # Set to false if your service is non-validating
    className : "net.corda.notarydemo.MyCustomValidatingNotaryService" # The fully qualified name of your service class
}
```

## Testing your custom notary service

To create a flow test that uses your custom notary service, you can set the class name of the custom notary service as follows in your flow test:

After this, your custom notary will be the default notary on the mock network, and can be used in the same way as described in flow-testing.


