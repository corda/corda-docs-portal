---
aliases:
- /releases/release-V4.0/tutorial-custom-notary.html
date: '2020-01-08T09:59:25Z'
menu:
  corda-os-4-0:
    identifier: corda-os-4-0-tutorial-custom-notary
    parent: corda-os-4-0-tutorials-index
    weight: 1130
tags:
- tutorial
- custom
- notary
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

```kotlin
notary : {
    validating : true # Set to false if your service is non-validating
    className : "net.corda.notarydemo.MyCustomValidatingNotaryService" # The fully qualified name of your service class
}
```

