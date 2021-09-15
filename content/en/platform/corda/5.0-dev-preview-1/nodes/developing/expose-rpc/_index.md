---
title: "Exposing RPC over HTTP"
date: '2021-09-13'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-developing
    identifier: corda-5-dev-preview-1-nodes-developing-exposing-rpc
    weight: 400
project: corda-5
section_menu: corda-5-dev-preview
description: >
  How to expose RPC functionality over HTTP.
---

As part of the Corda 5 Developer Preview, you can generate and host a secure HTTP API for your RPC interfaces using a
flexible module (HTTP-RPC). Clients no longer need to use the internal RPC interface to interact with their CorDapps.

HTTP-RPC generates web service endpoints from the properly annotated `RPCOps` interfaces and methods, and an
[OpenAPI 3](https://swagger.io/specification/)
standard JSON (also known as Swagger JSON) as a complete web service description. It also generates Swagger UI with
available authentication features that you can use to test the web service methods.

## Responses and results from endpoint methods

If no error occurs, an HTTP-RPC endpoint returns the expected response object, serialized to JSON. You'll need a Jackson style
custom deserializer ([JsonDeserializer](https://www.logicbig.com/tutorials/misc/jackson/json-serialize-deserialize.html))
for custom types.

HTTP response status codes indicate whether a request has been successfully completed.

### Successful request response

If your request is successfully completed, you'll see the HTTP response status `200`, and the response body will
contain the response object serialized to JSON.

### Error code responses

If your request is unsuccessful, you may see one of these error codes:

{{< table >}}

| HTTP response status          | Description                                                                  |
|-------------------------------|----------------------------------------------------------------------------|
| `401 Unauthrorized`           | The authentication information is missing from the HTTP header or is incorrect, or user login failed with the credentials provided. |
| `403 Forbidden`           | The request was authenticated but the credentials provided are not authorized to invoke the requested method. In the case of a start flow request, the `StartFlowPermissionException` thrown from the code is also mapped to `ForbiddenResponse`. |
| `404 Not found`           | Any `FlowNotFoundException` thrown from the code is mapped to `NotFoundResponse`. |
| `400 Bad Request`           | Any `BadRpcStartFlowRequestException`, `MissingParameterException` or `JsonProcessingException` thrown from the code is mapped to `BadRequestResponse`. |

{{< /table >}}

