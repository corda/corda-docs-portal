---
title: "Locating the OpenAPI specification"
date: '2021-08-25'
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-nodes-operating
    identifier: corda-5-dev-preview-1-nodes-operating-placeholder
    weight: 5000
project: corda-5
section_menu: corda-5-dev-preview
description: >
  How to locate your node's OpenAPI specification.
---

Use this guide to locate your node's OpenAPI specification.

As part of the Corda 5 Developer Preview, a dynamic [OpenAPI specification](https://swagger.io/docs/specification/about/)
(formerly known as the Swagger specification) is generated which details your node's RPC functionality, which is exposed
via a secure HTTP API. It describes:
* Endpoints, including operations and operation parameters (input and output).
* Authentication methods.

{{< note >}}

You need to [enable HTTP-RPC](configure-nodeconf.md) before you can use the OpenAPI specification.

{{< /note >}}

Your node's OpenAPI JSON is available on a URL. If your node's HTTP-RPC address is  `mynode:8888`, you would find it on `http[s]://mynode:8888/api/v1/swagger.json`.

Here is an excerpt of a node's OpenAPI JSON:

```
{
  "openapi" : "3.0.1",
  "info" : {
    "title" : "HTTP RPC demo",
    "description" : "Exposing RPCOps interfaces as webservices",
    "version" : "1"
  },
  "servers" : [ {
    "url" : "/api/v1"
  } ],
  "security" : [ {
    "basicAuth" : [ ]
  } ],
  "tags" : [
    { "name" : "FlowManagerRPCOps", "description" : ""},
    { "name" : "FlowStarterRPCOps", "description" : "FlowStarterRPCOps"},
    { "name" : "VaultQueryRPCOps", "description" : "Various operations to retrieve content of the Vault" },
    { "name" : "NodeIdentityRPCOps", "description" : "Various operations related to the identity of the Corda Node in the network"},
    { "name" : "NodeLifecycleRPCOps", "description" : "Various operations related which apply to the lifecycle of the node"}
  ],
  "paths" : {
    "/flowmanagerrpcops/dumpcheckpoints" : {
      "get" : {
        "tags" : [ "FlowManagerRPCOps" ],
        "description" : "",
        "operationId" : "get_flowmanagerrpcops_dumpcheckpoints",
        "parameters" : [ ],
        "responses" : {
          "200" : {
            "description" : "Success."
          },
          "401" : {
            "description" : "Unauthorized."
          },
          "403" : {
            "description" : "Forbidden."
          }
        }
      }
    },
...

    "/flowstarter/registeredflows" : {
      "get" : {
        "tags" : [ "FlowStarterRPCOps" ],
        "description" : "",
        "operationId" : "get_flowstarter_registeredflows",
        "parameters" : [ ],
        "responses" : {
          "200" : {
            "description" : "Success.",
            "content" : {
              "application/json" : {
                "schema" : {
                  "uniqueItems" : false,
                  "type" : "array",
                  "nullable" : false,
                  "items" : {
                    "type" : "string",
                    "nullable" : false,
                    "example" : "string"
                  }
                }
              }
            }
          },
          "401" : {
            "description" : "Unauthorized."
          },
          "403" : {
            "description" : "Forbidden."
          }
        }
      }
    },
...
  },
...
}
```
