---
title: "xxxxxxxxxxxxxxxxxxxx"
menu:
  corda-5-dev-preview:
    parent: corda-5-dev-preview-1-operate-node
    identifier: corda-5-dev-preview-1-operate-node-xxxxxxxxxxxxxxxxxxxxxx
    weight: 900
project: corda-5
section_menu: corda-5-dev-preview
description: >
  Instructions on how to xxxxxxx.
---

[comment]: <NOT DONE!!>

The OpenAPI specification (formerly known as the Swagger specification) is for machine-readable interface files for describing, producing, consuming, and visualizing RESTful web services. See the [OpenAPI overview](../../overview/open-api/) section for more information.

## OpenAPI for HTTP-RPC

If HTTP-RPC is enabled (read about [configuring HTTP-RPC in `node.conf`](../conf/)) it will be available on `/api/v1/swagger.json`. For example, if the node's HTTP-RPC address is set to `mynode:8888`, the OpenAPI JSON will be available on `http[s]://mynode:8888/api/v1/swagger.json`.

## OpenAPI JSON example

Below is an excerpt of a node's OpenAPI JSON showing some of the available endpoints' specification:

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
